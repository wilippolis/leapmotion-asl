# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import globalVariables as gv
from threading import Timer
import numpy as np
import random
import pprint
import pickle
import random
import Leap



####################### GLOBAL VARIABLES #######################


circle = plt.Circle((0, 0), radius=25, linewidth=0, fc='r')
database = pickle.load(open('userData/database.p','rb'))
testData = np.zeros((1,30),dtype='f')
ACTIVE_DIGIT = None
ACTIVE_USER = ''
PROGRAM_STATE = 0
bones = None
previousBones = None
clf = None
numIterations = 0
inputString = ''


####################### DATABASE METHODS #######################


def Login():
    global database
    global ACTIVE_USER
    userName = raw_input('Please enter your name: ')
    ACTIVE_USER = userName
    if userName in database:
        database[userName]['login_count'] += 1
    else:
        database[userName] = {'login_count':1}
    GenerateDigit()

def WriteToDatabase():
    global ACTIVE_DIGIT
    global ACTIVE_USER
    global database
    newAttempt = 'digit' + str(int(ACTIVE_DIGIT)) + 'attempted'
    if newAttempt in database[ACTIVE_USER]:
        database[ACTIVE_USER][newAttempt] += 1
    else:
        database[ACTIVE_USER][newAttempt] = 1

def SaveDatabase():
    global database
    pickle.dump(database,open('userData/database.p','wb'))
    

####################### UTILITY METHODS #######################


def adjustWindow(x, y):
    if ( x < gv.xMin ):
        gv.xMin = x
    if ( x > gv.xMax ):
        gv.xMax = x 
    if ( y < gv.yMin ):
        gv.yMin = y
    if ( y > gv.yMax ):
        gv.yMax = y

def toggleVisible(ax, ay, az, bx):
    global PROGRAM_STATE
    ay.set_visible(PROGRAM_STATE == 0)
    ax.set_visible(PROGRAM_STATE == 1)
    az.set_visible(PROGRAM_STATE == 2)
    bx.set_visible(PROGRAM_STATE == 3)
    
def initSubplots(fig):
    global circle
    global database
    global ACTIVE_USER
    global ACTIVE_DIGIT
    plt.ion()
    plt.xlim(gv.xMax, gv.xMin)
    plt.ylim(gv.yMax, gv.yMin)
    ay = fig.add_subplot(111)
    ay.axis('off')
    ay.set_visible(True)
    ay.imshow(plt.imread('hand2.png'), extent=[-150, 150, -150, 150])
    bx = fig.add_subplot(111, sharex=ay, sharey=ay)
    bx.axis('off')
    bx.set_visible(False)
    bx.imshow(plt.imread('success.png'), extent=[-150, 150, -150, 150])
    az = fig.add_subplot(111, sharex=bx, sharey=bx)
    az.set_visible(False)
    az.autoscale(False)
    az.set_xlim(-400,400)
    az.set_ylim(-400,400)
    az.axis('on')
    # az.imshow(plt.imread(str(int(ACTIVE_DIGIT)) + '.png'), extent=[-80, 80, -150, 150])
    az.text(0.55, 0.9, "Hand is hidden for privacy.",
        verticalalignment='bottom', horizontalalignment='right',
        transform=az.transAxes,bbox={'facecolor':'white','alpha':1.0, 'pad':10},
        color='black', fontsize=20)
    ax = fig.add_subplot(111, sharex=az, sharey=az)
    if (database[ACTIVE_USER]['login_count'] == 1):
        ax.text(0.98, 0.9, "Welcome! Please center your palm and sign your desired passcode.",
            verticalalignment='bottom', horizontalalignment='right',
            transform=az.transAxes,bbox={'facecolor':'white','alpha':1.0, 'pad':10},
            color='black', fontsize=14)
    if (database[ACTIVE_USER]['login_count'] > 1):
        ax.text(.98, .9, "Welcome back! Sign your passcode to continue.",
            verticalalignment='bottom', horizontalalignment='right',
            transform=az.transAxes,bbox={'facecolor':'white','alpha':1.0, 'pad':10},
            color='black', fontsize=20)
    ax.set_visible(False)
    ax.autoscale(False)
    ax.set_xlim(-400,400)
    ax.set_ylim(-400,400)
    ax.axis('on')
    plt.gca().add_patch(circle)
    return ax,ay,az,bx
    
def InitBones():
    bones = {}
    for i in range(0,5):
        for j in range(0,4):
            bones[i,j], = plt.plot([0,0] , [0,0])  
    return bones

def GenerateDigit():
    global ACTIVE_DIGIT
    ACTIVE_DIGIT = float(str(random.randint(0,9)) + '.0')
    
def HandIsCentered(hand):
    if(hand.palm_position.x > -15 and hand.palm_position.x < 15 and
       hand.palm_position.z > 10 and hand.palm_position.z < 40):
        return True
    else:
        return False
        

####################### DATA METHODS #######################

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
    

####################### STATE METHODS #######################


