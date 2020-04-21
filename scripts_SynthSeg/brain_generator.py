# python imports
import os
import time
import logging
import numpy as np

# project imports
from SynthSeg.brain_generator import BrainGenerator

# third party imports
from ext.lab2im import utils


logging.getLogger('tensorflow').disabled = True

# path training labels directory (can also be path of a single image) and result folder
paths = '../../training/extra_cerebral_generation'
result_folder = '../generated_images/'

# general parameters
n_examples = 2
batchsize = 1
output_shape = 160  # crop produced image to this size
output_divisible_by_n = 32
prior_distributions = 'normal'  # type of constraint

# list of all labels in training label maps, can also be computed and saved
load_generation_label_list = './labels_and_classes/mit_generation_extra_cerebral.npy'
load_segmentation_label_list = './labels_and_classes/mit_segmentation_labels.npy'

# optional parameters
path_generation_classes = './labels_and_classes/mit_classes_extra_cerebral.npy'

########################################################################################################

# load label list, classes list and intensity ranges if necessary
generation_list_labels, generation_neutral_labels = utils.get_list_labels(load_generation_label_list, FS_sort=True)
if load_segmentation_label_list is not None:
    segmentation_list_labels, _ = utils.get_list_labels(load_segmentation_label_list, FS_sort=True)
else:
    segmentation_list_labels = generation_list_labels

# instantiate BrainGenerator object
brain_generator = BrainGenerator(labels_dir=paths,
                                 generation_labels=generation_list_labels,
                                 output_labels=segmentation_list_labels,
                                 n_neutral_labels=generation_neutral_labels,
                                 batch_size=batchsize,
                                 output_shape=output_shape,
                                 output_div_by_n=output_divisible_by_n,
                                 prior_distributions=prior_distributions,
                                 generation_classes=path_generation_classes)

if not os.path.exists(os.path.join(result_folder)):
    os.mkdir(result_folder)

for n in range(n_examples):

    # generate new image and corresponding labels
    start = time.time()
    im, lab = brain_generator.generate_brain()
    end = time.time()
    print('deformation {0:d} took {1:.01f}s'.format(n, end - start))

    # save image
    for b in range(batchsize):
        utils.save_volume(np.squeeze(im[b, ...]), brain_generator.aff, brain_generator.header,
                          os.path.join(result_folder, 'minibatch_{}_image_{}.nii.gz'.format(n, b)))
        utils.save_volume(np.squeeze(lab[b, ...]), brain_generator.aff, brain_generator.header,
                          os.path.join(result_folder, 'minibatch_{}_labels_{}.nii.gz'.format(n, b)))