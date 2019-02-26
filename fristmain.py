# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 15:19:32 2018

@author: yibi
"""

import confocal as cf
import runconfocal as runc
import os
time_steps = 2000
def run():
    pots = cf.Confocal()
    points = cf.toperson(pots,8,50)   
    runc.del_file(r'D:\Contour_extraction\confocal\Step1')
    runc.del_file(r'D:\Contour_extraction\osc')    
    num1 = runc.run(points,r'D:\Contour_extraction\confocal\Step1')
    step = 2   
    while True:
        num2 = runc.oscblock(r'D:\Contour_extraction\osc',step,num1)
        num1 = num2
       
        if num2 == 1:
            break
        step +=1
    return step


def runfrist(path):
    pots = cf.Confocal()
    points = cf.toperson(pots,8,50)   
    conpath = path+'\\confocal'
    oscpath = path+'\\osc'
    if not os.path.exists(conpath+'\\Step1'):
        os.makedirs(conpath+'\\Step1')
    else:
        runc.del_file(conpath+'\\Step1')
    if not os.path.exists(oscpath):
        os.makedirs(oscpath)
    else:
        runc.del_file(oscpath)    
    num1 = runc.run(points,path)
    step = 1

    while True:
        print(str(step)+'______##################################_____________________________________________')
        num2 = runc.oscblock(path,step,num1)
        num1 = num2     
        if num2 == 1:
            break
        step +=1
    return step

runfrist(r'E:\test5')