def ResetState(az):
    global numIterations
    global PROGRAM_STATE
    global ACTIVE_DIGIT
    SaveDatabase()
    numIterations += 1
    if numIterations > 0 and numIterations < 20:
        GenerateDigit()
    elif numIterations >= 20 and numIterations < 35:
        GenerateDigit()
    elif numIterations >= 36:
        ACTIVE_DIGIT = 2.0
    PROGRAM_STATE = 1

def CheckState(ax, ay, az, bx, frame):
    global PROGRAM_STATE
    if(len(frame.hands) > 0):
        if(HandIsCentered(frame.hands[0]) and not PROGRAM_STATE == 3):
            PROGRAM_STATE = 2
            toggleVisible(ax,ay,az,bx)
        elif(PROGRAM_STATE == 3):
            toggleVisible(ax,ay,az,bx)
            r = Timer(5.0, ResetState, [az])
            r.start()
        elif(not HandIsCentered(frame.hands[0])):
            PROGRAM_STATE = 1
            toggleVisible(ax,ay,az,bx)
    elif(len(frame.hands) == 0 and not PROGRAM_STATE == 3):
        PROGRAM_STATE = 0
        toggleVisible(ax,ay,az,bx)

def HandleState0(ax, ay, az, bx, frame):
    CheckState(ax,ay,az,bx,frame)
    
def HandleState1(ax, ay, az, bx, frame, clf):
    global bones
    global circle
    toggleVisible(ax,ay,az,bx)
    hand = frame.hands[0]
    for i in range(0,5):
        finger = hand.fingers[i]
        for j in range(0,4):
            bone = finger.bone(j)
            boneBase = bone.prev_joint
            boneTip = bone.next_joint
            xBase = boneBase.x
            zBase = boneBase.z
            xTip = boneTip.x
            zTip = boneTip.z
            rad = abs((hand.palm_position.x + hand.palm_position.z)/2)
            bones[i,j].set_color('b')
            bones[i,j].set_linewidth(4)
            bones[i,j].set_xdata([ xBase * 1.25 , xTip * 1.25])
            bones[i,j].set_ydata([ -1.25 * zBase , -1.25 * zTip ]) 
            if(HandIsCentered(hand)):
                circle.set_facecolor('#90EE90')
                CheckState(ax,ay,az,bx,frame)
            else:
                circle.set_facecolor('r')
                circle.set_radius(rad)
            adjustWindow(boneBase.x, boneBase.y)  
    CheckState(ax,ay,az,bx,frame)
            
def HandleState2(ax, ay, az, bx, frame):
    global bones
    global previousBones
    global testData
    global clf
    global ACTIVE_DIGIT
    global PROGRAM_STATE
    global inputString
    hand = frame.hands[0]
    k = 0
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
            testData = CenterData(testData)
            predictedClass = clf.predict(testData)
            # az.imshow(plt.imread(str(int(ACTIVE_DIGIT)) + '.png'), extent=[-80, 80, -150, 150])
            print int(predictedClass[0])
            if(len(inputString) < 6 and int(predictedClass[0]) == 5):
                if(len(inputString) == 0):
                    inputString += "1"
                elif(len(inputString) == 1):
                    inputString += "2"
                elif(len(inputString) == 2):
                    inputString += "3"
                elif(len(inputString) == 3):
                    inputString += "4"
                elif(len(inputString) == 4):
                    inputString += "5"
                elif(len(inputString) == 5):
                    inputString += "6"
                elif(len(inputString) == 6):
                    inputString += "7"
                az.text(0.55, 0.65, inputString,
                    verticalalignment='bottom', horizontalalignment='right',
                    transform=az.transAxes,bbox={'facecolor':'white','alpha':1.0, 'pad':10},
                    color='g', fontsize=25)
            elif(len(inputString) >= 6):
                print "SUCCESS!!"
                PROGRAM_STATE = 3
            adjustWindow(boneBase.x, boneBase.y)
    CheckState(ax,ay,az,bx,frame)

def HandleState3(ax,ay,az,bx,frame):
    CheckState(ax,ay,az,bx,frame)
    
    
####################### MAIN METHOD #######################
# Deliverable 9
# Three forms of scaffolding:
## 1. Challenge user to sign an increasing number of digits as performance increases
## 2. Challenge user to remember digits
## 3. Challenge user to sign digits faster as they improve

def main():
    global PROGRAM_STATE
    global bones
    global previousBones
    global clf
    clf = pickle.load( open('userData/classifier.p','rb'))
    plt.interactive(True)
    Login()
    WriteToDatabase()
    fig = plt.figure()
    ax,ay,az,bx = initSubplots(fig)
    bones = InitBones()
    previousBones = InitBones()
    controller = Leap.Controller()
    while True:
        frame = controller.frame()
        if(PROGRAM_STATE == 0):
            HandleState0(ax,ay,az,bx,frame)
        elif(PROGRAM_STATE == 1):
            HandleState1(ax,ay,az,bx,frame,clf)
        elif(PROGRAM_STATE == 2):
            HandleState2(ax,ay,az,bx,frame)
        elif(PROGRAM_STATE == 3):
            HandleState3(ax,ay,az,bx,frame)
        plt.draw()
        plt.pause(0.45)
        
main()