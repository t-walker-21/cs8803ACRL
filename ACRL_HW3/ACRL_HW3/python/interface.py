import sys
import numpy as np

def main():
    statex = float(sys.argv[1])
    statey = float(sys.argv[2])
    theta = float(sys.argv[3])
    goalx = float(sys.argv[4])
    goaly = float(sys.argv[5])

    yDiff = goaly - statey
    xDiff = goalx - statex


    
    #print xDiff, yDiff
    angle = np.arctan(yDiff/xDiff)

    if (xDiff < 0 and yDiff > 0):
        angle += 180 * np.pi / 180

    elif (xDiff < 0 and yDiff < 0):
        angle -= 180 * np.pi / 180




    error = (theta - angle) * -1.5

    #print error

    if (error > 1):
        error = 1

    elif (error < -1):
        error = -1


    sys.stdout.write(str(error))


if __name__ == '__main__':

    main()