# uumatsci_utils -- Utrecht University Material Science Utility Functions
# Author: Ivan Vasconcelos, i.vasconcelos@uu.nl
# Date: Feb 5, 2020
# Copyrights: Utrecht University

# %% import libs
import numpy as np
import sys
import os
import subprocess
import shutil
from PIL import Image

import matplotlib
# matplotlib.use('Qt5Agg')
# matplotlib.use('MACOSX')
import matplotlib.pyplot as plt


from skimage import data, filters
from skimage import exposure
from skimage.filters import try_all_threshold, threshold_otsu, threshold_li, threshold_minimum, threshold_isodata
from skimage.restoration import denoise_tv_chambolle
from skimage.filters.rank import entropy, mean_bilateral, median
from skimage.morphology import disk

# local libs
from plot_equalize import plot_img_and_hist

# define Microstructre class


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
                    if structure[ix, iy] == 1:
                        self.ninclusion += 1
        elif self.dims == 3:
            for ix in range(self.ns):
                for iy in range(self.ns):
                    for iz in range(self.ns):
                        if structure[ix, iy, iz] == 0:
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
                    if structure[ix, iy] == 1:
                        inclist[0, iincl] = ix
                        inclist[1, iincl] = iy
                        iincl += 1
        elif self.dims == 3:
            for ix in range(self.ns):
                for iy in range(self.ns):
                    for iz in range(self.ns):
                        if structure[ix, iy, iz] == 0:
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
            print('%s_Mconfig.txt file exists in: %s' % (self.name, file_path))
            print('Mconfig.txt file replaced in current directory')
            print('These are assumed to be the same: S2 estimation will proceed.')
            # Copy self.name_Mconfig.txt into Mconfig.txt
            shutil.copyfile(file2name, file1name)
        else:
            print('Writing %s_Mconfig.txt file in: %s' % (self.name, file_path))
            print('Writing Mconfig.txt file for sample %s in current directory' % (self.name))
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
    def estimate_npolytope_functions(self, file_path='', cppcode_path='', runtime_path=os.getcwd(), verbose=False):
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
            print('%s_Mconfig.txt file exists in: %s' % (self.name, file_path))
            print('Mconfig.txt file replaced in current directory')
            print('These are assumed to be the same: Pn estimation will proceed.')
            # Copy self.name_Mconfig.txt into Mconfig.txt
            shutil.copyfile(file2name, file1name)
        else:
            print('Writing %s_Mconfig.txt file in: %s' % (self.name, file_path))
            print('Writing Mconfig.txt file for sample %s in current directory' % (self.name))
            self.write_Mconfig(file_path=outputpath)
            # Copy self.name_Mconfig.txt into Mconfig.txt
            shutil.copyfile(file2name, file1name)

        # check if compiled C++ code is there
        cpp_executable = cppcode_path + 'Sample_Pn_UU'
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


