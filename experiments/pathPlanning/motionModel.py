import numpy as np
import cv2
import pdb



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


x = 5
y = 5
theta = 0

control = 0.0


print x,y,theta, "beggining"
#pdb.set_trace()


world = np.ones((500,500,3))


while True:
    world2 = np.ones((500,500,3))
    control = 0

    x,y,theta = apply_model(x,y,theta,control)

    print x,y,theta




    cv2.circle(world2,(int(x),int(y)),2,(200,0,0),-1,1)


    
    cv2.imshow("car",world2)
    cv2.waitKey(1000)