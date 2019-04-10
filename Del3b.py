# -*- coding: utf-8 -*-
import numpy as np
import globalVariables as gv
import matplotlib.pyplot as plt

class Reader:

    def __init__(self):
        # Instantiate plot object
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(-400,400)
        self.ax.set_ylim(-400,400)
        self.gestureData = np.zeros((5,4,6),dtype='f')
        
        # Initialize bones object
        self.bones = {}
        
        # Set default coordinates to origin
        for i in range(0,5):
            for j in range(0,4):
                self.bones[i,j], = plt.plot([0,0] , [0,0])
        
        # Set limits for plot window
        plt.xlim(gv.xMax, gv.xMin)
        plt.ylim(gv.yMax, gv.yMin)
        
        self.numberOfGesturesSaved = 0
        # self.numberOfGestures = 0    
        # fileName = '/Users/will/Downloads/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/userData/numberOfGestures.dat'
        # f = open(fileName, 'r')
        # self.numberOfGestures = np.load(f)
        # f.close()
        
        self.gestureData = np.zeros((5,4,6),dtype='f')            
            
    def runForever(self):
        while True:
            self.printGestures()
            
    def printGestures(self):
        for i in range(0, len(self.gestureData)):
            self.printGesture(i)
        
    def printGesture(self, i):
        fileName = '/Users/will/Downloads/LeapDeveloperKit_2.3.1+31549_mac/LeapSDK/lib/userData/gesture'+str(i)+'.dat'
        # print fileName
        f = open(fileName, 'r')
        self.gestureData = np.load(f)
        f.close()
        self.drawPlot()
        for i in range(0,5):
            for j in range(0,4):
                print(self.gestureData[i])
                xBase = self.gestureData[i,j,0]
                yBase = self.gestureData[i,j,1]
                zBase = self.gestureData[i,j,2]
                xTip = self.gestureData[i,j,3]
                yTip = self.gestureData[i,j,4]
                zTip = self.gestureData[i,j,5]
                self.bones[i,j].set_xdata([ xBase , xTip ])
                self.bones[i,j].set_ydata([ zBase , zTip ])
                self.bones[i,j].set_color('b')  
                                     
    def printNumberOfGesturesSaved(self):
        print(self.numberOfGestures)        

    def drawPlot(self):
        # Render plot
        # plt.draw()
        # Set timeout 
        plt.pause(0.5)

def main():
    reader = Reader()
    reader.runForever()
    # reader.printNumberOfGesturesSaved()

main()
