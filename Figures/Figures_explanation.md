# **Explanation on construction and interpretation of figures**

## *Physical data graphs per depth*

![image](https://github.com/SerpRateAI/core-photo-analysis/assets/94477034/944b4865-dba4-47d1-84d6-fe1c1a5b062e)



The first essential piece of data to acquire is the degree of fracturing in the core at any given depth, enabling the establishment of a correlation between depth and the amount of fractures. The previous application of a connected component analysis permitted a straightforward calculation of the fractures total area using the skimage.measure module, which led to the desired percentage of fractures once divided by the total area of the image.

Calculation of the percentage of fractures have been made for three different takes of the segmentation 3: the raw segmentation, the segmentation with area filter, and the segmentation with eccentricity filter.  In the end, the variations in filters used have negligible impact on the results, as the curves share similar trends with a translation shift. Thus only a rolling mean of these three takes have been studied.

When compared with the lithological data from the core report, the percentage graph presents some coherent results. 
Throughout the top section mainly composed of dunite (0-160 meters), water infiltrated easily, causing carbonation and serpentinization reaction. A moderate amount of fractures is detected, from 3\% at the very top to 6\% near the transition area. A peak in fractures is detected near the transition zone between dunite and harzburgite rocks (160-180 meters), with up to 10\% of the image fractured; it can be explained by the shearing accompanying the change in minerals, along with reaction of serpentinization. The aqueous solution didn't infiltrate the bottom harzburgite section (180-400 meters) because of its depth, thus the fractures observed are less numerous (averaging 3\%), and probably not all caused by serpentinization or carbonation.

The adjacent graphs were plotted by extrapolating missing data from the physical measurements, and arranging these data by depth. They address possible correlation between those variables: features as cell abundance or magnetic susceptibility are closely related to depth changes, which can be explained by the variation in mineral composition along the borehole, bringing different properties. 

Here is the python code used for plotting the first graphs. The axs.plot can be replaced by axs.scatter to get a discrete view of the data.
```
data = pd.read_excel('Dataset_BA1B.xlsx')

fig, axs = plt.subplots(1, 6, sharey=True, figsize=(15,15))

x0 = data['Bulk density (g/cm³)']
x1 = data['Mean dry electrical Resistivity (ohmm)']
x2 = data['Cell abundance (cells/g)']
x3 = data['AMS bulk susceptibility']
x4 = data['H20 wt%']
x5 = data['CO2 wt%']
x6 = data['LOI wt%']
y = data.TOP_DEPTH

axs[0].plot(x2, y, color='orange')
axs[0].set_xlabel('Cell abundance (cells/g)', color='orange', fontsize=18)
axs[0].xaxis.labelpad = 0
axs[0].tick_params(axis="x", labelsize=10) 
axs[0].set_xticks([0,15000000,30000000]) 
axs[0].set_xticklabels([0,'1.5e7','3e7'])

axs[1].plot(x1, y, color='g')
axs[1].set_xlabel('Mean dry electrical Resistivity (ohmm)', color='g', fontsize=18)
axs[1].xaxis.labelpad = 15

axs[2].plot(x3, y, color='grey')
axs[2].set_xlabel('AMS bulk susceptibility', color='grey', fontsize=18)
axs[2].xaxis.labelpad = 0
axs[2].tick_params(axis="x", labelsize=10) 
axs[2].set_xticks([0,0.025,0.05]) 
axs[2].set_xticklabels([0,0.025,0.05])

axs[3].plot(x4, y, color='b')
axs[3].set_xlabel('H20 wt%', color='b', fontsize=18)

axs[4].plot(x5, y, color='black')
axs[4].set_xlabel('CO2 wt%', fontsize=18)

axs[5].plot(x6, y, color='purple')
axs[5].set_xlabel('LOI wt%', color='purple', fontsize=18)

axs[0].set_ylim(401,0)
fig.tight_layout()

```
One of the major feature supposed to be bounded with serpentinization process is Bulk density; we tried to plot the data concerning this density depending on depth to establish (or not) a correlation.
```
fig, ax = plt.subplots(figsize=(5,15))


x = data['Bulk density (g/cm³)']

y=data.TOP_DEPTH

ax.set_ylim(401,0)

ax.set_ylabel('TOP_DEPTH')
ax.set_xlabel('Bulk density (g/cm³)')

ax.scatter(x,y)
```

![image](https://github.com/SerpRateAI/core-photo-analysis/assets/94477034/37f9271e-ff84-4c92-be08-477842871274)

An interesting observation is the non apparent connection of data such as bulk density with depth; however, it is proven useful for the alteration prediction by the classification model. This outlines the classification relies on multiple features, and doesn't only try to predict depth.

## *Keywords graph*

![image](https://github.com/SerpRateAI/core-photo-analysis/assets/94477034/8004e1b0-0db1-4ebc-b621-ac183d31d4d1)


The remarks from geologists were covered by ChatGPT, which then extracted 10 relevant keywords for each of the 505 images. Following the keywords extraction, only the ones with multiple occurrences were retained, and the keywords with overlapping meaning were fused. The total number resulting keywords is of 55, and each of the core section is assigned 55 binary variables, being 1 if it possesses the feature described by the keyword, 0 if it does not.

They were then categorized based on the information they convey by ChatGPT. The prompt used for the classification was: Providing these keywords, can you group them based on common ideas they convey in the context of serpentinization process study: list of 55 keywords.
From this point, we've been able to construct a graphical representation of keywords distribution as a function of depth.

This serves as a preliminary result to the model's analysis. Some keywords seems to be bound to the top or the bottom zone, indicating a clear cut between the very altered and the partially altered areas. 

Concerning veins, carbonate veins can only be found at the top of the cores, while serpentine veins are present all along the cores. Plus we notice indicators of magmatic intrusions and hydrothermal activities in the bottom section. This could explain the partial alteration observed even in the depths of the core.

Oxidation and alteration section doesn't tell much about the core, it only indicates oxidation only occurs at the top of the borehole, which is linked with an easier infiltration of solutions bearing oxygen.

The structural features section indicates information about the formation and type of other cracks, that are mostly irrelevant for serpentinization study. However, it is worth mentioning the "Irregular" keyword, which may have been employed by geologists for describing all sort of networks, is mainly present at the top of the core.

The rock type section shows sharp cuts between the top and the bottom section. Of course, dunite and harzburgite repartition respects the lithological description of the borehole. But other minerals characteristics of serpentinization reaction can be found: magnetite along the top section, and pyroxenites along the bottom section. Gabbro and microgabbro are present throughout the entire borehole and don't seem to be linked to the serpentinization process.

Both mineralogy and physical characteristics sections don't provide much more information regarding depth dependence, as the composing keywords are present through the entire core.

This first analysis establish a correlation between some of the keywords and depth, and foresee the results we should expect with the machine learning model analysis. By highlighting the relative importance of these keywords and the way they affect the prediction of alteration degree, the model will confirm or invalidate the most deciding keywords presented in this graph, and thus evaluate the coherence of the data issued from keywords with the rest of the dataset.

Here is the code used for plotting such a graph:
```
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl

df = pd.read_excel("D:\SerpRateAI\Datasets\Dataset_BA1B.xlsx")

keywords=df.columns[49:]
K=[]
for i in keywords:
    K.append(i)

fname = "D:\SerpRateAI\Datasets\Dataset_BA1B_Final.xlsx"
wb = openpyxl.load_workbook(fname)
sheet = wb.get_sheet_by_name('Sheet1')

L=[]
for rowOfCellObjects in sheet['G2':'G656']:
    for cellObj in rowOfCellObjects:
        L.append(cellObj.value)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

data = df[K].to_numpy()
row_labels = L
col_labels = K

groups = [
    ['Veins', 'Serpentine vein', 'Carbonate veins', 'White veins', 'Green veins',
     'Blue patches', 'Magmatic veins', 'Dark green', 'Magmatic intrusions',
     'Hydrothermal', 'Offsets', 'Rodingite'],
    ['Oxidation', 'Black serpentinization', 'Alteration', 'Alteration halo',
     'Altered gabbro', 'Altered', 'Pyroxenite'],
    ['Network', 'Coalescence', 'Dyke', 'Shearing', 'Crack',  'Open cracks', 'Open crack', 'Irregular', 'Subvertical',
     'Subhorizontal', 'Lineation', 'Thickness', 'Offset', 'Fracture',
     'Sheared', 'Striations', 'Branching', 'Slickensides'],
    ['Dunite', 'Gabbro', 'Microgabbro', 'Harzburgite', 'Pxenites', 'Dunitic zone','Magnetite'],
    ['Plagioclase', 'Microbio sample', 'Bulk serp', 'Bulk'],
    ['Fine grained', 'Waxy green', 'Waxy', 'Wavy']
]

colors = ['red', 'blue', 'green', 'purple', 'orange', 'grey']


sorted_cols = []
group_indices = []
for i, group in enumerate(groups):
    for col in col_labels:
        if col in group:
            sorted_cols.append(col)
            group_indices.append(i)

sorted_data = data[:, [col_labels.index(col) for col in sorted_cols]]

plt.pcolormesh(sorted_data, cmap='Purples')

y_ticks = np.arange(0, 401.7, 100)
y_tick_positions = np.linspace(0, len(row_labels), len(y_ticks))
plt.yticks(y_tick_positions, y_ticks)

plt.xticks(np.arange(len(sorted_cols)) + 0.5, sorted_cols, rotation=45, ha="right", rotation_mode="anchor", fontsize=8)
plt.subplots_adjust(bottom=0.1)

for tick_label in plt.gca().get_xticklabels():
    label = tick_label.get_text()
    for i, group in enumerate(groups):
        if label in group:
            tick_label.set_color(colors[i])

plt.gca().invert_yaxis()

plt.xlabel("Columns")

plt.show()

```

## *ROC curves and R2 score table*

![image](https://github.com/SerpRateAI/core-photo-analysis/assets/94477034/7664d206-96a5-414e-a916-afb029aef2d9)


This graph was made by plotting the ROC curve for different subsets of features depending on their origin (physical, textual or image-extracted data), indicated in the legend. ROC curves compute True positive and False positive detection to provide an insight at a model’s performance. The more expanded the area under the ROC curve is, the better the model is. The point is to compare the performance of the model when it is given only data treated by AI tools and data issued from physical measurements

With all of the features excluding depth, our model function very well and reach an area under the ROC curve (ROC AUC) of 0.9881. 

If the physical data are cut out, and so only images and textual data that has been treated using artificial intelligence (Ilastik and ChatGPT) remain, the model shows an ROC AUC of 0.9547, and is still successful. 

It's worth mentioning using only physical measurements results in an ROC AUC of 0.94077. This means we got to recreate a comparable results with AI tools than the one obtained by physical measurements, and it justifies an AI-oriented approach for the treatment of geological data.

Using only textual data results in an ROC AUC of 0.9498; this subset of data is sufficient on its own and shows satisfying results. The extraction of keywords by ChatGPT proves to be powerful, and can be slightly improved by the addition of physical or images data.

Finally, if only the images-extracted data remain, i.e. the percentage of fractures and n-points correlation functions, the ROC AUC falls at 0.8118. This value is lower compared with other subsets, but is still acceptable given only 13 features are available. This result may be improved by a better segmentation or a better use of n-point correlation functions' curves, but it already shows promising result for a detection based only on fracture-related data. 

To try and build a better machine learning model out of our dataset, we also got interested in the use of a regressive XGBoost model. This model should then predict the value of bulk density for each sample. We ran this model with the same multiple subsets of data, and for each calculated the R2 score (an estimation on how accurately the model approach real points, the maximum value for a perfect detection being 1) of the model. The table computes those scores. Regressive model seems way less performant than the classification,  which is due to the additional complexity of the task. The data issued from AI treatment can't compete with physical data is this model: the corresponding features could be better exploited, by a better segmentation labelling or a more clever integration of connectivity estimation.


