# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 12:32:19 2018

@author: yibi
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

# inflections = np.array(
#     [[8, 0), [8, 8], [0, 8], [0, 32], [8, 32], [8, 40], [32, 40], [32, 32], [40, 32], [40, 8], [32, 8], [32, 0],
#      [8, 0]])
'''
分配网格
'''


def gridNum(outinflects, innerinflects,size):
    halfsize = size / 2
    outinflects = tutolist(outinflects)
    innerinflects = tutolist(innerinflects)
    bounds = Soutline(outinflects)
    #    print(bounds)
    startP = [bounds[0][0] + halfsize, bounds[0][1] + halfsize]
    gridsize = []
    gridsize = [int((bounds[1][0] - bounds[0][0]) / size), int((bounds[1][1] - bounds[0][1]) / size)]
    #    print(gridsize)
    grids = np.zeros((gridsize[0] * gridsize[1], 2))
    for i in range(gridsize[0]):
        for j in range(gridsize[1]):
            grids[i * gridsize[1] + j][0] = startP[0] + i * size
            grids[i * gridsize[1] + j][1] = startP[1] + j * size
            #    print(grids)
    calgrid = []
    if len(innerinflects) > 0:
        for i in range(len(grids)):
            if ifinpath(outinflects, grids[i]):
                    if not ifinpath(innerinflects,grids[i]):
                        calgrid.append(grids[i])
    else:
        for i in range(len(grids)):
             if ifinpath(outinflects, grids[i]):
                 calgrid.append(grids[i])
    return calgrid
'''
分配内层肿瘤轮廓
'''
def gridINNum(innerinflects,size):
    calgrid = []
    if len(innerinflects) != 0:
        halfsize = size / 2
        innerinflects = tutolist(innerinflects)
        bounds = Soutline(innerinflects)
#        print(bounds)
        startP = [bounds[0][0] + halfsize, bounds[0][1] + halfsize]
        gridsize = []
        gridsize = [int((bounds[1][0] - bounds[0][0]) / size), int((bounds[1][1] - bounds[0][1]) / size)]
#        print(gridsize)
        grids = np.zeros((gridsize[0] * gridsize[1], 2))
        for i in range(gridsize[0]):
            for j in range(gridsize[1]):
                grids[i * gridsize[1] + j][0] = startP[0] + i * size
                grids[i * gridsize[1] + j][1] = startP[1] + j * size
#                print(grids)     
        for i in range(len(grids)):
             if ifinpath(innerinflects, grids[i]):
                 calgrid.append(grids[i])
    return calgrid
    

'''
tuple转换为list
'''
def tutolist(tuplelist):
    elist = []
    for i in tuplelist:
        elist.append(list(i))
    return np.array(elist)


'''
找到轮廓的起点，在右下角

'''


def findstart(twoarray):
    x = twoarray[:, 0:1]
    indexs = np.where(x == np.min(x))
    xindex = indexs[0]
    #    print(xindex)
    startPs = []
    for i in range(len(xindex)):
        startPs.append(twoarray[xindex[i], 1])
    # print(startPs)
    startPoint = [np.min(x), np.min(startPs)]
    return startPoint


def drawpath(twoarray):
    path = Path(twoarray)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    patch = patches.PathPatch(path, facecolor='orange')
    ax.add_patch(patch)
    plt.axis('scaled')
    plt.axis('equal') 
    plt.show()


'''
判断一个点是否在一个轮廓内（不包含在边上的点）
'''


def ifinpath(twoarray, point):
    return Path(twoarray).contains_point(point)


'''
找到肿瘤的方块范围

'''


def Soutline(inflections):
    minx = min(inflections[:, 0:1])
    maxx = max(inflections[:, 0:1])
    miny = min(inflections[:, 1:2])
    maxy = max(inflections[:, 1:2])
    return [minx, miny], [maxx, maxy]


'''
判断一个点是否在一个方框区域内
'''


def ifinS(inflections, point):
    square = Soutline(inflections)
    if point[0] > square[0][0] and point[0] < square[1][0] and point[1] > square[0][1] and point[1] < square[1][1]:
        return True
    else:
        return False



'''
找到肿瘤轮廓
'''

def findcoutour(points):
    four_sides = tofour_sides(points)
    mapsides = countside(four_sides)
    outersides , innersides = oiside(mapsides)
    sortedsides = sortsides(outersides)
    pointdarray = sidestopoints(sortedsides)
    return pointdarray

'''
返回一个方块肿瘤的四条边
'''
def tofour_sides(arrays):
    sides = []
    for i in range(len(arrays)):
        sides.extend(singlesides(arrays[i]))
    return sides
    
