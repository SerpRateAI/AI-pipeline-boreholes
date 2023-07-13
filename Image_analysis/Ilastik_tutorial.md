# **Segmentation process using Ilastik**
Here is described the process leading to the segmentation of Core images using the Ilastik software. 
To begin with, you will have to [download Ilastik](https://www.ilastik.org).

<p align="center">
  <img src="https://i.ytimg.com/vi/SQeRGvHeT3o/maxresdefault.jpg?raw=true" alt="Sublime's custom image"/>
</p>

## **New project creation**
First of all, you'll have to choose a type of project, according to what you will run your segmentation on, and what your expectations are. You can learn more about each type [here](https://www.ilastik.org/documentation/index.html).
For segmenting fractures, we will choose Pixel Classification.

<p align="center">
  <img src="https://user-images.githubusercontent.com/94477034/228227644-efe32921-57ce-43b6-9db9-1a4beeac98c0.png?raw=true" alt="Sublime's custom image"/>
</p>


## **Image importation**
First of all, import the reference images on which you will train your model. You can label as many images as you want for the training, so make sure your images represent the whole batch you want to process. For example, we will take images of the borehole with regularly distributed depth, from the top to the bottom.

<p align="center">
  <img src="https://user-images.githubusercontent.com/94477034/228198685-1441c698-2a0a-4c04-8128-44b141ab84e1.png?raw=true" alt="Sublime's custom image"/>
</p>

## **Feature selection**
This second part enables to choose which features the model will consider as more important in the segmentation. For example, detecting cracks is a lot about detecting edge: it could be interesting to select all the edges features, but not all the texture and color ones. Selecting more features will result in a better detection, but slower and demanding on ressources, whereas selecting less features is faster but less efficient. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/94477034/228201472-1c8666e8-14f7-44ce-af2e-1ef130c3e24e.png"/>
</p>

For the record, you can also ask Ilastik to suggest the better features according to what you already labelled, with the *Suggest Features* button in the part 3: Training. Here you can choose the method of suggestion (faster or more precise), and eventually adapt new features judging by the results proposed.

<p align="center">
  <img src="https://user-images.githubusercontent.com/94477034/228229945-48785921-5611-4b38-9926-63d02cda1f96.png?raw=true" alt="Sublime's custom image"/>
</p>

## **Labelling and training**
Now come the actual training of your model: select the right amount of labels needed, and just label your pictures directly on Ilastik. You can see the actual prediction of your model on your training images by pressing the *Live Update* button.
To change the image to label, just select the image wanted in the *Current view* line. The model will train simulteanously on all the labelled images labelled.

<p align="center">
  <img src="https://user-images.githubusercontent.com/94477034/228201751-c4a10751-a310-4532-8c5a-697ac4964636.png?raw=true" alt="Sublime's custom image"/>
</p>

To see more precisely where your model lacks training or does the job, there are visualisation options that helps you visualise the segmentation, the probabilities of detection, what is uncertain for your model... Toggle the eye icon to display the corresponding layer.

<p align="center">
  <img src="https://user-images.githubusercontent.com/94477034/228231243-b8f59958-94e3-4031-ac12-a979d502f51d.png?raw=true" alt="Sublime's custom image"/>
</p>

You obviously don't have to label the entirety of the training images, but the more you give data to your model, the more it will be precise (but also heavier!).

## **Exportation settings**
Once you're done labelling and the model satisfies you, you have several options regarding how to export the results given after the batch processing. First of all, you can upload different types of prediction: the actual segmentation, a probability map of detection, the uncertain objects for your model, the features used by the model, or the labels you provided.

<p align="center">
  <img src="https://user-images.githubusercontent.com/94477034/228232803-3a18ac77-4980-4255-80ea-63dce46f69b9.png?raw=true" alt="Sublime's custom image"/>
</p>

Then there's a bunch of settings you can modify to correspond the format you want. To be able to view the results easily but still keep the depth of the probability map, I chose the tif format for the exportation (warning, not any lector does read tif formt, and will sometimes display it as if it was a jpeg. Drive lector does read tif with differene in intensity, which is useful for probabilities).

Here are the settings I chose for **Simple Segmentation**:

<p align="center">
  <img src="https://user-images.githubusercontent.com/94477034/228232924-345aebe1-a0a3-4dd3-bcdd-a0d95ce1c827.png?raw=true" alt="Sublime's custom image"/>
</p>

And here are the settings for **Probabilities**:

<p align="center">
  <img src="https://user-images.githubusercontent.com/94477034/228236125-1bc14fd6-8bdd-4f1c-818b-9f2029131946.png?raw=true" alt="Sublime's custom image"/>
</p>

Of course you can change it but I found those ones to work properly.

## **Batch processing**
Once you selected the settings for exportation, the only thing left to do is importing the images you want to segment: do it in the part 5, *Batch Processing*:

<p align="center">
  <img src="https://user-images.githubusercontent.com/94477034/228239661-74a6512c-6d45-40a8-8541-1ef7d8929d32.png?raw=true" alt="Sublime's custom image"/>
</p>

And then hit the *Process all files* button. Here it comes!

## **To improve segmentation**
There are a few things you can do to improve your segmentation before even starting, or after you got the results.

- Apply filters on your images beforehand: use the *skimage.filters* library to apply different filters on all of your data. For example, a sobel or a roberts filter apply edge enhancement, which could make the detection easier for your model.
```
skimage.filters.gaussian(image, sigma=sigma)
skimage.filters.roberts(image)
skimage.filters.sobel(image)
```
For the filters codes, please refer to the [Gaussian Filter](Gaussian_filters.py) and [Edge Enhancement Filters](Edge_filters.py) files.
- to "denoise" your results, and make sure only the wanted objects are detected, you can perform a connected component analysis with *"skimage.measure.label"* and then use the module *skimage.measure.regionprops* to remove the smaller object detected. This suppose a high connectivity between the objects you really want to be detected.
```
skimage.measure.label(binary_mask,connectivity=connectivity, return_num=True)
skimage.measure.regionprops(image)
```
Refer the the [Component Analysis](Component_analysis.py) file for the code leading to this process.
- to improve the visibility of your results, you can display the segmentation on top of the raw images, with the module *skimage.color.label2rgb*. 
```
skimage.color.label2rgb(segmentation_map, colors=color_list, alpha=alpha, image=raw_image, saturation=saturation, bg_label=0, bg_color=None)
```
An example of its use is presented on the [Component Analysis](Component_analysis.py) code.
- you can perform a Principal Component Analysis to know what's the feature with the higher importance in your detection, and then choose to keep only these features for the training of your model (work in progress !)

- finally, I presented the results with a graph of the percentage of fractures per depth, using *skimage.measure.regionprops* to calculate the total area of fractures in all the pictures. The code leading to the graph is on the [Depth graph](Depth_graph.py) file.

## **Method used**
I made several model training with different parameters; here are some of the options that gave interesting results:
- No entry filters for raw images, selecting only the first two columns of features in Ilastik, labelling of 2 images from the top and 2 images from the bottom --> named Segmentation 1
- No entry filters, selecting all the features in Ilastik, labelling of nearly 15 images through all the core (depth regularly distributed) --> named Segmentation 2
- Gaussian and Hessian filters, selecting all the "edges" features in Ilastik, same labelling as Segmentation 2 --> named Segmentation 3
- Some post processing made by removing smaller objects on the 3 batches of segmentation (named Augmented_Segmentation_X), and by overlaying segmentation map on top of raw images.

Some comparison between the results of the segmentation can be found on Drive (*"Segmentation_Comparison"*), along with results of differents augmented segmentation for an image, the last number of the file being the minimal area of the object ("*ilastik/augmented_segmentation*"), depth dependent pore plots for segmentation 3 and augmented segmentation 3 (*"Depth Graphs"* folder, number at the end of file being minimal area of objects), and some examples of segmentation mapped on top of raw images (*"Overlay View"* folder).
