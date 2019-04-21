import numpy as np
import cv2
import pdb



def draw_angled_rec(x0, y0, width, height, angle, img):

    _angle = angle * np.pi / 180.0
    b = np.cos(_angle) * 0.5
    a = np.sin(_angle) * 0.5
    pt0 = (int(x0 - a * height - b * width),
           int(y0 + b * height - a * width))
    pt1 = (int(x0 + a * height - b * width),
           int(y0 - b * height - a * width))
    pt2 = (int(2 * x0 - pt0[0]), int(2 * y0 - pt0[1]))
    pt3 = (int(2 * x0 - pt1[0]), int(2 * y0 - pt1[1]))

    return pt0,pt1,pt2,pt3




nominal_angle = 0.6
length = 3
width = 2
wb = 2.0
l_radius = 0.25
r_radius = 0.25

x = 10
y = 250
theta = 0

control = 0.0


print x,y,theta
#pdb.set_trace()


world = np.ones((500,500,3))


while True:
    world2 = np.ones((500,500,3))
    control = -0.1

    deltaLeft = nominal_angle - control
    deltaRight = nominal_angle + control

    R = r_radius * deltaRight
    L = l_radius * deltaLeft

    print R,L, "RL"

    if R == L:
        print "same"
        x += ((R+L) / 2) * np.cos(theta)
        y += ((R+L) / 2) * np.sin(theta)

    else:
        x += wb/2 * (R+L)/(R-L) * (np.sin((R-L)/wb + theta) - np.sin(theta))
        y -= wb/2 * (R+L)/(R-L) * (np.cos((R-L)/wb + theta) - np.cos(theta))
        
    theta += (R-L)/wb


    print x,y,theta

    cv2.circle(world2,(int(x),int(y)),2,(200,0,0),-1,1)

    pt0,pt1,pt2,pt3 = draw_angled_rec(int(x),int(y),14,7,theta,None)

    cv2.line(world2, pt0, pt1, (200, 0, 0), 1)
    cv2.line(world2, pt1, pt2, (200, 0, 0), 1)
    cv2.line(world2, pt2, pt3, (255, 0, 0), 1)
    cv2.line(world2, pt3, pt0, (255, 0, 0), 1)


    
    cv2.imshow("car",world2)
    cv2.waitKey(10)