# -*- coding: utf-8 -*-

"""
对像素进行聚类。
在像素级水平进行聚类可以用在一些很简单的图像

载入图像，并将其下采样到一个较低的分辨率，然后对这些区域用k-means进行聚类

K-means 的输入是一个有 stepsX × stepsY 行的数组,数组的每一行有 3 列,各列分别为区域块 R、G、B 三个通道的像素平均值。

为可视化最后的结果 , 我们用 SciPy 的imresize() 函数在原图像坐标中显示这幅图像。

参数 interp 指定插值方法;我们在这里采用最近邻插值法,以便在类间进行变换时不需要引入新的像素值。

"""

from scipy.cluster.vq import *
from scipy.misc import imresize

from pylab import *

from PIL import Image
import cv2
#steps*steps像素聚类
#参数
m_k = 16
m_maxsteps = 128

def clusterpixels_square(infile, k, steps):

    im = array(Image.open(infile))

    #im.shape[0] 高 im.shape[1] 宽
    dx = im.shape[0] / steps
    dy = im.shape[1] / steps
    # 计算每个区域的颜色特征
    features = []
    for x in range(steps):
        for y in range(steps):
            R = mean(im[x * dx:(x + 1) * dx, y * dy:(y + 1) * dy, 0])
            G = mean(im[x * dx:(x + 1) * dx, y * dy:(y + 1) * dy, 1])
            B = mean(im[x * dx:(x + 1) * dx, y * dy:(y + 1) * dy, 2])
            features.append([R, G, B])
    features = array(features, 'f')     # 变为数组
    # 聚类， k是聚类数目
    centroids, variance = kmeans(features, k)
    code, distance = vq(features, centroids)

    # 用聚类标记创建图像
    codeim = code.reshape(steps, steps)
    codeim = imresize(codeim, im.shape[:2], 'nearest')
    return codeim

#stepsX*stepsY像素聚类
def clusterpixels_rectangular(infile, k, stepsX):

    im = array(Image.open(infile))

    stepsY = stepsX * im.shape[1] / im.shape[0]

    #im.shape[0] 高 im.shape[1] 宽
    dx = im.shape[0] / stepsX
    dy = im.shape[1] / stepsY
    # 计算每个区域的颜色特征
    features = []
    for x in range(stepsX):
        for y in range(stepsY):
            R = mean(im[x * dx:(x + 1) * dx, y * dy:(y + 1) * dy, 0])
            G = mean(im[x * dx:(x + 1) * dx, y * dy:(y + 1) * dy, 1])
            B = mean(im[x * dx:(x + 1) * dx, y * dy:(y + 1) * dy, 2])
            features.append([R, G, B])
    features = array(features, 'f')     # 变为数组
    # 聚类， k是聚类数目
    centroids, variance = kmeans(features, k)
    code, distance = vq(features, centroids)
    # # 用聚类标记创建图像
    # codeim = code.reshape(stepsX, stepsY)
    # print "现在array"
    # print code
    # print code.shape
    # codeim = imresize(codeim, im.shape[:2], 'nearest')
    # return codeim
    return code



#计算最优steps 为保证速度以及减少噪点 最大值为maxsteps 其值为最接近且小于maxsteps 的x边长的约数
def getfirststeps(img,maxsteps):

    msteps = img.shape[0]

    n = 2

    while(msteps>maxsteps):

        msteps =   img.shape[0]/n
        n = n + 1

    return msteps

