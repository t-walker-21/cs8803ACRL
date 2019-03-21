# -*- coding: utf-8 -*-
import socket
import time as pytime
import random
import gym
import cv2
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.layers.convolutional import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten

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


#make a convolutional feature extractor!

feats = Sequential()
feats.add(Conv2D(16,(3,3),activation='relu',input_shape=(105,50,3)))
feats.add(MaxPooling2D((2,2)))
feats.add(Conv2D(32,(3,3),activation='relu'))
feats.add(MaxPooling2D((2,2)))
feats.add(Conv2D(64,(3,3),activation='relu'))
feats.add(MaxPooling2D((2,2)))
feats.add(Flatten())



class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.5    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.0
        self.epsilon_decay = 0.9995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(512, input_dim=self.state_size, activation='sigmoid'))
        model.add(Dense(512, activation='sigmoid'))
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
  
  for s in state:
   st.append(s)
  
  st2 = st[:]
  st.reverse()
  print "here"
  #piece = st[0]
  st = np.array(st,dtype=np.float32).reshape((21,10))
  st = np.fliplr(st)
  stIm = np.zeros((21,10,3))
  #print stIm.shape
  #print st.shape
  stIm[:,:,0] = st
  stIm[:,:,1] = st
  stIm[:,:,2] = st

  stIm = cv2.resize(stIm,(50,105))

  X = []
  X.append(stIm)
  X = np.array(X)
  #print X.shape
  out = feats.predict(X)[0]
  #print out.shape
  cv2.imshow("stateRaw",stIm)
  cv2.waitKey(1)

  #print st
    

  return out 


if __name__ == "__main__":


    state_size = 2816#210#env.observation_space.shape
    action_size = 20#40
    
    
    agent = DQNAgent(state_size, action_size)
    # agent.load("./save/cartpole-dqn.h5")
    done = False
    batch_size = 64

    for e in range(EPISODES):
        state = stringStateToNN(("0"*(210))) #initial state of no pieces on board
        
        state = np.reshape(state, [1, state_size])
        for time in range(5000):
            #env.render()
            action = agent.act(state)
            #pytime.sleep()
	        #take the action
            #print "sending response: " , str(action)
            sock2.sendto(str(action),(UDP_IP,5006))

            #next_state, reward, done, _ = env.step(action)
            #receive feedback
            nxtState, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            #print "next state: ", nxtState
            reward, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            reward = int(reward)
            #print "reward: ", reward
            done, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            if done == "false":
                done = False
            else:
                done = True
            #print "done: ", done

            if (reward == 5):
                print "line cleared!!"

            print "I've been alive for: " , time

            #reward = reward if not done else -10
            next_state = stringStateToNN(nxtState)
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
           
            if done:
                print("episode: {}/{}, score: {}, e: {:.2}".format(e, EPISODES, time, agent.epsilon))
                break

            
            if time > 4995:
                print "I beat the game!"
                exit()

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

            #if e % 10 == 0:
            #agent.save("./save/cartpole-dqn.h5")
