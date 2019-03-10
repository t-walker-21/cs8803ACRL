import gym
import time

# cartPos,cartVel,PolePos,PoleVel
NUM_STATES_CART_POS = 5
NUM_STATES_CART_VEL = 3
NUM_STATES_POLE_ANG = 5
NUM_STATES_POLE_VEL = 10

CARTPOLELOWER = -2.4
CARTPOLEUPPER = 2.4
CARTVELUPPER = 2
CARTVELLOWER = -2
POLEANGLOWER = -1.5
POLEANGUPPER = 1.5
POLEVELLOWER = -8
POLEVELUPPER = 8

env = gym.make('CartPole-v0')
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


def discretize(state):

    dSpace = []

    for i in range(NUM_STATES_CART_POS):
        interval = cartPolStateDict[i]
        if (state[0] < interval[1] and state[0] > interval[0]):
            print state[0],i, "cart pos"
            dSpace.append(i)

            break

    for i in range(NUM_STATES_CART_VEL):
        interval = cartVelStateDict[i]
        if (state[1] < interval[1] and state[1] > interval[0]):
            print state[1],i, "cart vel"
            dSpace.append(i)

            break

    for i in range(NUM_STATES_POLE_ANG):
        interval =  polAngStateDict[i]
        if (state[2] < interval[1] and state[2] > interval[0]):
            print state[2],i, "pole ang"
            dSpace.append(i)
            break


    for i in range(NUM_STATES_POLE_VEL):
        interval = polVelStateDict[i]
        if (state[3] < interval[1] and state[3] > interval[0]):
            print state[3],i, "pole vel"
            dSpace.append(i)
            break
    
    return dSpace


for i in range(1000):
    env.render()
    act = env.action_space.sample()
    #print act
    ret = env.step(1)
    state = ret[0]
    print discretize(state)
    time.sleep(1)