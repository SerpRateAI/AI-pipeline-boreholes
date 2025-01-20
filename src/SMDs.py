import numpy as np
from numba import jit
from tqdm import tqdm
from typing import Dict, List
import os
import shutil
import subprocess
from glob import glob


@jit 
# --> It is preferred to use numba here for a speed-up, if installed!!
def two_point_correlation(im, dim, var=0):
    """
    This method computes the two point correlation,
    also known as second order moment,
    for a segmented binary image in the three principal directions.
    
    dim = 0: x-direction
    dim = 1: y-direction
    dim = 2: z-direction
    
    var should be set to the pixel value of the pore-space. (Default 0)
    
    The input image im is expected to be three-dimensional.
    """
    if dim == 0: #x_direction
        dim_1 = im.shape[1] #y-axis
        dim_2 = im.shape[0] #x-axis
    elif dim == 1: #y-direction
        dim_1 = im.shape[0] #x-axis
        dim_2 = im.shape[1] #z-axis
        
    two_point = np.zeros((dim_1, dim_2))
    for n1 in range(dim_1):
        for r in range(dim_2):
            lmax = dim_2-r
            for a in range(lmax):
                if dim == 0:
                    pixel1 = im[a, n1]
                    pixel2 = im[a+r, n1]
                elif dim == 1:
                    pixel1 = im[n1, a]
                    pixel2 = im[n1, a+r]

                if pixel1 == var and pixel2 == var:
                    two_point[n1, r] += 1
            two_point[n1, r] = two_point[n1, r]/(float(lmax))
    return two_point

def calculate_smd_list(images):
    """This function calculate s2 for a stack of images and return a list of correlations s2 and scaled autocovariance
    The list contains correaltions of all the slices"""
    fn_list = []
    s2_list = []
#     Nr_list = []
    if len(images.shape) == 3: # if you read slices in a one stack of numpy array
        
        for i in tqdm(range(images.shape[0])):
            two_pt_dim0 = two_point_correlation(images[i], dim = 0, var = 1) #S2 in x-direction
            two_pt_dim1 = two_point_correlation(images[i], dim = 1, var = 1) #S2 in y-direction

            #Take average of directions; use half linear size assuming equal dimension sizes
            Nr = two_pt_dim0.shape[0]//2

            S2_x = np.average(two_pt_dim1, axis=0)[:Nr]
            S2_y = np.average(two_pt_dim0, axis=0)[:Nr]
            S2_average = ((S2_x + S2_y)/2)[:Nr]

            s2_list.append(S2_average)

            # autoscaled covriance---------------------------------------
            f_average = (S2_average - S2_average[0]**2)/S2_average[0]/(1 - S2_average[0])
            fn_list.append(f_average)
            
             # N(L) number of different size lines
#             Nr_list.append(Nr)
        return s2_list, fn_list
    
    elif len(images.shape) == 2: # in case we only have a 2D image, don't need to return a list 

        two_pt_dim0 = two_point_correlation(images, dim = 0, var = 1) #S2 in x-direction
        two_pt_dim1 = two_point_correlation(images, dim = 1, var = 1) #S2 in y-direction

        #Take average of directions; use half linear size assuming equal dimension sizes
        Nr = two_pt_dim0.shape[0]//2

        S2_x = np.average(two_pt_dim1, axis=0)[:Nr]
        S2_y = np.average(two_pt_dim0, axis=0)[:Nr]
        S2_average = ((S2_x + S2_y)/2)[:Nr]

        s2_list.append(S2_average)

        # autoscaled covriance---------------------------------------
        f_average = (S2_average - S2_average[0]**2)/S2_average[0]/(1 - S2_average[0])
        fn_list.append(f_average)
        
        # N(L) number of different size lines
#         Nr_list.append(Nr)
        return S2_average, f_average

