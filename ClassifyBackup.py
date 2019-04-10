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
    
def CenterData(X):
    allXCoordinates = X[:,:,0,:]
    meanValue = allXCoordinates.mean()
    X[:,:,0,:] = allXCoordinates - meanValue    
    allYCoordinates = X[:,0,:,:]
    meanValue = allYCoordinates.mean()
    X[:,0,:,:] = allYCoordinates - meanValue    
    allZCoordinates = X[0,:,:,:]
    meanValue = allZCoordinates.mean()
    X[0,:,:,:] = allZCoordinates - meanValue
    return X
    
def ReshapeData(set1,set2):
    X = np.zeros((2000,5*4*6),dtype='f')
    y = np.zeros(2000,dtype='f')
    for i in range(0,1000):
        n = 0
        for j in range(0,5):
            for k in range(0,4):
                for m in range(0,6):
                    y[i] = 8
                    X[i,n] = set1[j,k,m,i]
                    y[i+1000] = 9
                    X[i+1000,n] = set2[j,k,m,i]
                    n = n + 1
    return X,y

train8File = 'userData/train6.dat'
train9File = 'userData/train7.dat'
test8File = 'userData/test6.dat'
test9File = 'userData/test7.dat'

# train8File = 'userData/train8.dat'
# train9File = 'userData/train9.dat'
# test8File = 'userData/test8.dat'
# test9File = 'userData/test9.dat'

train8 = pickle.load( open( train8File, "rb" ) )
train9 = pickle.load( open( train9File, "rb" ) )
test8 = pickle.load( open( test8File, "rb" ) )
test9 = pickle.load( open( test9File, "rb" ) )

# train8 = ReduceData(train8)
# train9 = ReduceData(train9)
# test8 = ReduceData(test8)
# test9 = ReduceData(test9)

# train8 = CenterData(train8)
# train9 = CenterData(train9)
# test8 = CenterData(test8)
# test9 = CenterData(test9)

trainX, trainy = ReshapeData(train8,train9)
testX, testy = ReshapeData(test8, test9)

clf = neighbors.KNeighborsClassifier(15)
clf.fit(trainX,trainy)

numCorrect = 0

for i in range(0, len(testX)):
    prediction = float(clf.predict( [testX[i]] ))
    print "Prediction: ", prediction
    print "Actual: ", testy[i]
    if i == 1000:
        print "---------------------------"
    if prediction == testy[i]:
        numCorrect = numCorrect + 1
print numCorrect
print str(float(numCorrect)/len(testX) * 100)+"%"
