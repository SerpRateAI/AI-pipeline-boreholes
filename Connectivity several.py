from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
import matplotlib.patches as patches
from skimage import exposure
import os
from os import listdir
import matplotlib
matplotlib.use('TkAgg')
# matplotlib.use('Qt5Agg')
# matplotlib.use('MACOSX')
import matplotlib.pyplot as plt
import pandas as pd

# import the uumatsci_utils.py library
import uumatsci_utils as uumat
import numpy as np

sumPnS2_list=[]
sumPnL_list=[]
sumPnP3H_list=[]
sumPnP3V_list=[]
sumPnP4_list=[]
sumPnP6V_list=[]

sumFnS2_list=[]
sumFnL_list=[]
sumFnP3H_list=[]
sumFnP3V_list=[]
sumFnP4_list=[]
sumFnP6V_list=[]


rows = 2
cols = 6
figsize = (16, 10)

fig, axes = plt.subplots(rows, cols, sharey='row', figsize=figsize, constrained_layout=True)
axes[0,0].set_title('Pn S2')
axes[0,0].set_ylabel('Pn')
axes[0,0].set_xlabel('r (pixels)')

axes[0,1].set_title('Pn L')
axes[0,1].set_ylabel('Pn')
axes[0,1].set_xlabel('r (pixels)')

axes[0,2].set_title('Pn P3V')
axes[0,2].set_ylabel('Pn')
axes[0,2].set_xlabel('r (pixels)')

axes[0,3].set_title('Pn P3H')
axes[0,3].set_ylabel('Pn')
axes[0,3].set_xlabel('r (pixels)')

axes[0,4].set_title('Pn P4')
axes[0,4].set_ylabel('Pn')
axes[0,4].set_xlabel('r (pixels)')

axes[0,5].set_title('Pn P6V')
axes[0,5].set_ylabel('Pn')
axes[0,5].set_xlabel('r (pixels)')

axes[1,0].set_title('Fn S2')
axes[1,0].set_ylabel('Fn')
axes[1,0].set_xlabel('r (pixels)')

axes[1,1].set_title('Fn L')
axes[1,1].set_ylabel('Fn')
axes[1,1].set_xlabel('r (pixels)')

axes[1,2].set_title('Fn P3V')
axes[1,2].set_ylabel('Fn')
axes[1,2].set_xlabel('r (pixels)')

axes[1,3].set_title('Fn P3H')
axes[1,3].set_ylabel('Fn')
axes[1,3].set_xlabel('r (pixels)')

axes[1,4].set_title('Fn P4')
axes[1,4].set_ylabel('Fn')
axes[1,4].set_xlabel('r (pixels)')

axes[1,5].set_title('Fn P6V')
axes[1,5].set_ylabel('Fn')
axes[1,5].set_xlabel('r (pixels)')

