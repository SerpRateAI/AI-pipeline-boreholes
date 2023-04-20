# **Implementation of Polytope function to determine linear connectivity of segmented images**

Here is described the process leading to the process of Polytope function for segmented images. Credit and thanks to Hamed Amiri, Ivan Vasconcelos, Yang Jiao, Pei-En Chen & Oliver Plümper for [their work on Quantifying microstructures of earth materials using higher-order spatial correlations and deep generative adversarial networks](https://www.nature.com/articles/s41598-023-28970-w)

To begin with, you'll have to download the [Connectivity folder](Connectivity).

The main notebook to use is the [Polytope  for segmented images](Connectivity/PyMMat-master/Polytope_for_segmented_images.ipynb).

## **How it works**
To have an idea of the connectivity of our segmented images, we can use *n-point correlation functions*. These functions determine the probabilities fro several points to be linked by a polytope, which is a geometric figure with a large number of symmetries. Here are the Polytope functions used in this code:
  - the S2(r) function calculate the probability for 2 points of distance r to be in the same region. 
  - the L(r) function calculates the probability for a line of length r to occur entirely in the same region.
  - the P3V(r) and P3H(r) calculates the probabilities for 3 points forming respectively equilateral vertical triangle and equilateral horizontal triangle woth vertice of length r to occur in the same region.
  - and so on, P4(r) and P6(r) calculates the probabilities for 4 and 6 points forming square and hexagon of vertice lentgh r to occur in the same region...

All these probabilities are calculated for different r byt the Pn function in this code. The Fn function normalize those probabilities such as Fn(0) is always 1, and Fn tends towards 0 when r tends towards infinity. These two functions caracterize the same thing: an idea of connectivity among microstructures. Thus they should have the same tendencies.

Here's a visual example from [the original article](https://www.nature.com/articles/s41598-023-28970-w).

![image](https://user-images.githubusercontent.com/94477034/233375734-b258fae5-9858-47ae-a169-fc1587c81035.png)

For more precise information about the detailed working, please see [the original article](https://www.nature.com/articles/s41598-023-28970-w).

## **Step 1: Image importation**
First of all, make sure the [uumatsci_utils](Connectivity/PyMMat-master/uumatsci_utils.py) is in the same folder as the notebook, it's where all the important functions are defined. Run the first cell for the necessary importation.

In the second cell, replace the path to match where are stored your segmented images.
```
# %% set paths
path = 'D:/SerpRateAI/Results'
image_number='CS_5057_5_B_9_3_1'
image_file = path + '/' + image_number +'/' + image_number +'_Simple Segmentation_3.tif'
```
Warning ! The image_number variable will come back a lot when saving our future plots, so pick something recognizable.

The image is then displayed to make sure the path given is correct.


<p align="center">
  <img src=https://user-images.githubusercontent.com/94477034/233383314-23c3569d-6301-4208-bb0d-12960c3b9192.png?raw=true alt="Sublime's custom image"/>
</p>

## **Step 2: Convert into microstructures**
In the following cell, we transorm our image into the Microstructure class defined in [uumatsci_utils](Connectivity/PyMMat-master/uumatsci_utils.py) to ease the Polytope process function. We'll just consider a small square of our image, and so you'll have to pick the dimension of this square by choosing the top-left coordinate with *y_start* and *x_start* and the *square_size*. 

```
y_start=1000
x_start=300
square_size=701
```
IMPORTANT: once you chose the square dimension, open [Sample_Pn_UU.cpp](Connectivity/PyMMat-master/Cpp_source/Polytope/Sample_Pn_UU.cpp) in the [Cpp_source/Polytope folder](Connectivity/PyMMat-master/Cpp_source/Polytope) and change MAXX and MAXY to your square size + 1. for example if your square_size is 500, MAXX = 501.
Nt then should be set to half of your square size.
```
#define MAXX 501
#define MAXY 501
#define Nt 250
```
The square should then be displayed, along with some other informations: the number of pixels considered as cracks in the square (*Number of inclusions*), the corresponding fraction of cracks, and the beginning of this list of pixels.

<p align="center">
  <img src=https://user-images.githubusercontent.com/94477034/233383781-99978332-d153-45c9-bdb5-9c8791cd3d79.png?raw=true alt="Sublime's custom image"/>
</p>


```
(500, 500)
Number of inclusions: 34521
Volume fraction: 0.138084
(2, 34521)
0  79
0  80
0  81
0  82
0  83
0  84
0  85
0  86
0  87
0  106
```

## **Step 3: Polytope function**
In the next cell, we first set up some path to run the C++ code. Change path to match where they're stored carefully ! 

```
cpathPn = 'D:/SerpRateAI/Connectivity/PyMMat-master/Cpp_source/Polytope/'
runtimePn = 'D:/SerpRateAI/Connectivity/PyMMat-master/runtime/'
outputPn = 'D:/SerpRateAI/Connectivity/PyMMat-master/runtime/output/'
```
This cell also create Mconfig files tracking the pixels considered as cracks. We erase this file at the beginning of each run to make sure we don't get data from another image, or another part of the same image.

The output are the first dots of the S2-Polytope graphs, so you can check the most important data without necessarly plotting it first, and make sure it is reliable.

After that, the last cells compute the Polytope function to display the Pn and the Fn graphs. You can modify where your results are stored at the end of each cell.
The output is the graphs of Pn and Fn function for your square in the segmented image, with different polytope (S2, L, P3V, P3H, P4, P6V).

<p align="center">
  <img src=https://user-images.githubusercontent.com/94477034/233358006-afd0ef70-c37a-48f4-bbba-597d5cb04170.png?raw=true" alt="Sublime's custom image"/>
</p>








