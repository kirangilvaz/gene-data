import csv
import scipy.io;
from scipy import mat;
from numpy.linalg import svd
import numpy as np
import math as m
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from time import localtime, strftime
from numpy.linalg import svd
from collections import OrderedDict
import json

def getColor(region):
	return {
        'CENTRAL_SOUTH_ASIA': 'b',
        'EUROPE': 'g',
	'OCEANIA':'r',
	'MIDDLE_EAST':'m',
	'AFRICA':'y',
	'EAST_ASIA':'k',
	'AMERICA':'r',
        }.get(region, 'b') 

def drawPlot3D(matrix):
	print "Started plotting"
        print strftime("%Y-%m-%d %H:%M:%S", localtime())

	fig=plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	i=0
	while(i<matrix.shape[0]-1):
		ax.scatter([matrix[i][0]],[matrix[i][1]],[matrix[i][2]], c='r', marker='o')
		i=i+1
	ax.scatter([matrix[i][0]],[matrix[i][1]],[matrix[i][2]], c='b', marker='x')
	plt.show()
	print "Completed plotting"
        print strftime("%Y-%m-%d %H:%M:%S", localtime())


def drawPlot(matrix):
	print "Started plotting"
	print strftime("%Y-%m-%d %H:%M:%S", localtime())

        fig = plt.figure()
        i=0
        while(i<matrix.shape[0]):
                #print "Plotting:",i
                plt.plot([matrix[i][0]],[matrix[i][1]],'ro')
                i=i+1
	print "Completed plotting"
	print strftime("%Y-%m-%d %H:%M:%S", localtime())

        plt.show()

def demoPlot():

        fig = plt.figure()
	ax=fig.add_subplot(111,projection='3d')
	ax.scatter([1],[1],[1],c=getColor('AMERICA'),marker='o')
        #plt.plot([1],[1],getColor('EAST_ASIA'))

        plt.show()
def euclideanDistance(matrix):
	#matrix=mat([[9,8,9],[1,1,1],[0,0,0],[5,6,7],[8,8,8]])
	rowSize=matrix.shape[0]-1
	x=matrix[rowSize][0]
	y=matrix[rowSize][1]
	z=matrix[rowSize][2]
	
	i=0
	euclideanDist={}
	while(i<matrix.shape[0]-1):
		x1=matrix[i][0]
		y1=matrix[i][1]
		z1=matrix[i][2]
		euclideanDist[i]=m.sqrt(m.pow((x1-x),2)+m.pow((y1-y),2)+m.pow((z1-z),2))
		i=i+1

	orderedDist={}
	orderedDist=OrderedDict(sorted(euclideanDist.items(), key=lambda t: t[1], reverse=True))	
	
	matData=scipy.io.loadmat('/home/kirangilvaz/Documents/gene-data/trunk/geneticanalysis/gene/DATA/regions.mat')
        regions=matData.get('regions')
	
	closestRegions=[]
	i=0
	for k,v in orderedDist.items():
		closestRegions.append('Region :'+str(regions[k][0][0])+', Distance :'+str(v))
		if i==20:
			break
	return closestRegions

def generateOutput(matrix,fileName):
	filePath='/home/kirangilvaz/Documents/gene-data/trunk/geneticanalysis/gene/output/'
	fig2D=plt.figure()
	fig3D=plt.figure()
	ax2d = fig2D.add_subplot(111)
	ax3d = fig3D.add_subplot(111, projection='3d')
	matData=scipy.io.loadmat('/home/kirangilvaz/Documents/gene-data/trunk/geneticanalysis/gene/DATA/regions.mat')
	regions=matData.get('regions')
	jsonData=[]
	i=0
	while i < matrix.shape[0]-1:
		jsonValue={}
		jsonValue['x']=matrix[i][0]
		jsonValue['y']=matrix[i][1]
		jsonValue['z']=matrix[i][2]
		jsonValue['region']=regions[i][0][0]
		ax2d.scatter([jsonValue['x']],[jsonValue['y']],color=getColor(jsonValue['region']))
		ax3d.scatter([jsonValue['x']],[jsonValue['y']],[jsonValue['z']],color=getColor(jsonValue['region']),marker='o')
		jsonData.append(jsonValue)
		i=i+1
		
	jsonValue={}
        jsonValue['x']=matrix[i][0]
        jsonValue['y']=matrix[i][1]
        jsonValue['z']=matrix[i][2]
        jsonValue['region']='individual'
        ax2d.scatter([jsonValue['x']],[jsonValue['y']],color=getColor(jsonValue['region']))
        ax3d.scatter([jsonValue['x']],[jsonValue['y']],[jsonValue['z']],color=getColor(jsonValue['region']),marker='x')
        jsonData.append(jsonValue)
	
	f=open(filePath+fileName+'.json','w')
	f.write(json.dumps(jsonData))
	f.close()
	
	fig2D.savefig(filePath+fileName+'_2d.png')
	fig3D.savefig(filePath+fileName+'_3d.png')

