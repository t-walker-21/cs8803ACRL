import gym
import numpy as np
import time

#env = gym.make('FrozenLake-v0')

from gym.envs.registration import register
register(
    id='FrozenLakeNotSlippery-v0',
    entry_point='gym.envs.toy_text:FrozenLakeEnv',
    kwargs={'map_name' : '8x8', 'is_slippery': False},
    max_episode_steps=100,
    reward_threshold=0.78, # optimum = .8196
)

env = gym.make('FrozenLakeNotSlippery-v0')
env.reset()
env.render()


eps = 0.01
alpha = 0.8
gamma = 0.95

q_table = np.zeros((64,4))

def choose_action(state):
    if (np.random.random() < eps):
        act = np.random.randint(4)
        print "random!"
    else:
        act = np.argmax(q_table[state])
        
    print "taking action: ", act
    return act

episodes = 100000

state = 0
scoreCount = 0
deathCount = 0
delay = .01
for ep in range(0,episodes):
    if ep > episodes*0.99999:
        delay = 1

    q_table_old = q_table[:]
    act = choose_action(state)
    print "scoreCount: ",scoreCount
    print "deathCount: ", deathCount
    #act = input()
    obs = env.step(act)
    env.render()
    nextState = obs[0]
    reward = obs[1]
    print obs

    if (obs[2] and obs[0] == 63):
        reward = 5
        env.reset()
        q_table[state][act] = q_table_old[state][act] + alpha * (reward + gamma*max(q_table_old[nextState])-q_table_old[state][act])
        state = 0
        print q_table[14][2]
        
        print "SCORE!!!"
        scoreCount += 1
        #time.sleep(0.2)
        continue

    elif(obs[2]):
        reward = -1
        env.reset()
        q_table[state][act] = q_table_old[state][act] + alpha * (reward + gamma*max(q_table_old[nextState])-q_table_old[state][act])
        state = 0
        deathCount += 1
        #print "fell in hole!"
        #time.sleep(delay*2)
        continue


    elif(state == nextState):
        reward = -0.7
        
        q_table[state][act] = q_table_old[state][act] + alpha * (reward + gamma*max(q_table_old[nextState])-q_table_old[state][act])
        print "bumped into wall!"
        #print q_table
        #time.sleep(delay*2)
        continue

    reward = -0.001
    q_table[state][act] = q_table_old[state][act] + alpha * (reward + gamma*max(q_table_old[nextState])-q_table_old[state][act])    
    
    #print q_table
    eps *= 0.99995
    time.sleep(delay)
    state = nextState
    print eps
    if scoreCount > 300:
        break


print q_table