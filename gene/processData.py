import csv
import scipy.io;
from scipy import mat;
from numpy.linalg import svd
import numpy as np
import math as m
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import utility as util

def appendColumn(matrix,filePath):
        fileObj=csv.reader(open(filePath))
        i=0
        temp=[]
        for csv1 in fileObj:
                temp.append(csv1[0])

        matrix=np.column_stack((matrix,temp))
        return matrix

def populateMatrix(fileName,filePath):
        data=scipy.io.loadmat(fileName)
        A=data.get('A')
	print A.shape[0]
	'''temp=appendColumn(A,filePath)
        U,E2,V=svd(temp)
	drawPlot(V)'''
        #return V


def printMatrix(matrix):
        i=0
        while(i<matrix.shape[0]):
                print matrix[i][(matrix.shape[1]-3)]
                i+=1
        print matrix.shape[0],matrix.shape[1]

def drawPlot(matrix):
        fig = plt.figure()
        i=0
        while(i<matrix.shape[0]):
                print "Plotting:",i
                plt.plot([matrix[i][0]],[matrix[i][1]],'ro')
                i=i+1
        #plt.show()
	fig.savefig('/home/kirangilvaz/Documents/gene-data/trunk/geneticanalysis/gene/output/sample.png')
	util.sendMail('kirangilvaz@gmail.com','kirangilvaz@gmail.com','plot','plotdata','/home/kirangilvaz/Documents/gene-data/trunk/geneticanalysis/gene/output/sample.png')	

if __name__=='__main__':
        '''V=populateMatrix("chr1_2.mat")
        temp=appendColumn(V)
        drawPlot(temp)'''
        #printMatrix(temp)
	populateMatrix("/home/kirangilvaz/Documents/gene-data/trunk/geneticanalysis/gene/DATA/SNchr7B.mat",'/home/kirangilvaz/Documents/gene-data/trunk/geneticanalysis/gene/downloads/vector.csv')
	#drawPlot([])
