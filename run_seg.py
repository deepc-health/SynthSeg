from colorama import Fore
import glob
import tqdm
import datetime
from SynthSeg.predict import predict
from pathlib import Path
from SynthSeg.post_process import anatomy_seg, resample_og_size
from argparse import ArgumentParser
import tensorflow as tf
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
# parse arguments
parser = ArgumentParser()
# parameters
parser.add_argument("--crop", nargs='+', type=int, default=192, dest="cropping",
                    help="(optional) Size of 3D patches to analyse. Default is 192.")
parser.add_argument("--threads", type=int, default=1, dest="threads",
                    help="(optional) Number of cores to be used. Default is 1.")
parser.add_argument("--cpu", action="store_true", help="(optional) Enforce running with CPU rather than GPU.")

# parse commandline
args = vars(parser.parse_args())

# default parameters
args['segmentation_labels'] = './data/labels_classes_priors/segmentation_labels.npy'
args['n_neutral_labels'] = 18
args['segmentation_label_names'] = './data/labels_classes_priors/segmentation_names.npy'
args['topology_classes'] = './data/labels_classes_priors/topological_classes.npy'
args['path_model'] = './models/SynthSeg.h5'
args['padding'] = args['cropping']

if args['cpu']:
    print('using CPU, hiding all CUDA_VISIBLE_DEVICES')
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
else:
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    print("physical_devices-------------", len(physical_devices))
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
del args['cpu']

# limit the number of threads to be used if running on CPU
tf.config.threading.set_intra_op_parallelism_threads(args['threads'])
del args['threads']


line_length = 60
input_dir = './inp/'
anatomy_output_dir = './out/anatomy_seg/'
region_output_dir = './out/matter_seg/'
os.makedirs(anatomy_output_dir, exist_ok =True)
os.makedirs(region_output_dir, exist_ok =True)

nii_files = glob.glob(input_dir + '*.nii.gz')
mapping_path = "./inp/seg_config.yaml"

# print information
print(Fore.RED + "SEGMENTER".center(line_length, "*") + Fore.RESET)
print()
print('Found '+ Fore.GREEN +f"{len(nii_files)}"+ Fore.RESET + " Nifti Files to Process")
if len(nii_files) == 0:
    print('No Files found quiting program..')
    quit()

if os.path.isfile(mapping_path):
    print("Using "+ Fore.GREEN + "CUSTOM" + Fore.RESET + " `seg_config.yaml` for segmentation aggregation")
else:
    mapping_path = "./data/seg_config.yaml"
    print("Using "+ Fore.GREEN + "DEFAULT" + Fore.RESET + " `seg_config.yaml` for segmentation aggregation")

start_time = datetime.datetime.now()
print('Start time : '+ Fore.YELLOW +f"{start_time}"+ Fore.RESET)
print()
print("".center(line_length, "*"))
print()


for nii_file in tqdm.tqdm(nii_files, desc= "File Procesing"):
    args["path_images"] = nii_file
    name = str(Path(nii_file).name)
    args["path_segmentations"] = os.path.join(anatomy_output_dir,'seg_'+name)

    predict(**args)
    resample_og_size(inp_file_path = args["path_segmentations"] , op_file_path = args["path_segmentations"], tmp_file_path = args["path_images"])
    anatomy_seg(inp_file_path=args["path_segmentations"], op_file_path= os.path.join(region_output_dir,'seg_'+name) , mapping_path=mapping_path)


# print information
print(Fore.RED + "SEGMENTER".center(line_length, "*") + Fore.RESET)
print()
print(f'Processed '+ Fore.GREEN +f"{len(nii_files)}"+ Fore.RESET +  ' Nifti Files ')
time_delta = datetime.datetime.now() - start_time
print('End time :'+ Fore.YELLOW +f" {datetime.datetime.now()}"+ Fore.RESET)
print('Total time :'+ Fore.YELLOW +f" {time_delta}"+ Fore.RESET +" hh:mm:ss.ms")
print()
print("".center(line_length, "*"))
print()