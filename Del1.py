# -*- coding: utf-8 -*-
import globalVariables as gv
from Leap import *
from pylab import *
import random

def adjustWindow(x, y):
    # If x coordinate is smaller than window,
    # shrink window width to fit
    if ( x < gv.xMin ):
        gv.xMin = x
        print("Decreasing width...")

    # If x coordinate is larger than window,
    # increase window width
    if ( x > gv.xMax ):
        gv.xMax = x 
        print("Increasing width...")

    # If y coordinate is smaller than window,
    # shrink window height
    if ( y < gv.yMin ):
        gv.yMin = y
        print("Decreasing height...")

    # If y coordinate is larger than window,
    # shrink window height
    if ( y > gv.yMax ):
        gv.yMax = y
        print("Increasing height...")

def main():
    # Instantiate plot object
    ion()
    show()

    # Set origin
    xPt = 0
    yPt = 0

    # Define controller object
    controller = Controller()

    # Plot (xPt, yPt)
    pt, = plot(xPt,yPt,'ko',markersize=20)

    # Set limits for plot window
    xlim(gv.xMax, gv.xMin)
    ylim(gv.yMax, gv.yMin)

    # Initiate while loop
    while True:
        frame = controller.frame()

        # If hands are present
        if(len(frame.hands) > 0):

            # Parse input to find distal phalanx
            hand = frame.hands[0]
            fingers = hand.fingers
            indexFingerList = fingers.finger_type(Finger.TYPE_INDEX)
            indexFinger = indexFingerList[0]
            distalPhalanx = indexFinger.bone(Bone.TYPE_DISTAL)
            distalPhalanxPosition = distalPhalanx.next_joint

            # Set coordinates to parsed data
            xPt = distalPhalanxPosition.x
            yPt = distalPhalanxPosition.y

            # Update plot
            pt.set_xdata(xPt)
            pt.set_ydata(yPt)

            # Adjust plot window based on coordinates
            adjustWindow(distalPhalanxPosition.x, distalPhalanxPosition.y)

            # Log coordinates
            print(distalPhalanxPosition)

        # Render plot
        draw()

        # Set timeout 
        pause(0.00001)

main()