import sys
import time
import numpy as np
import random
import math
# According to the implementation, global storage is being done automatically by board_states_to_action_vectors.
# Local storage is being done in actions_taken vector.
# Here, instead of mapping current board state and move to be played, we map resultant board state and move that was played.
n=3
alpha_L=0.1 # should we change the learning rate i.e. decay it over training?
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


board_states_to_action_vectors={}
board_states_to_value_vectors={}
# The 2 lines below are for UCB:
# play_count={}
# win_count={}
empty_board_state='.'*(n*n)
# print(empty_board_state)
number_of_epochs=100
player1_win_track=np.zeros(number_of_epochs)
player2_win_track=np.zeros(number_of_epochs)
player1_win=0
player2_win=0
for epoch_number in range(number_of_epochs):
	print(epoch_number+1)
	board_state=empty_board_state
	actions_taken=[]
	while(find_if_terminal(board_state)==False):
		# the function below finds the action vector of the present board state and creates one if it is not present
		# print(board_state)
		if(board_states_to_action_vectors.get(board_state)==None):
			action_vector=[0]*(n*n)
			value_vector=[0]*(n*n)
			sum_values=0
			length=len(board_state)
			for j in range(length):
				# working on initialization of action probability values
				if(board_state[j]=='.'):
					value_vector[j]=1
				# the 2 lines below initialize the centre of board with higher value so that the first player tempts to play at the centre.
				# if(j==length/2):
				# 	value_vector[j]=2
			sum_values=sum(value_vector)
			for j in range(length):
				if(board_state[j]=='.'):
					action_vector[j]=value_vector[j]/sum_values
			board_states_to_value_vectors[board_state]=value_vector
			board_states_to_action_vectors[board_state]=action_vector

		maxm_prob=0
		# finding the best action to take - using epsilon greedy policy here. 
		epsilon=0.1 # how to decide optimal value of epsilon here?
		for j in range(n*n):
			if(action_vector[j]>maxm_prob and board_state[j]=='.'):
				maxm_prob=action_vector[j]
		list_max_indices=[]
		for j in range(n*n):
			if(action_vector[j]==maxm_prob and board_state[j]=='.'):
				list_max_indices.append(j)
		random_value=random.random()
		if(random_value>=epsilon):
			position_played=random.choice(list_max_indices)
		else:
			position_played=random.randint(0,n*n-1)
			while(board_state[position_played]=='X'):
				position_played=random.randint(0,n*n-1)
		assert board_state[position_played]!='X'
		board_state=board_state[:position_played]+'X'+board_state[position_played+1:]
		# The 6 lines below are for UCB
		# if(play_count.get((board_state,position_played))==None):
		# 	play_count[(board_state,position_played)]=1
		# else:
		# 	play_count[(board_state,position_played)] += 1
		# if(win_count.get((board_state,position_played))==None):
		# 	win_count[(board_state,position_played)]=0
		actions_taken.append((board_state,position_played))
	
	# the code below is to create the action vector for last encountered state i.e. terminal state
	if(board_states_to_action_vectors.get(board_state)==None):
		action_vector=[0]*(n*n)
		value_vector=[0]*(n*n)
		board_states_to_value_vectors[board_state]=value_vector
		board_states_to_action_vectors[board_state]=action_vector

	# print(actions_taken)
	cnt_x=board_state.count('X')
	player_win=0
	reward=0
	# theta=math.sqrt((epoch_number+1)/number_of_epochs)
	theta=1
	num_moves=len(actions_taken)
	# how to design reward function and theta(These are required when terminal state is reached, to update action vectors)? 
	# how to design value function and Q-function(These are required at every intermediate state)? Options: 1. Bellman Equation, 2. Learning rate and forgetting rate using equations in "parameter setting" paper
	# In our case, I feel that there is no value function.
	# the reward is oriented in support of player 1 => reward is +ve if player 1 wins.
	if(cnt_x%2==0):
		player_win=1
		player1_win=player1_win+1
		reward=theta/num_moves
		# reward=n*n
	else:
		player_win=2
		player2_win=player2_win+1
		# reward=-1*n*n
		reward=-1*theta/num_moves
	# updating the actions_taken vector using decided reward(a kind of backpropagation)
	# how to update the probability values of actions taken, using the reward?
	action_number=1
	for board_state, position_played in actions_taken:
		value_vector=board_states_to_value_vectors[board_state]
		if(action_number%2==1): # => the current moves was played by player 1.
			# if(reward>0):
			# 	win_count[(board_state,position_played)] +=1
			value_vector[position_played] += reward
			# value_vector[position_played] += alpha_L*(reward-value_vector[position_played])	
			# value_vector[position_played] += reward*win_count[(board_state,position_played)]/play_count[(board_state,position_played)]
		
		else: # => the current moves was played by player 2.
			# if(reward<0):
			# 	win_count[(board_state,position_played)] +=1
			value_vector[position_played] -= reward 
			# value_vector[position_played] -= alpha_L*(reward-value_vector[position_played]) 
			# value_vector[position_played] -= reward*win_count[(board_state,position_played)]/play_count[(board_state,position_played)]
		
		# we are using standard Q-learning model i.e. alpha_F => changing parameter for unchosen options is 0.
		sum_values=sum(value_vector)
		action_vector=board_states_to_action_vectors[board_state]
		for j in range(len(value_vector)):
			action_vector[j]=value_vector[j]/sum_values
		# binarization of the action vectors using xnor net technique - this doesn't seem to work for us since everytime we approximate the action vector with binary vector, we will get same probability for all action values in that action vector..? 
		# sign_vector=np.sign(action_vector)
		# alpha_scale=sum(np.absolute(action_vector))/(n*n)
		# action_vector=alpha_scale*sign_vector
		action_number += 1
	# the winning probabilities of both players based on the reward being given after every epoch
	player1_win_track[epoch_number]=player1_win/(epoch_number+1)
	player2_win_track[epoch_number]=player2_win/(epoch_number+1)

print("Number 	 Player1-win 	Player2-win ")
for epoch_number in range(number_of_epochs):
	print(epoch_number+1, "	",player1_win_track[epoch_number],"	", player2_win_track[epoch_number])	
	# This strategy involves more amount of exploitation and relatively less exploration. It is a kind of epsilon greedy algo. How to solve this?
	# it is being trained in negative direction for player1. How to solve this?
	# how to define state-value here?
	# think about choice trace weight, choice correlation factor.
	# Future work: To try Posterior Sampling Technique.
	# For UCB, we need to store win_count[board_state][position] and play_count[board_state][position] for each possible position of each possible board state. However, this actually doesn't seem to work for us since win_count=0 for some move => reward change in that move will be 0 whereas we wan't reward change to be non-zero always.
	# In UCB, reward change for each chosen move will be different.
