# RayCasterV2Test
not really a ray caster but renders simmilar to one 

# how does it work?
creates a bunch of points from 2 endpoints.     
the distance (hypotenuse) of these points from the camera is logged.     
the angle extracted from the triangle and is used as an index for where the object is.     
this is done to have an output that is not just the object.     
then, after all of this, its rendered via matplotlib (i did the worst crime imagenable (stealing code) to get this to work).      

# limitations
evreything is "transparent"    <= working on it            
currently only outputs a animation of the camera rotating
