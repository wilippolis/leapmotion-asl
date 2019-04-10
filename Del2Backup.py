# -*- coding: utf-8 -*-
import globalVariables as gv
import matplotlib.pyplot as plt
import Leap

def adjustWindow(x, y):
    # If x coordinate is smaller than window,
    # shrink window width to fit
    if ( x < gv.xMin ):
        gv.xMin = x

    # If x coordinate is larger than window,
    # increase window width
    if ( x > gv.xMax ):
        gv.xMax = x 

    # If y coordinate is smaller than window,
    # shrink window height
    if ( y < gv.yMin ):
        gv.yMin = y

    # If y coordinate is larger than window,
    # shrink window height
    if ( y > gv.yMax ):
        gv.yMax = y

def main():
    # Instantiate plot object
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(-400,400)
    ax.set_ylim(-400,400)

    # Define controller object
    controller = Leap.Controller()

    bones = {}
    for i in range(0,5):
        for j in range(0,4):
            bones[i,j], = plt.plot([0,0] , [0,0])    

    # Set limits for plot window
    plt.xlim(gv.xMax, gv.xMin)
    plt.ylim(gv.yMax, gv.yMin)

    # Initiate while loop
    while True:
        frame = controller.frame()

        # If hands are present
        if(len(frame.hands) > 0):
            # Parse input to find distal phalanx
            hand = frame.hands[0]
            for i in range(0,5):
                finger = hand.fingers[i]
                for j in range(0,4):
                    bone = finger.bone(j)
                    boneBase = bone.prev_joint
                    boneTip = bone.next_joint
                    xBase = boneBase.x
                    zBase = -1 * boneBase.z
                    xTip = boneTip.x
                    zTip = -1 * boneTip.z
                    bones[i,j].set_xdata([ xBase , xTip ])
                    bones[i,j].set_ydata([ zBase , zTip ]) 
                    adjustWindow(boneBase.x, boneBase.y)  

        # Render plot
        plt.draw()

        # Set timeout 
        plt.pause(0.00001)

main()
