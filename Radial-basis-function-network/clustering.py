from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
from hierarchical_clustering import * 
import numpy as np
import math

def findMembers(sample, clusID): # A helper function to find members of a cluster
    if(len(sample.clusterID2memb[clusID])==1):
        return sample.clusterID2memb[clusID]
    else:
        return findMembers(sample,sample.clusterID2memb[clusID][0])+findMembers(sample, sample.clusterID2memb[clusID][1])

class clustering():
    
    def __init__(self, labels, values):
        self.labels=labels
        self.values=values
   
    ''' This function performs hierarchical clustering and returns centroids and standard deviations of clusters.'''
    def cluster(self):
        sample = hierarchical_clustering(self.labels, self.values)
        sample.cluster()

        numClusters=4
        groups = {}
        clusters = [sample.total_clusters-1]
        while(len(clusters)!=numClusters):
            temp = []
            for c in clusters:
                temp+=sample.clusterID2memb[c]
            clusters=temp.copy()

        cluster_members={}
        for c in clusters:
            cluster_members[c]=findMembers(sample, c)
        
        self.values=np.array(self.values)
        centroids = []
        # Computing centroids
        for cluster in cluster_members.values():
            center=np.array([0,0,0,0])
            for x in cluster:
                center = self.values[x]+center
            center = center/len(cluster)
            centroids.append(list(center))
        centroids=np.array(centroids)

        # Computing standard deviation
        std_dev=[]
        for cluster in cluster_members.values():
            i=len(std_dev)
            diff=0
            for x in cluster:
                diff+=np.linalg.norm(x-centroids[i])
            diff=math.sqrt(diff/len(cluster))
            std_dev.append(diff)
        std_dev=np.array(std_dev)

        return (centroids,std_dev)