# qmri-pipelines
Pipelines for quantitative MRI techniques

## Registration and Resampling Recommendations

### Suckling et al. (2014) Recommendations

> All T1-weighted images from DESPOT1 and IRSPGR
> sequences were processed with FSL v4.0 (http://www.fmrib.
> ox.ac.uk/fsl). Extracerebral tissues were removed with the
> Brain Extraction Tool [Smith, 2002], and maps of partial vol-
> ume estimates of grey matter occupancy were calculated with
> FMRIB's Automated Segmentation Tool (FAST) [Zhang et al.,
> 2001]. All grey matter images were initially linearly registered
> (FLIRT) [Jenkinson et al., 2002] and then non-linearly registered
> (FNIRT) [Klein et al., 2009] to the stereotactic coordinate
> system of the Montreal Neurological Institute (MNI). Finally,
> to account for residual inter-subject misregistration, the maps
> of partial volume estimates of grey matter were smoothed
> with a three-dimensional Gaussian kernel with standard
> deviation 54mm (full width at half maximum = 9.4 mm).

### QUIT Developer Recommendations

According to [this](https://github.com/spinicist/old_QUIT/blob/master/doc/latex/DESPOT.tex) document, here is one recommendation re: coregistration:
>
> As with most MRI techniques, the effects of sample motion must be minimised before processing. This can be achieved by registering all the images together using either FSL, SPM, or your software package of choice. Because the contrast of the SPGR and SSFP images changes with the flip-angle, mutual information should be used as the registration cost function, and it is currently recommended to daisy-chain the registrations (i.e. flip-angle 1 to flip-angle 2, flip-angle 2 to flip-angle 3, etc.). How best to perform the registration is an open question.
>
> The scans must be resampled to the same matrix size.  Often the $B_1$ map will be acquired at lower resolution, and scanners may zero-fill images before reconstruction. It is highly recommended that this resampling is to the original matrix size used for the SPGR and SSFP images. Processing at a larger matrix size will not improve results but will considerably lengthen processing time.
>
>A template script ([`template_preprocess.sh`](https://github.com/spinicist/old_QUIT/blob/master/doc/latex/template_preprocess.sh)) that will carry out all these steps has been written by Anna Combes and should have been distributed with this manual. It assumes that all your converted NIFTIs are placed in one directory. It uses FSL to split the files into individual images for each flip-angle, register them together, merge them back for processing, and also creates a brain mask for you.
>
>You will need to edit the filenames on lines 14, 15 and 24 to match the filenames you used when converting your data. You may wish to add commands to delete the `splitfiles` directory it produces to save space.

> You will also need to edit line 16 to provide a target image to register to, with  a sensible matrix size as described above. When the template was written our files had been zero-filled to 256x256x192, so simply subsampling the first SPGR image by 2 created a target with the correct matrix size. You may wish to register to a template, or create a specific matrix size using `fslcreatehd`.

## Resources to Explore

#### Background and General Overviews of Quantitative MRI

* *MRI: The Basics*
* Tofts, P. (Ed.) (2004). *Quantitative MRI of the Brain: Measuring Changes Caused by Disease*

#### Quantitative Relaxometry

The Deoni et al. (2015) chapter is the best overview of qMRI I've come across, but you'll most likely get paywalled if you try and access it. The Deoni (2010) overview has a lot of overlap with this chapter and is open access. 

* Deoni, S. C. L. (2010). Quantitative relaxometry of the brain. *Topics in Magnetic Resonance Imaging.*
* Deoni, S. C. L. et al. (2015). Modern methods for accurate T1, T2, and proton density MRI. In M. Filippi (Ed.) *Oxford Textbook of Neuroimaging*
* Suckling, J. et al. (2014). Are power calculations useful? A multicentre neuroimaging study. *Human Brain Mapping*

#### Quantitative Magnetization Transfer

* Henkelman, R. M. et al. (2001). Magnetization transfer in MRI: A review. *Nuclear Magnetic Resonance in Biomedicine.*
* [Quantitative magnetization transfer imaging techniques and applications](http://etd.library.vanderbilt.edu/available/etd-11262007-150546/unrestricted/Dissertation_XiaweiOu.pdf)

#### Diffusion Kurtosis Imaging

* Soares, J. M. et al. (2013). A hitchhiker's guide to diffusion tensor imaging. *Frontiers in Neuroscience.*
* Marrale, M. et al. (2011). Physics, techniques and review of neuroradiological applications of diffusion kurtosis imaging (DKI). *Clinical Neuroradiology.*
* Steven, A. J. et al. (2014). Diffusion kurtosis imaging: An emerging technique for evaluating the microstructural environment of the brain. *American Journal of Roentgenology.*

#### NODDI

* Zhang, H. et al. (2012). NODDI: Practical *in vivo* neurite orientation dispersion and density imaging of the brain. *NeuroImage, 61*, 1000-1016.

## qMRI Software to Explore
* [QUIT (Quantitative Imaging Tools)](https://github.com/spinicist/QUIT) [C++]
* [QMAP (Quantitative MRI Analysis Package)](https://www.medphysics.wisc.edu/~samsonov/qmap/) [MATLAB]
* [mrQuant](https://github.com/vistalab/vistasoft/tree/master/mrQuant/relaxometry) [MATLAB]
* C-PAC (Configurable Pipeline for the Analysis of Connectomes) [Python]
* Nipype [Python]