def twoDCTimage2structure(input_image, par={'name': 'microstructure_from_image', 'begx': 10, 'begy': 10, 'nsamp': 251, 'edge_buffer': 10,
                                            'equalisation': True, 'equal_method': 'adaptive', 'stretch_percentile': 2,
                                            'clip_limit': 0.03, 'tvdnoise': True, 'tv_weight': 0.15, 'tv_eps': 2e-04,
                                            'median_filter': False, 'median_filter_length': 3,
                                            'thresholding_method': 'otsu', 'thresholding_weight': 1.0, 'nbins': 256,
                                            'make_figs': False, 'fig_res': 400, 'fig_path': ''}):

    #
    # begin by reading in image and check if ndarray class
    if type(input_image) is np.ndarray:
        pass
    else:
        raise Exception('The input image must be of the numpy.ndarray class.')

    # check dimensions, argument consistency, etc.
    im_shape = input_image.shape  # get array shape
    im_dims = len(im_shape)  # number of dimensions
    if im_dims != 2:  # dimensions must be 2
        raise Exception('input image must be 2D.')
    min_samp_num = par['nsamp'] + 2 * par['edge_buffer']  # minimum number of samples required
    if im_shape[0] < min_samp_num or im_shape[1] < min_samp_num:
        raise Exception('input image has too few samples for chosen nsamp and edge_buffer values.')

    # initiate output, window input for processing
    output_microstructure = Microstructure(im_dims, par['nsamp'])
    ix_beg = par['begx']  # index of window origin in x
    ix_end = ix_beg + (par['nsamp'])  # index of window end in x
    iy_beg = par['begy']  # index of window origin in y
    iy_end = iy_beg + (par['nsamp'])  # index of window end in y
    ixbuf_beg = ix_beg - par['edge_buffer']  # index of buffered window origin in x
    ixbuf_end = ix_end + par['edge_buffer']  # index of buffered window end in x
    iybuf_beg = iy_beg - par['edge_buffer']  # index of buffered window origin in x
    iybuf_end = iy_end + par['edge_buffer']  # index of buffered window end in x

    img = input_image[ixbuf_beg:ixbuf_end, iybuf_beg:iybuf_end]  # image for processing
    print(img.shape)
    # source image with no processing
    output_microstructure.sourceimage = input_image[ix_beg:ix_end, iy_beg:iy_end]
    # for subsequent windowing of buffered outputs into desired window
    ibeg = par['edge_buffer'] - 1
    iend = ibeg + par['nsamp']
    print(ibeg, iend)

    # 1) Histrogram equalisation
    if par['equalisation']:
        if par['equal_method'] == 'stretching':
            # Contrast stretching
            img_p2, img_p98 = np.percentile(img, (2, 98))
            img_cstretch = exposure.rescale_intensity(img, in_range=(img_p2, img_p98))
            img = img_cstretch
        elif par['equal_method'] == 'histogram':
            # Conventional histogram equalisation
            img_hist = exposure.equalize_hist(img)
            img = img_hist
        elif par['equal_method'] == 'adaptive':
            # Adative histogram equalisation
            img_adaptive = exposure.equalize_adapthist(img, clip_limit=par['clip_limit'])
            img = img_adaptive
        else:
            raise Exception(
                "invalid option for equal_method. Options are: 'stretching', 'histogram', 'adaptive'.")
        output_microstructure.sourceimage = img[ibeg:iend, ibeg:iend]

    # 2) TV Denoising
    if par['tvdnoise']:
        img_dnoise = denoise_tv_chambolle(
            img, weight=par['tv_weight'], eps=par['tv_eps'], multichannel=False)
        img = img_dnoise
        output_microstructure.sourceimage = img[ibeg:iend, ibeg:iend]

    # 3) Median filtering
    if par['median_filter']:
        img_median = median(img, disk(par['median_filter_length']))
        img = img_median
        output_microstructure.sourceimage = img[ibeg:iend, ibeg:iend]

    # 4) Thresholding (image segmentation)
    if par['thresholding_method'] == 'otsu':
        # Otsu method
        thresh_otsu = threshold_otsu(img)
        img_thresh = img >= par['thresholding_weight'] * thresh_otsu
    elif par['thresholding_method'] == 'isodata':
        # Isodata method
        thresh_isodata = threshold_isodata(img)
        img_thresh = img >= par['thresholding_weight'] * thresh_isodata
    elif par['thresholding_method'] == 'li':
        # Li method
        thresh_li = threshold_li(img)
        img_thresh = img >= par['thresholding_weight'] * thresh_li
    elif par['thresholding_method'] == 'minimum':
        # Minimum method
        thresh_minimum = threshold_minimum(img)
        img_thresh = img >= par['thresholding_weight'] * thresh_minimum
    else:
        raise Exception(
            "invalid option for thresholding_method. Options are: 'otsu', 'isodata', 'li','minimum'.")

    # Done: finalise output, make figures
    output_microstructure.structure = img_thresh[ibeg:iend, ibeg:iend]
    output_microstructure.name = par['name']

    if par['make_figs']:
        plt.figure()
        plt.imshow(output_microstructure.structure, cmap=plt.cm.gray)
        # plt.colorbar()
        plt.savefig(par['fig_path'] + par['name'] + '_structure.tif', dpi=par['fig_res'])

        plt.figure()
        plt.imshow(output_microstructure.sourceimage, cmap=plt.cm.gray)
        # plt.colorbar()
        plt.savefig(par['fig_path'] + par['name'] + '_sourceimage.tif', dpi=par['fig_res'])

        plt.figure()
        # image overlay
        x = np.arange(0, 501, 1)
        y = np.arange(0, 501, 1)
        extent = np.min(x), np.max(x), np.min(y), np.max(y)
        fig = plt.figure(frameon=False)
        Z1 = output_microstructure.structure
        im1 = plt.imshow(Z1, cmap=plt.cm.gray, interpolation='nearest',
                         extent=extent)
        Z2 = output_microstructure.sourceimage
        im2 = plt.imshow(Z2, cmap=plt.cm.viridis, alpha=.75, interpolation='bilinear',
                         extent=extent)
        plt.show()
        plt.savefig(par['fig_path'] + par['name'] + '_imgstruct_overlay.tif', dpi=par['fig_res'])

    return output_microstructure


