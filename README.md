# - 基于遗传算法进行肿瘤轮廓提取的技术研究
在XFDTD电磁仿真软件中建立一个二维的乳腺肿瘤模型，利用遗传算法优化找到肿瘤的轮廓，最大分辨率为1mm.
这个项目包含以下几个主要运行程序。
- runCAMain:这是项目的主要运行程序;             
- runCA:遗传算法的实现方法;                   
- firstmain:初期工作：主要包含共焦成像缩小肿瘤轮廓，以及小区域内遍历，找到轮廓的最佳位置。循环迭代找到最佳位置，然后输出最优的初始矩形轮廓。         
- runconfocal/confocal:firstmain实现的具体细节，以及一些文件处理方法（包含判断是否计算结束和无用文件夹的删除等工作，以免造成存储资源不够的情况）。   
- wirtefile:写每一个个体的fdtd文件和id文件
- mesh:修改网格，就类似与XFDTD的mesh操作。
- modifid:根据XFDTD软件的一些特点，填充网格，不影响最后结果，只是为了显示更加准确。
- fcontour:提取边缘轮廓的方法。
- fittxt:最优值函数的设置方法。
- calResult：基于XFDTD软件利用命令行多线程运行FDTD文件。
下面是函数调用的图结构：
-![avatar](https://github.com/yibibibibi/-/blob/master/%E5%87%BD%E6%95%B0%E8%B0%83%E7%94%A8%E5%9B%BE.jpg)
