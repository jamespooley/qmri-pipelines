# qmri-pipelines
Pipelines for quantitative MRI techniques

## Registration and Resampling

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


## qMRI Software to Explore
* [QUIT](https://github.com/spinicist/QUIT) [C++]
* [mrQuant](https://github.com/vistalab/vistasoft/tree/master/mrQuant/relaxometry) [MATLAB]

## Some Useful Papers/Books to Explore Whenever I Get the Time
* Deoni, S. C. L. (2010). Quantitative relaxometry of the brain. *Topics in Magnetic Resonance Imaging.*
* Henkelman, R. M. et al. (2001). Magnetization transfer in MRI: A review. *Nuclear Magnetic Resonance in Biomedicine.*
* Marrale, M. et al. (2011). Physics, techniques and review of neuroradiological applications of diffusion kurtosis imaging (DKI). *Clinical Neuroradiology.*
* Steven, A. J. et al. (2014). Diffusion kurtosis imaging: An emerging technique for evaluating the microstructural environment of the brain. *American Journal of Roentgenology.*
* *MRI: The Basics*
* *Quantitative MRI of the Brain: Measuring Change*
* Soares, J. M. et al. (2013). A hitchhiker's guide to diffusion tensor imaging. *Frontiers in Neuroscience.*
