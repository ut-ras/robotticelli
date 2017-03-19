---
layout: post
title: Robotticelli
---

We've just completed or demoing at this year's South by Southwest Create (SXSW Create). So, let's talk about Robotticelli -- what we've done and where we're headed. This is a follow-up to a [<span class="bodyLink">previous post</span>][primavera_blogpost] made a year and a half about roboticelli.

[primavera_blogpost]: http://ras.ece.utexas.edu/2015/11/06/primavera.html

In that post, you will be able to find more information about the motives and how the project came to fruition. Here, I will mostly talk about how the robot works and where it's headed.

### A High Level Overview

In essense, Robotticelli is a robot designed to paint murals on walls. In order to do this, it wirelessly communicates with motors placed at the four corners of the wall, and has those motors pull it around on ropes. 

![robotticelli at SXSW, with only two motors attached](http://i.imgur.com/dwBVJba.jpg)

Because the robot's system has a lot of moving parts (figuratively and literally), in any discussion of it's individual systems, it's important understand how these systems works in relation to everything else.

The project is split into three parts: Magi, Venus, and Primavera. **Primavera** is responsible for image processing and palette reduction to a set of spraypaint colors that we can order. **Venus** takes the reduced color image outputted by primavera, transforms it to a list of coordinates along the wall, and finds an efficient path to visit all these coordinates. It then generates a simple instruction set for the last system, Magi to follow. **Magi** is responsible for all of the robotic movement; this include everything from the servo drivers and communication modules to the non-linear control system.

Although we will talk about all of the systems, Magi is the beef of Robotticelli, so we will spend most of our time talking about that.

### Primavera

We do our image processing through a number of steps, but over-all, our system is pretty simple.

First, we unpack our image into a space of coordinates, with R, G, and B being their own individual axes. We do this because, based on its color, any given color we construct with RGB will fit somewhere in this cube:

<img src="http://www.frank-t-clark.com/Professional/Papers/ColorHCW/RGB-Cube.PNG" width='250' height='250'/>

However, this image is actually a bit misleading because human eyes are actually more sensitive to some colors than they are other colors.

<img src="http://i.imgur.com/TBlpDI0.gif)" width='250' height='200'/>

Because of this, it's useful to [<span class="bodyLink">weigh each axes differently</span>][colorspace], effectively skewing the color-space to reflect this imbalance. From there, we can more usefully seperate dense clusters of similar colors into groups. 
Using [<span class="bodyLink">k-means</span>][kmeans], we can form groups out of our colors clusters in our new, slightly modified color-space. With any luck, it may look something like this: 

<img src="http://2.bp.blogspot.com/-NGqA6ZvO2VU/T3yNXDsnvBI/AAAAAAAAAU4/i2tV1MOzrnE/s1600/kmeans3.png" width='500' height='400'/>

[colorspace]: https://en.wikipedia.org/wiki/Color_difference#Euclidean
[kmeans]: https://en.wikipedia.org/wiki/K-means_clustering

In this image, the pink dots represent the center of the clusters. Great! The easiest approach is to use these centers (which are coordinates in our RGB color space) as the color that best represents the entire group. We finally have a pallette! We can iterate through the image and reassign each pixel's color to the closest color in this palette.

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

---
### Venus

Venus is by far the simplest part of robotticelli, as it essentially acts as the 'glue' between Primavera and Magi. Because our images have been reduced in color, each pixel in the image can be represented by 1 of *n* colors. In our image shown above, we are using *five* (white, black, red, green, blue). 

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
0	1.34044201437	0.475335270899
0	1.38035365633	0.524025235112
0	1.46125931705	0.533556861478
0	1.50211968011	0.494171195527
0	1.50214185755	0.582192991505
0	1.5433541811	0.586750364702
0	1.5848504103	0.591159284143
0	1.58469801124	0.547034066398
0	1.62662131754	0.595392829286
0	1.54370117594	0.763061334969
```

---
### Magi
