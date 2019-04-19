import cv2
import numpy as np
REACHED_THRESH = 9



class Node:
    def __init__(self,x,y):
        self.edges = []
        self.confx = x
        self.confy = y


world = np.ones((500,500,3))
world2 = world[:][:][:] #for viz
start = np.array((49,380))
goal = np.array((380,36))
obst = np.array((50,50,100,100))
obst2 = np.array((80,200,288,210))
obst3 = np.array((200,200,400,300))

nodeList = []
nodeList.append(Node(start[0],start[1]))
nodeList.append(Node(goal[0],goal[1]))

#print nodeList



delta = 5
points = []

points.append(start)
cv2.circle(world,(start[0],start[1]),2,(200,0,0),1,1)
cv2.circle(world,(goal[0],goal[1]),2,(0,0,255),1,1)
cv2.rectangle(world,(obst[0],obst[1]),(obst[2],obst[3]),(0,0,0),-1)
cv2.rectangle(world,(obst2[0],obst2[1]),(obst2[2],obst2[3]),(0,0,0),-1)
cv2.rectangle(world,(obst3[0],obst3[1]),(obst3[2],obst3[3]),(0,0,0),-1)
cv2.circle(world,(380,320),4,(0,0,0),-1)


     



for _ in range(10000): 


    if (np.random.random() > 0.1):
        x,y = np.random.randint(1,len(world)-1,2)
    else:
        x = goal[0]
        y = goal[1]


    new_point = np.array((x,y))
    tempDist = 1000
    index = None
    unitVect = None
    for i in range(len(points)):
        dist = np.linalg.norm(points[i]-new_point)
        if (dist < tempDist):
            tempDist = dist
            index = i

    unitVect = (new_point - points[index])/tempDist


    scaledUnitVect = delta * unitVect
    scaledUnitVect = scaledUnitVect.astype(int)


    #print unitVect
    added_point = points[index] + scaledUnitVect

    if added_point[0] >= len(world):
        added_point[0] = len(world) - 1

    elif added_point[0] < 0:
        added_point[0] = 0


    if added_point[1] >= len(world):
        added_point[1] = len(world) - 1

    elif added_point[1] < 0:
        added_point[1] = 0

        
     
    #print "hard check: " , world[380][320]
    #print world[added_point[0]][added_point[1]]
    #print added_point
    if (world[added_point[1]][added_point[0]] != [1,1,1]).all() or (world[added_point[1]][added_point[0]] != [0,0,1]).all():
        #print "collision detected"
        continue

    points.append(added_point)
    
    cv2.line(world2,(points[index][0],points[index][1]),(added_point[0],added_point[1]),(0,0,0),1,1)
    cv2.circle(world2,(added_point[0],added_point[1]),1,(0,200,0),-1,1)
    cv2.waitKey(5)


    world_disp = cv2.resize(world2,(700,700))
    cv2.imshow("world",world_disp)
    
    #print np.linalg.norm(added_point-goal), added_point
    if (np.linalg.norm(added_point-goal) <= REACHED_THRESH):
        print "done!"
        break

    #cv2.waitKey(10)
cv2.imshow("world",world_disp)
cv2.waitKey(0)