class Microstructure:
    # init method
    def __init__(self, dims, ns):
        

        self.dims = dims  # number of dimensions (2 or 3)
        self.ns = ns  # number of samples per dimensions - all dims must have equal number of samples

        if dims == 2:  # 2D sample
            self.structure = np.ones((ns, ns))  # stores two-phase (binary) sampled microstructure
            self.sourceimage = np.ones((ns, ns))  # stores source image for self.structure
        elif dims == 3:  # 3D sample
            self.structure = np.ones((ns, ns, ns))
            self.sourceimage = np.ones((ns, ns, ns))
        else:  # only 2D or 3D are allowed
            raise Exception('Number of dimensions must be 2 or 3.')

    # Miscellanous class vars
    name = 'default_sample'  # sample name

    # dims = int(2)
    # ns = int(251)
    # structure = np.ones((ns, ns))
    # sourceimage = np.ones((ns, ns))

    def description(self):
        if self.dims == 2:
            desc_str = "Sample %s is a %dD microstructure with %d x %d pixels." % (
                self.name, self.dims, self.ns, self.ns)
        else:
            desc_str = "Sample %s is a %dD microstructure with %d x %d x %d pixels." % (
                self.name, self.dims, self.ns, self.ns, self.ns)
        return desc_str

    def volumefraction(self):
        self.ninclusion = 0  # number of inclusion/black pixels, assume black pixels have 0 value
        structure = self.structure
        # count inclusion pixels
        if self.dims == 2:
            for ix in range(self.ns):
                for iy in range(self.ns):
                    if structure[ix, iy] == 1: # pore =1, solid = 0
                        self.ninclusion += 1
        elif self.dims == 3:
            for ix in range(self.ns):
                for iy in range(self.ns):
                    for iz in range(self.ns):
                        if structure[ix, iy, iz] == 1:
                            self.ninclusion += 1
        # final volume fraction
        self.volfracvalue = self.ninclusion / (self.ns ** (self.dims))

    def list_inclusion_indeces(self):
        # set up
        self.volumefraction()
        inclist = np.zeros((self.dims, self.ninclusion), dtype=int)  # initiate array
        structure = self.structure  # get structure
        # get inclusion indeces
        iincl = 0
        if self.dims == 2:
            for ix in range(self.ns):
                for iy in range(self.ns):
                    if structure[ix, iy] == 1: #pore =1, solid=0
                        inclist[0, iincl] = ix
                        inclist[1, iincl] = iy
                        iincl += 1
        elif self.dims == 3:
            for ix in range(self.ns):
                for iy in range(self.ns):
                    for iz in range(self.ns):
                        if structure[ix, iy, iz] == 1:
                            inclist[0, iincl] = ix
                            inclist[1, iincl] = iy
                            inclist[2, iincl] = iz
                            iincl += 1
        # output
        self.inclusion_index_list = inclist

    def write_Mconfig(self, file_path=''):
        # check if inclusion list is there
        try:
            inclist = self.inclusion_index_list
        except ValueError:  # if not call listing method
            self.list_inclusion_indeces()
            inclist = self.inclusion_index_list

        # open files
        mconfig = 'Mconfig'
        extension = '.txt'
        myname = self.name
        filename = file_path + myname + '_' + mconfig + extension
        # filename = os.path.join(file_path, myname + '_' + mconfig + extension)

        file = open(filename, 'w')
        # print dims
        # print('%s' % self.ns, file=file)
        # print number of inclusion pixels
        print('%s' % self.ninclusion, file=file)
        # print inclusion index list
        for iincl in range(self.ninclusion):
            print('%s   %s' % (inclist[0, iincl], inclist[1, iincl]), file=file)
        # close file
        file.close()

    # calculating 2-point Correlation Function (S2)
    def estimate_twopoint_correlation(self, file_path='', cppcode_path='', runtime_path=os.getcwd(), verbose=False):
        # file info
        mconfig = 'Mconfig'
        extension = '.txt'
        myname = self.name
        currdir = os.getcwd()

        if runtime_path != currdir:
            os.chdir(runtime_path)

        file1name = runtime_path + mconfig + extension
        file2name = file_path + myname + '_' + mconfig + extension
        codepath = cppcode_path
        outputpath = file_path

        # check if Mconfig files exist
        if os.path.isfile(file2name):
#             print('%s_Mconfig.txt file exists in: %s' % (self.name, file_path))
#             print('Mconfig.txt file replaced in current directory')
#             print('These are assumed to be the same: S2 estimation will proceed.')
            # Copy self.name_Mconfig.txt into Mconfig.txt
            shutil.copyfile(file2name, file1name)
        else:
