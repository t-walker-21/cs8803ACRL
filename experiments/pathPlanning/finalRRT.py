import numpy as np
import cv2

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
        x_out = x_in + ((R+L) / 2) * np.cos(theta_in)
        y_out = y_in + ((R+L) / 2) * np.sin(theta_in)

    else:
        x_out = x_in + wb/2 * (R+L)/(R-L) * (np.sin((R-L)/wb + theta_in) - np.sin(theta_in))
        y_out = y_in - wb/2 * (R+L)/(R-L) * (np.cos((R-L)/wb + theta_in) - np.cos(theta_in))
        
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




world = np.ones((500,500,3))

#time steps
t_steps = 4

#rrt algorithm

#control samples
controls = [0.001,-0.001]

print(controls)



#starting config
s_config = np.array((50,50,0))

#goal region
g_region = np.array((300,300))


pointsQueue = []
pointsQueue.append(s_config)


cv2.circle(world,(s_config[0],s_config[1]),2,(0,0,200),-1,1)
cv2.circle(world,(g_region[0],g_region[1]),2,(200,0,0),-1,1)



for _ in range(10000):

    root = pointsQueue.pop(0)
    x_new = root[0]
    y_new = root[1]
    theta_new = root[2]
    print len(pointsQueue)
    



    for cont in controls:
        print cont
        
        for _ in range(t_steps):
            x_new,y_new,theta_new = apply_model(x_new,y_new,theta_new,cont)
        
        
        newPoint = np.array((x_new,y_new,theta_new))
        print newPoint
        cv2.circle(world,(int(newPoint[0]),int(newPoint[1])),1,(0,200,0),-1,1)
        pointsQueue.append(newPoint)
        cv2.imshow("im",world)
        cv2.waitKey(1)
    

cv2.imshow("im",world)
cv2.waitKey(0)