# Calculate effective acoustic properties from S2 with Strong-Contrast Expansion
def EffectiveAcoustic_fromS2_SCE(structure_S2, par={'C_p': 2000.0, 'C_q': 1800.0, 'A_p': 0.0, 'A_q': 0.0,
                                                    'Rho_p': 1000.0, 'Rho_q': 1000.0,
                                                    'freq_beg': 1.0, 'nfreq': 10, 'freq_end': 10.0,
                                                    'dr_scale': 1e02, 'medium_dims': 3, 'return_Keff': False}):
    # check inputs for consistency
    if par['medium_dims'] != 3:
        raise Exception('Only 3D solution is available at this time.')

    if par['freq_end'] < par['freq_beg']:
        raise Exception('End frequency must be greater or equal to begin frequency.')

    # set up
    S2 = structure_S2[:, 1]
    ndr = len(S2)  # number of points in S2
    dr = par['dr_scale']  # physical dr sampling for integration
    rvals = np.zeros(ndr)
    for ir in range(ndr):
        rvals[ir] = ir * dr

    # frequency range
    freqs = np.linspace(par['freq_beg'], par['freq_end'], num=par['nfreq'], endpoint=True)
    w = 2 * np.pi * freqs

    # medium properties
    dim = par['medium_dims']
    if dim == 3:
        Omega = 4 * np.pi  # solid angle of a 3D sphere

    Cq = par['C_q']  # 'white'-phase propagation wavespeed
    Cp = par['C_p']  # 'black'-phase propagation wavespeed
    Aq = par['A_q']  # 'white'-phase attenuation -> A_q = Im{cq}/Re{cq}
    Ap = par['A_p']  # 'black'-phase attenuation -> A_p = Im{cp}/Re{cp}
    cq = complex(Cq, Aq * Cq)  # 'white'-phase complex wavespeed
    cp = complex(Cp, Ap * Cp)  # 'black'-phase complex wavespeed
    rhoq = par['Rho_q']  # 'white'-phase density
    rhop = par['C_p']  # 'black'-phase density

    phip = S2[0]  # 'black'-phase volume fraction

    # freq-dependent parameters
    sigmaq = (w**2) / (cq**2)  # k_q^2 - wavenumber^2
    sigmap = (w**2) / (cp**2)  # k_p^2 - wavenumber^2
    kq = np.sqrt(sigmaq)  # k_q - wavenumber
    kp = np.sqrt(sigmap)  # k_p - wavenumber
    Betapq = (sigmap - sigmaq) / (sigmap + (dim - 1) * sigmaq)  # contrast term Beta_pq

    # initiate quantities for effective properties
    nfreqs = par['nfreq']
    Ap2 = np.zeros((nfreqs,), dtype=complex)  # integral over S2
    Qp2 = np.zeros((nfreqs,), dtype=complex)  # intermediate term
    sigma_eff = np.zeros((nfreqs,), dtype=complex)  # k_eff^2 : effective wavenumber^2
    c_eff = np.zeros((nfreqs,), dtype=complex)  # c_eff : effective wavespeed
    if par['return_Keff']:
        kappa_eff = np.zeros((nfreqs,), dtype=complex)  # kappa_eff : effective compressibility

    # Compute effective properties
    # Effective density
    rho_eff = rhop * phip + rhoq * (1 - phip)

    # Effective sigma
    for iw in range(nfreqs):  # loop over frequencies
        # q-phase Green's function in 3D: G_f(r)
        Gf_r = (rhoq / (4 * np.pi)) * (np.exp((1j) * kq[iw] * rvals[1:]) / (rvals[1:]))

        # tp(r) term
        tp_r = Omega * sigmaq[iw] * Gf_r

        # integration for A^(p)_2 and Q^(p)_2 term
        Ap2[iw] = (dim / Omega) * np.sum(tp_r * (S2[1:] - phip**2) * dr)
        Qp2[iw] = (1. / (Betapq[iw] * phip * phip)) * (phip - Ap2[iw] * Betapq[iw])

        # final quantities
        sigma_eff[iw] = - sigmaq[iw] * ((2 + Qp2[iw]) / (1 - Qp2[iw]))
        # print('sigma_eff=%s  sigmaq=%s' % (sigma_eff[iw], sigmaq[iw]))
        c_eff[iw] = np.sqrt((w[iw]**2) / (sigma_eff[iw]))
        if par['return_Keff']:
            kappa_eff[iw] = 1 / (c_eff[iw] * c_eff[iw] * rho_eff)

    # output
    if par['return_Keff']:
        return c_eff, kappa_eff, freqs
    else:
        return c_eff, freqs

# Calculate effective acoustic properties from S2 with Strong-Contrast Expansion