'''figPnS2, axesPnS2 = plt.subplots(rows, cols, sharey=True, figsize=figsize, constrained_layout=True)
axesPnS2.set_title('Pn S2')
axesPnS2.set_ylabel('Pn')
axesPnS2.set_xlabel('r (pixels)')

figPnL, axesPnL = plt.subplots(rows, cols, sharey=True, figsize=figsize, constrained_layout=True)
axesPnL.set_title('Pn L')
axesPnL.set_ylabel('Pn')
axesPnL.set_xlabel('r (pixels)')

figPnP3V, axesPnP3V = plt.subplots(rows, cols, sharey=True, figsize=figsize, constrained_layout=True)
axesPnP3V.set_title('Pn P3V')
axesPnP3V.set_ylabel('Pn')
axesPnP3V.set_xlabel('r (pixels)')

figPnP3H, axesPnP3H = plt.subplots(rows, cols, sharey=True, figsize=figsize, constrained_layout=True)
axesPnP3H.set_title('Pn P3H')
axesPnP3H.set_ylabel('Pn')
axesPnP3H.set_xlabel('r (pixels)')

figPnP4, axesPnP4 = plt.subplots(rows, cols, sharey=True, figsize=figsize, constrained_layout=True)
axesPnP4.set_title('Pn P4')
axesPnP4.set_ylabel('Pn')
axesPnP4.set_xlabel('r (pixels)')

figPnP6V, axesPnP6V = plt.subplots(rows, cols, sharey=True, figsize=figsize, constrained_layout=True)
axesPnP6V.set_title('Pn P6V')
axesPnP6V.set_ylabel('Pn')
axesPnP6V.set_xlabel('r (pixels)')

figFnS2, axesFnS2 = plt.subplots(rows, cols, sharey=True, figsize=figsize, constrained_layout=True)
axesFnS2.set_title('Fn S2')
axesFnS2.set_ylabel('Fn')
axesFnS2.set_xlabel('r (pixels)')

figFnL, axesFnL = plt.subplots(rows, cols, sharey=True, figsize=figsize, constrained_layout=True)
axesFnL.set_title('Fn L')
axesFnL.set_ylabel('Fn')
axesFnL.set_xlabel('r (pixels)')

figFnP3V, axesFnP3V = plt.subplots(rows, cols, sharey=True, figsize=figsize, constrained_layout=True)
axesFnP3V.set_title('Fn P3V')
axesFnP3V.set_ylabel('Fn')
axesFnP3V.set_xlabel('r (pixels)')

figFnP3H, axesFnP3H = plt.subplots(rows, cols, sharey=True, figsize=figsize, constrained_layout=True)
axesFnP3H.set_title('Fn P3H')
axesFnP3H.set_ylabel('Fn')
axesFnP3H.set_xlabel('r (pixels)')

figFnP4, axesFnP4 = plt.subplots(rows, cols, sharey=True, figsize=figsize, constrained_layout=True)
axesFnP4.set_title('Fn P4')
axesFnP4.set_ylabel('Fn')
axesFnP4.set_xlabel('r (pixels)')

figFnP6V, axesFnP6V = plt.subplots(rows, cols, sharey=True, figsize=figsize, constrained_layout=True)
axesFnP6V.set_title('Fn P6V')
axesFnP6V.set_ylabel('Pn')
axesFnP6V.set_xlabel('r (pixels)')'''


for file in listdir("/Camera"):
    image_number = file[:-4]
    print(image_number)
    number = int(image_number[12:-4])
    print(number)
    a = 13 + len(str(number))
    number2 = int(image_number[a:-2])
    print(number2)

