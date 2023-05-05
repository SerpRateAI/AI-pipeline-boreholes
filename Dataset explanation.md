# **Dataset explanation**
Here are described the different items present in the [dataset BA1B](https://github.com/SerpRateAI/core-photo-analysis/blob/ac5f9570f762d1f674059cee57904d1cbdb46138/Dataset_BA1B.xlsx): what they represent, where they come from, or some general information. This dataset will be helpful to create a predictive model.

## **Core**
The drilling bore is split in 142 cores, from the highest to the lowest in depth. Each core is approximately 3 meters deeper than the previous one. Given by the drilling team.

## **Section**
Each core is split in several section, with between 1 and 4 section for each, from the highest to the lowest in depth. Given by the drilling team.

## **Section Unit**
ULtimately, each section can include several subsections. However, images are linked with section, and are the same between two subsections of the same section. Given by the drilling team.

## **% of fractures**
Once we've made the segmentation of our pictures, we can access the percentage of cracks for each section. For this, we used skimage in [this code](https://github.com/SerpRateAI/core-photo-analysis/blob/ac5f9570f762d1f674059cee57904d1cbdb46138/Graph%20per%20depth/all_depth_graph.py) that gives the graph of percentage of cracks for each depth. We did it for several takes: the sheer segmentation issued from ilastik, plus with smaller object or [less eccentric object removed](https://github.com/SerpRateAI/core-photo-analysis/blob/cfaaf6da57c4f1e12391eb9d0a15f2a83c2ea27d/Eccentricity/Eccentricity_graph.py) in an attempt to reduce noise in the background. The final percentage is the mean of these different takes. We'll then use those statistics to build a predictive model of when/where cracks will occur.

## **Images**
The images that form the base of our segmentation are taken from the [Oman project public data](https://www.icdp-online.org/projects/by-continent/asia/oodp-oman/public-data-2). Those are vertical cuts of each section of each core of the drilling bore BA1B, and are the data we used to make our segmentation and our prediction of the % of fractures.

## **Segmentation**
To segment our images, we used the software [ilastik](ilastik.org). The goal is to extract the cracks for the base images, to then deduce what conditions favorise the cracking. The whole process is detailed in the [read me](README.md). We took several shot at the segmentation to keep the one that seems to fit the best to the cracks. 

## **Top depth**
For each section, gives the depth of the top of the section in meters. The drilling bore goes down to 400 meters. Given by the public data.

## **Unit Desc 4**
Structural comments on the  rocks from the section, made by the drilling analysis team: breccia, slickenslides...Those are rock formations created by movments (as friction for example).  Information only for the last cores.

## **Vein Intensity**
Veins are leaflike structures composed of crystallized minerals, that usually form when mineral are carried by water (or any solution) into the rock. The vein intensity gives a rough idea of the amount of vein in each section. The values goes from 0 to 4, 4 representing a section with a lot of vein. We easily remark there are more veins in the higher section, which is confirmed by our % of cracks calculation. Warning: data missing for some section (value -999,25 ?).

## **Alteration**
The alteration conists of a change in the properties of rocks and minerals due to various geological processes (weathering, hydrothermal activity...). This value gives the grade of alteration for each section. The top section are much more altered than the bottom one, we can imagine it's due a better exposition to the surface. Given by the drilling team.

## **Remarks**
Remarks 1: remarks from geologists concerning vein intensity for each core: shape of vein, type of minerals, size... To be treated.

Remarks 2: remarks from geologists concerning structural intensity for each core: disposal of samples, thickness, irregularity... To be treated.

Remarks 4: remarks from geologists concerning rock type for each core: color, state of serpentinization, minerals in the veins and size of it...To be treated.

Remarks 5: remarks from geologists concerning alteration intensity for each core: how the alteration is manifested for waht type of rocks... To be treated.

The remarks often overlap, say twice the same thing or give simultaneous information. To be considered as a whole.

## **Unit Desc 5**
Vein features comments on the type of rocks from the section, made by the drilling analysis team: type of cutting, type of networks, direction, colors...  Information given only for the last cores.

## **Unit Desc 3**
Alteration comments on the type of rocks from the section, made by the drilling analysis team: where the alteration occurs, how it manifests.  Information given only for the last cores.

## **Unit Type**
The lithological type of rocks in each section. That's basically the answer to "What rock is this ?". Given by the public data. This data is split using panda.get_dummies to draw several columns out of it, with boolean variable for each values possible.

## **Unit Class**
The lithological class of rocks in each section. Class includes several rock types. For example ophiolite are a group of litospheric rocks. It can include gabbro, dunites... Und stands for Undefined (?). Given by the public data. This data is split using panda.get_dummies to draw several columns out of it, with boolean variable for each values possible.

## **Texture**
More informations about how the rocks are arranged: are those a result of a shearing ? A compaction ? Given by public data. This data is split using panda.get_dummies to draw several columns out of it, with boolean variable for each values possible.

## **Grainsize**
Informations about the grain size of each section: grain size is the average diameter of particles composing the sediments. Cryptocrystalline: several μm, barely visible under the microscope. Fine grained: less than 0.075 mm. Coarse grained: between 80 mm to 0.075 mm. Medium grained: from 1 to 5 mm. Microcrystalline: several to 200 μm, visible only through the microscope. Pegmatitic: > 1cm. This data is split using panda.get_dummies to draw several columns out of it, with boolean variable for each values possible.