def singlesides(points):
    side = []
    side.append(((points[0][0],points[0][1]),(points[0][0],points[1][1])))
    side.append(((points[0][0],points[1][1]),(points[1][0],points[1][1])))
    side.append(((points[1][0],points[0][1]),(points[1][0],points[1][1])))
    side.append(((points[0][0],points[0][1]),(points[1][0],points[0][1])))
    return side
'''
统计每条边出现的次数
'''
def countside(arrays):
    sidecounts = {}
    for i in arrays:
        sidecounts[i] = sidecounts.get(i,0) +1
    return sidecounts

'''
返回外层的边,以及内层的边
'''

def oiside(sidecount):
    outersides = []
    innersides = []
    for key in sidecount:
        if sidecount[key] == 1:
            outersides.append(key)
        elif sidecount[key] >= 1:
            innersides.append(key)
    return outersides,innersides

'''
按照顺序排各个边
'''
            
def sortsides_2(sides):
    sortedside = []
    sortedside.append(sides.pop(0))
    while sides != []:
        j = tonext(sortedside[-1],sides)
#        print(j)
        if isreverse(sortedside[-1],sides[j]):
            sides[j] = reverse(sides[j])
        sortedside.append(sides.pop(j))
#        print(sortedside)
#        print(sides)
    return sortedside

'''
按照顺序排列各个边,并删除没有闭合的区域
'''
def sortsides(sides):
    sortedside = [[]]
    index = 0
    sortedside[index].append(sides.pop(0))
    while sides != []:  
        j = tonext(sortedside[index][-1],sides)
        if j != None:
            if isreverse(sortedside[index][-1],sides[j]):
                sides[j] = reverse(sides[j])
            sortedside[index].append(sides.pop(j))
        else:
            index+=1
            sortedside.append([])
            if sides != []:
                sortedside[index].append(sides.pop(0))
    maxlengthsort = sortedside[0]
    for sortedsidesing in sortedside:
        if len(maxlengthsort) <= len(sortedsidesing):
            maxlengthsort = sortedsidesing
    return  maxlengthsort
            
'''
判断是否需要颠倒
'''
def isreverse(side1,side2):
    if side1[1] == side2[0]:
        return False
    elif side1[1] == side2[1]:
        return True
'''
返回颠倒的边
'''
def reverse(sides):
    return sides[1],sides[0]

'''
返回下一条边
'''
def tonext(lastside,nextsides):
    lastpoint = lastside[1]
    for i in range(len(nextsides)):
        if lastpoint == nextsides[i][0] or lastpoint == nextsides[i][1]:
            return i

'''
cell转换为list
'''
def celltolist(celllist):
    pointlist = []
    for i in celllist:
        pointlist.append([list(i[0]),list(i[1])])
    return np.array(pointlist)
'''
排序好的边转换为点
'''
def sidestopoints(sidesarray):
    if len(sidesarray) != 0:
        points = celltolist(sidesarray)
        pathpoints = points[:,0]
        pathpoints = list(pathpoints)
        pathpoints.append(pathpoints[0])
        return pathpoints
    else:
        return []



#def toedgepoints(point, size):
#    edgepoints = []
#    edgepoints.append(((point[0]-size/2,point[1]-size/2),(point[0]+size/2,point[1]+size/2)))
#    return edgepoints

'''
返回边缘的边
'''

def toedgesides(point,size):
    side = []
    x = point[0]
    y = point[1]
    se = size/2
    side.append(((x-se,y-se),(x-se,y)))
    side.append(((x-se,y),(x-se,y+se)))
    side.append(((x-se,y+se),(x,y+se)))
    side.append(((x,y+se),(x+se,y+se)))
    side.append(((x+se,y),(x+se,y+se)))
    side.append(((x+se,y-se),(x+se,y)))
    side.append(((x,y-se),(x+se,y-se)))
    side.append(((x-se,y-se),(x,y-se)))
    return side


'''
按顺序排序各个边，升级版
如果有多个区域，返回多个封闭区域
'''
def sortside_2(sides):
    i = 0 
    sortedside = [[]]
    sortedside[0].append(sides.pop(0))
    while sides != []:
        j = tonext(sortedside[i][-1],sides)
        if j == None:
            i+=1
            sortedside.append([])
            sortedside[i].append(sides.pop(0))
            continue
        if isreverse(sortedside[i][-1],sides[j]):
            sides[j] = reverse(sides[j])
        sortedside[i].append(sides.pop(j))
        # print(i)
    return sortedside

'''
找到肿瘤的外层轮廓和内层轮廓
'''

