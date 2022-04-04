# -*- coding:utf-8 -*-
import wrapper
import os
import numpy as np

def mkdir(path):
 
	folder = os.path.exists(path)
 
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print ("---  new folder... "+path+" ---")
		print ("---  OK  ---")
 
	else:
		print ("---  There is this folder!  ---")

outroot = /mdata/vanishpoint #for PC

# for i in range(1,15,1):
#     print("Process image "+str(i))
#     wrapper.dealAImage("data/" + str(i),"data/result/" + str(i),True,True,True)

# # 测试kitti odometry 04 3 1 5 8
# seqid = 10
# seq = "%02d"%seqid
# sseq = str(seq)
# imageroot = '/media/kitti/dataset/sequences' 
# indata = os.path.join(imageroot,sseq,'image_0')
# print("indata: ",indata)
# # 建立该序列结果文件夹
# mkdir(os.path.join("kitti",sseq))
# g = os.walk(indata)#遍历下面所有文件
# for path,_,file_list in g:
#     for filename in sorted(file_list):
#         impath = os.path.join(path,filename)[:-4]
#         nid = impath[-6:]
#         # if int(nid) != 1883 :  #139
#         #     continue
#         print(nid)#impath 6位数序号 str  ,True,True,True
#         wrapper.dealAImage(impath,outroot + "/" + "kitti/" + sseq +"/" + nid,False,False,True)

# # 测试poss odometry 00 
# seqid = 6
# seq = "%02d"%seqid
# sseq = str(seq)
# imageroot = '/media/poss/dataset/sequences/00' 
# indata = os.path.join(imageroot,'image_0')
# print("indata: ",indata)
# # 建立该序列结果文件夹
# mkdir(os.path.join("poss",sseq))
# g = os.walk(indata)#遍历下面所有文件
# for path,_,file_list in g:
#     for filename in sorted(file_list):
#         impath = os.path.join(path,filename)[:-4]
#         nid = impath[-6:]
#         if int(nid) <31710 or int(nid) >34940 :  #139
#             continue
#         print(nid)#impath 6位数序号 str  ,True,True,True
#         nnid = int(nid) - 31710
#         snnid = "%06d"%nnid
#         wrapper.dealAImage(impath,outroot + "/" + "poss/" + sseq +"/" + snnid,False,False,True)

# # 测试 kt 360 00  的9个序列

# seqid = 8
# seq = "%01d"%seqid
# sseq = str(seq)
# imageroot = '/media/KITTI-360/dataset/sequences/00' 
# indata = os.path.join(imageroot,'image_0')
# print("indata: ",indata)
# # 建立该序列结果文件夹
# mkdir(os.path.join("kt360",sseq))
# g = os.walk(indata)#遍历下面所有文件
# count = 0
# for path,_,file_list in g:
#     for filename in sorted(file_list):
#         impath = os.path.join(path,filename)[:-4]
#         nid = impath[-10:] # kt360 是10位数
#         if int(nid) <11100 or int(nid) >11494 :  #139 4187 5178 5200 5483  4: 5802 8112 5: 8150 9072 6: 9522 10220 7:10250 11064 8:11100 11494
#             continue
#         print(nid)#impath 6位数序号 str  ,True,True,True
#         nnid = int(nid) - 11100
#         snnid = "%06d"%nnid
#         wrapper.dealAImage(impath,outroot + "/" + "kt360/" + sseq +"/" + snnid,False,False,True)
#         count = count+1
# print('total num: {:d}'.format(count)) 

# # kt360 更新后完整序列数据
# seqid = 2
# seq = "%02d"%seqid
# sseq = str(seq)
# imageroot = '/media/KITTI-360/dataset/sequences/'+sseq
# indata = os.path.join(imageroot,'image_0')
# print("indata: ",indata)
# # 建立该序列结果文件夹
# mkdir(os.path.join("kt360f",sseq))
# g = os.walk(indata)#遍历下面所有文件
# count = 0
# for path,_,file_list in g:
#     for filename in sorted(file_list):
#         impath = os.path.join(path,filename)[:-4]
#         nid = impath[-10:] # kt360 是10位数
#         # if int(nid) >18997: # or int(nid) <9698 :  # 00:11501 02: 18997 03:1030 04:11400 05:6723 06:9698 07:3161 09:13955 10:3743#139 4187 5178 5200 5483  4: 5802 8112 5: 8150 9072 6: 9522 10220 7:10250 11064 8:11100 11494
#         #     continue
#         print(nid)#impath 6位数序号 str  ,True,True,True
#         nnid = int(nid)
#         snnid = "%06d"%nnid
#         wrapper.dealAImage(impath,outroot + "/" + "kt360f/" + sseq +"/" + snnid,False,False,True)
#         count = count+1
# print('total num: {:d}'.format(count)) 

# # 测试 kt 360 作者给出的测试窗口的子序列 02(new)中选[11261,14384] 04中选 [54, 2906]

seqid = 14 #12 14
seq = "%01d"%seqid
sseq = str(seq)
imageroot = '/media/KITTI-360/dataset/sequences/04'  # 02 04
indata = os.path.join(imageroot,'image_0')
print("indata: ",indata)
# 建立该序列结果文件夹
mkdir(os.path.join("kt360f",sseq))
g = os.walk(indata)#遍历下面所有文件
count = 0
for path,_,file_list in g:
    for filename in sorted(file_list):
        impath = os.path.join(path,filename)[:-4]
        nid = impath[-10:] # kt360 是10位数
        if int(nid) <54 or int(nid) >2906 :  #12: 11261 14384 14: 54 2906
            continue
        print(nid)#impath 6位数序号 str  ,True,True,True
        nnid = int(nid) - 54
        snnid = "%06d"%nnid
        wrapper.dealAImage(impath,outroot + "/" + "kt360f/" + sseq +"/" + snnid,False,False,True)
        count = count+1
print('total num: {:d}'.format(count))

#---------------Oxford Robotcar---------------#


# sseq = '2019-01-10-14-36-48-radar-oxford-10k-partial'
# imageroot = '/media/oxfordradar/2019-01-10-14-36-48-radar-oxford-10k-partial/stereo/left_rect'  # /media/oxfordradar/2019-01-10-14-36-48-radar-oxford-10k-partial/stereo/left_rect
# # 读入 associations.txt
# asstimepath = '/media/oxfordradar/2019-01-10-14-36-48-radar-oxford-10k-partial/associations.txt'
# asstime = np.loadtxt(asstimepath,usecols=[0])
# asstime=asstime[0:-2].astype(np.int) #8733帧
# numf = asstime.shape[0]
# print("indata: ",imageroot)
# # 建立该序列结果文件夹
# mkdir(os.path.join("robotcar",sseq))

# count = 0
# for i in range(numf):
#     filename = str(asstime[i])
#     print(filename)
#     impath = os.path.join(imageroot,filename)
#     wrapper.dealAImage(impath,outroot + "/" + "robotcar/" + sseq +"/" + filename,False,False,True)
#     count = count+1

# print('total num: {:d}'.format(count))
