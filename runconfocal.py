# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 16:25:03 2018

@author: yibi
"""

import confocal as cf
import wirtefile as wf
import os
import calResult as cr
import runCA as nc
import pandas as pd
import numpy as np
import mesh as mh
import fittxt as ft
time_steps = 2000
#
# pots = cf.Confocal()
# points = cf.toperson(pots,8,50)

points = [[-50,0],[-35.36,35.36],[0,50],[35.36,35.36],[50,0],[35.36,-35.36],[0,-50],[-35.36,-35.36]]

'''
写需要计算的个体
'''
def write(readfile,path,points,size):
    wf.wirtefdtd(r'D:\Contour_extraction\meshtest\fdtd.txt',path)
    tumor = open(readfile)
    tumorlines = tumor.readlines()
    tumor.close()
    idfile = open(path+'\lktq.id','a+')
    tumorlines[1121] = 'Fill_Material {:.0f}\n'.format(1 + 2)
    tumorlines[1132] = 'vertex1 {0} {1} -0.001\n'.format((points[0]-size/2)/1000,(points[1]-size/2)/1000)
    tumorlines[1133] = 'vertex2 {0} {1} 0\n'.format((points[0]+size/2)/1000,(points[1]+size/2)/1000) 
    idfile.writelines(tumorlines)
    idfile.close()
    xlines,xgridmap = wf.togrid(path+'\lktq.id',True,r'D:\Contour_extraction\meshtest\xgrid.txt')
    ylines,ygridmap = wf.togrid(path+'\lktq.id',False,r'D:\Contour_extraction\meshtest\ygrid.txt')
    wf.changenums(r'D:\Contour_extraction\meshtest\last.txt',xgridmap,ygridmap)
    wf.wirtemodel(r'D:\Contour_extraction\meshtest\last.txt',path+'\lktq.id')
    wf.writegrid(xlines,path+'\lktq.id')
    wf.writegrid(ylines,path+'\lktq.id')
    wf.writezgrid(path+'\lktq.id',r'D:\Contour_extraction\meshtest\zgrid.txt')
'''
运行该个体群
''' 
    
def run(points,path):
    
    for i in range(len(points)):
        if(not os.path.exists(path+'\\confocal\\step1'+'\\'+str(i+1))):
            os.makedirs(path+'\\confocal\\step1'+'\\'+str(i+1))
        write(r'D:\Contour_extraction\meshtest\singlemodel.txt',path+'\\confocal'+'\\step1'+'\\'+str(i+1),points[i],8)
    flag = False
    flag = cr.runall(path+'\\confocal', 1 , len(points)+1, 10, 1)
    if flag:     
        maxpos= tomaxfitness(path,1,points,'confocal')
    return maxpos
'''
计算适应度找到最好的适应度的个体
'''
def tomaxfitness(path,Step,points,kind):
    fitnessnum = pd.Series(np.zeros(len(points)))
    inputlines = pd.DataFrame(np.zeros(8*time_steps).reshape(8,time_steps))
    for i in range(len(points)):
        fitnessnum[i] = newread(inputlines,path,Step,i,kind)
    elist = list(fitnessnum)
    # print(elist)
    return elist.index(max(elist))+1
'''
读取每个个体的电流信息并计算适应度值
'''
def newread(lines,path,Step,num,kind):
    antenna = pd.DataFrame(np.zeros(8*time_steps).reshape(8,time_steps))
    nc.read(lines,path+'\\{2}\\Step{0}\\{1}'.format(str(Step),str(num+1),kind))
    nc.read(antenna,r'D:\Contour_extraction\lktq\actualtumor')
    subtract = np.abs(antenna - lines)  
#    print(subtract)
    return 1/((subtract.sum()**2).sum())
    
        
#    fitness = calfit()
#    mostfitness = maxindex(fitness)
#    return points[i]

def write_2(readfile,path,point1,point2):
    wf.wirtefdtd(r'D:\Contour_extraction\meshtest\fdtd.txt',path)
    tumor = open(readfile)
    tumorlines = tumor.readlines()
    tumor.close()
    idfile = open(path+'\lktq.id','a+')
    tumorlines[1121] = 'Fill_Material {:.0f}\n'.format(1 + 2)
    tumorlines[1132] = 'vertex1 {0} {1} -0.001\n'.format((point1[0])/1000,(point1[1])/1000)
    tumorlines[1133] = 'vertex2 {0} {1} 0\n'.format((point2[0])/1000,(point2[1])/1000) 
    idfile.writelines(tumorlines)
    idfile.close()
    xlines,xgridmap = wf.togrid(path+'\lktq.id',True,r'D:\Contour_extraction\meshtest\xgrid.txt')
    ylines,ygridmap = wf.togrid(path+'\lktq.id',False,r'D:\Contour_extraction\meshtest\ygrid.txt')
    wf.changenums(r'D:\Contour_extraction\meshtest\last.txt',xgridmap,ygridmap)
    wf.wirtemodel(r'D:\Contour_extraction\meshtest\last.txt',path+'\lktq.id')
    wf.writegrid(xlines,path+'\lktq.id')
    wf.writegrid(ylines,path+'\lktq.id')
    wf.writezgrid(path+'\lktq.id',r'D:\Contour_extraction\meshtest\zgrid.txt') 
    
'''
写模型，并运行然后计算得到最优的个体
'''
def run_2(points,path,Step,kind):
    for i in range(len(points)):
        newpath = path+'\\'+kind+'\\'+'Step'+str(Step)+'\\'+str(i+1)
        if(not os.path.exists(newpath)):
            os.makedirs(newpath)
        write_2(r'D:\Contour_extraction\meshtest\singlemodel.txt',newpath,points[i][0],points[i][1])
    flag = False
    flag = cr.runall(path+'\\'+kind, 1 , len(points)+1, 10, Step)
    if flag:     
        maxpos= tomaxfitness(path,Step,points,kind)
    return maxpos
  
def oscblock(path,Step,num1):
    if Step == 1:
        kind = 'confocal'
        oscpoints = tosidepoint(kind,path,Step,num1)
        num = run_2(oscpoints, path, Step, 'osc')
    else:
        kind = 'osc'
        oscpoints = tosidepoint(kind,path,Step-1,num1)
        num = run_2(oscpoints, path, Step, kind)
    return  num
    
    
    
    
# 
#def tosidepoint(num1):
#    blockpoints = mh.totumor(r'D:\Contour_extraction\\osc\Step1\\{}'.format(str(num1)))
#    point1 = [blockpoints[0][0][0],blockpoints[0][0][1]]
#    point2 = [blockpoints[0][1][0],blockpoints[0][1][1]]
#    oscpoint  =  cf.oscContour(point1,point2)
#    return oscpoint
'''
根据一个肿瘤模型，获取振荡的点
'''
def tosidepoint(kind,path,Step,nums):
    blockpoints = mh.totumor(path+'\\{0}\\Step{1}\\{2}'.format(kind,str(Step),str(nums)))
    point1 = [blockpoints[0][0][0],blockpoints[0][0][1]]
    point2 = [blockpoints[0][1][0],blockpoints[0][1][1]]
    oscpoint  =  cf.oscContour(point1,point2)
    return oscpoint


'''
检测上一次计算到哪一步
'''

def detect1(path):
    Step = 1
    while os.path.exists(path+'\\Step'+str(Step)):
        Step +=1
    return Step-2
'''
删除某个目录的全部文件
'''
def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

'''
判断某个目录下的所有文件是否算完
'''        
def isRunOut(path):
    flagall = True
#    flagsome = False
    files = os.listdir(path)
    for i in range(len(files)):
         pathall = path+'\\'+files[i]
         if os.path.isfile(pathall + '\\' + 'tsfdtd.txt'):
             show = open(pathall+ '\\' + 'tsfdtd.txt')
             line = show.readline()
             test = line.split()[-1:]
             if str(test) == "['finished']":
                 continue
             else:
                 flagall = False
                 break
    return flagall

'''
判断某个目录下是否没有文件算完
'''
def isRunOut_2(path):
#    flagall = True
    flagsome = True
    files = os.listdir(path)
    for i in range(len(files)):
         pathall = path+'\\'+files[i]
         if os.path.isfile(pathall + '\\' + 'tsfdtd.txt'):
             show = open(pathall+ '\\' + 'tsfdtd.txt')
             line = show.readline()
             test = line.split()[-1:]
             if str(test) != "['finished']":
                 continue
             else:
                 flagsome = False
                 break
    return flagsome

                 
            

