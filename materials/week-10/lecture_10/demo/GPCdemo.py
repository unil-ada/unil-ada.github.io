
# Code from Chapter 18 of Machine Learning: An Algorithmic Perspective (2nd Edition)
# by Stephen Marsland (http://stephenmonika.net)

# You are free to use, change, or redistribute the code in any way you wish for
# non-commercial purposes, but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# Stephen Marsland, 2014

import numpy as np
import pylab as pl

iris = np.loadtxt('iris_proc.data',delimiter=',')
#iris[:,:4] = iris[:,:4]-iris[:,:4].mean(axis=0)
imax = np.concatenate((iris.max(axis=0)*np.ones((1,5)),iris.min(axis=0)*np.ones((1,5))),axis=0).max(axis=0)
#iris[:,:4] = iris[:,:4]/imax[:4]

target = -np.ones((np.shape(iris)[0],3));
indices = np.where(iris[:,4]==0) 
target[indices,0] = 1
indices = np.where(iris[:,4]==1)
target[indices,1] = 1
indices = np.where(iris[:,4]==2)
target[indices,2] = 1

# Randomly order the data
order = list(range(np.shape(iris)[0]))
np.random.shuffle(order)
iris = iris[order,:]
target = target[order,:]

train = iris[::2,0:4]
traint = target[::2]
test = iris[1::2,0:4]
testt = target[1::2]

#print train.max(axis=0), train.min(axis=0)

# Train the machines
output = np.zeros((np.shape(test)[0],3))

theta =np.zeros((3,1))
theta[0] = 1.0 #np.random.rand()*3
theta[1] = 0.7 #np.random.rand()*3
theta[2] = 0.

import gpc
import scipy.optimize as so

args = (train[:,:2],traint[:,0:1])   # column vector: 1-D targets broadcast wrongly
newTheta0 = so.fmin_cg(gpc.logPosterior, theta, fprime=gpc.gradLogPosterior, args=[args], gtol=1e-4,maxiter=20,disp=1)
pred = np.squeeze(np.array([gpc.predict(np.reshape(i,(1,2)),train[:,:2],traint[:,0:1],newTheta0) for i in test[:,:2]]))
output[:,0] = np.where(pred[:,0]<0,-1,1)
print(np.sum(np.abs(output-testt)))

args = (train[:,:2],traint[:,1:2])   # column vector: 1-D targets broadcast wrongly
newTheta1 = so.fmin_cg(gpc.logPosterior, theta, fprime=gpc.gradLogPosterior, args=[args], gtol=1e-4,maxiter=20,disp=1)
pred = np.squeeze(np.array([gpc.predict(np.reshape(i,(1,2)),train[:,:2],traint[:,1:2],newTheta1) for i in test[:,:2]]))
output[:,1] = np.where(pred[:,0]<0,-1,1)
print(np.sum(np.abs(output-testt)))

args = (train[:,:2],traint[:,2:3])   # column vector: 1-D targets broadcast wrongly
newTheta2 = so.fmin_cg(gpc.logPosterior, theta, fprime=gpc.gradLogPosterior, args=[args], gtol=1e-4,maxiter=20,disp=1)
pred = np.squeeze(np.array([gpc.predict(np.reshape(i,(1,2)),train[:,:2],traint[:,2:3],newTheta2) for i in test[:,:2]]))
output[:,2] = np.where(pred[:,0]<0,-1,1)
print(np.sum(np.abs(output-testt)))

#err1 = np.where((output==1.) & (test==-1.))[0]
#err2 = np.where((output==-1.) & (test==1.))[0]
#print "Class 1 errors ",len(err1)," from ",len(test[test==1])
#print "Class 2 errors ",len(err2)," from ",len(test[test==-1])
#print "Test accuracy ",1. -(float(len(err1)+len(err2)))/ (len(test[test==1]) + len(test[test==-1]))


# NOTE (2026): the remainder of the 2014 original chained an SVM demo onto this
# file (svm1/svm2 classifiers, a contour plot using an `svm0` that was never
# constructed and a `svm` module that is never imported).  That code could not
# run; the GP-classification part above is the part this lecture uses.  The SVM
# demo lives in its own script.

# Decide the class from the three one-vs-rest GP classifiers
bestclass = np.argmax(output, axis=1)
err = np.where(bestclass != iris[1::2, 4])[0]
print("misclassified:", len(err), "of", np.shape(iris)[0] / 2.)

pl.figure()
pl.scatter(test[:, 0], test[:, 1], c=bestclass, cmap=pl.cm.Paired)
pl.xlabel('sepal length')
pl.ylabel('sepal width')
pl.title('GP classification of the iris test set')
pl.show()
