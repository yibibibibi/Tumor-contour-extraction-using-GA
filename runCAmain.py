# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 21:07:10 2018

@author: yibi
"""
import runCA as rC
import numpy as np
import pandas as pd
import mesh as mh
import calResult as cr
import modifyid as md
import wirtefile as wf
import os
import runconfocal as rcf

import random
import shutil
"""
'''
内外层分开迭代运行遗传算法
path：上一代的最优个体
size：肿瘤方块的大小
dpath: 用来放计算文件的根目录
prob_tumor :生成肿瘤的概率
steps:总的迭代次数
ooi:计算内层或者外层
TRUE：外层
FALSE：内层
'''
def runMain(path,size,dpath,prob_tumor,steps,point,ooi=True,grouplength=80):
    outprofile,inprofile,pointdarray = rC.tobounds(path,size)
    if ooi:
        loct = rC.tooitumor(outprofile,pointdarray,size)
        inloc = rC.origtumor(pointdarray,size)
    else:
        loct = rC.tooitumor(pointdarray,inprofile,size)
        inloc = rC.origtumor(inprofile,size)

    antenna = rC.readantenna()
    fitnessnum = pd.Series(np.zeros(grouplength))
    step = 1
    flag = False
    codelength = len(loct)
    person = pd.DataFrame(np.zeros(grouplength * codelength).reshape(grouplength,codelength),dtype=int)
#    print(person)
    best_person = pd.Series(np.zeros(codelength),dtype = int)
    person= rC.population(codelength,person,prob_tumor,grouplength)
#    print(person)
 
  
    person = rC.modifyper(person)
    # print(person)
    rC.writeOtumor(inloc,size)
    while step < steps:
        rC.run(dpath,step,person,codelength,loct,size,grouplength)
        print('开始第'+str(step)+'次迭代')
        runflag = False
        runflag = cr.runall(dpath, 1, grouplength+1, 10, step)
        if runflag:
            print(step)
            best_fitness,best_person,flag,fitnessnum,step = rC.fitness(step,dpath,person,fitnessnum,grouplength,antenna,point)
            print(step)
            if(not flag):
                break
            person = rC.Modify(best_person, person, grouplength, prob_tumor, codelength, step - 1)
            person = rC.Selection(person,fitnessnum,codelength,best_person,best_fitness,grouplength)
            person = rC.Crossover(codelength,person,grouplength)
            person = rC.Mutation(codelength,person,grouplength)

            person = rC.addbest(best_person, person, grouplength)

