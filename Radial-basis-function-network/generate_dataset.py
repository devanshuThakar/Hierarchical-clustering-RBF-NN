from itertools import permutations
import pandas as pd
import random

''' Run this code to generate the test dataset for computing accuracy of model.'''
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
    
test_vector = []
test_output=[]

for i,j in permutations(A_int,2):
    for k in B_int:
        for l in C_int:
            test_vector.append([i,j,k,l])
            test_output.append(1)

for i,j in permutations(A_int,2):
    for k in B_int:
        for l in C_int:
            # adding all the wrong combinations
            test_vector.append([i,k,j,l]) # ABAC
            test_vector.append([i,k,l,j]) # ABCA
            test_vector.append([i,l,k,j]) # ACBA
            test_vector.append([i,l,j,k]) # ACAB
                    
            test_vector.append([k,i,j,l]) # BAAC
            test_vector.append([k,i,l,j]) # BACA
            test_vector.append([k,l,i,j]) # BCAA
            
            test_vector.append([l,k,i,j]) # CBAA
            test_vector.append([l,i,k,j]) # CABA
            test_vector.append([l,i,j,k]) # CAAB
            
            test_output=test_output+[0,0,0,0 ,0,0,0, 0,0,0]

for x in range(500-len(test_vector)):
    i,j,k,l=random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255)
    if(i in A_int):
        i=i+1
    if(j in A_int):
        j=j+1
    if(k in B_int):
        k+=1
    if(l in C_int):
        l+=1
    test_vector.append([i,j,k,l])
    test_output.append(0)

test = list(zip(test_vector,test_output))
random.shuffle(test)

[test_vec,test_out]=list(zip(*test))
test_vec=list(test_vec)
test_out=list(test_out)

dataset = {'input':test_vec,'output':test_out}
pd.DataFrame(dataset).to_csv('dataset.csv', index=False)