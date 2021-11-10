# Anatomy Based GM, WM and CSF Segmentation

In this repository, we repurpose the SynthSeg based model to 
do Gray Matter, White Matter and Cerebro Spinal Fluid segmentation for MRI of the brain. 
Using medical information we assign each of the anatomical region from the synthseg into one 
of the categories. This process is also configurable. The method is dockerised in to allow 
for plug and play approach. 

----------------

### Easily segment your data with one command

Once all the python packages are installed (see below), you can simply test SynthSeg on your own data with:
```
python ./scripts/commands/SynthSeg_predict.py --i <image> --o <segmentation> --post <post> --resample <resample> --vol <vol>
```
where:
- `<image>` is the path to an image to segment (supported formats are .nii, .nii.gz, and .mgz). \
This can also be a folder, in which case all the image inside that folder will be segmented.
- `<segmentation>` is the path where the output segmentation(s) will be saved. \
This must be a folder if `<image>` designates a folder.
- `<post>` (optional) is the path where the posteriors (given as soft probability maps) will be saved. \
This must be a folder if `<image>` designates a folder.
- `<resample>` (optional) SynthSeg segmentations are always given at 1mm isotropic resolution. Therefore, 
images are internally resampled to this resolution (except if they aleady are at 1mm resolution). 
Use this optional flag to save the resampled images: it must be the path to a single image, or a folder
if `<image>` designates a folder.
- `<vol>` (optional) is the path to an output csv file where the volumes of every segmented structures
will be saved for all scans (i.e., one csv file for all subjects; e.g. /path/to/volumes.csv)

\
Additional optional flags are also available:
- `--cpu`: to enforce the code to run on the CPU, even if a GPU is available.
- `--threads`: to indicate the number of cores to be used if running on a CPU (example: `--threads 3` to run on 3 cores).
This value defaults to 1, but we recommend increasing it for faster analysis.
- `--crop`: to crop the input images to a given shape before segmentation. The given size must be divisible by 32.
Images are cropped around their centre, and their segmentations are given at the original size). It can be given as a 
single (i.e., `--crop 160` to run on 160<sup>3</sup> patches), or several integers (i.e, `--crop 160 128 192` to crop to
different sizes in each direction, ordered in RAS coordinates). This value defaults to 192, but it can be decreased
for faster analysis or to fit in your GPU.


**IMPORTANT:** We resample the synthseg output to its original voxel dimension. So both the anatomy maps and the region maps 
are overlayable on the original input MRI.

The complete list of segmented structures is available in [labels table.txt](data/labels%20table.txt) along with their
corresponding values.

----------------

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
