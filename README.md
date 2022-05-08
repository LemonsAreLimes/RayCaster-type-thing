# RayCasterV2Test
not really a ray caster but renders simmilar to one 

# how does it work?
creates a bunch of points from 2 endpoints.     
the distance (hypotenuse, via x,y positions) of each point from the camera is logged.     
the angle extracted from the triangle and is used as an index for where the object is.     
this is done to have an output that is not just the object.     
object data is then interpolated to give a smooth render.          
then, after all of this, its rendered via pyplot.          

# limitations
evreything is "transparent"    <= i lied im not working on it                              
no movement (yet)    <= working on it                   
       
