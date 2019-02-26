# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:41:11 2018

@author: yibi
"""
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
timestep = 2000
nums  =8
points = [[-50,0],[-35.36,35.36],[0,50],[35.36,35.36],[50,0],[35.36,-35.36],[0,-50],[-35.36,-35.36]]
import numpy as np
import pandas as pd
def read(array, path):
    for i in range(nums):
        a = np.loadtxt(path + '\\lktq.ss.ptvc.p{0}.a0'.format(str(i + 1)), skiprows=2,dtype=float)
        col = a[:, 2]
        # print(str(col))
        array.T[i] = col
def numOut(path1,path2):
    inputlines1 = pd.DataFrame(np.zeros(nums*timestep ).reshape(nums,timestep ))
    inputlines2 = pd.DataFrame(np.zeros(nums*timestep ).reshape(nums,timestep ))
    read(inputlines1,path1)
    read(inputlines2,path2)
#    print(inputlines2)
    subtract = np.abs(inputlines1 - inputlines2)
#    return subtract,inputlines1 ,inputlines2 
    return subtract.T.sum()**2
               
gougu = lambda x1,y1,x2,y2 :np.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

def straights(points,org):
    straightsr = []
    for point in points:
        straightsr.append(gougu(point[0],point[1],org[0],org[1]))
    return pd.Series(straightsr)
#    return straightsr
        
def beishu(stras):

    maxnum = max(stras)
    beis = []
    for star in stras:
        beis.append(star/maxnum)
    return pd.Series(beis)
def beishu_2(points,org):
    stras = straights(points,org)
    return beishu(1/(stras**2))

def numOut_1(path1,path2,stras):
    inputlines1 = pd.DataFrame(np.zeros(nums*timestep ).reshape(nums,timestep ))
    inputlines2 = pd.DataFrame(np.zeros(nums*timestep ).reshape(nums,timestep ))
    read(inputlines1,path1)
    read(inputlines2,path2)
#    print(inputlines2)
    subtract = (inputlines1 - inputlines2) ** 2
    subtract =  subtract.T.sum()*(stras)
    print(subtract)
    return 1/(subtract.sum())

def tocalsum():
    orig = pd.DataFrame(np.zeros(nums*timestep ).reshape(nums,timestep ))
    actu = pd.DataFrame(np.zeros(nums*timestep ).reshape(nums,timestep ))
    read(orig,r'D:\Contour_extraction\lktq\originmodel')
    read(actu,r'D:\Contour_extraction\lktq\actualtumor')
    subt = actu - orig
    zeroid = tozeroindex(subt)
    return pd.Series(zeroid)
 
def tozeroindex(dataNzero):
    index0 = []
    lies = dataNzero.shape[1]
    for i in range(dataNzero.shape[0]):
        index0.append(lies - tozero(dataNzero[i:i+1])+1)
    return index0
def tozero(onelie):
    onelie = onelie.values.tolist()
#    onelie = list(onelie.T[:])
#    print(onelie)
    for i in range(len(onelie[0])):
        if onelie[0][i] != 0.0:
            break
    return i
def tomaxchumix(array):
    maxnum = max(array)
    minnum = min(array)
    return maxnum/minnum
def numOut_2(path1,path2):
    inputlines1 = pd.DataFrame(np.zeros(nums*timestep ).reshape(nums,timestep ))
    inputlines2 = pd.DataFrame(np.zeros(nums*timestep ).reshape(nums,timestep ))
    read(inputlines1,path1)
    read(inputlines2,path2)
#    print(inputlines2)
    subtract = np.abs(inputlines1 - inputlines2)
    ti = tocalsum()
    ti = beishu(ti)
    subtract =  subtract.T.sum()/ti
#    print(subtract)
    return 1/(subtract.sum())

def drawline(subtract,indexs):
#    fig = plt.figure() 
#    axes = fig.add_subplot(111) 
    x = np.array(list(range(0,2000)))
    for i in range(indexs[0],indexs[1]+1):
        lines = subtract[i:i+1].values.tolist()[0]
        plt.plot(x,lines,label = 'wrie'+str(i+1),lw = 0.5)
#    plt.axis('equal')
    #plt.title('yibi')
    plt.rcParams['savefig.dpi'] = 300
    # ==========================================
    plt.legend()
    # ==========================================
    plt.show()
    
def drawthree():
    sub,a1,a2 = numOut(r'D:\Contour_extraction\lktq\actualtumor',r'D:\Contour_extraction\lktq\originmodel')
    print(sub.T.sum())
    print(a1.T.sum())
    drawline(sub,[0,7])
    drawline(a1,[0,7])
    drawline(a2,[0,7])
    
def numOut_3(path1,path2):
    inputlines1 = pd.DataFrame(np.zeros(nums*timestep ).reshape(nums,timestep ))
    inputlines2 = pd.DataFrame(np.zeros(nums*timestep ).reshape(nums,timestep ))
    read(inputlines1,path1)
    read(inputlines2,path2)
    inputlines1 = inputlines1.iloc[:,1000:]
    inputlines2 = inputlines2.iloc[:,1000:]
    sub = np.abs(inputlines2- inputlines1)
    return sub.T.sum()

def origin(path):
    inputlines1 = pd.DataFrame(np.zeros(nums*timestep ).reshape(nums,timestep ))
    read(inputlines1,path)
    inputlines1 = inputlines1.iloc[:,1000:]
    sub = (inputlines1 - 0)**2
    return sub.T.sum()

def towriepower(point):
    r = numOut(r'D:\Contour_extraction\lktq\actualtumor',r'D:\Contour_extraction\lktq\originmodel')
    stras = beishu_2(points,point)
    a1 =  max(r)/min(r)
    a2 = max(r/stras)/min(r/stras)
    return a1,a2