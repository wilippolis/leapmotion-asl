# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors, datasets

iris = datasets.load_iris()
clf = neighbors.KNeighborsClassifier(15)

trainX = iris.data[::2,1:3]
trainy = iris.target[::2]
testX = iris.data[1::2,1:3]
testy = iris.target[1::2]

clf.fit(trainX,trainy)

colors = np.zeros((3,3),dtype='f')
colors[0,:] = [1,0.5,0.5]
colors[1,:] = [0.5,1,0.5]
colors[2,:] = [0.5,0.5,1]

plt.figure()

numCorrect = 0

[numItems,numFeatures] = iris.data.shape
for i in range(0,numItems/2):
    itemClass = int(trainy[i])
    currColor = colors[itemClass,:]
    plt.scatter(trainX[i,0],trainX[i,1],facecolor=currColor,s=50,lw=2)

for i in range(0,numItems/2):
    prediction = int( clf.predict( [testX[i,:]] ) )
    edgeColor = colors[prediction,:]
    itemClass = int(testy[i])
    if prediction == itemClass:
        numCorrect = numCorrect + 1
    currColor = colors[itemClass,:]
    plt.scatter(testX[i,0],testX[i,1],facecolor=currColor,edgecolor=edgeColor,s=50,lw=2)
    
print str(float(numCorrect)/len(testX) * 100)+"%"
plt.show()