def EffectiveAcoustic_fromS2_SCE_ver2(structure_S2, par={'C_p': 2000.0, 'C_q': 1800.0, 'A_p': 0.0, 'A_q': 0.0,
                                                         'Rho_p': 1000.0, 'Rho_q': 1000.0,
                                                         'scale_beg': 4.0, 'nfreq': 10, 'scale_end': 20.0,
                                                         'dr_scale': 1e02, 'corrlength_scaling': 20, 'medium_dims': 3, 'return_Keff': False}):
    # check inputs for consistency
    if par['medium_dims'] != 3:
        raise Exception('Only 3D solution is available at this time.')

    if par['scale_end'] < par['scale_beg']:
        raise Exception('End frequency must be greater or equal to begin frequency.')

    # set up
    S2 = structure_S2[:, 1]
    ndr = len(S2)  # number of points in S2
    dr = par['dr_scale']  # physical dr sampling for integration
    rvals = np.zeros(ndr)
    for ir in range(ndr):
        rvals[ir] = ir * dr

    # medium properties
    dim = par['medium_dims']
    if dim == 3:
        Omega = 4 * np.pi  # solid angle of a 3D sphere

    Cq = par['C_q']  # 'white'-phase propagation wavespeed
    Cp = par['C_p']  # 'black'-phase propagation wavespeed
    Aq = par['A_q']  # 'white'-phase attenuation -> A_q = Im{cq}/Re{cq}
    Ap = par['A_p']  # 'black'-phase attenuation -> A_p = Im{cp}/Re{cp}
    cq = complex(Cq, Aq * Cq)  # 'white'-phase complex wavespeed
    cp = complex(Cp, Ap * Cp)  # 'black'-phase complex wavespeed
    rhoq = par['Rho_q']  # 'white'-phase density
    rhop = par['Rho_p']  # 'black'-phase density

    phip = S2[0]  # 'black'-phase volume fraction

    # frequency range: function of medium scales and reference phase wavespeed C_q
    medium_scale = par['corrlength_scaling'] * dr  # get medium correlation length in real terms
    lambda_min = par['scale_beg'] * medium_scale  # minimum wavelength
    lambda_max = par['scale_end'] * medium_scale  # maximum wavelength
    freq_min = Cq / lambda_max  # maximum wavelength -> minimum frequency
    freq_max = Cq / lambda_min  # maximum wavelength -> minimum frequency
    freqs = np.linspace(freq_min, freq_max, num=par['nfreq'], endpoint=True)
    w = 2 * np.pi * freqs

    # freq-dependent parameters
    sigmaq = (w**2) / (cq**2)  # k_q^2 - wavenumber^2
    sigmap = (w**2) / (cp**2)  # k_p^2 - wavenumber^2
    kq = np.sqrt(sigmaq)  # k_q - wavenumber
    kp = np.sqrt(sigmap)  # k_p - wavenumber
    Betapq = (sigmap - sigmaq) / (sigmap + (dim - 1) * sigmaq)  # contrast term Beta_pq

    # initiate quantities for effective properties
    nfreqs = par['nfreq']
    Ap2 = np.zeros((nfreqs,), dtype=complex)  # integral over S2
    Qp2 = np.zeros((nfreqs,), dtype=complex)  # intermediate term
    sigma_eff = np.zeros((nfreqs,), dtype=complex)  # k_eff^2 : effective wavenumber^2
    c_eff = np.zeros((nfreqs,), dtype=complex)  # c_eff : effective wavespeed
    if par['return_Keff']:
        kappa_eff = np.zeros((nfreqs,), dtype=complex)  # kappa_eff : effective compressibility

    # Compute effective properties
    # Effective density
    rho_eff = rhop * phip + rhoq * (1 - phip)

    # Effective sigma
    for iw in range(nfreqs):  # loop over frequencies
        # q-phase Green's function in 3D: G_f(r)
        Gf_r = - (rhoq / (4 * np.pi)) * (np.exp((1j) * kq[iw] * rvals[1:]) / (rvals[1:]))

        # tp(r) term
        tp_r = Omega * sigmaq[iw] * Gf_r

        # integration for A^(p)_2 and Q^(p)_2 term
        Ap2[iw] = (dim / Omega) * np.sum(tp_r * (S2[1:] - phip**2) * dr)
        Qp2[iw] = (1. / (Betapq[iw] * phip * phip)) * (phip - Ap2[iw] * Betapq[iw])

        # final quantities
        sigma_eff[iw] = - sigmaq[iw] * ((2 + Qp2[iw]) / (1 - Qp2[iw]))
        # print('sigma_eff=%s  sigmaq=%s' % (sigma_eff[iw], sigmaq[iw]))
        c_eff[iw] = np.sqrt((w[iw]**2) / (sigma_eff[iw]))
        if par['return_Keff']:
            kappa_eff[iw] = 1 / (c_eff[iw] * c_eff[iw] * rho_eff)

    # output
    if par['return_Keff']:
        return c_eff, kappa_eff, freqs
    else:
        return c_eff, freqs

print('rfcuyferczeicruygezr')