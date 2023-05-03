"""
this script proposes two solutions to a rice on a N*M chessboard problem : 
gathering rice starting from the top left corner going down and right to the bottom right corner

the first solution is exhaustive and checks all possible paths, and then computes the value of each path:
    the efficiency corresponds to the number of choices : O(C(N-1 M+N-1)) in time and O((N+M-2)*C(N-1 M+N-2)) in space (please don't)
    DO NOT try to use this for high values of N or M (it really doesn't work at all past a couple dozens)

the second solution rather looks at the maximum grains at each possible square, based off of the previous maximums:
    the efficiency is already better, only storing a matrix of N by M : O(N*M) in time and space
    is about as fast as creating the initial matrix with randint for each element (72 sec for n =  9530 , m =  7389)
"""


import random
import numpy as np
import time

limit = 10000
n = random.randint(1,limit)
m = random.randint(1,limit)
#the case where either is null is not checked, as the maximum rice is 0

A = np.zeros((n,m))

for i in range(n):
    for j in range(m):
        A[i][j] = random.randint(0,200)
print('n = ',n,', m = ',m)
#print(A)


#A =[[10,2,3],[2,10,0],[15,3,3]]

#first approach : get all possible paths, get the amount of rice on each path
#extremely inefficient, but easy access to the path
def solution(A):
    n,m = len(A),len(A[0])
    highestRice =0

    paths = [[[0,0]]]
    for k in range(n+m-2):
        paths = pathChoice(paths,n,m)
    for path in paths:
        riceSum = 0
        for [i,j] in path:
            riceSum+=A[i][j]
        if riceSum >highestRice:
            highestRice = riceSum
            #pathTaken = path
    #print(pathTaken)
    return(highestRice)

def pathChoice(paths,n,m):
    #for each choice there is to make, create the corresponding paths
    pathsToAdd = []
    for path in range(len(paths)):
        i,j = paths[path][-1]
        if i==n-1: #if on the bottom, no way other than to the right
            paths[path].append([i,j+1])
        elif j==m-1: #if on the right, no way other than to the bottom
            paths[path].append([i+1,j])
        else:
            pathsToAdd.append(paths[path].copy()+[[i+1,j]])
            paths[path].append([i,j+1])
    return (paths+pathsToAdd)

#second approach: get the maximum possible at each square
#to get the path, you need to get the maxiumm previous square starting from the end
def solution2(A):
    n,m = len(A),len(A[0])
    maxRice = np.zeros((n,m))
    maxRice[0][0] = A[0][0]
    for i in range(n-1): #computing first column (edge case)
        maxRice[i+1][0] = A[i+1][0] + maxRice[i][0]
    for j in range(m-1): #first row (edge case)
        maxRice[0][j+1] = A[0][j+1] + maxRice[0][j]
    for i in range(n-1): #filling the maximum based on previous squares
        for j in range(m-1):
            maxRice[i+1][j+1] = A[i+1][j+1] + max(maxRice[i][j+1], maxRice[i+1][j])
    #print(maxRice)
    return(maxRice[n-1][m-1])

#start1 = time.perf_counter()
#print(solution(A))
start2 = time.perf_counter()
print(solution2(A))
end = time.perf_counter()
print('time of the second solution : ',end-start2)