def toioprofile(propoints,size):
    profileside = []
    profilepoints = propoints[:-1]
    for point in profilepoints:
        profileside.extend(toedgesides(point,size))
    mapsides = countside(profileside)
    outersides , innersides = oiside(mapsides)
    sortedsides = sortside_2(outersides)
    pointdarray = []
    for sortedside in sortedsides:
        pointdarray.append(sidestopoints(sortedside))
#    print(len(pointdarray))

    if len(pointdarray) == 1:
        outprofile,inprofile = pointdarray[0],[]
    elif len(pointdarray) ==2:
        outprofile,inprofile = toio(pointdarray)
    return outprofile,inprofile

def toio(pointlist):
    if len(pointlist[0]) > len(pointlist[1]):
        outprofile1 = pointlist[0]
        inprofile1 = pointlist[1]
    else:
        outprofile1 = pointlist[1]
        inprofile1 = pointlist[0]
    return  outprofile1,inprofile1 

'''
将区域分割成1mm的小块
'''
def toonemm(arrays):
    sides = tofour_sides(arrays)
    sortedside = sortsides(sides)
    points = sidestopoints(sortedside)
    midpoint = gridINNum(points,2)
    midblock = pointtoblock(midpoint)
    return midblock
'''
中心点转换为区域
'''
def pointtoblock(pointlist):
    blocklist =[] 
    for point in pointlist:
        blocklist.append(pointb(point))
    return blocklist


'''
点转换为肿瘤区域
'''
def pointb(opoint,size):
    return [[opoint[0] - size/2,opoint[1]-size/2],[opoint[0] + size/2,opoint[1] + size/2]]

'''
返回1mm的内外层边缘
'''     
def tocontour(pointsarray):
    midpoints = findcoutour(pointsarray)
    outerpoints,innerpoints = toioprofile(midpoints,2)
    outgrid = gridNum(outerpoints, midpoints,1)
    ingrid = gridNum(midpoints,innerpoints,1)
    return outgrid,ingrid

'''
中心点转换为边

'''

def centerPoint(points,size):
    arrays = []
    for i in points:
        arrays.append(pointb(i,size))
    return arrays
    
    
    
'''
返回内外轮廓的点
'''
def tofourpoints(inflections,size):
    pointlist = []
    for point in inflections:
        pointlist.extend(aroundp(point,size))
    pointlist = list(set(pointlist))
    point = tutolist(pointlist)
    return point
    
'''
返回内外轮廓的点（一个）
'''      
        
        
        
def aroundp(point,size):
    pointtu = []
    pointtu.append((point[0]-size/2,point[1]-size/2))
    pointtu.append((point[0]-size/2,point[1]+size/2))
    pointtu.append((point[0]+size/2,point[1]-size/2))
    pointtu.append((point[0]+size/2,point[1]+size/2))
    return pointtu
'''
根据点找到轮廓
'''

def findcoutour_2(pointslist,size):
    points= centerPoint(pointslist,size)
    four_sides = tofour_sides(points)
    mapsides = countside(four_sides)
    outersides , innersides = oiside(mapsides)
    sortedsides = sortside_2(outersides)
    pointdarray = []
    for sides in sortedsides:
        pointdarray.append(sidestopoints(sides))
    outprofile,inprofile = [],[]
    if len(pointdarray) == 1:
        outprofile,inprofile = pointdarray[0],[]
    elif len(pointdarray) ==2:
        outprofile,inprofile = toio(pointdarray)
    return outprofile,inprofile

        
'''
找到1mm边缘轮廓
'''
def refine(points):
    onepoint = []
    for i in range(len(points)-1):
        onepoint.append(list(points[i]))
        onepoint.extend(refineside(points[i],points[i+1]))
    onepoint.append(list(points[-1]))
    return onepoint


'''
细化一条边
'''
def refineside(point1,point2):
    points = []
    if point1[0] == point2[0]:
        for i in range(int(mixnum(point1[1],point2[1])),int(maxnum(point1[1],point2[1]))):
            points.append([point1[0],i])
        return points
        
    elif point1[1] == point2[1]:
        for i in range(int(mixnum(point1[0],point2[0])),int(maxnum(point1[0],point2[0]))):
            points.append([i,point1[1]])
        return points
        


def mixnum(num1,num2):
    return   num2 if  num1>num2 else num1

def maxnum(num1,num2):
    return   num2 if  num1<=num2 else num1
    
             
        
    
    


    

   
 
    
        
        
    
#id = open(r'D:\Contour_extraction\lktq\best\lktq.id')
#
#lines = id.readlines()
#
#findtumor(lines)  