"""
"""
双层同时进行迭代运行遗传算法
"""
def runMain_2(path, size, dpath, prob_tumor, steps, point, grouplength=80):
    outprofile, inprofile, pointdarray = rC.tobounds(path, size)

    loct1 = rC.tooitumor(outprofile, pointdarray, size)
    loct2 = rC.tooitumor(pointdarray, inprofile, size)
    loct =  loct1+loct2
    inloc = rC.origtumor(inprofile, size)
    antenna = rC.readantenna()
    fitnessnum = pd.Series(np.zeros(grouplength))
    step = 1
    flag = False
    codelength = len(loct)
    person = pd.DataFrame(np.zeros(grouplength * codelength).reshape(grouplength, codelength), dtype=int)
    #    print(person)
    best_person = pd.Series(np.zeros(codelength), dtype=int)
    person = rC.population(codelength, person, prob_tumor, grouplength)
    #    print(person)


    person = modifyperson(person,len(loct1),len(loct2))
    # print(person)
    rC.writeOtumor(inloc, size)
    while step < steps:
        rC.run(dpath, step, person, codelength, loct, size, grouplength)
        print('开始第' + str(step) + '次迭代')
        runflag = False
        runflag = cr.runall(dpath, 1, grouplength + 1, 10, step)
        if runflag:
            print(step)
            best_fitness, best_person, flag, fitnessnum, step = rC.fitness(step, dpath, person, fitnessnum, grouplength,
                                                                           antenna, point)
            print(step)
            if (not flag):
                break

            person = rC.Selection(person, fitnessnum, codelength, best_person, best_fitness, grouplength)
            person = rC.Crossover(codelength, person, grouplength)
            person = rC.Mutation(codelength, person, grouplength)
            person = rC.addbest(best_person, person, grouplength)
            person = rC.Modify(best_person, person, grouplength, prob_tumor, codelength, step - 1)

'''
修改person
'''
def modifyperson(person,len1,len2):
    list1 = [0 for i in range(len1)]
    list2=  [1 for i in range(len2)]
    list1.extend(list2)
    p = person.T
    a = pd.Series(list1)
#    print(a)
    p[random.randint(0, person.shape[0])] = a
#    print(person)
    return p.T

'''
返回最佳的肿瘤模型
'''           
def thebesttumor(dpath):
    a = np.loadtxt(dpath + '\\best_fitness.txt',delimiter=' ')
    col = a[:,2]
    col = np.array(col)
#    col.astype(np.float)
    ind = col.argmax()
    return a[ind]

'''
根据软件特点修改当前肿瘤模型
'''
def modifytumor(opath,npath):
    if not os.path.exists(npath):
        os.makedirs(npath)
    pointsblock = mh.totumor(opath)
    points = md.blocktopoints(pointsblock)
    newpoints = md.fill(points)
    cpoints = md.centerpoints(newpoints)
    write(npath,cpoints,1)
#    return cpoints
'''
写肿瘤文件
'''   
def write(path,points,size):
    wf.wirtefdtd(r'D:\Contour_extraction\meshtest\fdtd.txt',path)
    wf.wirtemodel(r'D:\Contour_extraction\meshtest\model.txt',path+'\lktq.id')
    for point in points:
        wf.writeOneTumor(r'D:\Contour_extraction\meshtest\block.txt',path+'\lktq.id',point,size)   
    xlines,xgridmap = wf.togrid(path+'\lktq.id',True,r'D:\Contour_extraction\meshtest\xgrid.txt')
    ylines,ygridmap = wf.togrid(path+'\lktq.id',False,r'D:\Contour_extraction\meshtest\ygrid.txt')
    wf.changenums(r'D:\Contour_extraction\meshtest\last.txt',xgridmap,ygridmap)
    wf.wirtemodel(r'D:\Contour_extraction\meshtest\last.txt',path+'\lktq.id')
    wf.writegrid(xlines,path+'\lktq.id')
    wf.writegrid(ylines,path+'\lktq.id')
    wf.writezgrid(path+'\lktq.id',r'D:\Contour_extraction\meshtest\zgrid.txt')    
'''
判断是否计算完成

''' 
    
def isRunout(message,path):
    strings = []
    for i in message:
        strings.append(str(i)+' ')
    with open(path+'\\message.txt','w') as f:
        f.writelines(strings)
    return  message[-1] >= 1E19,message[0] == 1.0


def writefitness(wpath,mpathall):
    with open(wpath+'\\best_fitness.txt') as f:
        lines = f.readlines()
        # print(lines)
        f.close()
    removen(lines)
    with open(mpathall+'\\best_fitness.txt','w') as f:
        f.writelines(lines)
        f.close()
        
def removen(lists):
    for i in lists:
        if i == '\n':
            lists.remove('\n')

"""
 ### 内外层分开进行迭代的主运行函数 
        
'''
opath:初始的最佳肿瘤
wpath:外层轮廓计算放置的位置
npath:内层轮廓计算放置的位置
mpath:调整后肿瘤放置的位置
steps :每一代遗传算法迭代的次数
    
'''
def runmain(opath,wpath,npath,mpath,steps):
    step = 1
    point = tocenterpoint(opath)
    while True:        
        runMain(opath,1,wpath,0.4,steps,point,True)
        message = thebesttumor(wpath)
        opath = wpath+'\\Step'+str(int(message[0]))+'\\'+str(int(message[1]))
        
        modifytumor(opath,mpath+'\\'+str(step)+'\\wai')
        writefitness(wpath,mpath+'\\'+str(step)+'\\wai')
        one, two = isRunout(message,mpath+'\\'+str(step)+'\\wai')
        if one or two:
            break
        opath = mpath+'\\'+str(step)+'\\wai'
        # t = threading.Thread(target=rcf.del_file, args=(wpath))
        # t.start()
        rcf.del_file(wpath)
        shutil.rmtree(wpath)
        runMain(opath,1,npath,0.7,steps,point,False)
        message = thebesttumor(npath)
        opath = npath+'\\Step'+str(int(message[0]))+'\\'+str(int(message[1]))
        
        modifytumor(opath,mpath+'\\'+str(step)+'\\nei')
        writefitness(npath, mpath + '\\' + str(step) + '\\nei')
        one ,two = isRunout(message,mpath+'\\'+str(step)+'\\nei')
        if one or two:
            break
        opath = mpath+'\\'+str(step)+'\\nei'
        # t = threading.Thread(target=rcf.del_file, args=(npath))
        # t.start()
        rcf.del_file(npath)
        shutil.rmtree(npath)
        step += 1