def appendColumn(matrix,filePath):
        fileObj=csv.reader(open(filePath))
        i=0
        temp=[]
        for csv1 in fileObj:
                temp.append(csv1[0])

        #matrix=np.column_stack((matrix,temp))
	print matrix.shape[0],len(temp)
        return matrix


def processThis(fileName):
	print "Started at ",strftime("%Y-%m-%d %H:%M:%S", localtime())
	T=np.zeros(shape=(1032,1032))
	data=scipy.io.loadmat('/home/kirangilvaz/Documents/gene-data/trunk/geneticanalysis/gene/DATA/SET1.mat')
        set1=data.get('set1')
	
	#T=np.zeros(shape=(aCols,aCols))
	for k in range(22):
		print "Computing ",k
		matData=scipy.io.loadmat('/home/kirangilvaz/Documents/gene-data/trunk/geneticanalysis/gene/DATA/SNchr'+str(k+1)+'A.mat')
		A=matData.get('A')
		aCols=A.shape[1]
		aRows=A.shape[0]
		#print aCols
		count=0
		for i in range(aCols):
			if i not in set1:
				#print "deleting ",(i-count)
				A=scipy.delete(A,(i-count),1)
				count+=1

		aCols=A.shape[1]
		#A=appendColumn(A,'/home/kirangilvaz/Documents/gene-data/trunk/geneticanalysis/gene/downloads/kirangmailcom_vector.csv')
		
		print "Processing values"
		for j in range(aCols):
			colSum=0
			indexExcludeCount=0
			for i in range(aRows):
				if A[i][j] !=2:
					colSum+=A[i][j]
				else:
					indexExcludeCount+=1
			colMean=colSum/(A.shape[0]-indexExcludeCount)
	
			for i in range(aRows):
				if A[i][j] !=2:
					A[i][j]-=colMean

		print strftime("%Y-%m-%d %H:%M:%S", localtime())
		print "Matrix calculation"
		At=np.transpose(A)
		AtdA=np.dot(At,A)
		T=T+AtdA
		
	print "Completed A series with ",T.shape[0],T.shape[1]
	print strftime("%Y-%m-%d %H:%M:%S", localtime())


        for k in range(22):
                matData=scipy.io.loadmat('/home/kirangilvaz/Documents/gene-data/trunk/geneticanalysis/gene/DATA/SNchr'+str(k+1)+'B.mat')
                A=matData.get('A')
                aCols=A.shape[1]
                aRows=A.shape[0]
                #print aCols
                count=0
		print "Computing ",k
		print strftime("%Y-%m-%d %H:%M:%S", localtime())
                for i in range(aCols):
                        if i not in set1:
                                #print "deleting ",(i-count) 
                                A=scipy.delete(A,(i-count),1)
                                count+=1

                aCols=A.shape[1]
                #print set1.shape[1],aCols

                for j in range(aCols):
                        colSum=0
                        indexExcludeCount=0
                        for i in range(aRows):
                                if A[i][j] !=2:
                                        colSum+=A[i][j]
                                else:
                                        indexExcludeCount+=1
                        colMean=colSum/(A.shape[0]-indexExcludeCount)

                        for i in range(aRows):
                                if A[i][j] !=2:
                                        A[i][j]-=colMean
		
		print strftime("%Y-%m-%d %H:%M:%S", localtime())
                print "Matrix calculation"
                At=np.transpose(A)
                AtdA=np.dot(At,A)
                T=T+AtdA
        print "Completed B series",T.shape[0],T.shape[1]
        print strftime("%Y-%m-%d %H:%M:%S", localtime())
	print "begin SVD"
	
	U,E2,V=svd(T)
	return U



if __name__=='__main__':
	euclideanDistance([])
	#U=processThis()
	#drawPlot3D(U)
	generateJSON([],'')
	#print getColor('AMERICA')
