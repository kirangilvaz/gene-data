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

geneDataDirectory='C:/wamp/www/geneticanalysis/gene/DATA/'
outputDirectory='C:/Users/Kiran/Documents/NetBeansProjects/plot/web/'
downloadDirectory='C:/wamp/www/geneticanalysis/gene/downloads/'
def getColor(region):
	return {
        'CENTRAL_SOUTH_ASIA': 'b',
        'EUROPE': 'g',
	'OCEANIA':'r',
	'MIDDLE_EAST':'m',
	'AFRICA':'y',
	'EAST_ASIA':'DarkBlue',
	'AMERICA':'DarkOrange',
        }.get(region, 'k') 

def euclideanDistance(matrix):
	matData=scipy.io.loadmat(geneDataDirectory+'regions.mat')
        regions=matData.get('regions')
	rowSize=matrix.shape[0]-1
	x=matrix[rowSize][0]
	y=matrix[rowSize][1]
	z=matrix[rowSize][2]
	i=0
	euclideanDist={}
	while(i<matrix.shape[0]-2):
		x1=matrix[i][0]
		y1=matrix[i][1]
		z1=matrix[i][2]
		euclideanDist[i]=m.sqrt(m.pow((x1-x),2)+m.pow((y1-y),2)+m.pow((z1-z),2))
		i=i+1

	orderedDist={}
	orderedDist=OrderedDict(sorted(euclideanDist.items(), key=lambda t: t[1], reverse=False))	
	
	
	
	closestRegions=''
	i=0
	for k,v in orderedDist.items():
		closestRegions=closestRegions+'Region :'+str(regions[k][0][0])+', Distance :'+str(v)+'\n'
		if i==20:
			break
		i=i+1
	print 'User region '+str(regions[rowSize][0][0])
	return closestRegions

def generateOutput(matrix,fileName):
	fig2D=plt.figure()
	fig3D=plt.figure()
	ax2d = fig2D.add_subplot(111)
	ax3d = fig3D.add_subplot(111, projection='3d')
	matData=scipy.io.loadmat(geneDataDirectory+'regions.mat')
	regions=matData.get('regions')
	jsonData=[]
	i=0
	while i < matrix.shape[0]-1:
		jsonValue={}
		jsonValue['x']=str(matrix[i][0])
		jsonValue['y']=str(matrix[i][1])
		jsonValue['z']=str(matrix[i][2])
		jsonValue['region']=str(regions[i][0][0])
		ax2d.scatter([matrix[i][0]],[matrix[i][1]],color=getColor(jsonValue['region']))
		ax3d.scatter([matrix[i][0]],[matrix[i][1]],[matrix[i][2]],color=getColor(jsonValue['region']),marker='o')
		jsonData.append(jsonValue)
		i=i+1
		
	jsonValue={}
        jsonValue['x']=str(matrix[i][0])
        jsonValue['y']=str(matrix[i][1])
        jsonValue['z']=str(matrix[i][2])
        jsonValue['region']='INDIVIDUAL'
        ax2d.scatter([matrix[i][0]],[matrix[i][1]],color=getColor(jsonValue['region']))
        ax2d.annotate('Individual', xy=(matrix[i][0], matrix[i][1]),  xycoords='data', xytext=(0, 60), textcoords='offset points',arrowprops=dict(arrowstyle="->"))
	ax3d.scatter([matrix[i][0]],[matrix[i][1]],[matrix[i][2]],color=getColor(jsonValue['region']),marker='x')
	
	p1=plt.Rectangle((0, 0), 1, 1, fc="b")
	p2=plt.Rectangle((0, 0), 1, 1, fc="g")
	p3=plt.Rectangle((0, 0), 1, 1, fc="r")
	p4=plt.Rectangle((0, 0), 1, 1, fc="m")
	p5=plt.Rectangle((0, 0), 1, 1, fc="y")
	p6=plt.Rectangle((0, 0), 1, 1, fc="DarkBlue")
	p7=plt.Rectangle((0, 0), 1, 1, fc="DarkOrange")
	p8=plt.Rectangle((0, 0), 1, 1, fc="k")
	ax2d.legend([p1,p2,p3,p4,p5,p6,p7,p8], ["Central South Asia","Europe","Oceania","Middle East","Africa","East Asia","America","Individual"])
	ax3d.legend([p1,p2,p3,p4,p5,p6,p7,p8], ["Central South Asia","Europe","Oceania","Middle East","Africa","East Asia","America","Individual"])
	jsonData.append(jsonValue)
	
	f=open(outputDirectory+fileName+'.json','w')
	f.write(json.dumps(jsonData))
	f.close()
	
	fig2D.savefig(outputDirectory+fileName+'_2d.png')
	fig3D.savefig(outputDirectory+fileName+'_3d.png')

def processThis(fileName,userFileName):
        fileObj=csv.reader(open(downloadDirectory+userFileName))
	csvList=[]
	print "Processing user vector"
	for csvRow in fileObj:
		csvList.append(float(csvRow[0]))

	T=np.zeros(shape=(1033,1033))
	data=scipy.io.loadmat(geneDataDirectory+'SET1.mat')
        set1=data.get('set1')
	currentUserVectorRow=0	
	for k in range(22):
		print "Computing ",str(k+1),strftime("%Y-%m-%d %H:%M:%S", localtime())
		matData=scipy.io.loadmat(geneDataDirectory+'SNchr'+str(k+1)+'A.mat')
		A=matData.get('A')
		aCols=A.shape[1]
		aRows=A.shape[0]
		count=0
		for i in range(aCols):
			if i not in set1:
				A=scipy.delete(A,(i-count),1)
				count+=1

		A=np.column_stack((A,csvList[currentUserVectorRow:(currentUserVectorRow+aRows)]))
		currentUserVectorRow=currentUserVectorRow+aRows
		aCols=A.shape[1]
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

		At=np.transpose(A)
		AtdA=np.dot(At,A)
		T=T+AtdA

                matData=scipy.io.loadmat(geneDataDirectory+'SNchr'+str(k+1)+'B.mat')
                A=matData.get('A')
                aCols=A.shape[1]
                aRows=A.shape[0]
                count=0
                for i in range(aCols):
                        if i not in set1:
                                A=scipy.delete(A,(i-count),1)
                                count+=1

		A=np.column_stack((A,csvList[currentUserVectorRow:(currentUserVectorRow+aRows)]))
                currentUserVectorRow=currentUserVectorRow+aRows
		aCols=A.shape[1]
	
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
		
                At=np.transpose(A)
                AtdA=np.dot(At,A)
                T=T+AtdA
        	print "Completed ",str(k+1)," with ",T.shape[0],T.shape[1]," @ ",strftime("%Y-%m-%d %H:%M:%S", localtime())
	print "Begin SVD"
	U,E2,V=svd(T)
	print "SVD completed"
	return U



if __name__=='__main__':
	euclideanDistance([])
	#U=processThis()
	#drawPlot3D(U)
	generateJSON([],'')
	#print getColor('AMERICA')
