# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 20:04:47 2018

@author: yibi
"""

import numpy as np
import pandas as pd
import wirtefile as wf
import fcontour as fc
import random
import os
import mesh as mh
import fittxt as ft
import shutil

global time_steps,antenna,time,parameter,grouplength,prob_vaty,fitness_limit,bounds


time_steps = 2000   # 模型的时间步数
antenna = pd.DataFrame(np.zeros(8 * time_steps).reshape(8,time_steps)) # 天线接收的参数
time = pd.Series(np.zeros(time_steps))      
#        confocal = pd.DataFrame(np.zeros(8 * time_steps).reshape(8,time_steps))
#        cx, cy, x, y = 0., 0., 0., 0.
parameter = pd.DataFrame([[9.8, 0.4], [50.74, 4.82]])  # 设置模型的介电参数

# grouplength = 80  # 种群规模

prob_cross = 0.7 # 交叉概率
prob_vaty = 0.01  # 变异概率、
fitness_limit = 1e+20 # 最大限度
points = [[-50,0],[-35.36,35.36],[0,50],[35.36,35.36],[50,0],[35.36,-35.36],[0,-50],[-35.36,-35.36]]   # 天线的位置
#person = pd.DataFrame(np.zeros(grouplength * codelength).reshape(grouplength,codelength),dtype=int)
#best_person = pd.Series(np.zeros(codelength),dtype = int)
#best_fitness = 0.
# fitnessnum = pd.Series(np.zeros(grouplength))
#flag = False
#step = 1
person_soup = []

'''
返回路径中模型的肿瘤的内层轮廓和外层轮廓
size : 肿瘤块的大小(mm)
'''
def tobounds(path,size):
    points = mh.totumor(path)
#    print(len(points))
    pointdarray =fc.findcoutour(points)
    onedarray = fc.refine(pointdarray)
    newpoints = fc.tofourpoints(onedarray,size)
    outprofile,inprofile = fc.findcoutour_2(newpoints,size)
    return outprofile,inprofile,pointdarray

'''
通过内外层轮廓返回内外层的肿瘤
size : 肿瘤块的大小(mm)
'''
def tooitumor(outprofile,inprofile,size):
    loct = fc.gridNum(outprofile,inprofile ,size)
    return loct
'''
返回不需要计算的肿瘤
size : 肿瘤块的大小(mm)
'''
def origtumor(inprofile,size):
    inloc = fc.gridINNum(inprofile ,size)
    return inloc
'''
读取8个天线的电流
'''
def read(array, path):
    for i in range(8):
        a = np.loadtxt(path + '\\lktq.ss.ptvc.p{0}.a0'.format(str(i + 1)), skiprows=2,dtype=float)
        col = a[:, 2]
        # print(str(col))
        array.T[i] = col
'''
给person单行赋值
'''
def readp(person,path):
    a = np.loadtxt(path+'\person.txt',dtype=int)
    for i in range(50):
        single = a[i,:]
        person.T[i] = single

"""
'''
判断上一次是否中断
'''
def detect(dpath,step,flag,person,grouplength):
    print("正在检测以往数据\n")
    path = dpath+'\\Step{0}'.format(str(step))
    while (os.path.exists(path)):
        print("已经检测到第" + str(step) + "次迭代数据，正在导入.....")
        readp(person, path)
        for i in range(grouplength):
            temp = person.iloc[i]
            person_soup.append(temp)
        step += 1
        path = dpath+'\\Step{}'.format(str(step))
    if step != 1:
        step += -1
        flag = True
    return step,flag
