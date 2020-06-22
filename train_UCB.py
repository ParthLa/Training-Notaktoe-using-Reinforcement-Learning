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
def find_if_terminal(board_state,verbose):
	ans=False
	board=np.chararray((n,n))
	assert len(board_state)==n*n
	# we assume that the board_state string is representing the board row_wise i.e. first n elements => first row, next n elements => 2nd row and so on.
	for j in range(n*n):
		row=j//n
		column=j%n
		board[row][column]=board_state[j]
	if(bool(verbose)==True):
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

n=int(input("Enter Board side length to train: "))
verbose=input("Do you wish to observe the board states during training? ")
if(verbose=="No"):
	verbose=False
else:
	verbose=True
print("Training the computer model")

board_states_to_win_count={}
board_states_to_play_count={}
board_states_to_value_vectors={}
empty_board_state='.'*(n*n)
number_of_epochs=100000
player1_win_track=np.zeros(number_of_epochs)
player2_win_track=np.zeros(number_of_epochs)
player1_win=0
player2_win=0
for epoch_number in range(number_of_epochs):
	# print(epoch_number+1)
	if(epoch_number%1000==0):
		print("Number of games played: "+str(epoch_number))
	board_state=empty_board_state
	actions_taken=[]
	while(find_if_terminal(board_state,verbose)==False):
		# the function below finds the action vector of the present board state and creates one if it is not present
		# print(board_state)
		if(board_states_to_value_vectors.get(board_state)==None):
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
		elif(board_states_to_play_count.get(board_state)==None):
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
		sign_vector=np.sign(value_vector)
		alpha_scale=sum(np.absolute(value_vector))/(n*n)
		value_vector=alpha_scale*sign_vector
		board_states_to_value_vectors[board_state]=value_vector
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
		player1_win=player1_win+1
		reward=theta/num_moves
	else:
		player_win=2
		player2_win=player2_win+1
		reward=-1*theta/num_moves
	# updating the actions_taken vector using decided reward(a kind of backpropagation)
	action_number=1
	for board_state, position_to_play in actions_taken:
		win_count=board_states_to_win_count[board_state]
		if(action_number%2==1): # => the current moves was played by player 1.
			if(reward>0):
				win_count[position_to_play] +=1
			# value_vector[position_to_play]=win_count[position_to_play]/play_count[position_to_play] + math.sqrt(1.5*math.log(epoch_number+1)/play_count[position_to_play])
		
		else: # => the current moves was played by player 2.
			if(reward<0):
				win_count[position_to_play] +=1
			# value_vector[position_to_play]=win_count[position_to_play]/play_count[position_to_play] + math.sqrt(1.5*math.log(epoch_number+1)/play_count[position_to_play])
		board_states_to_win_count[board_state]=win_count
		action_number += 1	
	# the winning probabilities of both players based on the reward being given after every epoch
	player1_win_track[epoch_number]=player1_win/(epoch_number+1)
	player2_win_track[epoch_number]=player2_win/(epoch_number+1)

value_data=open("data"+str(n)+".pkl","wb")
pickle.dump(board_states_to_value_vectors,value_data)
value_data.close()

with open("results_train_UCB.txt","a") as file:
	file.write("Number 	 Player1-win 	Player2-win ")
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
