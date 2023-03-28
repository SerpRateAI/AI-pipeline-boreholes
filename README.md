# **Segmentation process using Ilastik**
Here is described the process leading to the segmentation of Core images using the Ilastik software. 
To begin with, you will have to [download Ilastik](https://www.ilastik.org).

![logo Ilastik](https://i.ytimg.com/vi/SQeRGvHeT3o/maxresdefault.jpg)

## **New project creation**
First of all, you'll have to choose a type of project, according to what you will run your segmentation on, and what your expectations are. You can learn more about each type [here](https://www.ilastik.org/documentation/index.html).
For segmenting fractures, we will choose Pixel Classification.

![image](https://user-images.githubusercontent.com/94477034/228227644-efe32921-57ce-43b6-9db9-1a4beeac98c0.png)


## **Image importation**
First of all, import the reference images on which you will train your model. You can label as many images as you want for the training, so make sure your images represent the whole batch you want to process. For example, we will take images of the borehole with regularly distributed depth, from the top to the bottom.

![image](https://user-images.githubusercontent.com/94477034/228198685-1441c698-2a0a-4c04-8128-44b141ab84e1.png)

## **Feature selection**
This second part enables to choose which features the model will consider as more important in the segmentation. For example, detecting cracks is a lot about detecting edge: it could be interesting to select all the edges features, but not all the texture and color ones. Selecting more features will result in a better detection, but slower and demanding on ressources, whereas selecting less features is faster but less efficient. 

![image](https://user-images.githubusercontent.com/94477034/228201472-1c8666e8-14f7-44ce-af2e-1ef130c3e24e.png)

For the record, you can also ask Ilastik to suggest the better features according to what you already labelled, with the *Suggest Features* button in the part 3: Training. Here you can choose the method of suggestion (faster or more precise), and eventually adapt new features judging by the results proposed.

![image](https://user-images.githubusercontent.com/94477034/228229945-48785921-5611-4b38-9926-63d02cda1f96.png)


## **Labelling and training**
Now come the actual training of your model: select the right amount of labels needed, and just label your pictures directly on Ilastik. You can see the actual prediction of your model on your training images by pressing the *Live Update* button.
To change the image to label, just select the image wanted in the *Current view* line. The model will train simulteanously on all the labelled images labelled.

![image](https://user-images.githubusercontent.com/94477034/228201751-c4a10751-a310-4532-8c5a-697ac4964636.png)

To see more precisely where your model lacks training or does the job, there are visualisation options that helps you visualise the segmentation, the probabilities of detection, what is uncertain for your model... Toggle the eye icon to display the corresponding layer.

![image](https://user-images.githubusercontent.com/94477034/228231243-b8f59958-94e3-4031-ac12-a979d502f51d.png)

You obviously don't have to label the entirety of the training images, but the more you give data to your model, the more it will be precise (but also heavier!).

## **Exportation settings**
Once you're done labelling and the model satisfies you, you have several options regarding how to export the results given after the batch processing. First of all, you can upload different types of prediction: the actual segmentation, a probability map of detection, the uncertain objects for your model, the features used by the model, or the labels you provided.

![image](https://user-images.githubusercontent.com/94477034/228232803-3a18ac77-4980-4255-80ea-63dce46f69b9.png)

Then there's a bunch of settings you can modify to correspond the format you want. To be able to view the results easily but still keep the depth of the probability map, I chose the tif format for the exportation (warning, not any lector does read tif formt, and will sometimes display it as if it was a jpeg. Drive lector does read tif with differene in intensity, which is useful for probabilities).

Here are the settings I chose for **Simple Segmentation**:

![image](https://user-images.githubusercontent.com/94477034/228232924-345aebe1-a0a3-4dd3-bcdd-a0d95ce1c827.png)

And here are the settings for **Probabilities**:

![image](https://user-images.githubusercontent.com/94477034/228236125-1bc14fd6-8bdd-4f1c-818b-9f2029131946.png)

Of course you can change it but I found those ones to work properly.

## **Batch processing**
Once you selected the settings for exportation, the only thing left to do is importing the images you want to segment: do it in the part 5, *Batch Processing*:

![image](https://user-images.githubusercontent.com/94477034/228239661-74a6512c-6d45-40a8-8541-1ef7d8929d32.png)

And then hit the *Process all files* button. Here it comes!

## **To improve segmentation**
There are a few things you can do to improve your segmentation before even starting, or after you got the results.

	1. Apply filters on your images beforehand
