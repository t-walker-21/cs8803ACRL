import sys
import numpy as np

def main():


    controls = np.linspace(-1,1,1000)

    print controls
    exit()
    statex = float(sys.argv[1])
    statey = float(sys.argv[2])
    theta = float(sys.argv[3])
    goalx = float(sys.argv[4])
    goaly = float(sys.argv[5])




    tempDistConf = 1e10
    x_final = 0
    y_final = 0
    theta_final = 0

    nominal_angle = 0.6
    length = 3
    width = 2
    wb = 2.0
    l_radius = 0.25
    r_radius = 0.25

    x_rob = statex 
    y_rob = statey
    theta_rob = theta
    

    bestCont = None

    for cont in controls:

        deltaLeft = nominal_angle - cont
        deltaRight = nominal_angle + cont

        R = r_radius * deltaRight
        L = l_radius * deltaLeft
        
        

        if R == L:
            
            xNew = x_rob + ((R+L) / 2) * np.cos(theta)
            yNew = y_rob + ((R+L) / 2) * np.sin(theta)

        else:
            xNew = x_rob + wb/2 * (R+L)/(R-L) * (np.sin((R-L)/wb + theta) - np.sin(theta))
            yNew = y_rob - wb/2 * (R+L)/(R-L) * (np.cos((R-L)/wb + theta) - np.cos(theta))
            
        thetaNew = theta + (R-L)/wb

        goal = np.array((goalx,goaly))
        now = np.array((xNew,yNew))

        dist = np.linalg.norm(goal-now)

        if (dist < tempDistConf):
            tempDistConf = dist
            x_final = xNew
            y_final = yNew
            theta_final = thetaNew
            bestCont = cont
            
            
    sys.stdout.write(str(cont))


if __name__ == '__main__':

    main()