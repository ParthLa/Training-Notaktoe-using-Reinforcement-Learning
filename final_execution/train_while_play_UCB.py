import sys
import time
import numpy as np
import random
import math
import pickle
# According to the implementation, global storage is being done automatically by board_states_to_action_vectors.
# Local storage is being done in actions_taken vector.
# Here, we map current board state with value vector,win count vector and play count vector of the possible_actions vector from that state.
# This program is training both players to play optimal moves simulteneously.
# def savePolicy(self):
#         fw = open('policy_' + str(self.name), 'wb')
#         pickle.dump(self.states_value, fw)
#         fw.close()

# def loadPolicy(self, file):
#         fr = open(file, 'rb')
#         self.states_value = pickle.load(fr)
#         fr.close()

n=int(input("Enter Board side length to play: "))
# We assume that computer plays first - computer is player 1.
def find_if_terminal(board_state):
	ans=False
	board=np.chararray((n,n))
	assert len(board_state)==n*n
	# we assume that the board_state string is representing the board row_wise i.e. first n elements => first row, next n elements => 2nd row and so on.
	for j in range(n*n):
		row=j//n
		column=j%n
		board[row][column]=board_state[j]
	i=0
	while(i<n*n):
		j=i
		printer=""
		for cnt in range(n):
			printer=printer+board_state[j]+' '
			j=j+1
		print(printer)
		i=i+n
	print()
	reference_string='X'*n
	# check if any row is complete with X
	for j in range(n):
		s1=""
		for k in range(n):
			s1=s1+board_state[j*n+k]
		if(s1==reference_string):
			ans=True
			return ans
	# check if any column is complete with X
	for j in range(n):
		s1=""
		for k in range(n):
			s1=s1+board_state[k*n+j]
		if(s1==reference_string):
			ans=True
			return ans
	# check if any diagonal is complete with X
	diagonal1=""
	diagonal2=""
	for j in range(n):
		diagonal1=diagonal1+board_state[j*n+j]
		diagonal2=diagonal2+board_state[j*n+n-1-j]
	if(diagonal1==reference_string):
		ans=True
		return ans
	if(diagonal2==reference_string):
		ans=True
		return ans
	assert ans==False
	return bool(ans)

board_states_to_win_count={}
board_states_to_play_count={}

value_data=open("data"+str(n)+".pkl","rb")
board_states_to_value_vectors=pickle.load(value_data)
value_data.close()