def runmain_2(opath, wpath, npath, mpath, steps):
    step = 1
    point = tocenterpoint(opath)
    while True:
        runMain(opath, 1, npath, 0.7, steps, point,False)
        message = thebesttumor(npath)
        opath = npath + '\\Step' + str(int(message[0])) + '\\' + str(int(message[1]))
        
        modifytumor(opath, mpath + '\\' + str(step) + '\\nei')
        writefitness(npath, mpath + '\\' + str(step) + '\\nei')
        one, two = isRunout(message, mpath + '\\' + str(step) + '\\nei')
        if one or two:
            break
        opath = mpath + '\\' + str(step) + '\\nei'
        # t = threading.Thread(target=rcf.del_file, args=(npath))
        # t.start()
        rcf.del_file(npath)
        shutil.rmtree(npath)
        runMain(opath, 1, wpath, 0.4, steps,point,True)
        message = thebesttumor(wpath)
        opath = wpath + '\\Step' + str(int(message[0])) + '\\' + str(int(message[1]))
        
        modifytumor(opath, mpath + '\\' + str(step) + '\\wai')
        writefitness(wpath, mpath + '\\' + str(step) + '\\wai')
        one, two = isRunout(message, mpath + '\\' + str(step) + '\\wai')
        if one or two:
            break
        opath = mpath + '\\' + str(step) + '\\wai'
        # t = threading.Thread(target=rcf.del_file, args=(wpath))
        # t.start()
        rcf.del_file(wpath)
        shutil.rmtree(wpath)

        step += 1
"""
'''
双层迭代的运行函数
'''
def runMain_3(opath,runpath,steps):
    step = 1
    point = tocenterpoint(opath)

    mpath = runpath+'\\modify'
    while True:
        ppath = runpath + '\\shuang' + '\\' + str(step)
        runMain_2(opath,1,ppath,0.5,steps,point)
        message = thebesttumor(ppath)
        opath = ppath + '\\Step' + str(int(message[0])) + '\\' + str(int(message[1]))
        modifytumor(opath, mpath + '\\' + str(step))
        writefitness(ppath, mpath + '\\' + str(step))
        one, two = isRunout(message, mpath + '\\' + str(step))
        if one or two:
            break
        opath = mpath + '\\' + str(step)
        rcf.del_file(ppath)
        shutil.rmtree(ppath)
        step+=1
        
        
        
        
        

def tocenterpoint(opath):
    blockpoints = mh.totumor(opath)
    point1 = [blockpoints[0][0][0],blockpoints[0][0][1]]
    point2 = [blockpoints[0][1][0],blockpoints[0][1][1]]
    point = [(point2[0]+point1[0])/2,(point1[1]+point2[1])/2]
    return point      

# runMain(r'E:\Contour_extraction_4\modify\1\nei',1,r'E:\Contour_extraction_4\wai',0.4,30,[-10.5,-31.0],True,1000)
   
# runMain_2(r'E:\test3\osc\Step3\1',1,r'E:\Contour_extraction_10',0.5,1000,[20.5,4.5],80)
# runmain_2(r'E:\test2\osc\Step2\1',r'E:\Contour_extraction_6\wai',r'E:\Contour_extraction_6\nei',r'E:\Contour_extraction_6\modify',160)

runMain_3(r'E:\test5\osc\Step5\1',r'E:\Contour_extraction_12',80)
