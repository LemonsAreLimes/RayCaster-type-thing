import matplotlib.pyplot as plt
import keyboard
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


def ToDistanceList(LineRay, direction, fov, angle_round):
    res = 1 * 10**angle_round
    DistanceList = []
    RayPos = []


    #add rays to the DistanceList (without cutting out non viewable)
    for pos in range(0, 360*res):
        angle = pos/res
        found = False

        for ray in LineRay:
            if round(ray[0], angle_round) == angle:
                found = True
                #fixes objects firther becoming larger
                DistanceList.append(res-ray[1])
                RayPos.append(pos)
                break
        
        if found == False:
            DistanceList.append(0)

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
                pass

        else:
            NewDistanceList.append(0)

    #chop off the non viewable data
    ViewData = []
    if direction + fov > 360 or direction - fov < 0:
        if direction - fov <0:
            high = (direction - fov) + 360
        else:
            high = direction - fov 

        if direction + fov > 360:
            low = (direction + fov) - 360
        else:
            low = direction + fov

        for x in range(high*res, 360*res):
            try:
                ViewData.append(NewDistanceList[x])
            except IndexError:
                pass

        for y in range(0, low*res):
            try:
                ViewData.append(NewDistanceList[y])
            except IndexError:
                pass
    else:
        high = direction + fov
        low = direction - fov
        for i in range(low*res, high*res):
            try:
                ViewData.append(NewDistanceList[i])
            except IndexError:
                pass

    return ViewData

def subRender(obj, cam_cords, direction, fov, angle_round):
    lines = len(obj)

    OutputList = []

    for i in range(lines):
        curent_line = obj[i]

        Raylist = SeeLine(curent_line, cam_cords, angle_round)
        output = ToDistanceList(Raylist, direction, fov, angle_round)

            #overlays largest data 
        if len(OutputList) == 0:
            OutputList = output
        else:
            for i in range(len(output)):
                if output[i] > OutputList[i]:
                    OutputList[i] = output[i]

    return OutputList


def reset_angle(angle):
    if angle >= 360:
        angle = 0
    elif angle <= 0:
        angle = 360
    return angle

def change_rotation(angle, key):
    if key == 'e':         #rot+
        direction = reset_angle(angle+5)
        return direction

    elif key == 'q':         #rot-
        direction = reset_angle(angle-5)
        return direction

    else:
        print('no key recognized in change rotaiton')

def change_position(angle, key, pos):
    movement_constant = 5
                                        #movement
    if key == 'w':          #forward
        x = math.sin(math.radians(angle)) * movement_constant
        y = math.cos(math.radians(angle)) * movement_constant
        cam_cords = [pos[0] + x, pos[1] + y]
        return cam_cords

    elif key == 's':          #backward
        x = math.sin(math.radians(angle)) * movement_constant
        y = math.cos(math.radians(angle)) * movement_constant
        cam_cords = [pos[0] - x, pos[1] - y]
        return cam_cords    

    elif key == 'd':          #right
        angle = reset_angle(angle-90)
        x = math.sin(math.radians(angle)) * movement_constant
        y = math.cos(math.radians(angle)) * movement_constant
        cam_cords = [pos[0] - x, pos[1] - y]
        return cam_cords    
        
    elif key == 'a':          #left
        angle = reset_angle(angle-90)
        x = math.sin(math.radians(angle)) * movement_constant
        y = math.cos(math.radians(angle)) * movement_constant
        cam_cords = [pos[0] + x, pos[1] + y]
        return cam_cords    

    else:
        print('no key recognized in change position')


def play(obj, cam_cords, direction, fov, angle_round, returnInfo=True):
    codeTimeList = []
    i = 0

    while True:
        i+=1

        keypress = keyboard.read_key()
        if keypress in ['q', 'e']:
            direction = change_rotation(direction, keypress)
        
        elif keypress in ['w','a','s','d']:
            cam_cords = change_position(direction, keypress, cam_cords)

        elif keypress == 'r':
            cam_cords = [0,0]

        elif keyboard.read_key() == 'esc':
            plt.close()
            print('closed the window')

            if returnInfo:
                print(f'Frames: {i}, Average render time: {sum(codeTimeList) / len(codeTimeList)}')
                print('code time list data: ')
                print(codeTimeList)
                print()
                return
            else:
                return


        codeTimeStart = time.perf_counter()

            #calculates frame time average
        if len(codeTimeList) != 0:          
            codeTimeAVG = round((sum(codeTimeList) / len(codeTimeList)), 4)
        else:
            codeTimeAVG = 0

        output = subRender(obj, cam_cords, direction, fov, angle_round)

            #sets up the window: fix y value, turn axis off, set title. 
        plt.ylim(0, 200) 
        plt.axis('off')     
        plt.title(f"Frame: {i}, Rotation:{direction}, Pos:{int(cam_cords[0])} ,{int(cam_cords[1])}, Avg render time (ms):{codeTimeAVG}")
         
        plt.plot(output)
        plt.draw(); plt.pause(0.0001); plt.clf()    #this somehow makes it an animation

        codeTimeEnd = time.perf_counter() 
        codeTimeList.append(codeTimeEnd - codeTimeStart)


cam_cords = [0, 0]
obj = [[[5, 5], [5, 10]] , [[5,10], [15,10]] , [[15,10], [5,5]]]

direction = 0
feild_of_view = 45      #is actually 90

print('e = +rotation, q = -rotation')
print('w = +x, a = -y, s = -x, d = +y')

play(obj, cam_cords, fov=feild_of_view, direction=direction, angle_round=2, returnInfo=True)