empty_board_state='.'*(n*n)
number_of_games=int(input("Enter number of games to play: "))
print()
number_of_epochs=number_of_games
player1_win_track=np.zeros(number_of_epochs)
player2_win_track=np.zeros(number_of_epochs)
player1_win=0
player2_win=0
for epoch_number in range(number_of_epochs):
	print("Game: "+str(epoch_number+1))
	print()
	board_state=empty_board_state
	actions_taken=[]
	player_to_play=1
	while(find_if_terminal(board_state)==False):
		if(player_to_play==1):
			# the function below finds the action vector of the present board state and creates one if it is not present
			# print(board_state)
			if(str(board_states_to_value_vectors.get(board_state))=="None"):
				win_count=[0]*(n*n)
				play_count=[0]*(n*n)
				value_vector=[0]*(n*n)
				length=len(board_state)
				for j in range(length):
					# working on initialization of action probability values
					if(board_state[j]=='.'):
						value_vector[j]=1e5
					# the 2 lines below initialize the centre of board with higher value so that the first player tempts to play at the centre.
					# if(j==length/2):
					# 	value_vector[j]=2
				board_states_to_win_count[board_state]=win_count
				board_states_to_play_count[board_state]=play_count
				board_states_to_value_vectors[board_state]=value_vector
			elif(str(board_states_to_play_count.get(board_state))=="None"):
				play_count=[0]*(n*n)
				win_count=[0]*(n*n)
				board_states_to_win_count[board_state]=win_count
				board_states_to_play_count[board_state]=play_count
			else:
				play_count=board_states_to_play_count[board_state]
				value_vector=board_states_to_value_vectors[board_state]
				length=len(board_state)
				for j in range(length):
					if(play_count[j]==0):
						value_vector[j]=1e5
					else:
						value_vector[j]=win_count[j]/play_count[j] + math.sqrt(1.5*math.log(epoch_number+1)/play_count[j])
				board_states_to_value_vectors[board_state]=value_vector

			play_count=board_states_to_play_count[board_state]
			value_vector=board_states_to_value_vectors[board_state]
			maxm_value=0
			# finding the best action to take - using UCB policy here. 
			for j in range(n*n):
				if(value_vector[j]>maxm_value and board_state[j]=='.'):
					maxm_value=value_vector[j]
			list_max_indices=[]
			for j in range(n*n):
				if(value_vector[j]==maxm_value and board_state[j]=='.'):
					list_max_indices.append(j)
			position_to_play=random.choice(list_max_indices)
			if(play_count[position_to_play]==0):
				play_count[position_to_play]=1
			else:
				play_count[position_to_play] += 1
			board_states_to_play_count[board_state]=play_count
			actions_taken.append((board_state,position_to_play))
			# binarization of the action vectors using xnor net technique - 
			# this doesn't seem to work on action vectors since everytime we approximate the action vector with binary vector, 
			# we will get same probability for all action values in that action vector. so we do it on value vectors 
			row_num=position_to_play//n+1
			column_num=position_to_play%n+1
			print("Computer's position to play: "+str(row_num)+" "+str(column_num))
			sign_vector=np.sign(value_vector)
			alpha_scale=sum(np.absolute(value_vector))/(n*n)
			value_vector=alpha_scale*sign_vector
			board_states_to_value_vectors[board_state]=value_vector
			player_to_play=2
		else:
			valid_move=False
			while(bool(valid_move)!=True):
				row_num,column_num=[int(val) for val in input("Enter position to play: ").split()]
				position_to_play=(row_num-1)*n + (column_num-1)
				if(0<=position_to_play and position_to_play<n*n and board_state[position_to_play]!='X'):
					valid_move=True
				else:
					print("Enter a valid move")
			player_to_play=1
		assert board_state[position_to_play]!='X'
		board_state=board_state[:position_to_play]+'X'+board_state[position_to_play+1:]		
	
	cnt_x=board_state.count('X')
	player_win=0
	theta=1
	num_moves=len(actions_taken)
	# In our case, I feel that there is no value function.
	# the reward is oriented in support of player 1 => reward is +ve if player 1 wins.
	if(cnt_x%2==0):
		player_win=1
		print("YOU LOSE!!!")
		player1_win=player1_win+1
		reward=theta/num_moves
	else:
		player_win=2
		print("YOU WON!!!")
		player2_win=player2_win+1
		reward=-1*theta/num_moves
	print()
	# updating the actions_taken vector using decided reward(a kind of backpropagation)
	for board_state, position_to_play in actions_taken:
		win_count=board_states_to_win_count[board_state]
		if(reward>0):
			win_count[position_to_play] +=1
			# value_vector[position_to_play]=win_count[position_to_play]/play_count[position_to_play] + math.sqrt(1.5*math.log(epoch_number+1)/play_count[position_to_play])
		board_states_to_win_count[board_state]=win_count
	# the winning probabilities of both players based on the reward being given after every epoch
	player1_win_track[epoch_number]=player1_win/(epoch_number+1)
	player2_win_track[epoch_number]=player2_win/(epoch_number+1)

with open("results_play_UCB.txt","a") as file:
	file.write("Number 	 Computer-win 	Human-win ")
	file.write("\n")
	for epoch_number in range(number_of_epochs):
		file.write(str(epoch_number+1)+ "	"+str(player1_win_track[epoch_number])+"	"+ str(player2_win_track[epoch_number]))	
		file.write("\n")
	file.write("\n")
	# it is being trained in negative direction for player1. How to solve this?
	# how to define state-value here?
	# think about choice trace weight, choice correlation factor.
	# Future work: To try Posterior Sampling Technique.
	# In UCB, reward change for each chosen move will be different.
