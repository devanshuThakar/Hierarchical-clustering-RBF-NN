## Radial Basis function

This repository contains an implementaion of RBF to perform a pattern classification task. RBF network is implemented as generic class. RBF.py generates the training data and trains the RBF network. The given pattern classification problem was solved using 4 Gaussian function. 

To find the centers and standard deviation, a hierarchical clustering algorithm was performed. Standard deviations were computed within a memberes of particular cluster and its centroid. The weights can be computed as a pseudo inverse matrix by the least square technique.