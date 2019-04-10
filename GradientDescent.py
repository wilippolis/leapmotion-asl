import numpy as np

def calcVectorizedCost(X, y, theta):
    n = len(X)
    arg1 = np.transpose(np.matmul(X,theta)-y)
    arg2 = np.matmul(X,theta)-y
    cost = ((1)/(2*n))*np.matmul(arg1,arg2)
    return cost

def gradientDescent(X, y, theta, alpha, iters):
    cost = []
    for n in range(iters):
        theta0 = theta[:,0]
        theta1 = theta[:,1]
        theta0 = theta0 - alpha*(1/n)*np.matmul(X,theta)-y
        theta1 = theta1 - alpha*(1/n)*np.matmul((np.matmul(X,theta0)-y),X)
        newCost = calcVectorizedCost(X,y,theta1)
        print newCost
        cost.append(newCost)
    return theta,cost

def main():
    cost = gradientDescent()    
    print cost
        

        