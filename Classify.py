from sklearn import neighbors, datasets
import numpy as np
import pickle

def ReduceData(X):
    X = np.delete(X,1,1)
    X = np.delete(X,1,1)
    X = np.delete(X,0,2)
    X = np.delete(X,0,2)
    X = np.delete(X,0,2)
    return X;
    
def CenterData(testData):
    allXCoordinates = testData[:,:,0,:]
    meanValue = allXCoordinates.mean()
    testData[:,:,0,:] = allXCoordinates - meanValue    
    allYCoordinates = testData[:,0,:,:]
    meanValue = allYCoordinates.mean()
    testData[:,0,:,:] = allYCoordinates - meanValue    
    allZCoordinates = testData[0,:,:,:]
    meanValue = allZCoordinates.mean()
    testData[0,:,:,:] = allZCoordinates - meanValue
    return testData
    
def ReshapeData(set1, set2, set3, set4, set5, set6, set7, set8, set9, set10):
    X = np.zeros((10000,5*2*3),dtype='f')
    y = np.zeros(10000,dtype='f')
    for i in range(0,1000):
        n = 0
        for j in range(0,5):
            for k in range(0,2):
                for m in range(0,3):
                    y[i] = 0
                    y[i+1000] = 1
                    y[i+2000] = 2
                    y[i+3000] = 3
                    y[i+4000] = 4
                    y[i+5000] = 5
                    y[i+6000] = 6
                    y[i+7000] = 7
                    y[i+8000] = 8
                    y[i+9000] = 9
                    X[i,n] = set1[j,k,m,i]
                    X[i+1000,n] = set2[j,k,m,i]
                    X[i+2000,n] = set3[j,k,m,i]
                    X[i+3000,n] = set4[j,k,m,i]
                    X[i+4000,n] = set5[j,k,m,i]
                    X[i+5000,n] = set6[j,k,m,i]
                    X[i+6000,n] = set7[j,k,m,i]
                    X[i+7000,n] = set8[j,k,m,i]
                    X[i+8000,n] = set9[j,k,m,i]
                    X[i+9000,n] = set10[j,k,m,i]
                    n = n + 1
    return X,y
    
train0File = 'userData/gestureData/train0 (2).dat'  # WORKING
train1File = 'userData/gestureData/train1 (3).dat'  # WORKING
train2File = 'userData/gestureData/train2 (7).dat'  # NOT WORKING
train3File = 'userData/gestureData/train3 (3).dat'  # NOT WORKING
train4File = 'userData/gestureData/train4 (2).dat'  # NOT WORKING
train5File = 'userData/gestureData/train5 (2).dat'  # WORKING
train6File = 'userData/gestureData/train6 (2).dat'  # NOT WORKING
train7File = 'userData/gestureData/train7 (10).dat'  # NOT WORKING
train8File = 'userData/gestureData/train8 (7).dat'  # NOT WORKING
train9File = 'userData/gestureData/train9 (3).dat'  # NOT WORKING
test0File = 'userData/gestureData/test0 (2).dat'
test1File = 'userData/gestureData/test1 (3).dat'
test2File = 'userData/gestureData/test2 (7).dat'
test3File = 'userData/gestureData/test3 (3).dat'
test4File = 'userData/gestureData/test4 (2).dat'
test5File = 'userData/gestureData/test5 (2).dat'
test6File = 'userData/gestureData/test6 (2).dat'
test7File = 'userData/gestureData/test7 (10).dat'
test8File = 'userData/gestureData/test8 (7).dat'
test9File = 'userData/gestureData/test9 (3).dat'

train0 = pickle.load(open(train0File, "rb" ))
train1 = pickle.load(open(train1File, "rb" ))
train2 = pickle.load(open(train2File, "rb" ))
train3 = pickle.load(open(train3File, "rb" ))
train4 = pickle.load(open(train4File, "rb" ))
train5 = pickle.load(open(train5File, "rb" ))
train6 = pickle.load(open(train6File, "rb" ))
train7 = pickle.load(open(train7File, "rb" ))
train8 = pickle.load(open(train8File, "rb" ))
train9 = pickle.load(open(train9File, "rb" ))
test0 = pickle.load(open(test0File, "rb" ))
test1 = pickle.load(open(test1File, "rb" ))
test2 = pickle.load(open(test2File, "rb" ))
test3 = pickle.load(open(test3File, "rb" ))
test4 = pickle.load(open(test4File, "rb" ))
test5 = pickle.load(open(test5File, "rb" ))
test6 = pickle.load(open(test6File, "rb" ))
test7 = pickle.load(open(test7File, "rb" ))
test8 = pickle.load(open(test8File, "rb" ))
test9 = pickle.load(open(test9File, "rb" ))

train0 = ReduceData(train0)
train1 = ReduceData(train1)
train2 = ReduceData(train2)
train3 = ReduceData(train3)
train4 = ReduceData(train4)
train5 = ReduceData(train5)
train6 = ReduceData(train6)
train7 = ReduceData(train7)
train8 = ReduceData(train8)
train9 = ReduceData(train9)
test0 = ReduceData(test0)
test1 = ReduceData(test1)
test2 = ReduceData(test2)
test3 = ReduceData(test3)
test4 = ReduceData(test4)
test5 = ReduceData(test5)
test6 = ReduceData(test6)
test7 = ReduceData(test7)
test8 = ReduceData(test8)
test9 = ReduceData(test9)

train0 = CenterData(train0)
train1 = CenterData(train1)
train2 = CenterData(train2)
train3 = CenterData(train3)
train4 = CenterData(train4)
train5 = CenterData(train5)
train6 = CenterData(train6)
train7 = CenterData(train7)
train8 = CenterData(train8)
train9 = CenterData(train9)
test0 = CenterData(test0)
test1 = CenterData(test1)
test2 = CenterData(test2)
test3 = CenterData(test3)
test4 = CenterData(test4)
test5 = CenterData(test5)
test6 = CenterData(test6)
test7 = CenterData(test7)
test8 = CenterData(test8)
test9 = CenterData(test9)

trainX, trainy = ReshapeData(train0,train1,train2,train3,train4,train5,train6,train7,train8,train9)
testX, testy = ReshapeData(test0,test1,test2,test3,test4,test5,test6,test7,test8,test9)

clf = neighbors.KNeighborsClassifier(15)
clf.fit(trainX,trainy)

numCorrect = 0

for i in range(0, len(testX)):
    prediction = clf.predict([testX[i]])
    if prediction == testy[i]:
        numCorrect = numCorrect + 1
print "Accuracy: " + str(float(numCorrect)/len(testX) * 100) + "%"

pickle.dump(clf, open('userData/classifier.p','wb'))