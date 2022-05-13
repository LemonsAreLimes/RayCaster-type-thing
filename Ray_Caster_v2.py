import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import math
import time         


def triangulatePoint(point, camera_cords, angle_round):
    if point[0] > camera_cords[0]:      #prevents negative angles
        adj = point[0] - camera_cords[0] 
    else:
        adj = camera_cords[0] - point[0]
    
    if point[1] > camera_cords[1]:
        opp = point[1] - camera_cords[1] 
    else:
        opp = camera_cords[1] - point[1]
 
    hyp = math.sqrt(adj**2 + opp**2)

    angle_unconverted = math.atan2(opp, adj)
    angle = math.degrees(angle_unconverted)
    angleRounded = round(angle, angle_round)

    data = [angleRounded, hyp]
    return data

def SeeLine(line, camera_cords, angle_round):
    point0 = line[0]
    point1 = line[1]

    tri0 = triangulatePoint(point0, camera_cords, angle_round)
    tri1 = triangulatePoint(point1, camera_cords, angle_round)

    ray0 = [tri0[0], int(tri0[1])]
    ray1 = [tri1[0], int(tri1[1])]

    LineRay = [ray0, ray1]
    return LineRay

def ToDistanceList(LineRay, fov, angle_round):
    res = 1 * 10**angle_round
    DistanceList = []
    RayPos = []

        #checks if the full object is in the fov (should speed it up a bit hopefully)
    if int(LineRay[0][0]) in range(fov[0], fov[1]) or int(LineRay[1][0]) in range(fov[0], fov[1]):

        #add rays to the DistanceList (without cutting out non viewable)
        for pos in range(0, 360*res):
            angle = pos/res
            found = False

            for ray in LineRay:
                if round(ray[0], angle_round) == angle:
                    found = True
                                            #fixes objects firther becoming larger
                    dist = (1/(ray[1]))     #did not want to use a fixed value
                    DistanceList.append(ray[1])
                    RayPos.append(pos)
                    break
            
            if found == False:
                DistanceList.append(0)

        print(RayPos)
        print(len(DistanceList))

        #interpolate distance
        start = DistanceList[RayPos[0]]
        end = DistanceList[RayPos[1]]
        diff = RayPos[1] - RayPos[0]
        InterpolatedRayDistance = np.linspace(start, end, diff).tolist()

        #add interpolated ray distance into the DistanceList
        NewDistanceList = []
        for i in range(len(DistanceList)):
            if i in range(RayPos[0]+10, RayPos[1]+10):
                newnumber = i - RayPos[0]
                try:
                    NewDistanceList.append(InterpolatedRayDistance[newnumber])
                except IndexError:
                    print()

            else:
                NewDistanceList.append(0)

        #chop off the non viewable data
        ViewData = []
        for i in range(len(NewDistanceList)):
            if i in range(fov[0]*res, fov[1]*res):
                ViewData.append(NewDistanceList[i])

        return ViewData

    else:
        print('full object not in view')
        return False

def AnimRender2(obj, cam_cords, fov, res, angle_round, returnInfo=True):
    codeTimeList = []
    i = 0
    rot = fov

    while True:
        i+=1

        keypress = keyboard.read_key()

            #position input
        if keypress == 'w':         #y+
            cam_cords = [cam_cords[0], cam_cords[1]+1]
        if keypress == 's':         #y-
            cam_cords = [cam_cords[0], cam_cords[1]-1]
        if keypress == 'd':         #x+
            cam_cords = [cam_cords[0]+1, cam_cords[1]]
        if keypress == 'a':         #x-
            cam_cords = [cam_cords[0]-1, cam_cords[1]-1]

            #Rotation input
        if keypress == 'e':         #rot+
            rot = [rot[0]+1, rot[1]+1]
        if keypress == 'q':       #rot-
            rot = [rot[0]-1, rot[1]-1]

        elif keyboard.read_key() == 'esc':
            plt.close()
            print('closed the window')

            if returnInfo:
                print(codeTimeList)
                plt.title('Render time')
                plt.ylabel('Speed')
                plt.xlabel('Frame')
                plt.plot(codeTimeList)
                plt.show()
                return
            else:
                return

            #starts timer now because keyboard.read_key() pauses the loop untill something is pressed >:/
        codeTimeStart = time.perf_counter()

            #resets rotation 'seamlessly'
        if rot[1] > 360:
            rot = fov 
            print('rot=fov')
        if rot[0] < 0:
            print('reset 360')
            rot = [360-fov[1], 360]


        if len(codeTimeList) != 0:          #calculates frame time average
            codeTimeAVG = round((sum(codeTimeList) / len(codeTimeList)), 4)
        else:
            codeTimeAVG = 0

            #does some calculations or something idk
        Raylist = SeeLine(obj, cam_cords, angle_round)
        output = ToDistanceList(Raylist, rot, angle_round)

            #sets up the window: fix y value, turn axis off, set title. 
        plt.ylim(0, 0.2); plt.axis('off')     
        plt.title(f"Frame: {i}, Angle:{rot}, Avg render time (ms):{codeTimeAVG}")
        
        plt.plot(output)
        plt.draw(); plt.pause(0.0001); plt.clf()    #this somehow makes it an animation

        codeTimeEnd = time.perf_counter() 
        codeTimeList.append(codeTimeEnd - codeTimeStart)



cam_cords = [32, 32]
FOV = [0,90]
RES = 100
obj = [[2, 9], [4, 15]]

print('e = +rotation, q = -rotation')
print('w = +x, a = -y, s = -x, d = +y')

AnimRender2(obj, cam_cords, FOV, RES, angle_round=2, returnInfo=True)


