#!/usr/bin/python 
from __future__ import division
import math
import random
import sys
import numpy
import matplotlib.pyplot as plt
def prop(sum):
	prop=(1/math.sqrt(2*math.pi*1))*math.exp(-(sum/2*(1**2)))
	return prop
def Dxi(a0,x,b0,y,c0,alpha0):
	Dx=a0*x+b0*y+c0+alpha0*19.8
	return Dx
##########take data##############
xlist=[]
ylist=[]
Dxdatalist=[]
with open('plane2.dat', 'r') as fd:
	for line in fd:
		data=line.split()
		x=float(data[0])
		y=float(data[1])
		Dxdata=float(data[2])+1.5
		xlist.append(x)
		ylist.append(y)
		Dxdatalist.append(Dxdata)
#######intialize########
Kloop=100000
a0=0
b0=0
c0=0
alpha0=0
alphalist=[]
for k in range(1,Kloop):
	Dxlist=[]
	for i in range(0,len(xlist)):
		x=xlist[i]
		y=ylist[i]
		Dx=float(Dxi(a0,x,b0,y,c0,alpha0))
		Dxlist.append(Dx)
	#########calculate the length between the two vector
	sum=0
	for i in range(0,len(xlist)):
		dot=(Dxlist[i]-Dxdatalist[i])**2
		sum=sum+dot
	#########calculate the likelyhood
	f0=prop(sum)
########propagete to the next point#########
	mean=[a0,b0,c0,alpha0]
	cov=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
	ap, bp, cp,alphap=numpy.random.multivariate_normal(mean,cov,1).T
	Dxnewlist=[]
	for i in range(0,len(xlist)):
		x=xlist[i]
		y=ylist[i]
		Dx=float(Dxi(ap,x,bp,y,cp,alphap))
		Dxnewlist.append(Dx)
	#########calculate the length between the two vector
	sumnew=0
	for i in range(0,len(xlist)):
		dot=(Dxnewlist[i]-Dxdatalist[i])**2
		sumnew=sumnew+dot
	#########calculate the likelyhood
	fp=prop(sumnew)
	#print 'prop is'+str(fp)+''
	pp=float(numpy.random.uniform(0,1,1))
	#print 'pp is'+str(pp)+''
	if pp <= fp/f0:
		a0=float(ap)
		b0=float(bp)
		c0=float(cp)
		alpha0=float(alphap)
		alphalist.append(float(alphap))
		#print 'replace'
	else:
		a0=a0
		b0=b0
		c0=c0
		alpha0=alpha0
		alphalist.append(float(alphap))
##############print########################
f = plt.figure()
plt.xlabel("alpha", fontsize=16)  
plt.ylabel("numbers", fontsize=16)
plt.xticks(fontsize=14)  
plt.yticks(fontsize=14)
plt.hist(alphalist, bins=100)
f.savefig("foo.pdf", bbox_inches='tight')