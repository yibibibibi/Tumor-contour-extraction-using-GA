# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 14:20:26 2018

@author: yibi
"""

import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle, Circle
import matplotlib.pyplot as plt
global time_steps,v 
points = [[-50,0],[-35.36,35.36],[0,50],[35.36,35.36],[50,0],[35.36,-35.36],[0,-50],[-35.36,-35.36]]

eps_0 = 8.854187817 * 1e-12
mur_0 = 4 * np.pi * 1e-7
eps_r = 9.8
v = 1 / np.sqrt(mur_0 * eps_0 * eps_r)
time_steps = 2000
antenna = pd.DataFrame(np.zeros(8 * time_steps).reshape(8,time_steps))
confocal = pd.DataFrame(np.zeros(8 * time_steps).reshape(8,time_steps))
flag = False
def read(array, path):
    for i in range(8):
        a = np.loadtxt(path + '\\lktq.ss.ptvc.p{0}.a1'.format(str(i + 1)), skiprows=2,dtype=float)
        col = a[:, 2]
        # print(str(col))
        array.T[i] = col
'''
共焦成像
'''
def Confocal():
    global time_steps,v
    print("读取数据")
    read(antenna, r'D:\Contour_extraction\lktq\actualtumor - 副本')
    if flag == False:
        print("共焦成像对比区域")
        read(confocal,r'D:\Contour_extraction\lktq\originmodel - 副本')
        a = np.loadtxt(r'D:\Contour_extraction\lktq\actualtumor - 副本\lktq.ss.ptvc.p1.a1', skiprows=2)
        time = a[:, 0]
        position = pd.Series(np.zeros(8))
        tmp = 0
        temp = 0
        focus = np.abs(antenna - confocal)
#        print(antenna.to_string)
#        print(confocal.to_string)
#        print(focus)
        for i in range(focus.index.size):
            for j in range(focus.columns.size):
                if focus.T[i][j] != 0:
                    tmp = j
                    if i == 0:
                        temp = int(np.ceil(j / 2))
                    break
            indexd = np.abs(tmp - temp)
#            print(indexd)
            position[i] = v * time[indexd]
        
    return position

'''
根据勾股定理计算点的距离
'''
def gougu(point1,point2):
    a = np.sqrt((point2[1]-point1[1])**2 + (point2[0]-point1[0])**2)
    return a
'''
公交区域可视化
'''

def draw(position,points,drawpoints= []):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cir1 = Circle(xy = (0.0, 0.0), radius=50, color = 'peachpuff')
    
    ax.add_patch(cir1)
    cir2 = Circle(xy = (20.0, 4.0), radius=5, color = 'r')
    ax.add_patch(cir2)
    positions = list(position)
    locs = toloc(positions)
    rect = Rectangle((locs[0][0],locs[0][1]), locs[1][0], locs[1][1],color = 'r',alpha=0.3)
    ax.add_patch(rect)
    rect1 = Rectangle((15,0), 10, 8,color = 'g',alpha=0.4)
    ax.add_patch(rect1)
    rect1 = Rectangle((15,4), 10, 10,color = 'g',alpha=0.4)
    ax.add_patch(rect1)
    rect2 = Rectangle((17,6), 6, 6,color = 'b',alpha=0.4)
    ax.add_patch(rect2)
    for i in range(len(points)):
        drawcl(ax,points[i],positions[i]*1000,2.5,0.7)
    for j in range(len(drawpoints)):
        plt.scatter(drawpoints[j][0],drawpoints[j][1])
    for k in points:
        cir = Circle(xy = (k[0],k[1]), radius=2, color = 'green')
        ax.add_patch(cir)
#    x, y = 0, 0
    plt.rcParams['savefig.dpi'] = 300
#    ax.plot(x, y,color = 'w')
    plt.axis('scaled')
    plt.axis('equal')   #changes limits of x or y axis so that equal increments of x and y have the same length
    plt.show()
def drawpoints(points):
    for i in range(len(points)):
        plt.scatter(points[i][0],points[i][1])
def drawcl(axes,point,r,rad= 2,lw=1):
    theta = np.arange(0, rad*np.pi, 0.1)
    x = point[0] + r * np.cos(theta)
    y = point[1] + r * np.sin(theta) 
    axes.plot(x, y,'black',linewidth=lw)
'''
给出成像范围
'''   
def toloc(position):
    xmin = np.round(position[0]*1000+(-50)-2)
    ymin = np.round(position[6]*1000+(-50)-2)
    xmax = np.round(52 - position[4]*1000)
    ymax = np.round(52 - position[2]*1000)
    return [[xmin,ymin],[xmax-xmin,ymax-ymin]]

'''
通过成像范围获得需要计算的个体
'''
def toperson(position,size,rad):
    locs = toloc(position)
    locs = np.array(locs)
    intloc = locs.astype(np.int)
    positions = topos(intloc,size,rad)
    return positions

'''
获得符合范围的所有个体的
'''
def topos(locations,size,rad):
    positions = []  
    for i in range(locations[1][0]-size+1):
        for j in range(locations[1][1]-size+1):
            x = locations[0][0] + i + size/2
            y = locations[0][1] + j + size/2
            if isincricle(x,y,size,rad):
                positions.append([x,y])
    return positions
'''
判断是否在圆形乳房范围内
'''

def isincricle(x,y,size,rad):
    blockpoints = toblock(x,y,size)
    lengths = []
    for i in range(len(blockpoints)):
        lengths.append(gougu(blockpoints[i],[0,0]))
    return max(lengths)<= rad
'''
返回一个点的四周点
'''
def toblock(x,y,size):
    blockpoints = []
    blockpoints.append([x-size/2,y-size/2])
    blockpoints.append([x-size/2,y+size/2])
    blockpoints.append([x+size/2,y+size/2])
    blockpoints.append([x+size/2,y-size/2])
    return blockpoints
'''
1mm的范围内调整轮廓
'''
def oscContour(point11,point22,size = 1):
   
    points11 = aroundpoints(point11,size)
    points22 = aroundpoints(point22,size)
    oscpoints = []
    for i in points11:
        for j in points22:
            oscpoints.append([i,j])
            
    return oscpoints

def aroundpoints(point,size):
    points = []
    points.append(point)
    points.append([point[0] - size, point[1] - size])
    points.append([point[0] - size, point[1] + size])
    points.append([point[0] + size, point[1] + size])
    points.append([point[0] + size, point[1] - size])
    points.append([point[0] , point[1] - size])
    points.append([point[0] , point[1] + size])
    points.append([point[0] + size, point[1]])
    points.append([point[0] - size, point[1]])
    return points



                



