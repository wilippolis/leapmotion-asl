# -*- coding: utf-8 -*-
import globalVariables as gv
import matplotlib.pyplot as plt
import numpy as np
import Leap

class Deliverable:
    
    def __init__(self):
        # Instantiate plot object
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(-400,400)
        self.ax.set_ylim(-400,400)
        self.previousNumberOfHands = 0
        self.currentNumberOfHands = 0
        self.gestureData = np.zeros((5,4,6),dtype='f')
        self.numberOfGesturesSaved = 0
            
        # Connect to Leap controller
        self.controller = Leap.Controller()
    
        # Initialize bones object
        self.bones = {}
        
        # Set default coordinates to origin
        for i in range(0,5):
            for j in range(0,4):
                self.bones[i,j], = plt.plot([0,0] , [0,0])    
    
        # Set limits for plot window
        plt.xlim(gv.xMax, gv.xMin)
        plt.ylim(gv.yMax, gv.yMin)
        
    def runForever(self):
        # Initiate infinite loop
        while True:
            self.runOnce(self.controller.frame())
            self.drawPlot()
            
    def runOnce(self, frame):
        # If hands are present
        self.previousNumberOfHands = self.currentNumberOfHands
        self.currentNumberOfHands = len(frame.hands)
        print(self.currentNumberOfHands)
        if(self.currentNumberOfHands > 0):
            self.handleHand(frame.hands[0])
        
    def handleHand(self, hand):
        # Initialize ranged loop for fingers in hand
        for i in range(0,5):
            self.handleFinger(hand.fingers[i], i)
        if (self.RecordingIsEnding()):
            print self.numberOfGesturesSaved
            self.saveGesture()
            
    def handleFinger(self, finger, i):        
        # Initialize ranged loop for bones in fingers
        for j in range(0,4):
            self.handleBone(finger.bone(j), i, j)
    
    def handleBone(self, bone, i, j):
        boneBase = bone.prev_joint
        boneTip = bone.next_joint
        print(boneBase)
        print(boneTip)
        xBase = boneBase.x
        xTip = boneTip.x
        zBase = -1 * boneBase.z
        zTip = -1 * boneTip.z
        self.bones[i,j].set_xdata([ xBase , xTip ])
        self.bones[i,j].set_ydata([ zBase , zTip ]) 
        self.bones[i,j].set_linewidth(4)
        if(self.currentNumberOfHands == 1):
            self.bones[i,j].set_color('g')
        elif(self.currentNumberOfHands == 2):
            self.bones[i,j].set_color('r')
        if(self.RecordingIsEnding()):
            self.gestureData[i,j,0] = boneBase.x
            self.gestureData[i,j,1] = boneBase.y
            self.gestureData[i,j,2] = boneBase.z
            self.gestureData[i,j,3] = boneTip.x
            self.gestureData[i,j,4] = boneTip.y
            self.gestureData[i,j,5] = boneTip.z
        self.adjustWindow(boneBase.x, boneBase.y) 
    
    def saveGesture(self):
        fileName = '/Users/will/Downloads/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/userData/gesture'+str(self.numberOfGesturesSaved)+'.dat'
        print(fileName)
        f = open(fileName, 'w')
        np.save(f, self.gestureData)
        f.close()
        
        # Save number of gestures saved
        self.numberOfGesturesSaved = self.numberOfGesturesSaved + 1
        fileName = '/Users/will/Downloads/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/userData/numberOfGestures.dat'
        f = open(fileName, 'w')
        f.write(str(self.numberOfGesturesSaved))
        f.close()
    
    def RecordingIsEnding(self):
        return (self.previousNumberOfHands==2) & (self.currentNumberOfHands==1)
                    
    def drawPlot(self):
        # Render plot
        plt.draw()
        # Set timeout 
        plt.pause(0.00001)

    def adjustWindow(self, x, y):
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

    deliverable = Deliverable()
    deliverable.runForever()
    
main()
