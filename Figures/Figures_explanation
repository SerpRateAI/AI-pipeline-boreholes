# **Explanation on construction and interpretation of figure**

## *Physical data graphs per depth*

The first essential piece of data to acquire is the degree of fracturing in the core at any given depth, enabling the establishment of a correlation between depth and the amount of fractures. The previous application of a connected component analysis permitted a straightforward calculation of the fractures total area using the skimage.measure module, which led to the desired percentage of fractures once divided by the total area of the image.

Calculation of the percentage of fractures have been made for three different takes of the segmentation 3: the raw segmentation, the segmentation with area filter, and the segmentation with eccentricity filter.  In the end, the variations in filters used have negligible impact on the results, as the curves share similar trends with a translation shift. Thus only a rolling mean of these three takes have been studied.

When compared with the lithological data from the core report, the percentage graph presents some coherent results. 
Throughout the top section mainly composed of dunite (0-160 meters), water infiltrated easily, causing carbonation and serpentinization reaction. A moderate amount of fractures is detected, from 3\% at the very top to 6\% near the transition area. A peak in fractures is detected near the transition zone between dunite and harzburgite rocks (160-180 meters), with up to 10\% of the image fractured; it can be explained by the shearing accompanying the change in minerals, along with reaction of serpentinization. The aqueous solution didn't infiltrate the bottom harzburgite section (180-400 meters) because of its depth, thus the fractures observed are less numerous (averaging 3\%), and probably not all caused by serpentinization or carbonation.

The adjacent graphs were plotted by extrapolating missing data from the physical measurements, and arranging these data by depth. They address possible correlation between those variables: features as cell abundance or magnetic susceptibility are closely related to depth changes, which can be explained by the variation in mineral composition along the borehole, bringing different properties. An interesting observation is the non apparent connection of data such as bulk density with depth; however, it is proven useful for the alteration prediction by the classification model. This outlines the classification relies on multiple features, and doesn't only try to predict depth.

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