#             print('Writing %s_Mconfig.txt file in: %s' % (self.name, file_path))
#             print('Writing Mconfig.txt file for sample %s in current directory' % (self.name))
            self.write_Mconfig(file_path=outputpath)
            # Copy self.name_Mconfig.txt into Mconfig.txt
            shutil.copyfile(file2name, file1name)

        # check if compiled C++ code is there
        cpp_executable = cppcode_path + 'L-S2_sample.2D'
        if os.path.isfile(cpp_executable):
            pass
        else:
            raise Exception('Executable L-S2_sample.2D not in: %s' % cppcode_path)

        # run C++ code
        cpp_output = subprocess.run(cpp_executable, capture_output=True)
        if verbose:
            print(cpp_output)

        # load output from file into class attribute
        outputS2_file = runtime_path + 'TS2.txt'
        self.twopoint_corrfunc = np.loadtxt(outputS2_file)

        # return to current directory when done
        os.chdir(currdir)

    # calculating n-Polytope functions
    def estimate_npolytope_functions(self, file_path='', cppcode_path='', runtime_path='', verbose=False):
        # file info
        mconfig = 'Mconfig'
        extension = '.txt'
        myname = self.name
        currdir = os.getcwd()

        if runtime_path != currdir:
            os.chdir(runtime_path)

        file1name = runtime_path + mconfig + extension
        file2name = file_path + myname + '_' + mconfig + extension
        codepath = cppcode_path
        outputpath = file_path

        # check if Mconfig files exist
        if os.path.isfile(file2name):
#             print('%s_Mconfig.txt file exists in: %s' % (self.name, file_path))
#             print('Mconfig.txt file replaced in current directory')
#             print('These are assumed to be the same: Pn estimation will proceed.')
            # Copy self.name_Mconfig.txt into Mconfig.txt
            shutil.copyfile(file2name, file1name)
        else:
#             print('Writing %s_Mconfig.txt file in: %s' % (self.name, file_path))
#             print('Writing Mconfig.txt file for sample %s in current directory' % (self.name))
            self.write_Mconfig(file_path=outputpath)
            # Copy self.name_Mconfig.txt into Mconfig.txt
            shutil.copyfile(file2name, file1name)

        # check if compiled C++ code is there
        cpp_executable = cppcode_path + '/Sample_Pn_UU'
        if os.path.isfile(cpp_executable):
            pass
        else:
            raise Exception('Executable Sample_Pn_UU not in: %s' % cppcode_path)

        # run C++ code
        cpp_output = subprocess.run(cpp_executable, capture_output=True)
        if verbose:
            print(cpp_output)

        # load output from files into class attributes
        # S2
        outputS2_file = runtime_path + 'sobjS2.txt'
        self.polytope_S2 = np.loadtxt(outputS2_file)
        # L
        outputL_file = runtime_path + 'sobjL.txt'
        self.polytope_L = np.loadtxt(outputL_file)
        # P3V
        outputP3V_file = runtime_path + 'SobjTriV.txt'
        self.polytope_P3V = np.loadtxt(outputP3V_file)
        # P3H
        outputP3H_file = runtime_path + 'SobjTriH.txt'
        self.polytope_P3H = np.loadtxt(outputP3H_file)
        # P4
        outputP4_file = runtime_path + 'SobjSQF.txt'
        self.polytope_P4 = np.loadtxt(outputP4_file)
        # P6V
        outputP6V_file = runtime_path + 'SobjHesaVer.txt'
        self.polytope_P6V = np.loadtxt(outputP6V_file)
        # P8
        #outputP8_file = runtime_path + 'SobjOctagon.txt'
        #self.polytope_P8 = np.loadtxt(outputP8_file)

        # return to current directory when done
        os.chdir(currdir)

    # scaled autocovariance from S2
    def calculate_scaled_autocovariance(self):

        try:  # check for S2 from polytope sampling
            S2 = self.polytope_S2[:, 1]
            pass
        except ValueError:
            raise Exception("No previous S2 exists: first generate S2.")

        # then calculate f(r):
        phi1 = self.volfracvalue   # black phase volume fraction
        phi2 = 1.0 - phi1          # white phase volume fraction
        Xi_of_r = S2 - phi1**2
        f_of_r = Xi_of_r / (phi1 * phi2)
        self.scal_autocov = np.zeros(self.polytope_S2.shape)
        self.scal_autocov[:, 1] = f_of_r
        self.scal_autocov[:, 0] = self.polytope_S2[:, 0]

    # scaled correlations from polytopes
    def calculate_polytope_fn(self):

        try:
            Pn = self.polytope_P3V[:, 1]
        except ValueError:
            raise Exception("Pn functions not found.")

        # P3V
        Pn = self.polytope_P3V[:, 1]
        phi = Pn[0]
        if Pn[-1] != 0.0:
            phi_n = Pn[-1]
        else:
            phi_n = Pn[-2]
        fn = (Pn - phi_n) / (phi - phi_n)
        self.polyfn_P3V = np.zeros(self.polytope_P3V.shape)
        self.polyfn_P3V[:, 1] = fn
        self.polyfn_P3V[:, 0] = self.polytope_P3V[:, 0]

        # P3H
        Pn = self.polytope_P3H[:, 1]
        phi = Pn[0]
        if Pn[-1] != 0.0:
            phi_n = Pn[-1]
        else:
            phi_n = Pn[-2]
        fn = (Pn - phi_n) / (phi - phi_n)
        self.polyfn_P3H = np.zeros(self.polytope_P3H.shape)
        self.polyfn_P3H[:, 1] = fn
        self.polyfn_P3H[:, 0] = self.polytope_P3H[:, 0]

        # P4
        Pn = self.polytope_P4[:, 1]
        phi = Pn[0]
        if Pn[-1] != 0.0:
            phi_n = Pn[-1]
        else:
            phi_n = Pn[-2]
        fn = (Pn - phi_n) / (phi - phi_n)
        self.polyfn_P4 = np.zeros(self.polytope_P4.shape)
        self.polyfn_P4[:, 1] = fn
        self.polyfn_P4[:, 0] = self.polytope_P4[:, 0]

        # P6V
        Pn = self.polytope_P6V[:, 1]
        phi = Pn[0]
        if Pn[-1] != 0.0:
            phi_n = Pn[-1]
        else:
            phi_n = Pn[-2]
        fn = (Pn - phi_n) / (phi - phi_n)
        self.polyfn_P6V = np.zeros(self.polytope_P6V.shape)
        self.polyfn_P6V[:, 1] = fn
        self.polyfn_P6V[:, 0] = self.polytope_P6V[:, 0]


