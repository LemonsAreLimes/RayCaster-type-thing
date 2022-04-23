

import math

import matplotlib.pyplot as plt
import numpy as np

def CreatePointArray(line, obj_res):    #this will return the 'non-real' cords of a line
                                        #this only works on a non-angled line, dont know if im going to change this
    print('creating point array')
    
    if(line[0][0] == line[1][0]):       #if x=x
        print('x==x')
        lineY1 = line[0][1]*obj_res
        lineY2 = line[1][1]*obj_res

        print(lineY1, lineY2)

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

def RayToDistanceList(RayList, Viewable, res):        #now supports camera rotation
    DistanceList = []
    for ang in range(Viewable[0]*res, Viewable[1]*res):
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
    plt.title("Line graph")
    plt.plot(map)   
    plt.show()

obj_res = 1

cam_cords = [32,32]
FOV = [1,90]
RES = 100


#boundary
TopLeft = [0, 64]
TopRight = [64, 64]

BottomLeft = [0, 0]
BottomRight = [64, 0]

Top = CreatePointArray([TopLeft, TopRight], obj_res)
print([TopLeft, TopRight])

Bottom = CreatePointArray([BottomLeft, BottomRight], obj_res)
print([BottomLeft, BottomRight])

bounds = Top + Bottom 


for angle in range(180):
    rot = [FOV[0]+angle, FOV[1]+angle]

    RayList = GetDist(bounds, cam_cords)
    DistanceList = RayToDistanceList(RayList, rot, RES)
    Render(DistanceList)
