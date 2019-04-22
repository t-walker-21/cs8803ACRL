import cv2
import numpy as np
import pdb
import hashlib

REACHED_THRESH = 9


def apply_model(x_in,y_in,theta_in,control):


    d_theta_nom = 0.6
    length = 3
    width = 2
    wb = 2.0
    l_radius = 0.25
    r_radius = 0.25
    d_theta_max_dev = 0.2
    d_theta_reverse = d_theta_nom/3
    
    r_dTheta = d_theta_nom + d_theta_max_dev*control
    l_dTheta = d_theta_nom - d_theta_max_dev*control

    R = r_radius * r_dTheta
    L = l_radius * l_dTheta

    x_out = 0
    y_out = 0
    theta_out = 0

    #print R,L, "RL"

    if R == L:
        #print "same"
        x_out = x_in + ((R+L) / 2) * np.cos(theta)
        y_out = y_in + ((R+L) / 2) * np.sin(theta)

    else:
        x_out = x_in + wb/2 * (R+L)/(R-L) * (np.sin((R-L)/wb + theta) - np.sin(theta))
        y_out = y_in - wb/2 * (R+L)/(R-L) * (np.cos((R-L)/wb + theta) - np.cos(theta))
        
    theta_out  = theta_in + (R-L)/wb


    return x_out,y_out,theta_out



def buildGraph(vertices,edges):
 
 g = {}

 for vert in vertices:
  nodes = []
  

  for edge in edges:
   if (vert == edge[0]):
    #print vert,edge
    nodes.append(edge[1])

  g[vert] = nodes
  
 return g


def DFS(g,startNode,goalNode):
  queue = []
  visited = []
  maxQSize = 0

  queue.append(startNode)
    
  while len(queue) != 0:
    path = queue.pop(0)
    node = path[-32:]
    #print "node", node
    if node == goalNode:
      #print "Goal state found. Path is: ", path
      return path, maxQSize
    
      
    #get all edges of current node
    e = g[node]
    e = np.sort(np.array(e))
    #print "bordering states-->", e   
      
    for edge in e:
      #print edge
      if not(edge in visited):
        queue.insert(0,path+"-"+edge)
        visited.append(edge)
    
    if not(node in visited):
      visited.append(node)
    #print "visited", visited
    #print "queue", queue
    #if len(queue) > maxQSize:
      #maxQSize = len(queue)




edges = []


world = np.ones((800,800,3))
world2 = world[:][:][:] #for viz
start = np.array((49,680,0))
goal = np.array((600,40,0))
obst = np.array((50,50,600,100))
obst2 = np.array((80,200,488,210))
obst3 = np.array((200,200,400,300))


#print nodeList



delta = 10
points = []
pointsHashed = []
hashmap = {}


hashed = hashlib.md5(start).hexdigest()
hashmap[hashed] = start

points.append(start)
pointsHashed.append(hashed)
cv2.circle(world,(start[0],start[1]),2,(200,0,0),1,1)
cv2.circle(world,(goal[0],goal[1]),2,(0,0,255),1,1)
cv2.rectangle(world,(obst[0],obst[1]),(obst[2],obst[3]),(0,0,0),-1)
cv2.rectangle(world,(obst2[0],obst2[1]),(obst2[2],obst2[3]),(0,0,0),-1)
cv2.rectangle(world,(obst3[0],obst3[1]),(obst3[2],obst3[3]),(0,0,0),-1)
cv2.circle(world,(380,320),4,(0,0,0),-1)


     



for _ in range(10000): 


    if (np.random.random() > 0.2):
        x,y = np.random.randint(1,len(world)-1,2)
        theta = np.random.normal(-2*np.pi,2*np.pi)
    else:
        x = goal[0]
        y = goal[1]
        theta = 0


    new_point = np.array((x,y,theta))
    tempDist = 1000
    index = None
    unitVect = None
    for i in range(len(points)):
        dist = np.linalg.norm(points[i]-new_point)
        if (dist < tempDist):
            tempDist = dist
            index = i

    #print tempDist
 
    if (tempDist < 1e-4):
     continue

    unitVect = (new_point - points[index])/tempDist
    

    scaledUnitVect = delta * unitVect
    scaledUnitVect[0] = int(scaledUnitVect[0])
    scaledUnitVect[1] = int(scaledUnitVect[1])


    
    
    
    
    random_point = points[index] + scaledUnitVect

    print "random conf: " , random_point

    

    if random_point[0] >= len(world):
        random_point[0] = len(world) - 1

    elif random_point[0] < 0:
        random_point[0] = 0


    if random_point[1] >= len(world):
        random_point[1] = len(world) - 1

    elif random_point[1] < 0:
        random_point[1] = 0

    if random_point[3] > 2*np.pi:
        random_point[3] -= 2*np.pi

    elif random_point[3] < -2*np.pi:
        random_point[3] += 2*np.pi
        

    #now that I've sampled a random configuration within some delta of the current configuration,
    #generate a control that gets the closest to this random configuration.

    controls = np.random.normal


        
     
    #print "hard check: " , world[380][320]
    #print world[added_point[0]][added_point[1]]
    #print added_point
    if (world[random_point[1]][random_point[0]] != [1,1,1]).all() or (world[random_point[1]][random_point[0]] != [0,0,1]).all():
        #print "collision detected"
        continue


    hashed = hashlib.md5(random_point).hexdigest()
    hashmap[hashed] = random_point
    points.append(random_point)
    pointsHashed.append(hashed)
    edges.append([hashlib.md5(points[index]).hexdigest(),hashed])
    
    cv2.line(world2,(points[index][0],points[index][1]),(random_point[0],random_point[1]),(0,0,0),1,1)
    cv2.circle(world2,(random_point[0],random_point[1]),1,(0,200,0),-1,1)
    cv2.waitKey(1)


    world_disp = cv2.resize(world2,(700,700))
    cv2.imshow("world",world_disp)
    
    #print np.linalg.norm(added_point-goal), added_point
    if (np.linalg.norm(random_point-goal) <= REACHED_THRESH):
        #print "done!"
        #print len(points)
        #print len(edges)

        graph = buildGraph(pointsHashed,edges)
        #print graph[str(points[0])]
        startVert = hashlib.md5(start).hexdigest()
        goalVert = hashlib.md5(added_point).hexdigest()
        path,_ = DFS(graph,startVert,goalVert)
        path = path.split("-")
        
        finalPath = []

        for pNum in range(len(path)-1):
            temp = hashmap[path[pNum]]
            temp2 = hashmap[path[pNum+1]]
            cv2.line(world2,(temp[0],temp[1]),(temp2[0],temp2[1]),(20,0,20),3,1)
            cv2.circle(world2,(temp[0],temp[1]),2,(0,200,0),1,1)

            finalPath.append(temp)

        #print finalPath



        break

    #cv2.waitKey(10)
world_disp = cv2.resize(world2,(700,700))
cv2.imshow("world",world_disp)
cv2.waitKey(0)
#pdb.set_trace()
