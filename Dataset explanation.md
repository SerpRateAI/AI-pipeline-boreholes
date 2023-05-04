# **Dataset explanation**
Here are described the different items present in the dataset BA1B: what they represent, where they come from, or some general information.

## **Core**
The drilling bore is split in 142 cores, from the highest to the lowest in depth. Each core is approximately 3 meters deeper than the previous one. Given by the drilling team.

## **Section**
Each core is split in several section, with between 1 and 4 section for each, from the highest to the lowest in depth. Given by the drilling team.

## **Section Unit**
ULtimately, each section can include several subsections, however images are linked with section, and are the same between two subsections of the same section. Given by the drilling team.

## **% of fractures**

## **Images**
The images that form the base of our segmentation are taken from the [Oman project public data](https://www.icdp-online.org/projects/by-continent/asia/oodp-oman/public-data-2). Those are vertical cuts of each section of each core, and the data we used to make our segmentation and our prediction of the % of fractures.

## **Segmentation**
To segment our images, we used the software [ilastik](ilastik.org). The whole process is detailed in the [read me](README.md). We took several shot at the segmentation to keep the one that seems to fit the best to the cracks. 

## **Top depth**
For each section, gives the depth of the top of the section in meters. The drilling bore goes down to 400 meters. Given by the public data.

## **Unit Desc 4**
Structural comments on the type of rocks from the section, made by the drilling analysis team.  Information only for the last cores.

## **Vein Intensity**
Veins are leaflike structures composed of crystallized minerals, that usually form when mineral are carried by water (or any solution) into the rock. The vein intensity gives an idea of the amount of vein in each section. The values goes from 0 to 4, 4 representing a section with a lot of vein. 

## **Alteration**

## **Remarks**

## **Unit Desc 5**
Vein features comments on the type of rocks from the section, made by the drilling analysis team.  Information given only for the last cores.

## **Unit Desc 3**
Alteration comments on the type of rocks from the section, made by the drilling analysis team.  Information given only for the last cores.

## **Unit Type**

## **Unit Class**

## **Core**

## **Texture**

## **Grainsize**
