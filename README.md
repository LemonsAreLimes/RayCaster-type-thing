# RayCasterV3
not really a ray caster but renders simmilar to one 
vertex caster might be a better name

# how does it work?
```
#quick rundown
    #TriangluatePoint / Createline             <= manupulated for position
        #create 2 vertex at cords
        #find: dist from camera and angle
        #TriangluatePoint returns [angle, distance]
        #CreateLine returns [[angle, distance], [angle, distance]]

    #ToDistanceList                            <= manupulated for rotation
        #determine if any part of the object is in view, if so:
        #add rays to the distancelist                           [0,0,1,0,0,2,0,0]                  ----|
        #interpolate the 2 distances                            [0,0,1,0,0,2,0,0] => [1,1.25,1.75,2]   |
        #add the interpolated list into the distance list       [0,0,1,1.25,1.75,2,0,0]                |  = Distance List
        #chop off data outside the feild of view                [0,0,1,1.25,1.75]                  ----|

    #RenderLoop
        #wait for input 
        #reset camera rotation if needed 
        #Createline
        #ToDistanceList
        #display data
        #clear

```
# limitations
evreything is "transparent" => only rendering one thing at a time                                                           
if you go really vlose to the object it renders really really big           
movement is independant of camera rotaion           
cameras rotation resets oddly         
