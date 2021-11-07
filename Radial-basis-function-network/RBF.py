from itertools import permutations
from clustering import *
import numpy as np
import pandas as pd
import json

# All should be numpy arrays
class RBF:
    
    def __init__(self,centers,sigma,a):
        self.centers=centers # size 4 X (dim of input=4)
        self.sigma=sigma     # size 1 X 4
        self.a=a             # size 1X4
        self.W=None          # size 1X4-
        self.bW=None         # bias of W
        self.W_assigned=False
        self.HL=None # Hidden Gaussian layer
    
    def forward(self,X):
        HL=[]
        for i in range(np.shape(self.centers)[0]):
            HL.append(self.a[i]*np.exp( -(np.sum(np.square(X-self.centers[i,:]))/(2*self.sigma[i]**2)) ))
            
        self.HL=np.array(HL)
        if(self.W_assigned):
            y=np.dot(self.HL,self.W)
            y=y+self.bW
            # y=1/(1+np.exp(-y))
            y= 1 if y>=1 else 0
            # y= 1 if y>=0.5 else 0
            return y

''' This is the main code for the problem. Before running this make sure dataset.csv file is present.'''

# Generation of training data
A = ['10100001','01110000','10100101']
B = ['01011100','10100011']
C = ['01000111','11000011']
A_int,B_int,C_int= [],[],[]

for pattern in A:
    A_int.append(int(pattern,2))
for pattern in B:
    B_int.append(int(pattern,2))
for pattern in C:
    C_int.append(int(pattern,2))
    
unlock_vectors = []

for i,j in permutations(A_int,2):
    for k in B_int:
        for l in C_int:
            unlock_vectors.append([i,j,k,l])
print('Generated training data')

## Hirerachical clustering
unlock_vectors=np.array(unlock_vectors)
labels = [i for i in range(len(unlock_vectors))]
cluster = clustering(labels,unlock_vectors)
centers,std_devi=cluster.cluster()
print('Clustering of the train data done.')
print('centroids of clusters are  :\n',centers)
print('standard deviation of clusters are : ',std_devi)

# RBF started
print('\nRBF network started\n')
scale = np.array([1,1,1,1])    
network = RBF(centers,std_devi,scale)

phi = []
y = []

for x in unlock_vectors:
    network.forward(list(x))
    phi.append(network.HL)
    y.append(1)

w = np.linalg.inv(np.matmul(np.transpose(phi),phi))
w = np.matmul(w,np.transpose(phi))
w = np.matmul(w,y)
network.W = w
network.bW=0.229
network.W_assigned=True
print('Training of the network completed.')
print('The weight matrix is ', network.W)
print('The bias for weight matrix is ',network.bW)

print("\n###########################\n")
print("Testing the model on test dataset")
y_network=[]
df = pd.read_csv('dataset.csv')
test_vector=list(map(json.loads,df['input'].tolist()))
test_output=df['output'].tolist()

total_correct=0
for i in range(len(test_vector)):
    y_rbf=network.forward(test_vector[i])
    y_network.append(y_rbf)
    if(y_rbf==test_output[i]):
        total_correct+=1

accuracy=total_correct/len(test_output) * 100
print("Accuracy of model on dataset of size", str(len(test_output)), "is", str(accuracy)+"%.")