def twoDCTimage2structure_mod(binary_image, par={'name': 'microstructure_from_image', 'begx': 10, 'begy': 10, 'nsamp': 1001, 'edge_buffer': 20,
                                            'thresholding_method': 'otsu', 'thresholding_weight': 1.0, 'nbins': 256,
                                            'make_figs': False, 'fig_res': 400, 'fig_path': ''}):

    #
    # begin by reading in image and check if ndarray class
    if type(binary_image) is np.ndarray:
        pass
    else:
        raise Exception('The input image must be of the numpy.ndarray class.')

    # check dimensions, argument consistency, etc.
    im_shape = binary_image.shape  # get array shape
    im_dims = len(im_shape)  # number of dimensions
    if im_dims != 2:  # dimensions must be 2
        raise Exception('input image must be 2D.')

    output_microstructure = Microstructure(im_dims, par['nsamp'])

    img_binary =binary_image

    output_microstructure.structure = img_binary
    output_microstructure.name = par['name']


    return output_microstructure


def calculate_polytopes(images, par, outputPn, cpathPn, runtimePn, polytope= 's2'):
    
    """this functions calculates polytopes for each image in batch and returns a dataframe with average polytope values.
     it also removes the **Mconfig.txt files in the runtime/output folder.
     we need to delete these files, otherwise it copies the results of previous implementation of the function.
    Inputs:
    images: real or fake batch of images:numpy array (slice, height, width)
    polytope: each of these polytopes can be calculated:
    s2: two-point correlation
    fn: autoscaled s2
    p3h: horizontal triangle
    p3v: vertical triangle
    p4: square
    p6: 
    L: lineal path
    
    Returns:
    1) dataframe containing polytope values
    2) the scaled version of dataframe"""
    
    if len(images.shape) == 3:
        
        
        poly_list = []
        fn_list = [] #scaled version

        image_number = 1
        for i in tqdm(range(images.shape[0])):
            #convert images in each batch into microstructure
            par['name']= f'batch_{image_number}'
            image_number += 1
            img_micr = twoDCTimage2structure_mod(images[i], par)
            img_micr.volumefraction()
            img_micr.list_inclusion_indeces()
            img_micr.estimate_npolytope_functions(file_path=outputPn, cppcode_path=cpathPn, runtime_path=runtimePn,verbose=False)

            img_micr.calculate_scaled_autocovariance()
            img_micr.calculate_polytope_fn()

            if polytope == 's2':
                poly_list.append(img_micr.polytope_S2)
                fn_list.append(img_micr.scal_autocov)
                
            elif polytope == 'p3h':
                poly_list.append(img_micr.polytope_P3H)
                fn_list.append(img_micr.polyfn_P3H)

            elif polytope == 'p3v':
                poly_list.append(img_micr.polytope_P3V)
                fn_list.append(img_micr.polyfn_P3V)

            elif polytope == 'p4':
                poly_list.append(img_micr.polytope_P4)
                fn_list.append(img_micr.polyfn_P4)

            elif polytope == 'p6':
                poly_list.append(img_micr.polytope_P6V)
                fn_list.append(img_micr.polyfn_P6V)
            elif polytope ==  'L':
                poly_list.append(img_micr.polytope_L)
                fn_list.append(img_micr.scal_autocov)
            else:
                raise Exception('Polytope function name is not correct. use one of the s2, p3h, p3v, p4, p6, or L')
        for filename in glob(outputPn + '/batch*'):
            os.remove(filename)         
        return poly_list, fn_list
    
    
    elif len(images.shape) == 2:
        image_number = 1
        
        par['name']= f'batch_{image_number}'
        image_number += 1
        img_micr = twoDCTimage2structure_mod(images, par)
        img_micr.volumefraction()
        img_micr.list_inclusion_indeces()
        img_micr.estimate_npolytope_functions(file_path=outputPn, cppcode_path=cpathPn, runtime_path=runtimePn,verbose=False)

        img_micr.calculate_scaled_autocovariance()
        img_micr.calculate_polytope_fn()
        
        for filename in glob(outputPn + '/batch*'):
            os.remove(filename) 

        if polytope == 's2':
            return img_micr.polytope_S2, img_micr.scal_autocov

        elif polytope == 'p3h':
            return img_micr.polytope_P3H, img_micr.polyfn_P3H

        elif polytope == 'p3v':
            return img_micr.polytope_P3V, img_micr.polyfn_P3V

        elif polytope == 'p4':
            return img_micr.polytope_P4, img_micr.polyfn_P4

        elif polytope == 'p6':
            return img_micr.polytope_P6V, img_micr.polyfn_P6V
        
        elif polytope ==  'L':
            
            return img_micr.polytope_L, img_micr.scal_autocov
        else:
            raise Exception('Polytope function name is not correct. use one of the s2, p3h, p3v, p4,  p6, or L')
            
    for filename in glob(outputPn + '/batch*'):
            os.remove(filename) 


