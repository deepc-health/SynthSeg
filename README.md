# Anatomy Based GM, WM and CSF Segmentation

In this repository, we repurpose the SynthSeg based model to 
do Gray Matter(GM), White Matter(WM) and Cerebro-Spinal Fluid(CSF) segmentation for MRI of the brain. 
Using medical information we assign each of the anatomical region from the synthseg into one 
of the categories. This process is also configurable. The method is dockerised in to allow 
for plug and play approach. 


<img width="671" alt="Sample Segmentation Result" src="https://user-images.githubusercontent.com/23334003/153214599-cc600e9e-5f0f-476f-83a9-5f61ef657662.png">


----------------

### Easily segment your data with one command

Once all the docker and its dependencies are installed, you can simply test brain matter segmentation on your own data with:

**Run with GPUs:**

default:
```
docker run --gpus all --user "$(id -u):$(id -g)" -v <inpdir>:/synthseg/inp -v <outdir>:/synthseg/out aparida12/brainseg
```
 with additional flags:
```
docker run --gpus all --user "$(id -u):$(id -g)" -v <inpdir>:/synthseg/inp -v <outdir>:/synthseg/out aparida12/brainseg python -u run_seg.py <optional_flags>
```
**Run without GPUs:**

default:
```
docker run --user "$(id -u):$(id -g)" -v <inpdir>:/synthseg/inp -v <outdir>:/synthseg/out aparida12/brainseg
```
 with additional flags:
```
docker run --user "$(id -u):$(id -g)" -v <inpdir>:/synthseg/inp -v <outdir>:/synthseg/out aparida12/brainseg python -u run_seg.py <optional_flags>
```

where:
- `<inpdir>` is the directory with all nifti files(extn .nii.gz or .nii) that need to be segmented.
- `<outdir>` is the directory where all outputs are stored(`<inpdir>` should not be `<outdir>`). 

\
Additional optional flags are also available:
- `--cpu`: to enforce the code to run on the CPU, even if a GPU is available.
- `--threads`: to indicate the number of cores to be used if running on a CPU (example: `--threads 3` to run on 3 cores).
This value defaults to 1, but we recommend increasing it for faster analysis.
- `--crop`: to crop the input images to a given shape before segmentation. The given size must be divisible by 32.
Images are cropped around their center, and their segmentations are given at the original size). It can be given as a 
single (i.e., `--crop 160` to run on 160<sup>3</sup> patches), or several integers (i.e, `--crop 160 128 192` to crop to
different sizes in each direction, ordered in RAS coordinates). This value defaults to 192, but it can be decreased
for faster analysis or to fit in your GPU.


**IMPORTANT:**, Unlike the original synthseg, we resample the synthseg output to its original voxel dimension. So both the anatomy maps and the region maps 
are overlay able on the original input MRI.

----------------

### Input Folder Structure

The `seg_config.yaml` is optional inside the `<inpdir>`. It is only required when the user wants to change the classification of the default anatomy into different regions than in the default `seg_config.yaml`
```
│
└───<inpdir>
│   │   file011.nii.gz
│   │   file012.nii.gz
│   │   file012.nii.gz
│   │.  seg_config.yaml

```
----------------
### Output Folder Structure
After processing is over the `<outdir>` has folders - `anatomy_seg` and `matter_seg`.

where:
- `anatomy_seg` is the directory where the files with the different brain structures are segmented separately(the resampled to original size output of the SynthSeg algorithm)
- `matter_seg` is the directory where the files where the anatomies are aggregated into different regions like GM, WM, CSF, and others as specified by the `seg_config.yaml`
- `labels.txt` is a TXT file that has the mapping between pixel values of the nifti file with the corresponding name of the structure or region and some suggested color scheme that can be used by ITKSnap in the segmentation mode.

```
│
└───<outdir>
│   │─── anatomy_seg
│   │   │   │seg_file011.nii.gz
│   │   │   │seg_file012.nii.gz
│   │   │   │seg_file012.nii.gz
│   │   │   │.  labels.txt
│   │
│   │─── matter_seg
│   │   │   │seg_file011.nii.gz
│   │   │   │seg_file012.nii.gz
│   │   │   │seg_file012.nii.gz
│   │   │   │.  labels.txt

```
----------------
### User Specified `seg_config.yaml`