#for i in [10,25,34]:#,52,65,79,91,104,115,134]:
    #number = i
    #number2 =3
    path = 'D:/SerpRateAI/Results'
    #image_number='CS_5057_5_B_'+str(i)+'_3_1'
    image_file = path + '/' + image_number +'/' + image_number +'_Simple Segmentation_3.tif'


    # %% alternative image read method
    img_ct = plt.imread(image_file)
    print(img_ct.shape)

    height=img_ct.shape[0]
    width=img_ct.shape[1]
    print(width, height)
    if width >= (2*height//3):
        y_start = 10
    else:
        y_start=height//3
    x_start=10
    x_size=min(width, height)-20
    y_size=x_size-10

    # this 'par' is a dictionary with the arguments passed to the image-to-structure method
    par={'name':image_number,'begx': y_start, 'begy': x_start, 'nsampx': x_size, 'nsampy':y_size, 'edge_buffer': 10,
        'equalisation': True, 'equal_method': 'adaptive', 'stretch_percentile': 2,
        'clip_limit': 0.03, 'tvdnoise': True, 'tv_weight': 0.15, 'tv_eps': 2e-04,
        'median_filter': False, 'median_filter_length': 3,
        'thresholding_method': 'otsu', 'thresholding_weight': 0.85, 'nbins': 256,
        'make_figs': False, 'fig_res': 400, 'fig_path':'D:/SerpRateAI/'}


    # test function
    imct_microstructure = uumat.twoDCTimage2structure(img_ct, par)
    #print(type(imct_microstructure))
    imm = imct_microstructure.sourceimage
    #print(imm.shape)
    #img_adaptive = exposure.equalize_adapthist(imm, clip_limit=par['clip_limit'])

    # test volume fraction calculation
    imct_microstructure.volumefraction()
    imct_nincl = imct_microstructure.ninclusion
    imct_phi = imct_microstructure.volfracvalue
    print("Number of inclusions: %s" % imct_nincl)
    print("Volume fraction: %s" % imct_phi)

    # test listing inclusion indeces
    imct_microstructure.list_inclusion_indeces()
    imct_inclist = imct_microstructure.inclusion_index_list
    #print(imct_inclist.shape)
    #for j in range(10):
    #   print("%s  %s" % (imct_inclist[0, j], imct_inclist[1, j]))

    #plt.figure()
    #plt.imshow(imct_microstructure.structure, cmap=plt.cm.gray)

    # Set up to run C++ polytope codes
    # test writing Mconfig files
    if os.path.isfile('/Connectivity/PyMMat-master/runtime/Mconfig.txt'):
        os.remove('/Connectivity/PyMMat-master/runtime/Mconfig.txt')

    if os.path.isfile('D:/SerpRateAI/Connectivity/PyMMat-master/runtime/output/' + image_number +'_Mconfig.txt'):
        os.remove('D:/SerpRateAI/Connectivity/PyMMat-master/runtime/output/' + image_number +'_Mconfig.txt')


    cpathPn = 'D:/SerpRateAI/Connectivity/PyMMat-master/Cpp_source/Polytope/'
    runtimePn = 'D:/SerpRateAI/Connectivity/PyMMat-master/runtime/'
    outputPn = 'D:/SerpRateAI/Connectivity/PyMMat-master/runtime/output/'

    # test polytope estimations
    imct_microstructure.estimate_npolytope_functions(file_path=outputPn, cppcode_path=cpathPn, runtime_path=runtimePn, verbose=False)
    imct_PnS2 = imct_microstructure.polytope_S2
    #print(imct_PnS2.shape)
    #print(imct_PnS2[0:10,:])


    ## Calculate f and fn functions
    imct_microstructure.calculate_scaled_autocovariance()
    imct_microstructure.calculate_polytope_fn()

    # plot Pn
    #print(os.getcwd())
    '''axes[0, 0].plot(imct_microstructure.polytope_S2[0:50, 0], imct_microstructure.polytope_S2[0:50, 1], 'o', ls='-', ms=2, markevery=None, label=str(number)+'_'+str(number2))
    axes[0, 1].plot(imct_microstructure.polytope_L[0:50, 0], imct_microstructure.polytope_L[0:50, 1], 'o', ls='-', ms=2, markevery=None, label=str(number)+'_'+str(number2))
    axes[0, 2].plot(imct_microstructure.polytope_P3V[0:50:2, 0], imct_microstructure.polytope_P3V[0:50:2, 1], 'o', ls='-', ms=2, markevery=None, label=str(number)+'_'+str(number2))
    axes[0, 3].plot(imct_microstructure.polytope_P3H[0:50:2, 0], imct_microstructure.polytope_P3H[0:50:2, 1], 'o', ls='-', ms=2, markevery=None, label=str(number)+'_'+str(number2))
    axes[0, 4].plot(imct_microstructure.polytope_P4[0:50, 0], imct_microstructure.polytope_P4[0:50, 1], 'o', ls='-', ms=2, markevery=None, label=str(number)+'_'+str(number2))
    axes[0, 5].plot(imct_microstructure.polytope_P6V[0:50:2, 0], imct_microstructure.polytope_P6V[0:50:2, 1], 'o', ls='-', ms=2, markevery=None, label=str(number)+'_'+str(number2))

    axes[1, 0].plot(imct_microstructure.scal_autocov[0:50, 0], imct_microstructure.scal_autocov[0:50, 1], 'o', ls='-', ms=2, markevery=None, label=str(number)+'_'+str(number2))
    axes[1, 1].plot(imct_microstructure.polyfn_L[0:50, 0], imct_microstructure.polyfn_L[0:50, 1], 'o', ls='-', ms=2, markevery=None, label=str(number)+'_'+str(number2))
    axes[1, 2].plot(imct_microstructure.polyfn_P3V[0:50:2, 0], imct_microstructure.polyfn_P3V[0:50:2, 1], 'o', ls='-', ms=2, markevery=None, label=str(number)+'_'+str(number2))
    axes[1, 3].plot(imct_microstructure.polyfn_P3H[0:50:2, 0], imct_microstructure.polyfn_P3H[0:50:2, 1], 'o', ls='-', ms=2, markevery=None, label=str(number)+'_'+str(number2))
    axes[1, 4].plot(imct_microstructure.polyfn_P4[0:50, 0], imct_microstructure.polyfn_P4[0:50, 1], 'o', ls='-', ms=2, markevery=None, label=str(number)+'_'+str(number2))
    axes[1, 5].plot(imct_microstructure.polyfn_P6V[0:50:2, 0], imct_microstructure.polyfn_P6V[0:50:2, 1], 'o', ls='-', ms=2, markevery=None, label=str(number)+'_'+str(number2))
    '''

    print(imct_microstructure.polytope_S2[0:50, 0], imct_microstructure.polytope_S2[0:50, 1])
    print(imct_microstructure.polytope_S2[0:50, 1][0])

    sumPnS2=0
    sumPnL=0
    sumPnP3V=0
    sumPnP3H=0
    sumPnP4=0
    sumPnP6V=0

    sumFnS2 = 0
    sumFnL = 0
    sumFnP3V = 0
    sumFnP3H = 0
    sumFnP4 = 0
    sumFnP6V = 0

    for i in range(len(imct_microstructure.polytope_S2[0:50, 1])):
        sumPnS2+=imct_microstructure.polytope_S2[0:50, 1][i]
        sumPnL += imct_microstructure.polytope_L[0:50, 1][i]
        sumPnP3V += imct_microstructure.polytope_P3V[0:50, 1][i]
        sumPnP3H += imct_microstructure.polytope_P3H[0:50, 1][i]
        sumPnP4 += imct_microstructure.polytope_P4[0:50, 1][i]
        sumPnP6V += imct_microstructure.polytope_P6V[0:50, 1][i]

        sumFnS2 += imct_microstructure.scal_autocov[0:50, 1][i]
        sumFnL += imct_microstructure.polyfn_L[0:50, 1][i]
        sumFnP3V += imct_microstructure.polyfn_P3V[0:50, 1][i]
        sumFnP3H += imct_microstructure.polyfn_P3H[0:50, 1][i]
        sumFnP4 += imct_microstructure.polyfn_P4[0:50, 1][i]
        sumFnP6V += imct_microstructure.polyfn_P6V[0:50, 1][i]

    print(sumPnS2)

    sumPnS2_list.append((number,number2,sumPnS2))
    sumPnL_list.append((number,number2,sumPnL))
    sumPnP3H_list.append((number,number2,sumPnP3H))
    sumPnP3V_list.append((number,number2,sumPnP3V))
    sumPnP4_list.append((number,number2,sumPnP4))
    sumPnP6V_list.append((number,number2,sumPnP6V))

    sumFnS2_list.append((number, number2, sumFnS2))
    sumFnL_list.append((number, number2, sumFnL))
    sumFnP3H_list.append((number, number2, sumFnP3H))
    sumFnP3V_list.append((number, number2, sumFnP3V))
    sumFnP4_list.append((number, number2, sumFnP4))
    sumFnP6V_list.append((number, number2, sumFnP6V))

    '''
    axesPnS2.plot(imct_PnS2[0:50,0], imct_PnS2[0:50,1], 'o', ls='-', ms=4, markevery=None, label='S2')
    axesPnL.plot(imct_microstructure.polytope_L[0:50,0], imct_microstructure.polytope_L[0:50,1], 'o', ls='-', ms=4, markevery=None, label='L')
    axesPnP3V.plot(imct_microstructure.polytope_P3V[0:50:2,0], imct_microstructure.polytope_P3V[0:50:2,1], 'o', ls='-', ms=4, markevery=None, label='P3V')
    axesPnP3H.plot(imct_microstructure.polytope_P3H[0:50:2,0], imct_microstructure.polytope_P3H[0:50:2,1], 'o', ls='-', ms=4, markevery=None, label='P3H')
    axesPnP4.plot(imct_microstructure.polytope_P4[0:50,0], imct_microstructure.polytope_P4[0:50,1], 'o', ls='-', ms=4, markevery=None, label='P4')
    axesPnP6V.plot(imct_microstructure.polytope_P6V[0:50:2,0], imct_microstructure.polytope_P6V[0:50:2,1], 'o', ls='-', ms=4, markevery=None, label='P6V')

    axesFnS2.plot(imct_microstructure.scal_autocov[0:50,0], imct_microstructure.scal_autocov[0:50,1], 'o', ls='-', ms=4, markevery=None, label='S2')
    axesFnL.plot(imct_microstructure.polyfn_L[0:50,0], imct_microstructure.polyfn_L[0:50,1], 'o', ls='-', ms=4, markevery=None, label='L')
    axesFnP3V.plot(imct_microstructure.polyfn_P3V[0:50:2,0], imct_microstructure.polyfn_P3V[0:50:2,1], 'o', ls='-', ms=4, markevery=None, label='P3V')
    axesFnP3H.plot(imct_microstructure.polyfn_P3H[0:50:2,0], imct_microstructure.polyfn_P3H[0:50:2,1], 'o', ls='-', ms=4, markevery=None, label='P3H')
    axesFnP4.plot(imct_microstructure.polyfn_P4[0:50,0], imct_microstructure.polyfn_P4[0:50,1], 'o', ls='-', ms=4, markevery=None, label='P4')
    axesFnP6V.plot(imct_microstructure.polyfn_P6V[0:50:2,0], imct_microstructure.polyfn_P6V[0:50:2,1], 'o', ls='-', ms=4, markevery=None, label='P6V')
    '''

axes[0,0].grid(True)
axes[0,1].grid(True)
axes[0,2].grid(True)
axes[1,0].grid(True)
axes[1,1].grid(True)
axes[1,2].grid(True)
axes[0,3].grid(True)
axes[0,4].grid(True)
axes[0,5].grid(True)
axes[1,3].grid(True)
axes[1,4].grid(True)
axes[1,5].grid(True)

axes[0,0].legend()
axes[0,1].legend()
axes[0,2].legend()
axes[1,0].legend()
axes[1,1].legend()
axes[1,2].legend()
axes[0,3].legend()
axes[0,4].legend()
axes[0,5].legend()
axes[1,3].legend()
axes[1,4].legend()
axes[1,5].legend()

'''
axesPnL.grid(True)
axesPnL.legend()

axesPnP3V.grid(True)
axesPnP3V.legend()

axesPnP3H.grid(True)
axesPnP3H.legend()

axesPnP4.grid(True)
axesPnP4.legend()

axesPnP6V.grid(True)
axesPnP6V.legend()

axesFnS2.grid(True)
axesPnS2.legend()

axesFnL.grid(True)
axesFnL.legend()

axesFnP3V.grid(True)
axesFnP3V.legend()

axesFnP3H.grid(True)
axesFnP3H.legend()

axesFnP4.grid(True)
axesFnP4.legend()

axesFnP6V.grid(True)
axesFnP6V.legend()'''

Number_col=[x[0]for x in sumPnS2_list]
Number2_col=[x[1]for x in sumPnS2_list]

PnS2_col=[x[2]for x in sumPnS2_list]
PnL_col=[x[2]for x in sumPnL_list]
PnP3V_col=[x[2]for x in sumPnP3V_list]
PnP3H_col=[x[2]for x in sumPnP3H_list]
PnP4_col=[x[2]for x in sumPnP4_list]
PnP6V_col=[x[2]for x in sumPnP6V_list]

FnS2_col=[x[2]for x in sumFnS2_list]
FnL_col=[x[2]for x in sumFnL_list]
FnP3V_col=[x[2]for x in sumFnP3V_list]
FnP3H_col=[x[2]for x in sumFnP3H_list]
FnP4_col=[x[2]for x in sumFnP4_list]
FnP6V_col=[x[2]for x in sumFnP6V_list]

d = {'PnS2_sum': PnS2_col, 'PnL_sum': PnL_col, 'PnP3V_sum': PnP3V_col,
     'PnP3H_sum': PnP3H_col, 'PnP4_sum': PnP4_col, 'PnP6V_sum': PnP6V_col,
     'FnS2_sum': FnS2_col, 'FnL_sum': FnL_col, 'FnP3V_sum': FnP3V_col,
     'FnP3H_sum': FnP3H_col, 'FnP4_sum': FnP4_col, 'FnP6V_sum': FnP6V_col,
     'CORE': Number_col,'SECTION': Number2_col
     }
df = pd.DataFrame(data=d)
df.set_index(['CORE', 'SECTION'], inplace=True)
print(df)

df.to_excel("D:/SerpRateAI/Datasets/Connectivity Sum.xlsx")



plt.show()
plt.savefig('D:/SerpRateAI/test.png')

