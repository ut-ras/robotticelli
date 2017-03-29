---
layout: post
title: Robotticelli
---

We've just completed demoing at this year's South by Southwest Create (SXSW Create). So, let's talk about Robotticelli -- what we've done and where we're headed. This is a follow-up to a [<span class="bodyLink">previous post</span>][primavera_blogpost] made a year and a half ago about roboticelli.

[primavera_blogpost]: http://ras.ece.utexas.edu/2015/11/06/primavera.html

In that post, you will be able to find more information about the motives and how the project came to fruition. Here, I will mostly talk about how the robot works and where it's headed.

### A High Level Overview

In essense, Robotticelli is a robot designed to paint murals on walls. In order to do this, it wirelessly communicates with motors placed at the four corners of the wall, and has those motors pull it around on ropes. 

![robotticelli at SXSW, with only two motors attached](http://i.imgur.com/dwBVJba.jpg)

Because the robot's system has a lot of moving parts (figuratively and literally), in any discussion of it's individual systems, it's important understand how each of these systems works in relation to everything else.

The project is split into three parts: Magi, Venus, and Primavera. **Primavera** is responsible for image processing and palette reduction to a set of spraypaint colors that we can order. **Venus** takes the reduced color image outputted by primavera, transforms it to a list of coordinates along the wall, and finds an efficient path to visit all these coordinates. It then generates a simple instruction set for the last system, Magi to follow. **Magi** is responsible for all of the robotic movement; this include everything from the servo drivers and communication modules to the non-linear control system.

Although we will talk about all of the systems, Magi is the beef of Robotticelli, so we will spend most of our time discussing that.

### Primavera

We do our image processing through a number of steps, but over-all, our system is pretty simple.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;First, we unpack our image into a space of coordinates, with R, G, and B being their own individual axis. We do this because, based on its color, any given color we construct with RGB will fit somewhere in this cube:

<img src="http://www.frank-t-clark.com/Professional/Papers/ColorHCW/RGB-Cube.PNG" width='250' height='250'/>

However, this image is actually a bit misleading because human eyes are actually more sensitive to some colors than they are other colors.

<img src="http://i.imgur.com/TBlpDI0.gif)" width='250' height='200'/>

Because of this, it's useful to [<span class="bodyLink">weigh each axes differently</span>][colorspace], effectively skewing the color-space to reflect this imbalance. From there, we can more usefully seperate dense clusters of similar colors into groups. 
Using [<span class="bodyLink">k-means</span>][kmeans], we can form groups out of our colors clusters in our new, slightly modified color-space. With any luck, it may look something like this: 

<img src="http://2.bp.blogspot.com/-NGqA6ZvO2VU/T3yNXDsnvBI/AAAAAAAAAU4/i2tV1MOzrnE/s1600/kmeans3.png" width='500' height='400'/>

[colorspace]: https://en.wikipedia.org/wiki/Color_difference#Euclidean
[kmeans]: https://en.wikipedia.org/wiki/K-means_clustering

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In this image, the pink dots represent the center of the clusters. Great! The easiest approach is to use these centers (which are coordinates in our RGB color space) as the color that best represents the entire group. We finally have a pallette! We can iterate through the image and reassign each pixel's color to the closest color in this palette.

Now, we're close to being done, but we actually still have a bit left to do. Running our algorithm on an image gives us results like this:

<span>
<img src="http://i.imgur.com/QKtRiIX.jpg" width='400' height='220'/>
<img src="http://i.imgur.com/GVb9ZhW.png" width='400' height='220'/>
</span>

This is nice, but it's mostly huge blobs of intense color, and we have no way of representing the colors in-between. This is called color banding, and we can get around this by applying an approach called [<span class="bodyLink">dithering</span>][dithering], which smoothes out the error in the image by diffusing it to neighboring pixels. 

For instance, if you had a grey pixel and assigned it the color black, the algorithm would say "okay, make the pixels surrounding this one a bit brighter to compensate for the fact that we made this one darker." 
We can do this over all the color channels (red, green, and blue) to get a good color diffusion. The result of dithering is this:

[dithering]: https://en.wikipedia.org/wiki/Dither

<span>
<img src="http://i.imgur.com/QKtRiIX.jpg" width='400' height='220'/>
<img src="http://i.imgur.com/BhEYfCl.png" width='400' height='220'/>
</span>

With the image looking much better, we are now ready to pass this on to our next stage, Venus.

------------
### Venus

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Venus is by far the simplest part of Robotticelli, as it essentially acts as the 'glue' between Primavera and Magi. Because our images have been reduced in color, each pixel in the image can be represented by 1 of *n* colors. In our image shown above, we are using *five* (white, black, red, green, blue). 

To start, we assign each pixel in the image to a coordinate on the wall by linearly scaling. Then, we split the image up into clouds of each color (shown below) and apply a greedy approximation to the [<span class="bodyLink">travelling sales man problem</span>][tsp]. This will generate a path that is about 30% longer than the optimal path.

<span>
<img src="http://i.imgur.com/PURbNwM.png" width='200' height='110'/>
<img src="http://i.imgur.com/n2H3ERa.png" width='200' height='110'/>
<img src="http://i.imgur.com/GjN3iVj.png" width='200' height='110'/>
<img src="http://i.imgur.com/DPEH0Dc.png" width='200' height='110'/>
</span>

[tsp]: https://en.wikipedia.org/wiki/Travelling_salesman_problem#Constructive_heuristics

That's about it, we can now unload this into a file that specifies which servo to actuate (based on color) and the XY coordinates for the robot to visit, which looks something like this:

```tsv
SERVO   X               Y
0	1.30054567448	0.514252838307
1	1.34044201437	0.475335270899
2	1.38035365633	0.524025235112
3	1.46125931705	0.533556861478
3	1.50211968011	0.494171195527
2	1.50214185755	0.582192991505
0	1.5433541811	0.586750364702
1	1.5848504103	0.591159284143
2	1.58469801124	0.547034066398
3	1.62662131754	0.595392829286
2	1.54370117594	0.763061334969
```

---

### Magi (and Electronics)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Magi is the most complicated piece of code in the robot, as it dictates everything about how the robot gets from point A to point B. Magi is split up into two interworking parts: **motor** and **robot**. Since the robot has to communicate with different parts of itself wirelessly, we found it sensible to assign the **robot** as the master communication device and the **motors** as slave communication devices. 

*There can only be one robot, but up to four motors.* Thinking about it in this way simplifies the problem dramatically, because now we no longer have to worry about having motors communicate to other motors. All flow of information will be of the form **robot → motor** or **motor → robot**.

For means of wirelessly communicating, we chose the fairly-often used choice of HTTP over a WIFI connection, as there are a lot of libraries  and other resources available to quickly build solutions. We then set up a private wifi-network and configured static IPs for all devices so that messages are consistently sent to the same devices, with each node having it's own Flask server. Flask is a microframework for web-driven programming, and it has proven useful for prototyping our robot's wireless communication systems before we move on to a more robust system. Using this, we can listen for requests of specific endpoints and execute code from other modules like so:

###### ROBOT:
```python
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/", methods=['POST'])
def run_step_when_ready():
    #Executes only after every motor has asked for a new instruction
    if all_motors_requested():
        execute_instruction()
    else:
        request_instruction(request.form.motor_id)
    
    return jsonify({"response": "Success"})
```

###### MOTOR:
```python
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/", methods=['POST'])
def run_step():
    #Runs immediately when instruction is received
    execute_instruction_and_request_another(request.form.instruction)

    return jsonify({"response": "Success"})
```
(bulk of code cut out for brevity)

We then create a separate module that defines a number of requests each node can make over the network, and now we have a very basic framework for a robot-motor control loop, which looks something like this: 

<img src="http://i.imgur.com/NjegxpQ.png" height='200'/>

With four motors attached, it remains mostly the same.

<img src="http://i.imgur.com/2qOdBZJ.png" height='400'/>
FIX THIS BEFORE SENDING IT OUT

Great! We can work off of this. Next we need to look at how exactly the robot moves through our space -- and how we can pull the ropes to get to a specific point. Using some simple rules of triangles, we can rewrite our XY coordinates as pair of distances -- one from the upper left motor, and one from the upper right motor. 

<img src="http://i.imgur.com/hBMwiha.jpg" height='400'/>

Here, we know that r<sub>1</sub> is defined by the length of the vector formed by x and y', and r<sub>2</sub> is defined by x' and y'. Shortly put,

<i>r<sub>1</sub></i> ≈ sqrt(<i>x <sup>2</sup> + y' <sup>2</sup></i>) <br/>
<i>r<sub>2</sub></i> ≈ sqrt(<i>x' <sup>2</sup> + y' <sup>2</sup></i>)

Because two rope lengths automatically define an (X,Y) pair, the lengths of the bottom two ropes are defined by the lengths of the top two.

With some minor adjustments to the x and y based on the robot's width and rotation, we can get an even better estimate. Without getting too much into the math of calculating how the robot rotates along the wall, an exact solution can be derived from finding the point at which the torques applied by the two ropes cancel out. Writing this in code and using python's numpy linear algebra library, we are easily able to take the length of the vectors we previously constructed.

~~~python
import numpy as np

def get_rope_lengths(x, y):
   '''
   Takes an x, y on the wall and transforms it into an |r1|, |r2|
   (lengths as opposed to vectors in xytransform)
   '''
   x_prime = W - x
   y_prime = H - y
   to_top_left  = np.linalg.norm([x, y_prime])
   to_top_right = np.linalg.norm([x_prime, y_prime])
	
   return to_top_left, to_top_right
~~~

So, how do we use this coordinate change to calculate how we need to pull the motors? Run get_rope_lengths(x,y)
  on both the current position and the target. Or, if we store our current rope lengths as a state, just on the target. Regardless, if we know how much rope we <i>currently</i> have out and how much rope we <i>will</i> have out when we are at our final position, we can just let in or out  rope accordingly to meet these goals.

Here is some code utilizing our past two functions to do just that.

```python
def get_rope_length_change(x, y, goal_x, goal_y):
   '''
	This is like get_motor_spin_capped but it will take the path of
	lowest tension rather than try to stick to a straight line. Also
	does not need to perform gradient decent to correctly hit target
	'''
   r_x, r_y = get_rope_lengths(x, y)
   r_goal_x, r_goal_y = get_rope_lengths(goal_x, goal_y)

   r_dx = r_goal_x - r_x
   r_dy = r_goal_y - r_y

   return r_dx, r_dy
```

Sparing the technical details of our implementation, this brings us to the current state of Robotticelli. Two of our committee members, Sid Desai and John Duncan, have began working on developing a much-improved non-linear control system for our robot that will be used to more effectively guide and locate our robot along the wall. Meanwhile, Sarah Muschinske and I have opened the table to improvements in our communication mechanism, looking for technologies that will allow us to scale our robot to larger walls. We are also beginning to revisit our robot's sprayer carriage. Mark Jennings is updating its design and gearing down motors, while the electrical team furiously writes code to integrate wheel encoder and IMU data into our algorithms for more precise robot localization.

Although we have a long way to go, we are covering ground more quickly than we ever have before. Surely, it won't be much longer before Robotticelli is the next hot artist in austin.

###### Author: Aaron Evans