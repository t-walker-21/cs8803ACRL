import gym
import time
import numpy as np

# cartPos,cartVel,PolePos,PoleVel
NUM_STATES_CART_POS = 11
NUM_STATES_CART_VEL = 11
NUM_STATES_POLE_ANG = 11
NUM_STATES_POLE_VEL = 11

CARTPOLELOWER = -2.4
CARTPOLEUPPER = 2.4
CARTVELUPPER = 7
CARTVELLOWER = -7
POLEANGLOWER = -1.5
POLEANGUPPER = 1.5
POLEVELLOWER = -8
POLEVELUPPER = 8

env = gym.make('CartPole-v0')
env.env.theta_threshold_radians = 1
print (env.env.theta_threshold_radians)

env.reset()

#build stateDict to map discrete states to ranges
cartPolStateDict = {}
cartVelStateDict = {}
polAngStateDict = {}
polVelStateDict = {}

step = (CARTPOLEUPPER*2)/NUM_STATES_CART_POS
step2 = (CARTVELUPPER*2)/NUM_STATES_CART_VEL
step3 = (POLEANGUPPER*2)/NUM_STATES_POLE_ANG
step4 = (POLEVELUPPER*2)/NUM_STATES_POLE_VEL

for i in range(NUM_STATES_CART_POS):
    #print i, (CARTPOLELOWER+i*step,CARTPOLELOWER+i*step+step)
    cartPolStateDict[i] = (CARTPOLELOWER+i*step,CARTPOLELOWER+i*step+step)

for i in range(NUM_STATES_CART_VEL):
    #print i, (CARTVELLOWER+i*step2,CARTVELLOWER+i*step2+step2)
    cartVelStateDict[i] = (CARTVELLOWER+i*step2,CARTVELLOWER+i*step2+step2)

for i in range(NUM_STATES_POLE_ANG):
    #print i, (POLEANGUPPER+i*step3,POLEANGUPPER+i*step3+step3)
    polAngStateDict[i] = (POLEANGLOWER+i*step3,POLEANGLOWER+i*step3+step3)

for i in range(NUM_STATES_POLE_VEL):
    #print i, (POLEVELUPPER+i*step4,POLEVELUPPER+i*step4+step4)
    polVelStateDict[i] = (POLEVELLOWER+i*step4,POLEVELLOWER+i*step4+step4)

#print cartPolStateDict
#print cartVelStateDict
#print polAngStateDict
#print polVelStateDict

#exit()

stateMap = {}
counter = 0

#for i in range(NUM_STATES_CART_POS): #cart pos
for j in range(NUM_STATES_CART_VEL): #cart vel
    for k in range(NUM_STATES_POLE_ANG): #pol ang
        #print i,j,k
        stateMap[(j,k)] = (counter)
        counter += 1




def discretize(state):

    dSpace = []

    """for i in range(NUM_STATES_CART_POS):
        interval = cartPolStateDict[i]
        if (state[0] < interval[1] and state[0] > interval[0]):
            #print state[0],i, "cart pos"
            dSpace.append(i)

            break"""

    for i in range(NUM_STATES_CART_VEL):
        interval = cartVelStateDict[i]
        if (state[1] < interval[1] and state[1] > interval[0]):
            #print state[1],i, "cart vel"
            dSpace.append(i)

            break

    for i in range(NUM_STATES_POLE_ANG):
        interval =  polAngStateDict[i]
        if (state[2] < interval[1] and state[2] > interval[0]):
            #print state[2],i, "pole ang"
            dSpace.append(i)
            break


    """for i in range(NUM_STATES_POLE_VEL):
        interval = polVelStateDict[i]
        if (state[3] < interval[1] and state[3] > interval[0]):
            print state[3],i, "pole vel"
            dSpace.append(i)
            break"""
    
    dSpace = (dSpace[0],dSpace[1])
    return dSpace



eps = 0.99
alpha = 0.8
gamma = 0.9

q_table = np.zeros((pow(NUM_STATES_CART_POS,2),2))



def choose_action(state):
    if (np.random.random() < eps):
        act = np.random.randint(1)
        #print "random!"
    else:
        act = np.argmax(q_table[state])
        
    #print "taking action: ", act
    return act


state = (5,5)
state = stateMap[state]
#print "mapped -->", stateMap[state]
maxVel = 0
totalReward = 0
maxReward = 0

for i in range(90000):
    q_table_old = q_table[:]
    act = choose_action(state)
    obs = env.step(act)
    nextState = obs[0]
    maxVel = max([maxVel,abs(obs[0][1])])
    nextState = discretize(nextState)
    #print obs
    env.render()

    if (obs[2]):
        env.reset()
        state = (5,5)
        state = stateMap[state]
        totalReward = 0
        continue

    if not(obs[0][2] > -0.1 and obs[0][2] < 0.1): #reward agent with -1 if it doesn't enter stability
        reward = -1
        nextState = stateMap[nextState]
        q_table[state][act] = q_table_old[state][act] + alpha * (reward + gamma*max(q_table_old[nextState])-q_table_old[state][act])
    
        #print q_table[14][2]
        #print "SCORE!!!"
        continue

    totalReward += 1

    maxReward = max(totalReward,maxReward)

    if i % 100 == 0:
        print "epsilon: " , eps
        print "max vel: ", maxVel
        print "max reward: ", maxReward

    
    #print act    

    state = stateMap[nextState]
    eps *= 0.995
    #time.sleep(0.2)