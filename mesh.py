# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 16:37:46 2018

@author: yibi
"""
import numpy as np
from copy import deepcopy
import re

# id = open('D:\CA\Simulation\simulation.id')
# lines = id.readlines()

'''
返回某个模型的肿瘤位置
'''
def totumor(idfile):
    with open(idfile+'\lktq.id') as f:
        lines = f.readlines()
    f.close()
    return findtumor(lines)




'''
返回方块的位置
'''


def squareloc(lines, index):
    vertex1 = lines[index + 94]
    vertex2 = lines[index + 95]
    xyz1 = str2nums(vertex1)
    xyz2 = str2nums(vertex2)
    return [xyz1, xyz2]


def str2nums(sql):
    sql = np.array(sql.split()[1:])
    nums = sql.astype(np.float64)
    xyz = nums * 1000
    return xyz


'''
计算得到 origin of object in millmeters,并且保留俩位有效数字
'''


def origin(lines):
    xyz = gridOrigin(lines)
    lxyz = []
    lxyz = rlxyz(lines)
    return np.around(lxyz - xyz, decimals=2)


'''
返回id文件的GridOriginInMeters 信息，并转换成mm为单位
'''


def gridOrigin(lines):
    girdO = lines[5]
    xyz = []
    xyz = girdO.split()
    #    for i in range(len(xyz)):
    #        xyz[i] = float(xyz[i])
    xyz = np.array(xyz)
    xyz = xyz.astype(np.float64)
    xyz = np.abs(xyz) * 1000
    return xyz


'''
返回id文件中的PaddingLowerX,Y,Z
'''


def rlxyz(lines):
    i = 0
    while 'PaddingLowerX' not in lines[i]:
        i += 1
    lx = lines[i]
    lxnum = str2num(lx)
    ly = lines[i + 1]
    lynum = str2num(ly)
    lz = lines[i + 2]
    lznum = str2num(lz)
    return [lxnum, lynum, lznum]


def str2num(string):
    num = string.split()[-1]
    return int(num)


'''
找到id文件中的方块的模型
'''


def fsquare(lines):
    string = 'begin_<simplifiedblockobject> Rectangular Block\n'
    nums = []
    if string in lines:
        start = 0
        for i in range(lines.count(string)):
            a = lines.index(string, start)
            nums.append(a)
            start = a + 1
    return nums


'''
根据方块的实际位置找到网格的位置
'''


def Sspatial2cell(scope, originloc, low):
    scopes = scope - originloc + low + 1
    return scopes.astype(np.int64)


'''
判断方块模型的是否是肿瘤
'''


def iftumor(lines, index):
    fillM = lines[index + 83]
    materials = str2num(fillM)
    return materials == 3


'''
找到肿瘤模型
'''


def findtumor(lines):
    tumors = []
    squares = fsquare(lines)
    for i in range(len(squares)):
        if iftumor(lines, squares[i]):
            tumors.append(squares[i])
    tumorloc = []
    for i in range(len(tumors)):
        tumorloc.append(squareloc(lines, tumors[i]))
    return tumorloc


'''
找到肿瘤的网格位置
'''


def xyzcell(lines):
    tumorloc = findtumor(lines)
    originloc = origin(lines)
    low = rlxyz(lines)
    gridlocs = []
    for i in range(len(tumorloc)):
        gridlocs.append(Sspatial2cell(tumorloc[i], originloc, low))
    return gridlocs


'''
找到需要改变的行列
'''


def bdgrid(xyloc, xoy):
    xyzlines = []
    if xoy:
        for i in range(len(xyloc)):
            xrange = xyloc[i]
            for i in range(xrange[1][1] - xrange[0][1]):
                xyzlines.append([[xrange[0][0], xrange[0][1] + i, xrange[0][2]],
                                 [xrange[1][0], xrange[0][1] + i + 1, xrange[1][2]]])
        return xyzlines
    else:
        for i in range(len(xyloc)):
            xrange = xyloc[i]
            for i in range(xrange[1][0] - xrange[0][0]):
                xyzlines.append([[xrange[0][0] + i, xrange[0][1], xrange[0][2]],
                                 [xrange[0][0] + i + 1, xrange[1][1], xrange[1][2]]])
        return xyzlines


'''
判断需要改变的行，列，纵
ind = True 为列
ind = False 为行

'''


def gridxy(lines, ind):
    xyzloc = xyzcell(lines)
    gridloc = bdgrid(xyzloc, ind)
    changex = {}
    xoy = 1 if ind else 0
    for i in range(len(gridloc)):
        if gridloc[i][0][xoy] not in changex:
            changex[gridloc[i][0][xoy]] = []
        if gridloc[i][1][xoy] not in changex:
            changex[gridloc[i][1][xoy]] = []
        changex[gridloc[i][0][xoy]].append((gridloc[i][0][not xoy], gridloc[i][1][not xoy]))
        changex[gridloc[i][1][xoy]].append((gridloc[i][0][not xoy], gridloc[i][1][not xoy]))
    newchange = deduplication(changex)
    return newchange

def deduplication(newMap):
    for keys in newMap:
        newMap[keys] = list(set(newMap[keys]))
    return newMap


def gridz(lines):
    gridloc = xyzcell(lines)
    changez = []
    for i in range(len(gridloc)):
        for j in range(gridloc[i][0][0], gridloc[i][1][0] + 1):
            for k in range(gridloc[i][0][1], gridloc[i][1][1] + 1):
                changez.append((j, k))
    return set(changez)


'''
插入排序
'''


def Insertion_Sort(arr):
    length = len(arr)
    for i in range(1, length):
        x = arr[i][0]
        x2 = arr[i][1]
        for j in range(i, -1, -1):
            # j为当前位置，试探j-1位置
            if x < arr[j - 1][0]:
                arr[j][0] = arr[j - 1][0]
                arr[j][1] = arr[j - 1][1]
            else:
                # 位置确定为j
                break
        arr[j][0] = x
        arr[j][1] = x2
    return arr


'''
鉴于map中的元素有可能有重复，方便去重所以元素是元组
因为要修改元素，所以元组要转换为列表
'''


def tuple2list(Mtuple):
    newMap = deepcopy(Mtuple)
    for keys in Mtuple:
        for i in range(len(Mtuple[keys])):
            newMap[keys][i] = list(Mtuple[keys][i])
    return newMap


'''
map中的元素从小到大排序
'''


def sortlist(newMap):
    sortedMap = deepcopy(newMap)
    for keys in newMap:
        if len(newMap[keys]) >= 1:
            sortedMap[keys] = Insertion_Sort(newMap[keys])
    return sortedMap


'''
如果x,y方向有重叠就应该修正map
'''
def correctMap(mapEx):
    mapExlist = tuple2list(mapEx)
#    print(mapExlist)
    sortlist(mapExlist)
    for keys in mapExlist:
        if len(mapExlist[keys]) > 1:
            i = 0
            while i+1 < len(mapExlist[keys]):
                if mapExlist[keys][i+1] == [0,0]:
                    break
                if mapExlist[keys][i][1] >= mapExlist[keys][i+1][0]:
                    if mapExlist[keys][i][1] <= mapExlist[keys][i+1][1]:
                        mapExlist[keys][i][1] = mapExlist[keys][i+1][1]
                    del mapExlist[keys][i+1]
                    mapExlist[keys].append([0,0])
                else:
                    i+=1

    return deleteZero(mapExlist)

'''
统计某一个数组某个值出现的个数
'''
def single_list(arr, target):
    return arr.count(target)


'''
删除每个数组末尾的[0,0]
'''
def deleteZero(Exmap):
    for keys in Exmap:
        times = single_list(Exmap[keys],[0,0])
        if times > 0 :
            for i in range(times):
                Exmap[keys].remove([0,0])
    return Exmap



'''
根据某些特征（正则表达式给出），找到对应的行的索引
'''


def toTumorlines(epattern1, epattern2, exmap, lines):
    gridmap = {}
    for key in exmap:
        #        key = key.astype(np.str)
        pattern = re.compile(epattern1 + str(key) + epattern2)
        i = 0
        while pattern.match(lines[i]) == None:
            i += 1
        gridmap[key] = i
    return gridmap


'''
给出这一行的一些特征值
'''


def torange(gridmap, num1, num2, lines):
    exrange = {}
    for key in gridmap:
        grids = lines[gridmap[key]]
        gridlist = np.array(grids.split())
        gridlist = gridlist.astype(np.int64)
        exrange[key] = [gridlist[num1], gridlist[num2]]
    return exrange


'''
给出要修改的map
'''


def rightgrid(exmap, exrange):
    correctgrid = {}
    for key in exmap:
        if len(exmap[key]) == 1:
            correctgrid[key] = [0 for i in range(3)]
            correctgrid[key][0] = [exrange[key][0], exmap[key][0][0], 2]
            correctgrid[key][1] = [exmap[key][0][0], exmap[key][0][1], 3]
            correctgrid[key][-1] = [exmap[key][0][1], exrange[key][1], 2]
        else:
            correctgrid[key] = [0 for i in range(len(exmap[key] * 2) + 1)]
            correctgrid[key][0] = [exrange[key][0], exmap[key][0][0], 2]
            correctgrid[key][-1] = [exmap[key][-1][1], exrange[key][1], 2]
            for i in range(len(exmap[key]) - 1):
                correctgrid[key][i * 2 + 1] = [exmap[key][i][0], exmap[key][i][1], 3]
                correctgrid[key][i * 2 + 2] = [exmap[key][i][1], exmap[key][i + 1][0], 2]
            correctgrid[key][-2] = [exmap[key][-1][0], exmap[key][-1][1], 3]
    return correctgrid


'''
修改x方向的表格

'''


def xGridCorrect(xgridpath, xmap):
    xfile = open(xgridpath)
    xlines = xfile.readlines()
    xfile.close()
    xgridmap = toTumorlines('^\d+\s', '\s1', xmap, xlines)
    xrange = torange(xgridmap, 0, 3, xlines)
    correctxgrid = rightgrid(xmap, xrange)
    sqlmap = listwrite(correctxgrid, True)
    for key in sqlmap:
        xlines[xgridmap[key]] = sqlmap[key][0]
        xlines[xgridmap[key] + 1] = sqlmap[key][1]
    return xlines,correctxgrid


def listwrite(gridmap, xoy):
    sqlmap = {}
    if xoy:
        for key in gridmap:
            sqlmap[key] = list2str(key, gridmap[key])
        return sqlmap

    else:
        for key in gridmap:
            sqlmap[key] = list2str2(key, gridmap[key])

        return sqlmap


def list2str(key, arrays):
    s1, s2 = '', ''
    for i in range(len(arrays)):
        s1 += (str(arrays[i][0]) + ' ' + str(key) + ' 1 ' + str(arrays[i][1]) + ' ' + str(arrays[i][2]) + '\n')
    for i in range(len(arrays)):
        s2 += (str(arrays[i][0]) + ' ' + str(key) + ' 2 ' + str(arrays[i][1]) + ' ' + str(arrays[i][2]) + '\n')
    return [s1, s2]


def list2str2(key, arrays):
    s1, s2 = '', ''
    for i in range(len(arrays)):
        s1 += (str(key) + ' ' + str(arrays[i][0]) + ' 1 ' + str(arrays[i][1]) + ' ' + str(arrays[i][2]) + '\n')
    for i in range(len(arrays)):
        s2 += (str(key) + ' ' + str(arrays[i][0]) + ' 2 ' + str(arrays[i][1]) + ' ' + str(arrays[i][2]) + '\n')
    return [s1, s2]


#    print(xrange)




#
#
#
'''
修改y方向的表格
'''


def yGridCorrect(ygridpath, ymap):
    yfile = open(ygridpath)
    ylines = yfile.readlines()
    yfile.close()
    ygridmap = toTumorlines('^', '\s\d+\s1', ymap, ylines)
    yrange = torange(ygridmap, 1, 3, ylines)
    correctygrid = rightgrid(ymap, yrange)
    sqlmap = listwrite(correctygrid, False)
    for key in sqlmap:
        ylines[ygridmap[key]] = sqlmap[key][0]
        ylines[ygridmap[key] + 1] = sqlmap[key][1]
    return ylines,correctygrid


'''
有id模型文件输出网格文件
'''
def togridfile(idlines,xoy,writefile):
    if xoy:
        xmap = gridxy(idlines,True)
        xgridmap = correctMap(xmap)
        return xGridCorrect(writefile,xgridmap)
    else:
        ymap = gridxy(idlines,False)
        ygridmap = correctMap(ymap)
        return yGridCorrect(writefile,ygridmap)



'''
修改z方向的表格
'''


def zGridCorrect(zgridpath, zindexs):
    zindexslist = list(zindexs)
    zfile = open(zgridpath)
    zlines = zfile.readlines()
    zfile.close()
    for i in range(len(zindexslist)):
        index = findzindex(zlines, zindexslist[i])
        s = zlines[index]
        zlines[index] = changesql(s)
    return zlines





def wirte(filename, gridlines):
    with open(filename, 'a') as f:
        f.writelines(gridlines)


def findzindex(zlist, tuples):
    pattern = re.compile(str(tuples[0]) + '\s' + str(tuples[1]) + '\s' + '1 ')
    i = 0
    while pattern.match(zlist[i]) == None:
        i += 1
    return i


def changesql(strings):
    stringlist = strings[:-2]
    return stringlist + '3\n'


def changegridnums(num1, num2, lines):
    strings = 'Array format: endpoints\n'
    if strings in lines:
        linesnum = lines.index(strings)
    origin = lines[linesnum + 2].split()[-1]
    lines[linesnum + 2] = str(num1) + ' ' + str(num2) + ' ' + origin
    print(lines[linesnum + 2])
'''

返回一个需要修改的x，y的行列数
'''
def changenums(Exmap):
    i = 0
    for key in Exmap:
        i += len(Exmap[key])-1
    return i*2
        
