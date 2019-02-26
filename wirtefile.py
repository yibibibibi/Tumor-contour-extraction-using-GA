# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 17:47:21 2018

@author: yibi
"""

import mesh as mh
'''

写fdtd文件
'''

def wirtefdtd(readfile,writefile):
     fdtd = open(writefile+'\\lktq.fdtd','w')
     name = writefile+'\lktq.id\n'
     br = open(readfile)
     lines = br.readlines()
     lines[3] = name
     fdtd.writelines(lines)
     br.close()
     fdtd.close()
        
    
 
'''
写模型
'''

def wirtemodel(readfile,writefile):
    model = open(readfile)
    idfile = open(writefile,'a+')
    idfile.writelines(model)
    idfile.close()
    model.close()
    
   
    

    
'''
写肿瘤
'''

def wirteTumor(readfile,writefile,loct,size,sigperson):   
    tumor = open(readfile)
    tumorlines = tumor.readlines()
    tumor.close()
    idfile = open(writefile,'a+')
    for i in range(len(sigperson)):
        if sigperson[i] == 1:
            writeOnet(tumorlines,loct[i],size)
            idfile.writelines(tumorlines)
    idfile.close()
 
def writeOneTumor(readfile,writefile,points,size):
    tumor = open(readfile)
    tumorlines = tumor.readlines()
    tumor.close()
    idfile = open(writefile,'a+')
    writeOnet(tumorlines,points,size)
    idfile.writelines(tumorlines)
    idfile.close()
    

def writeOnet(tlines,points,size):
    tlines[83] = 'Fill_Material {:.0f}\n'.format(1 + 2)
    tlines[94] = 'vertex1 {0} {1} -0.001\n'.format((points[0]-size/2)/1000,(points[1]-size/2)/1000)
    tlines[95] = 'vertex2 {0} {1} 0\n'.format((points[0]+size/2)/1000,(points[1]+size/2)/1000)   
    return tlines
    
                

'''
写grid
'''
def togrid(readfile,xoy,writefile):
    with open(readfile) as f:
        idlines = f.readlines()
        f.close()
    return mh.togridfile(idlines,xoy,writefile)
    


def writegrid(idlines,wirtefile):
    with open(wirtefile,'a+') as f:
        f.writelines(idlines)
        f.close()
   
  


    
def writezgrid(readfile,writefile):
    with open(readfile) as f:
        idlines = f.readlines()
        f.close()
    zmap = mh.gridz(idlines)
    zlines = mh.zGridCorrect(writefile,zmap)
    with open(readfile,'a+') as f:
         f.writelines(zlines)
         f.close()
    
def changenums(file,mapx,mapy):
    xnum = mh.changenums(mapx)
    ynum = mh.changenums(mapy)
    with open(file) as f:
        lines = f.readlines()
        f.close()
    lastline = lines[-1].split()
#    print(lastline)
    lastline[0] = str(202+xnum)
    lastline[1] = str(202+ynum)
    lines[-1] = lastline[0] +' '+lastline[1]+' '+lastline[-1]+'\n'
    with open(file,'w') as f:
        f.writelines(lines)
        f.close
 
 