Download the template `seg_config.yaml` from [here](https://raw.githubusercontent.com/a-parida12/SynthSeg/master/data/seg_config.yaml)(You can right-click save-as `seg_config.yaml`). Modify the various regions by following the steps mentioned in the YAML file. Do not forget to put the modified file inside the `<inpdir>` along with the other Nifti Files.


--------------------------------

### How does it work ?

In short, we train a network with synthetic images sampled on the fly from a generative model based on the forward
model of Bayesian segmentation. Crucially, we adopt a domain randomisation strategy where we fully randomise the 
generation parameters which are drawn from uninformative uniform distributions. Therefore, by maximising the variability
of the training data, we force to learn domain-agnostic features. As a result SynthSeg is able to readily segment
real scans of any target domain, without retraining or fine-tuning. 

The following figure illustrates the the workflow of a training iteration, and provides an overview of the generative 
model:
\
\
![Generation examples](data/README_figures/overview.png)
\
\
Finally we show additional examples of the synthesised images along with an overlay of their target segmentations:
\
\
![Generation examples](data/README_figures/training_data.png)
\
\
If you are interested to learn more about SynthSeg, you can read the associated publication (see below), and watch this
presentation, which was given at MIDL 2020 for a related article on a preliminary version of SynthSeg (robustness to
MR contrast but not resolution).
\
\
[![Talk SynthSeg](data/README_figures/youtube_link.png)](https://www.youtube.com/watch?v=Bfp3cILSKZg&t=1s)


----------------

### Citation/Contact

This code is under [Apache 2.0](LICENSE.txt) licensing. \
If you use it, please cite one of the following papers:

**SynthSeg: Domain Randomisation for Segmentation of Brain MRI Scans of any Contrast and Resolution** \
B. Billot, D.N. Greve, O. Puonti, A. Thielscher, K. Van Leemput, B. Fischl, A.V. Dalca, J.E. Iglesias \
[[arxiv](https://arxiv.org/abs/2107.09559) | [bibtex](bibtex.bib)]

**A Learning Strategy for Contrast-agnostic MRI Segmentation** \
B. Billot, D.N. Greve, K. Van Leemput, B. Fischl, J.E. Iglesias*, A.V. Dalca* \
*contributed equally \
MIDL 2020 \
[[link](http://proceedings.mlr.press/v121/billot20a.html) | [arxiv](https://arxiv.org/abs/2003.01995) | [bibtex](bibtex.bib)]

**Partial Volume Segmentation of Brain MRI Scans of any Resolution and Contrast** \
B. Billot, E.D. Robinson, A.V. Dalca, J.E. Iglesias \
MICCAI 2020 \
[[link](https://link.springer.com/chapter/10.1007/978-3-030-59728-3_18) | [arxiv](https://arxiv.org/abs/2004.10221) | [bibtex](bibtex.bib)]

If you have any question regarding the usage of this code, or any suggestions to improve it, you can contact us at: \
benjamin.billot.18@ucl.ac.uk


----------------

### References

[1] *[Anatomical Priors in Convolutional Networks for Unsupervised Biomedical Segmentation](http://www.mit.edu/~adalca/files/papers/cvpr2018_priors.pdf)* \
Adrian V. Dalca, John Guttag, Mert R. Sabuncu \
CVPR 2018

[2] *[Unsupervised Data Imputation via Variational Inference of Deep Subspaces](https://arxiv.org/abs/1903.03503)* \
Adrian V. Dalca, John Guttag, Mert R. Sabuncu \
Arxiv preprint 2019

----------------
###  External Links
 - [Original Code Repo](https://github.com/BBillot/SynthSeg)
 - [Docker Code Repo](https://github.com/deepc-health/SynthSeg)
 - [Docker Container Repo](https://hub.docker.com/r/aparida12/brainseg)
--------------------------------
--------------------------------
