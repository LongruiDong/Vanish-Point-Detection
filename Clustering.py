import cv2 as cv
import numpy as np
import copy
import math
import Edges
import INTPoint
from functools import cmp_to_key

eps = 1e-7

def filterVotes(votes,ratio = 0.8,minnum = 5):
    votes2 = sorted(votes.items(),key=lambda votes:votes[1],reverse=True)
    lenofvotes = min(len(votes2),max(minnum,int(len(votes2) * ratio)))
    votesFinal = {}
    for i in range(0,lenofvotes,1):
        votesFinal[votes2[i][0]] = votes2[i][1]
    for i in range(lenofvotes,len(votes2),1):
        if votes2[i][0][0] == 'h' or votes2[i][0][0] == 'v' or votes2[i][0][0] == 'p':
            votesFinal[votes2[i][0]] = votes2[i][1]
    return votesFinal

def getGraPoint(cluster):
    if len(cluster) == 0:
        return ()
    count = 0.0
    sumx = 0.0
    sumy = 0.0
    for point in cluster:
        w = point[2]
        if w==0:
            print("w= ",w)
        count += w #abs(w)
        sumx += w * point[0]
        sumy += w * point[1]
    if count==0: # 只有一个 且票数0
        return ()
    return (sumx/count,sumy/count,count)

def getMaxPoint(cluster):
    if len(cluster) == 0:
        return ()
    maxdata = 0.0
    maxx = 0
    maxy = 0
    for point in cluster:
        w = point[2]
        if point > maxdata:
            maxdata = point
            maxx = point[0]
            maxy = point[1]
    return (maxx,maxy,maxdata)

def cmp(a,b):
    return int(a>b) - int(a<b)

# 层次聚类
def getCluster(votesdict,arange = 100,Max = False):
    votes = []
    ret = []
    for p in votesdict:
        if p[0] == 'h' or p[0] == 'p' or p[0] == 'v':
            ret.append((p[0],p[1],votesdict[p]))#先把异常点拿出
            continue
        votes.append((p[0],p[1],votesdict[p]))
    clunum = []
    clusters = [] #用来保存聚类
    for p in votes:
        clunum.append(-1)
        clusters.append([]) #层次聚类 最初每个元素为1类
    count = 0
    for i in range(0,len(votes),1): #遍历当前所有候选点
        now = clunum[i]
        if clunum[i] == -1: #聚类初始
            now = count
            count += 1
            clusters[now].append((votes[i][0],votes[i][1],votes[i][2],i))#(x,y,votes,pos)
            clunum[i] = now
        
        for j in range(i+1,len(votes),1):
            if INTPoint.getLinesLength((votes[i][0],votes[i][1],votes[j][0],votes[j][1])) <= arange:
                if clunum[j] == -1:
                    clunum[j] = now
                    clusters[now].append((votes[j][0],votes[j][1],votes[j][2],j))
                else:
                    if clunum[j] == now:
                        continue
                    target = clunum[j]
                    if len(clusters[target]) > len(clusters[now]):
                        tmp = target
                        target = now
                        now = tmp
                    for item in clusters[target]:
                        clunum[item[3]] = now
                        clusters[now].append(item)
                    clusters[target] = []

    for cluster in clusters:
        if len(cluster) == 0:
            continue
        if Max:
            ret.append(getMaxPoint(cluster))
        else:
            if getGraPoint(cluster) == (): #若返回为空 不加入待排序中 出现于聚类就一个 且票数0
                continue
            ret.append(getGraPoint(cluster))
    # ret.sort(cmp=lambda x,y:cmp(x[2],y[2]),reverse = True)
    ret.sort(key=cmp_to_key(lambda x,y:cmp(x[2],y[2])),reverse=True)
    return ret

def removeBelongingLines(lines,point,arange = math.pi / 18):
    ret = []
    belong = []
    for line in lines:
        flag = True
        if point[0] == 'v':
            if abs(line[4] - math.pi/2)<= eps or abs(line[4] + math.pi / 2) <= eps:
                flag = False
        if point[0] == 'h':
            if abs(line[4] - 0) <= eps:
                flag = False 
        if point[0] == 'p':
            if line[2] - line[0] == 0:
                pass
            else:
                k = (line[3] - line[1]) / (line[2] - line[0])
                flag = not (k == point[1])
        if point[0] != 'h' and point[0] != 'v' and point[0] != 'p':
            arch = INTPoint.getArch(line,point)
            if arch <= arange:
                flag = False
        if flag:
            ret.append(line)
        else:
            belong.append(line)
    return ret,belong

def getAnCenter(lines,filter = 0.8):
    VPoints = INTPoint.getVPoints2(lines)#6：与相邻一定角度的线段求所在直线的交点做候选点 已去重 可能 v,v h,h
    print ("got vote points : " + str(len(VPoints)))
    votes,voters = INTPoint.voteForPoint(lines,VPoints)#7:所有线段对所有候选点投票
    print ("voted")
    votes = filterVotes(votes,0.8)#
    centers = getCluster(votes,50)#8:对投票之后的待选点做层次聚类 9对于每个聚类计算票数加权重心，作为新的待选点
    print ("got clusters : " + str(len(centers)))
    if centers == []:
        return None,None,None
    lines,anslines = removeBelongingLines(lines,centers[0]) #10 选择票数最高的聚类，作为第一个输出点
    print ("removed belonging lines")
    return centers[0],lines,anslines