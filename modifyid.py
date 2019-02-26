# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:44:53 2018

@author: yibi
"""

import mesh as mh
from copy import deepcopy
#pointsblock = mh.totumor(r'D:\Contour_extraction\Group\Step64\25')
#points = blocktopoints(pointsblock)
'''
递归填充肿瘤点
'''
def fill(points):  
    xmap = toxmap(points)
    ymap = toymap(points)
    sortedxmap = sortedmap(xmap)
    sortedymap = sortedmap(ymap)
    xpoints = xmaptopoints(sortedxmap)
    ypoints = ymaptopoints(sortedymap)
    newpoints = topoints(xpoints,ypoints)
#    print(str(len(points))+' '+str(len(newpoints)))
    if len(points) == len(newpoints):
        return newpoints
    else: 
        return fill(newpoints)
'''
矩形区域变成点
'''    
def blocktopoints(points):
    newp = []
    for point in points:
        newp.append([point[0][0],point[0][1]])
    return newp
'''
以横坐标为值，纵坐标为键的map
'''
def toxmap(points):
    xmap = {}
    for point in points:
        if point[1] not in xmap:
            xmap[point[1]] = [point[0]]
        else:
            xmap[point[1]].append(point[0])
    return xmap

def toymap(points):
    ymap = {}
    for point in points:
        if point[0] not in ymap:
            ymap[point[0]] = [point[1]]
        else:
            ymap[point[0]].append(point[1])
    return ymap
'''
将map中的数组排序
'''    
def sortedmap(Exmap):
    newMap = deepcopy(Exmap)
    for key in Exmap:
        newMap[key] = insertSort(Exmap[key])
    for key in Exmap:
        newMap[key] = fillBlock(newMap[key])
    return newMap
'''
插入排序
'''
def insertSort(arr):
    length = len(arr)
    for i in range(1,length):
        x = arr[i]
        for j in range(i,-1,-1):
            # j为当前位置，试探j-1位置
            if x < arr[j-1]:
                arr[j] = arr[j-1]
            else:
                # 位置确定为j
                break
        arr[j] = x
    return arr


'''
补充点
'''
def fillBlock(array):
    newlist = []
    newlist.append(array[0])
    for i in range(len(array)-1):
        last = array[i]
        nextp = array[i+1]
        if nextp == last+2.0:
            newlist.append(last+1.0)
            newlist.append(nextp)
        else:      
            newlist.append(nextp)
    return newlist
            

'''
xmap转换为点
'''
def xmaptopoints(Exmap):
    points = []
    for key in Exmap:
        for xs in Exmap[key]:
            points.append([xs,key])
    return points
def ymaptopoints(Exmap):
    points = []
    for key in Exmap:
        for ys in Exmap[key]:
            points.append([key,ys])
    return points
def topoints(points1,points2):
    tupoints1 = listtotuple(points1)
    tupoints2 = listtotuple(points2)
    newpoints = []
    newpoints.extend(tupoints1)
    newpoints.extend(tupoints2)
    newpoints = list(set(newpoints))
    newpoint = tupletolist(newpoints)
    return newpoint

def listtotuple(points):
    newp = []
    for i in points:
        newp.append(tuple(i))
    return newp

def tupletolist(newpoints):
    pointlist = []
    for i in newpoints:
        pointlist.append(list(i))
    return pointlist

def centerpoints(points):
    cpoints = []
    for point in points:
        cpoints.append([point[0]+0.5,point[1]+0.5])
    return cpoints