"""

'''
读取初始天线数据
'''
def readantenna():
    antenna = pd.DataFrame(np.zeros(8 * time_steps).reshape(8,time_steps))
    read(antenna, 'D:\\Contour_extraction\\lktq\\actualtumor')
    return antenna

'''
生成单个person的码
'''
def toSingleperson(codel,ptumor):

    randnum = pd.Series(np.zeros(codel),dtype = int)
    for i in range(codel):
        randnum[i] = int(np.ceil(random.random() + ptumor)) - 1
    # while randnum.sum() == codel or randnum.sum() == 0:
    #     for i in range(codel):
    #         randnum[i] = int(np.ceil(random.random() + ptumor)) - 1
    return randnum

    
'''
生成初始种群
'''

def population(codelength,person,prob_tumor,grouplength):
    for i in range(grouplength):  
        person.T[i] = toSingleperson(codelength,prob_tumor)
        person_soup.append(person.T[i])
    return person
'''
修改种群
'''
def modifyper(person):
    person = person.values
    a = np.ones(person.shape[1],np.int)
    if not ismember(a,person):
        person[random.randint(0, person.shape[0]-1)] = a
    b = np.zeros(person.shape[1],np.int)
    if not ismember(b,person):
        person[random.randint(0, person.shape[0]-1)] = b
    return pd.DataFrame(person)
def tomax(lines):
    position = lines.argmax()
    tmp = lines[position]
    return position,tmp

def readinput(lines,antenna,num1,num2,path,point):
#    print(lines)
    read(lines,path+'\\Step{0}\\{1}'.format(str(num1), str(num2+1)))
#    print(lines)
    subtract = np.abs(antenna - lines)
#    print(subtract)
    stars = ft.straights(points,point)
    beis = ft.beishu(1/(stars**2))
    # print(beis)
    nsubtract = (subtract.T.sum())**2 / beis
    sumnum = nsubtract.sum()
    if sumnum  == 0.:
        sumnum = 1E-20
    return 1/sumnum

    
def tofitness(lines,antenna,step,path,fitnessnum,grouplength,point):
    for i in range(grouplength):
        fitnessnum[i] = readinput(lines,antenna,step,i,path,point)
      
'''
计算种群的适应度
'''
def fitness(step,path,person,fitnessnum,grouplength,antenna,point):
    inputlines = pd.DataFrame(np.zeros(8*time_steps).reshape(8,time_steps))
    tofitness(inputlines,antenna,step,path,fitnessnum,grouplength,point)
#    return fitnessnum
    maxpos,maxnum = tomax(fitnessnum)
    best_fitness = maxnum
    best_person = person.T[maxpos]
    print("该种群的最佳适应值为"+str(best_fitness)+",最佳个体为第"+str(maxpos+1)+"个")
    best = open(path+'\\best_fitness.txt','a+')
    best.seek(2)
    best.write(str(step) + " " + str(maxpos+1) + " " + str(best_fitness) + "\r\n" )
    best.close()
    flag = True
    if best_fitness >= fitness_limit:
        flag = False
        print("该种群的最佳个体为"+str(maxpos+1))
    else:
        step += 1
    return best_fitness,best_person,flag,fitnessnum,step

def tosum_mid(fitnessnum,grouplength):
#    tmp_person = pd.DataFrame(np.zeros(grouplength*codelength).reshape(grouplength,codelength),dtype= int)
    sum_mid = pd.Series(np.zeros(grouplength+1))
    for i in range(1,sum_mid.size):
        sum_mid[i] = sum_mid[i-1] + fitnessnum[i-1]
    return sum_mid
def tonewperson(pro,myperson,codelength,best_person,best_fitness,grouplength):
    newperson = np.zeros(grouplength*codelength,np.int64).reshape(grouplength,codelength)
    for i in range(grouplength):
        randnum = pro.max() * random.random()
        for j in range(grouplength):
            if (randnum > pro[j] and randnum < pro[j + 1]):
                newperson[j] =myperson[j]
                break

    if not ismember(best_person,newperson):
        num = np.ceil((best_fitness/pro[len(pro)-1])*grouplength)
        for i in range(int(num)):
            newperson[random.randint(0, grouplength-1)] = best_person.values

    return pd.DataFrame(newperson)

def ismember(single,dperson):
    for i in range(len(dperson.T)):
        if list(single) == list(dperson.T[i:i+1]):
            return True
    return False
'''
选择
'''
def Selection(person,fitnessnum,codelength,best_person,best_fitness,grouplength):
    print("选择") 
#    print(person.T.sum())
    nperson = person.values
    sum_mid = tosum_mid(fitnessnum,grouplength)
    mperson = tonewperson(sum_mid,nperson,codelength,best_person,best_fitness,grouplength)
    return pd.DataFrame(mperson)


def todivide(grouplength):
    tmp = list(range(grouplength))
    random.shuffle(tmp)
    return tmp

'''
交叉
'''

def Crossover(codelength,person,grouplength):
    print("交叉")
    person = person.values
    tmp_group_divide = todivide(grouplength)
    for i in range(0,grouplength,2):
        randnum = random.random()
        if(randnum < prob_cross):
            cross_pos = int(np.ceil((codelength - 1) * random.random()))
            tmp_person = person[tmp_group_divide[i]]
            for j in range(codelength):
                if j > cross_pos:
                    person[tmp_group_divide[i]][j] = person[tmp_group_divide[i + 1]][j]
                    person[tmp_group_divide[i + 1]][j] = tmp_person[j]
    return pd.DataFrame(person)


'''
变异
'''
def Mutation(codelength,person,grouplength):
    print("变异")
    person = person.values
    for i in range(grouplength):
        for j in range(codelength):
            randnum = random.random()
            if randnum < prob_vaty:
                person[i][j] = np.abs(person[i][j] - 1)
    return pd.DataFrame(person)
'''
获取person的map
'''

def getptimes(person):
    pshape = person.shape[0]
    personmap = {}
    for i in range(pshape):
        single = tuple(person.T[i].values)
        personmap[single] = personmap.get(single, 0) + 1
    return personmap
'''
获取修改之后的person
'''

def mtonewperson(personmap, bestperson, grouplength, prob_tumor, codelength,step):
    bestperson = tuple(bestperson.values)
    newperson = []
    for k in personmap:
        if k == bestperson:
            for i in range(personmap[k]):
                newperson.append(list(k))
        else:
            newperson.append(list(k))
    for i in range(grouplength - len(newperson)):
            newperson.append(modibest(bestperson))
    random.shuffle(newperson)
    newperson = pd.DataFrame(newperson)
    return newperson

'''
对最优染色体做变化
'''
def modibest(bestperson):
    bestperson = list(bestperson)
    indexs = toindex(bestperson)
    for nindex in indexs:
        pro_v = random.random()
        if pro_v < 0.6:
            bestperson[nindex] = np.abs(bestperson[nindex] - 1)
    return bestperson


def toindex(bestperson):
    lens = len(bestperson)
    indexs = set()
    for i in range(lens):
        if bestperson[i] == 1:
            indexs.add(i-1)
            indexs.add(i)
            indexs.add(i+1)
    indexs = list(indexs)
    if -1 in indexs:
        indexs.remove(-1)
    if lens in indexs:
        indexs.remove(lens)
    return indexs

'''
修改染色体群
'''
def Modify(best_person,person,grouplength,prob_tumor, codelength,step):
    if step%3 == 0:
        personmap = getptimes(person)
        nperson = mtonewperson(personmap, best_person, grouplength, prob_tumor, codelength,step)
    else:
        nperson =person
    return nperson

def addbest(best_person,person,grouplength):
    p = person.T
    if  not ismember(best_person,person):
        p[random.randint(0, grouplength-1)] = best_person
    return p.T
'''
写person到文件
'''
def wirteperson(path,person,codelength,grouplength):
    if(not os.path.exists(path)):
        os.makedirs(path)
    bw = open(path + '\person.txt','w')
    for i in range(grouplength):
        for j in range(codelength):
            bw.write(str(person.T[i][j]) + " ")
        bw.write('\r\n')
    bw.close()
'''
根据person文件写id文件
'''
def wirteid(path,loct,size,person,grouplength):
    for i in range(grouplength):
        filepath = path + '\\' + str(i+1)
        if (not os.path.exists(filepath)):
            os.makedirs(filepath)
            write(i,filepath,loct,size,person,grouplength)
'''
整合写person文件和写id文件的过程
'''         
def run(dpath,step,person,codelength,loct,size,grouplength):
#    path =r'D:\Contour_extraction\Group\Step{}'.format(str(step))
#    if(not os.path.exists(path)):
#        os.makedirs(path)
#    bw = open(path + '\person.txt','w')
#    for i in range(grouplength):
#        for j in range(codelength):
#            bw.write(str(person.T[i][j]) + " ")
#        bw.write('\r\n')
#    bw.close()
    path =dpath+'\\Step{}'.format(str(step))
    wirteperson(path,person,codelength,grouplength)
    wirteid(path,loct,size,person,grouplength)
'''
写初始肿瘤，即已经确认是肿瘤的部分。就是内层轮廓以内的部分
'''   
def writeOtumor(inloc,size):
    if os.path.exists(r'D:\Contour_extraction\meshtest\oblock.txt'):
        os.remove(r'D:\Contour_extraction\meshtest\oblock.txt')
    if len(inloc) > 0:
        for point in inloc:
            wf.writeOneTumor(r'D:\Contour_extraction\meshtest\block.txt',r'D:\Contour_extraction\meshtest\oblock.txt',point,size)
            
'''
写单个的id文件
'''
        
def write(ind,path,loct,size,person,grouplength):
    wf.wirtefdtd(r'D:\Contour_extraction\meshtest\fdtd.txt',path)
    wf.wirtemodel(r'D:\Contour_extraction\meshtest\model.txt',path+'\lktq.id')
    if os.path.exists(r'D:\Contour_extraction\meshtest\oblock.txt'):
        wf.wirtemodel(r'D:\Contour_extraction\meshtest\oblock.txt',path+'\lktq.id')
    wf.wirteTumor(r'D:\Contour_extraction\meshtest\block.txt',path+'\lktq.id',loct,size,person.T[ind])
    xlines,xgridmap = wf.togrid(path+'\lktq.id',True,r'D:\Contour_extraction\meshtest\xgrid.txt')
    ylines,ygridmap = wf.togrid(path+'\lktq.id',False,r'D:\Contour_extraction\meshtest\ygrid.txt')
    wf.changenums(r'D:\Contour_extraction\meshtest\last.txt',xgridmap,ygridmap)
    wf.wirtemodel(r'D:\Contour_extraction\meshtest\last.txt',path+'\lktq.id')
    wf.writegrid(xlines,path+'\lktq.id')
    wf.writegrid(ylines,path+'\lktq.id')
    wf.writezgrid(path+'\lktq.id',r'D:\Contour_extraction\meshtest\zgrid.txt')
                    
