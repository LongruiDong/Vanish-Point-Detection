import cv2 as cv
import numpy as np
import copy
import math
import Edges
eps = 1e-7

# 计算给定两条线交点
def getIntersectPoint(linea,lineb):
    a1,b1,c1 = Edges.getLineABC(linea)
    a2,b2,c2 = Edges.getLineABC(lineb)
    if a2 != 0 and b2 != 0:
        if abs(a1/a2 - b1/b2) <= eps:
            return ('p',a2/b2)#斜率一样 p表示 平行
    else:
        if a2 == 0 and b2 == 0:
            pass
        if a1 == 0 and a2 == 0:
            return ('h','h') # 两条 都是 h 水平的
        if b1 == 0 and b2 == 0:
            return ('v','v') # 两条都是 v 竖直的 即平行于图像y轴
#    if abs(Edges.getCirAnch(a1,b1) - Edges.getCirAnch(a2,b2)) <= 0.03:
#        return ('n','n')
    try:
        y = (1 - float(a2)/a1) / ((b1 * float(a2) / a1) - b2)
        x = (-y * b1 - 1) / a1
    except: # a1为0时 交点不存在 none
        return('n','n') #
    if math.isnan(y) or math.isnan(x): #上面会出现漏判。。 所以再判断
        return('n','n')
    return (int(x),int(y)) #ValueError: cannot convert float NaN to integer

# 计算若干线段的交点
def getVPoints2(lines,arange = 0.2617):
    l = 0
    r = 0
    ret = []
    for i in range(0,len(lines),1): #遍历每个线段 得到i斜率左右各arange内的线段
        while (lines[r][4] - lines[i][4] <= arange and r < len(lines) - 1):
            r += 1
        while (lines[i][4] - lines[l][4] >= arange):
            l += 1
        for j in range(l,r,1):# j弧度 在 [i-arange.i+arange]
            if j == i:
                continue
            ret.append(getIntersectPoint(lines[i],lines[j]))#计算两条线交点
    ret = removeSame(ret)# 去除重复 和 n n 但 h h or v v 会保存一个
    return ret

def removeSame(list):
    dic = {}
    ret = []
    flag = False
    for item in list:
        if item[0] == 'n':
            flag = True
        tmp = (item[0],item[1])
        # if dic.has_key(tmp):
        if tmp in dic:
            continue
        dic[tmp] = 1
        ret.append(tmp)
    if flag:
        ret.remove(('n','n'))
    return ret

def getLinesLength(line):
    return math.sqrt((line[3] - line[1]) ** 2 + (line[2] - line[0]) ** 2)

def getMidPoint(line):
    return ((line[0] + line[2]) / 2,(line[1] + line[3]) / 2)

def getArch(line,point):
    Mid = getMidPoint(line)
    dx = line[0] - Mid[0]
    dy = line[1] - Mid[1]
    px = point[0] - Mid[0]
    py = point[1] - Mid[1]
    if dx == dy == 0 or px == py == 0:
        return 0
    dot = dx*px + dy * py
    lens = math.sqrt(dx ** 2 + dy ** 2)
    lens2 = math.sqrt(px ** 2 + py ** 2)
    mir = dot / lens
    cos = abs(mir / lens2)
    if abs(cos) > 1:
        cos = float(int(cos))
    arch = math.acos(cos)
    return arch

# 7:每个线对每个候选交点投票
def voteForPoint(lines,VPoints):
    votes = {}
    voters = {}
    for p in VPoints:
        votes[p] = 0.0
        voters[p] = 0
    for line in lines:
        a,b,c = Edges.getLineABC(line)
        lens = getLinesLength(line) #线段长度
        for p in VPoints:
            fakep = p
            if p[0] == 'h': # 来自两个水平线
                if a == 0:
                    votes[p] += lens
                    voters[p] += 1
                    continue
                else:
                    fakep = (1000000,line[1])
            if p[0] == 'v':
                if b == 0:
                    votes[p] += lens
                    voters[p] += 1
                    continue
                else:
                    fakep = (line[0],1000000)
            if p[0] == 'p': # 来自两平行 但非 水平 or 竖直
                if b == 0:
                    continue
                if abs(a/b-p[1]) < eps:
                    votes[p] += lens
                    voters[p] += 1
                    continue
                else:
                    fakep = (line[0] + 1000000,line[1] + p[1] * 1000000)
            arch = getArch(line,fakep)
            if arch >= math.pi/18:
                continue
            votes[p] += lens * math.exp(-( arch / ( 2 * (0.1 ** 2 ) ) ) )#夹角越大 分低
            voters[p] += 1
#    for item in votes:
#        if voters[item] <= 4:
#            votes[item] = 0
    return votes,voters