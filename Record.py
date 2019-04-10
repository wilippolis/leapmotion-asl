# -*- coding: utf-8 -*-
import globalVariables as gv
import matplotlib.pyplot as plt
import numpy as np
import pickle
import Leap
import sys

class Deliverable:
    
    def __init__(self):
        # Instantiate plot object
        self.previousNumberOfHands = 0
        self.currentNumberOfHands = 0
        self.numberOfGestures = 1000
        self.gestureData = np.zeros((5,4,6,self.numberOfGestures),dtype='f')
        self.gestureIndex = 0
            
        # Connect to Leap controller
        self.controller = Leap.Controller()
        
    def runForever(self):
        # Initiate infinite loop
        while True:
            self.runOnce(self.controller.frame())
            
    def runOnce(self, frame):
        # If hands are present
        self.previousNumberOfHands = self.currentNumberOfHands
        self.currentNumberOfHands = len(frame.hands)
        if(self.currentNumberOfHands > 0):
            self.handleHand(frame.hands[0])
        
    def handleHand(self, hand):
        # Initialize ranged loop for fingers in hand
        for i in range(0,5):
            self.handleFinger(hand.fingers[i], i)
        if ( self.currentNumberOfHands == 2 ):
            # print 'gesture ' + str(self.gestureIndex) + ' stored.'
            self.gestureIndex = self.gestureIndex + 1
            print self.gestureIndex
            if ( self.gestureIndex == self.numberOfGestures ):
                print self.gestureData[:,:,:,0]
                print self.gestureData[:,:,:,99]
                self.saveGesture()
                sys.exit(0)
            
    def handleFinger(self, finger, i):        
        # Initialize ranged loop for bones in fingers
        for j in range(0,4):
            self.handleBone(finger.bone(j), i, j)
    
    def handleBone(self, bone, i, j):
        boneBase = bone.prev_joint
        boneTip = bone.next_joint
        if(self.currentNumberOfHands == 2):
            self.gestureData[i,j,0] = boneTip.x
            self.gestureData[i,j,1] = boneTip.y
            self.gestureData[i,j,2] = boneTip.z
            self.gestureData[i,j,3] = boneBase.x
            self.gestureData[i,j,4] = boneBase.y
            self.gestureData[i,j,5] = boneBase.z
    
    def saveGesture(self):
        fileName = '/Users/will/Downloads/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/userData/train1.dat'
        f = open(fileName, 'wb')
        pickle.dump( self.gestureData, f )
        f.close()

def main():

    deliverable = Deliverable()
    deliverable.runForever()
    
main()
