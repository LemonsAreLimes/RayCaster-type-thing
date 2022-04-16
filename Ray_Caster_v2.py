#the aim of this is to reduce render times, eliminate artifacts seen in prev version

import math

import matplotlib.pyplot as plt
import numpy as np


def CreatePointArray(line, obj_res):    #this will return the 'non-real' cords of a line
                                        #this only works on a 1D line (non angle), dont know if im going to change this
    print('creating point array')
    
    if(line[0][0] == line[1][0]):       #if x=x
        print('x==x')
        lineY1 = line[0][1]*obj_res
        lineY2 = line[1][1]*obj_res

        PointArray = []
        for i in range(lineY1, lineY2):
            PointArray.append([line[0][0], i/obj_res])      #X, Y frac

        return PointArray


    elif(line[0][1] == line[1][1]):  #if y=y
        print('y==y')

        lineX1 = line[0][0]*obj_res
        lineX2 = line[1][0]*obj_res

        print(lineX1, lineX2)

        PointArray = []                 #create points in range of the inital conditions
        for i in range(lineX1, lineX2):
            PointArray.append([i/obj_res, line[0][1]])      #X frac, Y 

        return PointArray

    else:
        print('not devloped yet')

def GetDist(PointArray, cam_cords):
        #does not yet account for intercetions with outher lines
        #or camera cords
    RayList = []
    for point in PointArray:
        x = point[0]
        y = point[1]

        distX = cam_cords[0] - x 
        distY = cam_cords[1] - y  

        hyp = math.sqrt(distX ** 2 + distY ** 2)
        angle = GetAngle(distX, distY)                  #angle used for indexing in ray list since not casting empty ray

        RayList.append([angle, hyp])

    return RayList

def GetAngle(opp, adj):
    angle = math.atan2(opp, adj)
    return math.degrees(angle)

def RayToDistanceList(RayList, fov, res):
    DistanceList = []
    for ang in range(fov*res):
        angle = ang/res
        found = False

        for ray in RayList:
            if round(ray[0], 2) == angle:
                found = True
                DistanceList.append(ray[1])
                break
        
        if found == False:
            DistanceList.append(0)

    return DistanceList
            
def Render(map):
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    x = np.array(map)
    plt.title("Line graph")
    plt.plot(x)
    plt.show()

line = [3,6]
ypos = 5
obj_res = 10

cam_cords = [20,20]
FOV = 90
RES = 100

line1 = [[3,6],[3,9]]
line2 = [[3,6],[6,6]]
pointlist1 = CreatePointArray(line1, obj_res)
pointlist2 = CreatePointArray(line2, obj_res)

pointlist = pointlist1 + pointlist2

for x in range(20):
    cord = [x, 20]

    RayList = GetDist(pointlist, cord)
    DistanceList = RayToDistanceList(RayList, FOV, RES)
    Render(DistanceList)
