import cv2
import numpy as np
REACHED_THRESH = 2


world = np.ones((500,500,3))
start = np.array((5,5))
goal = np.array((400,400))
delta = 25
points = []

points.append(start)
cv2.circle(world,(start[0],start[1]),2,(200,0,0),8,1)
cv2.circle(world,(goal[0],goal[1]),2,(0,0,200),8,1)


while True: 
    x,y = np.random.randint(0,len(world),2)

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


    unitVect *= delta
    unitVect = unitVect.astype(int)
    #print unitVect
    added_point = points[index] + unitVect
    points.append(added_point)
    
    cv2.line(world,(points[index][0],points[index][1]),(added_point[0],added_point[1]),(0,0,0),1,1)
    cv2.circle(world,(added_point[0],added_point[1]),1,(0,200,0),8,1)

    world_disp = cv2.resize(world,(600,600))
    cv2.imshow("world",world_disp)
    if (np.linalg.norm(added_point-goal) <= REACHED_THRESH):
        print "done!"
        break

    cv2.waitKey(10)

cv2.waitKey(0)
