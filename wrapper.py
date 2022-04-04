import cv2 as cv
import numpy as np
import copy
import math
import Edges
import INTPoint
import Clustering

def drawLines(image,lines,color = (0,0,255),width = 2):
    for item in lines:
        cv.line(image,(item[0],item[1]),(item[2],item[3]),color,width)
    return image

def drawPoints(image,points,color = (255,0,0),width = 10):
    for point in points:
        if (type(point[0])==type('v') or type(point[1])==type('v')):
            print("point type err: ",point[0],point[1])
            continue
        
        if point[0] > 0 and point[1] > 0:
            if point[0] < image.shape[1] and point[1] < image.shape[0]:
                cv.line(image,(int(point[0]),int(point[1])),(int(point[0]),int(point[1])),color,width)
    return image

def dealAImage(inputname,outputname,Oedges = False,Olines = False,OExLines = False,Oclassfy = True,Ostandard = True):
    image = cv.imread(inputname + '.png') # kitti png jpg
    orEdges = Edges.getEdges(image) # 1，2：降噪 检测边缘
    print ("got edges")
    orLines = Edges.getLines(orEdges,20) # 3：20为最短直线长度，小于它不计入
    print ("got lines , num : " + str(len(orLines)))
    exLines = Edges.extenLines(orLines,orEdges)# 4 扩展直线段
    print ("extend lines")
    exLines = Edges.mergeLines(exLines)#5： 合并接近的线段  线段端点 和 斜率的弧度值（含正负）
    print ("merged lines")

    lines = copy.deepcopy(exLines)# 合并后的lines的item type是tuple 否则是list
    ans = [('a',0),('a',0),('a',0)]
    anslines = [[],[],[]]
    ansnum = -1
    ans[0],lines,anslines[0] = Clustering.getAnCenter(lines)
    print ("first vanish point")
    if lines != None:
        ans[1],lines,anslines[1] = Clustering.getAnCenter(lines)
    print ("second vanish point")
    if lines != None:
        ans[2],lines,anslines[2] = Clustering.getAnCenter(lines)
    print ("third vanish point")
    for i in range (0,3,1):
        if ans[i] != None:
            ansnum = i
        else:
            break
    if Oedges:
        cv.imwrite(outputname + "_edges.jpg",orEdges)
    if Olines:
        image_lines = copy.deepcopy(image)
        drawLines(image_lines,orLines)
        cv.imwrite(outputname + "_lines.jpg",image_lines)
    if OExLines:
        image_ExLines = copy.deepcopy(image)
        drawLines(image_ExLines,exLines)
        cv.imwrite(outputname + "_exLines.jpg",image_ExLines)
    
    image_classfy = copy.deepcopy(image)
    if Oclassfy:
        if ansnum >= 0:
            image_classfy = drawLines(image_classfy,anslines[0],(255,255,0)) # yellow
        if ansnum >= 1:
            image_classfy = drawLines(image_classfy,anslines[1],(0,255,255)) #青色
        if ansnum >= 2:
            image_classfy = drawLines(image_classfy,anslines[2],(255,0,255)) #淡红
    else:
        image_classfy = drawLines(image_classfy,exLines)
    if Ostandard:
        fd = open(outputname + 'answer.txt','w') #answer表示只保留图像区域内的灭点
        if ansnum >= 0:
            image_classfy = drawPoints(image_classfy,[ans[0]],(255,255,0))
            if (type(ans[0][0])!=type('v') and type(ans[0][1])!=type('v')):
                #kitti: 1226 370  poss: W 1024 H 768
                if ((ans[0][0] < image_classfy.shape[1] and ans[0][0] >= 0.0)
                and (ans[0][1] < image_classfy.shape[0] and ans[0][1] >= 0.0)):
                    fd.write(str(ans[0][0]) + ' ' + str(ans[0][1]) + '\n') #只保留在图像区域内的有效灭点 
                else:
                    print("image W,H: {:d},{:d}".format(image_classfy.shape[1],image_classfy.shape[0]))
                # fd.write(str(ans[0][0]) + ' ' + str(ans[0][1]) + '\n')
            # fd.write(" ( " + str(ans[0][0]) + ' , ' + str(ans[0][1]) + ' ) ')
        if ansnum >= 1:
            image_classfy = drawPoints(image_classfy,[ans[1]],(0,255,255))
            if (type(ans[1][0])!=type('v') and type(ans[1][1])!=type('v')):
                if ((ans[1][0] < image_classfy.shape[1] and ans[1][0] >= 0.0)
                and (ans[1][1] < image_classfy.shape[0] and ans[1][1] >= 0.0)):
                    fd.write(str(ans[1][0]) + ' ' + str(ans[1][1]) + '\n')
                # fd.write(str(ans[1][0]) + ' ' + str(ans[1][1]) + '\n')
            # fd.write(" ( " + str(ans[1][0]) + ' , ' + str(ans[1][1]) + ' ) ')

        if ansnum >= 2:
            image_classfy = drawPoints(image_classfy,[ans[2]],(255,0,255))
            if (type(ans[2][0])!=type('v') and type(ans[2][1])!=type('v')):
                if ((ans[2][0] < image_classfy.shape[1] and ans[2][0] >= 0.0)
                and (ans[2][1] < image_classfy.shape[0] and ans[2][1] >= 0.0)):
                    fd.write(str(ans[2][0]) + ' ' + str(ans[2][1]) + '\n')
                # fd.write(str(ans[2][0]) + ' ' + str(ans[2][1]) + '\n')
            # fd.write(" ( " + str(ans[2][0]) + ' , ' + str(ans[2][1]) + ' ) ')
        fd.close()
    cv.imwrite(outputname + "_final.jpg",image_classfy)
