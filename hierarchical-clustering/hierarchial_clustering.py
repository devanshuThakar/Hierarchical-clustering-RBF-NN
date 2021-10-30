from scipy.cluster.hierarchy import dendrogram
import numpy as np
import matplotlib.pyplot as plt

import math
import pandas as pd

class hierarchical_clustering:

    def __init__(self,labels,values):
        self.labels=labels
        self.values=values
        self.dist_matrix=[[0 for i in range(len(labels))] for j in range(len(labels))]
        self.id2name={}
        self.total_clusters=0
        for i in range(len(labels)):
            self.id2name[i]=self.labels[i]
        # This can be 2D numpy array (or 2D list) of size (n-1)X4
        # The columns contains(1st,2nd,3rd,4th) - id of cluster-1, id of cluster 2, 
        #  distance between two clusters, number of orginal observation in the newely formed cluster
        self.clusterID2memb={}
        self.linkage_matrix=[]
        
    def distance(self,x,y):
        dist=0
        for i in range(len(x)):
            dist+=(x[i]-y[i])**2
        return math.sqrt(dist)

    def cluster(self):
        labels=self.labels
        # Mapping of cluster IDs to its members
        clusterID2memb={}
        numOriginal = {} # Mapping of cluster_id to the number of orginal observations 
        for i in range(len(labels)):
            clusterID2memb[i],numOriginal[i]=[i],1

        dist_matrix = [[-1 for i in range(2*len(labels))] for j in range(2*len(labels))]
        for i in range(len(self.labels)):
            for j in range(i):
                dist_matrix[i][j]=dist_matrix[j][i]=self.distance(self.values[i],self.values[j])
        rc = [i for i in range(len(labels))] # rc = remaining clusters
        curr_clus_id=len(labels)-1
        for itr in range(len(labels)-1):
            pair = []
            min_dist = math.inf
            # Finding the minimum distance
            for i in range(len(rc)):
                for j in range(i):
                    if(dist_matrix[rc[i]][rc[j]]<min_dist):
                        min_dist = dist_matrix[rc[i]][rc[j]]
                        if(rc[i]<rc[j]):
                            pair = [rc[i],rc[j]]
                        else:
                            pair = [rc[j],rc[i]]
                            
            # Found a cluster - Add it to the linkage matrix
            curr_clus_id+=1
            clusterID2memb[curr_clus_id]=[pair[0],pair[1]]
            numOriginal[curr_clus_id]=numOriginal[pair[0]]+numOriginal[pair[1]]
            self.linkage_matrix.append([pair[0],pair[1],min_dist,numOriginal[curr_clus_id]])
            
            #Update the weight matrix - Find the distance of the newly formed cluster with the remaining clusters
            rc[rc.index(pair[0])]=curr_clus_id
            rc.remove(pair[1])
            for i in range(len(rc)):
                if(rc[i]!=curr_clus_id):
                    #Compute distance
                    x = clusterID2memb[curr_clus_id]
                    dist = max(dist_matrix[rc[i]][x[0]], dist_matrix[rc[i]][x[1]])
                    dist_matrix[curr_clus_id][rc[i]]=dist_matrix[rc[i]][curr_clus_id]=dist

        # Assigning the dictionary of cluster ID to members, total number of clusters
        self.clusterID2memb=clusterID2memb
        self.total_clusters=curr_clus_id+1 # curr_clus_id starts from 0 index

data = pd.read_csv("Exam_IITGn.csv")

names = data['Name'].tolist()
totals = list(map(float, data['Total'].tolist()))
totals = [[totals[i]] for i in range(len(totals))]

sample = hierarchical_clustering(names, totals)
sample.cluster()

plt.figure()
plt.title("Dendrograms")
dendrogram = dendrogram(sample.linkage_matrix)
plt.savefig('dendrogram.png')
plt.show()


''' The hirachical clustering algorithm ends here. 
    Some post processing is performed to print the list of students with grades for both the case '''
numGrades=4
groups = {}
clusters = [sample.total_clusters-1]
while(len(clusters)!=numGrades):
    temp = []
    for c in clusters:
        temp+=sample.clusterID2memb[c]
    clusters=temp.copy()

def findMembers(clusID):
    if(len(sample.clusterID2memb[clusID])==1):
        return sample.clusterID2memb[clusID]
    else:
        return findMembers(sample.clusterID2memb[clusID][0])+findMembers(sample.clusterID2memb[clusID][1])


members={}
for c in clusters:
    members[c]=findMembers(c)

Grades = {}
for x in members.keys():
    Grades[x]={'students':[], 'average':0}
    tot=0
    for student in members[x]:
        Grades[x]['students'].append((names[student][0],totals[student][0]))
        tot+=totals[student][0]
    Grades[x]['average']=tot/len(members[x])

z = list(zip(Grades.keys(),Grades.values()))
foo = [(x[0],x[1]['average']) for x in z]
foo.sort(key=lambda x:x[1], reverse=True)
Final_Grades = {}
list_of_grades=['A','B','C','D']

for i in range(len(foo)):
    Final_Grades[list_of_grades[i]]=Grades[foo[i][0]]['students']

for x in Final_Grades.keys():
    string = "Grade "+ x + " : "
    for y in Final_Grades[x]:
        string +=y[0]+" "
    print(string)
    
print("\nFinal Grades if atlead ONE F grade is to be given. \n")
Final_Grades['F']=[min(Final_Grades['D'],key=lambda x:x[1])]
Final_Grades['D'].remove(Final_Grades['F'][0])

for x in Final_Grades.keys():
    string = "Grade "+ x + " : "
    for y in Final_Grades[x]:
        string +=y[0]+" "
    print(string)