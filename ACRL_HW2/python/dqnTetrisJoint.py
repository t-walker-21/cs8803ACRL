# -*- coding: utf-8 -*-
import socket
import time as pytime
import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

EPISODES = 100000

UDP_IP = "localhost"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

sock2 = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
"""
while True:
    resp = str(input())
    print "sending response: " , resp
    sock2.sendto(resp,(UDP_IP,5006))

    nxtState, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "next state: ", nxtState
    reward, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "reward: ", reward
    done, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "done: ", done"""

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.5    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.0
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(25, input_dim=self.state_size, activation='sigmoid'))
        model.add(Dense(25, activation='sigmoid'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            print "random!!"
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
	
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


class DQNAgent2:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.5    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.0
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(50, input_dim=self.state_size, activation='sigmoid'))
        model.add(Dense(50, activation='sigmoid'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            print "random!!"
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
	
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


def stringStateToNN(state):
  st = []
  state = state.split(",")
  #print "corrected state: " , state
  for s in state:
   if s == "":
       continue
   s = int(s) / 1.0
   st.append(s)

  #print "state is: " , st
  return np.array(st) 


if __name__ == "__main__":


    state_size = 10#env.observation_space.shape
    action_size = 20
    
    
    agent = DQNAgent(state_size, action_size)
    agent2 = DQNAgent(state_size, action_size)
    agent3 = DQNAgent(20, 40)
    agent4 = DQNAgent(20, 40)
    agent5 = DQNAgent2(20, 40)
    agent6 = DQNAgent2(20, 40)
    agent7 = DQNAgent2(20, 40)

    agent.load("dqn1.h5")
    agent2.load("dqn0.h5")
    agent3.load("dqn2.h5")
    agent4.load("dqn3.h5")
    agent5.load("dqn4.h5")
    agent6.load("dqn5.h5")
    agent7.load("dqn6.h5")

    agent.epsilon = 0
    agent2.epsilon = 0
    agent3.epsilon = 0
    agent4.epsilon = 0
    agent5.epsilon = 0
    agent6.epsilon = 0
    agent7.epsilon = 0
    done = False
    batch_size = 64
    e = 0
    while True:
        print "done? --> " , done

        if (e == 0):
            state, _ = sock.recvfrom(1024) # buffer size is 1024 bytes
            state = stringStateToNN(state) #initial state
        
        print state.shape
        if (state.shape[0] == 20):
            if (state[0] <= 1):
                state = state[:10]
                state = np.reshape(state, [1, state_size])

            else:
                state = np.reshape(state, [1, 20])

        else:
            if (state[0][0] <= 1):
                state = state[:10]
                state = np.reshape(state, [1, state_size])

            else:
                state = np.reshape(state, [1, 20])

        for time in range(1000):
            #env.render()
            if (state[0][0] == 0):
                action = agent2.act(state)
            
            elif (state[0][0] == 1):
                action = agent.act(state)

            elif (state[0][0] == 2):
                action = agent3.act(state)

            elif (state[0][0] == 3):
                action = agent4.act(state)

            elif (state[0][0] == 4):
                action = agent5.act(state)

            elif (state[0][0] == 5):
                action = agent6.act(state)

            elif (state[0][0] == 6):
                action = agent7.act(state)

            

            pytime.sleep(.250)
	        #take the action
            #print "sending response: " , str(action)
            sock2.sendto(str(action),(UDP_IP,5006))

            #next_state, reward, done, _ = env.step(action)
            #receive feedback
            reward, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            reward = int(reward)
            print "reward: ", reward
            done, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            if done == "false":
                done = False
            else:
                done = True
            #print "done: ", done

            nxtState, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            #print "next state: ", nxtState

            if (reward == 5):
                print "line cleared!!"

            print "I've been alive for: " , time

            #reward = reward if not done else -10
            next_state = stringStateToNN(nxtState)
            if (next_state[0] <= 1):
                next_state = next_state[:10]
                next_state = np.reshape(next_state, [1, state_size])
                

            else:
                next_state = np.reshape(next_state, [1, 20])

            agent.remember(state, action, reward, next_state, done)
            state = next_state
           
            if done:
                print "episodes: ", time
                #print("episode: {}/{}, score: {}, e: {:.2}".format(e, EPISODES, time))#, agent.epsilon))
                break

            
            if time > 995:
                pass
                #print "I beat the game!"
                #agent.save("./dqn0.h5")
                #exit()

            if len(agent.memory) > batch_size:
                pass
                #agent.replay(batch_size)
            e += 1

            #if e % 10 == 0:
            #agent.save("./save/cartpole-dqn.h5")
