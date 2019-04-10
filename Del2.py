# -*- coding: utf-8 -*-
import globalVariables as gv
import matplotlib.pyplot as plt
import numpy as np
import Leap
import pickle

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
        
def CenterData(X):
    allXCoordinates = X[0,::3]
    meanValue = allXCoordinates.mean()
    X[0,::3] = allXCoordinates - meanValue 
    allYCoordinates = X[0,1::3]
    meanValue = allYCoordinates.mean()
    X[0,1::3] = allYCoordinates - meanValue    
    allZCoordinates = X[0,2::3]
    meanValue = allZCoordinates.mean()
    X[0,2::3] = allZCoordinates - meanValue
    return X

def main():
    # Instantiate plot object
    clf = pickle.load( open('userData/classifier.p','rb'))
    testData = np.zeros((1,30),dtype='f')
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(-400,400)
    ax.set_ylim(-400,400)

    bones = {}
    for i in range(0,5):
        for j in range(0,4):
            bones[i,j], = plt.plot([0,0] , [0,0])    

    # Set limits for plot window
    plt.xlim(gv.xMax, gv.xMin)
    plt.ylim(gv.yMax, gv.yMin)
    
    # Define controller object
    controller = Leap.Controller()

    # Initiate while loop
    while True:
        frame = controller.frame()

        # If hands are present
        if(len(frame.hands) > 0):
            k = 0
            # Parse input to find distal phalanx
            hand = frame.hands[0]
            for i in range(0,5):
                finger = hand.fingers[i]
                for j in range(0,4):
                    bone = finger.bone(j)
                    boneBase = bone.prev_joint
                    boneTip = bone.next_joint
                    xBase = boneBase.x
                    zBase = boneBase.z
                    yTip = boneTip.y
                    xTip = boneTip.x
                    zTip = boneTip.z
                    bones[i,j].set_xdata([ xBase , xTip ])
                    bones[i,j].set_ydata([ -1 * zBase , -1 * zTip ]) 
                    if ( (j == 0) | (j == 3) ):
                        testData[0,k] = xTip
                        testData[0,k+1] = yTip
                        testData[0,k+2] = zTip
                        k = k + 3                    
                    adjustWindow(boneBase.x, boneBase.y)  
            
            testData = CenterData(testData)

            predictedClass = clf.predict(testData)

            print predictedClass

        # Render plot
        plt.draw()

        # Set timeout 
        plt.pause(0.0001)

main()