###-------Omega
def omega_n(polytope:List[np.ndarray],
            delta_time:tuple =None):
    """delta_time: tuple showing the first and last time step. e.g., (0,10)--> t0, t10"""
    polytope =np.nan_to_num(polytope) # Convert Nan values to 0
    
    if not delta_time:
        delta_time = list(range(0, len(polytope)))
    else:
        delta_time = list(range(delta_time[0], delta_time[1]))
    
    # N(L)--> number of different sized polytopes which will be number of r??
    # for example if image size = 512, we have 256 rs--> N(L) = 256
    # the function for calculating s2 is different than higher-order functions.
     # s2 input is a list of length= number of timesteps
    # each s2 in the list is a 1D vector of s2 values with length of r (Nl)
    omega_list = []
    if polytope[-1].ndim ==1:
        N_L= 1/ len(polytope[-1])
        for time in delta_time:
            if type(polytope[time]) == int and polytope[time] == 0:
                omega = 0
            else:
                omega =np.linalg.norm(polytope[time]-polytope[0], ord =1) # L1_norm
            omega_t = N_L* omega
            omega_list.append(omega_t)
        
    elif polytope[0].ndim == 2:
        N_L = 1/len(polytope[0][:, 0])
        
        for time in delta_time:
            omega =np.linalg.norm(polytope[time][:, 1]-polytope[0][:, 1], ord =1) # L1_norm
            omega_t = N_L* omega
            omega_list.append(omega_t)

    return omega_list