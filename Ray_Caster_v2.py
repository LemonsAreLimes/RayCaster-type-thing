import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import math
import time         #going to be used for calculating render times



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

def CamViewable(RayList, Viewable, res):
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

def FindHighAndLow(listy):
    high = [0, 0]   #[value, position]
    low = [1000, 0]

    zeros = 0
    for i in range(len(listy)):
        if listy[i] != 0:

            if listy[i] >  high[0]:
                high = [listy[i], i]

            if listy[i] < low[0]:
                low = [listy[i],i]

        else:
            zeros+=1

    if zeros == len(listy):     #prevents spitting out broken data
        return False
    else:
        return [high, low]

def AvgPoints(inital_list, HighAndLow):
    High = HighAndLow[0]
    Low = HighAndLow[1]

            #find the start, end and diffrence 
    if High[1] > Low[1]:
        first = HighAndLow[1][0]
        end = HighAndLow[0][0]

        diff = HighAndLow[0][1] - HighAndLow[1][1]
        startIndex = HighAndLow[0][1]
        endIndex = HighAndLow[1][1]

    elif Low[1] > High[1]:
        first = HighAndLow[0][0]
        end = HighAndLow[1][0]

        diff = HighAndLow[1][1] - HighAndLow[0][1]
        startIndex = HighAndLow[0][1]
        endIndex = HighAndLow[1][1]

    elif Low[1] == High[1]:
        first = HighAndLow[0][0]
        end = HighAndLow[1][0]

        diff = HighAndLow[1][1] - HighAndLow[0][1]
        startIndex = HighAndLow[0][1]
        endIndex = HighAndLow[1][1]

    else:
        print("SOMETHING WENT WRONG LINE 404")

        #actually generates the desired data
    new_range = interpolate(first, end, diff)
    ini_len = len(inital_list)

        #creates new list the same length as the inital, with new data inserted

    new = []
    for i in range(ini_len):
        if i < startIndex:                          #if before new range append inintal list
            new.append(inital_list[i])

        elif i > endIndex:                          #if after new range append inital list
            new.append(inital_list[i])

        elif i >= startIndex and i <= endIndex:     #if in list append new
            z = i - startIndex
            try:
                new.append(new_range[z])
            except IndexError:
                print('index error')

        else:
            print('uhhh', i)
    
    return new

def interpolate(start, end, diff):
    x = np.linspace(start, end, diff)
    y = x.tolist()
    return y

def smooth_cam_output(Distance_list):
    HighAndLow = FindHighAndLow(Distance_list)
    
    if HighAndLow != False:
        print(HighAndLow)
        avg = AvgPoints(Distance_list, HighAndLow)    
        return avg
    else:
        return 0

def Render(map):
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    plt.title("Line graph")
    plt.plot(map)   
    plt.show()

def RenderAnim(obj, cam_cords, res, frame_cap=None):
    fig = plt.figure(figsize=(6, 2.5))

    codeTimeList = []

    RayList = GetDist(obj, cam_cords)

    def animation_func(i):
        codeTimeStart = time.perf_counter()

        if i == frame_cap-1:               #slightly more elagant way of closing the animation
            plt.close()
            print('done animation')
            print('please, plot this infromation manually:')
            print(codeTimeList)

        plt.clf()
        plt.ylim(0,100)

        rot = [FOV[0]+i, FOV[1]+i]

        DistanceList = CamViewable(RayList, rot, res)
        output = smooth_cam_output(DistanceList)

        if len(codeTimeList) != 0:          #calculates frame time average
            codeTimeAVG = round((sum(codeTimeList) / len(codeTimeList)), 4)
        else:
            codeTimeAVG = 0

        plt.title(f"Frame: {i}, Angle: 90+{i}, Avg render time (ms):{codeTimeAVG}")
        plt.plot(output)

        codeTimeEnd = time.perf_counter()
        codeTimeList.append(codeTimeEnd - codeTimeStart)

    anim = animation.FuncAnimation(fig, animation_func, frames=frame_cap, interval = 1, repeat=False)
    plt.show()





#config
RES = 100
obj_res = 1

FOV = [1,90]
cam_cords = [32,32]

#boundary
TopLeft = [0, 64]
TopRight = [64, 64]

BottomLeft = [0, 0]
BottomRight = [64, 0]


# obj_list = [[[0, 64],[64, 64]], [[0, 0],[64, 0]]]



Top = CreatePointArray([TopLeft, TopRight], obj_res)
print([TopLeft, TopRight])

# Bottom = CreatePointArray([BottomLeft, BottomRight], obj_res)
# print([BottomLeft, BottomRight])

bounds = Top

RenderAnim(bounds, cam_cords, RES)

# for angle in range(180):
#     rot = [FOV[0]+angle, FOV[1]+angle]

#     RayList = GetDist(bounds, cam_cords)
#     DistanceList = RayToDistanceList(RayList, rot, RES)
#     Render(DistanceList)

