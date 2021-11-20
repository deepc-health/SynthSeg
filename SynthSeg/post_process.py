import json
import numpy as np
import nibabel as nib
from nilearn.image import resample_to_img
from nilearn import image
import yaml
import textwrap

def store_labels_json(mapping_path:str):
    with open(mapping_path, "r") as stream:
        seg_map = yaml.full_load(stream)

    itk_header="""################################################ 
# ITK-SnAP Label Description File 
# File format: 
# IDX   -R-  -G-  -B-  -A--  VIS MSH  LABEL 
# Fields: 
#    IDX:   Zero-based index 
#    -R-:   Red color component (0..255) 
#    -G-:   Green color component (0..255) 
#    -B-:   Blue color component (0..255) 
#    -A-:   Label transparency (0.00 .. 1.00)
#    VIS:   Label visibility (0 or 1)
#    IDX:   Label mesh visibility (0 or 1) 
#  LABEL:   Label description 
################################################"""
    txt = """\n  {:>3}   {:>3}  {:>3}  {:>3}        {}  {}  {}    "{}" """
    
    f = open("data/color_lut.txt", 'r')
    colors = []
    for line in f:
        colors.append(line)
    f.close()

    # Open file for writing
    fileObject = open("./out/matter_seg/labels.txt", "w")
    fileObject.write(itk_header)
    for i, new_regions in enumerate(seg_map['Regions']):
        
        if new_regions['seg value'] == 0:
            fileObject.write(txt.format(new_regions['seg value'], 0,0,0,0,0,0,new_regions['seg name']))
        
        else:
            color=colors[i-1].split(',')
            fileObject.write(txt.format(new_regions['seg value'], color[0],color[1],color[2].strip(),1,1,1,new_regions['seg name']))
    fileObject.close()

    fileObject = open("./out/anatomy_seg/labels.txt", "w")
    fileObject.write(itk_header)
    for i, (key, value) in enumerate(seg_map['SYNTHSEG_MAP'].items()):
        
        if value == 0:
            fileObject.write(txt.format(value, 0,0,0,0,0,0,key))

        else:
            color=colors[i-1].split(',')
            fileObject.write(txt.format(value, color[0],color[1],color[2].strip(),1,1,1,key))
    fileObject.close()


def anatomy_seg(inp_file_path:str, op_file_path:str, mapping_path:str):
    try:
        nii = nib.load(inp_file_path)
        ref_header = nii.header
        in_arr = nii.get_fdata()  
        out_arr = np.zeros_like(in_arr, dtype=np.uint8)
        
        with open(mapping_path, "r") as stream:
            seg_map = yaml.full_load(stream)

        for new_regions in seg_map['Regions']:

            part_list = new_regions['synthseg_labels']
            new_region_val = new_regions['seg value']
            for part in part_list:
                og_value = seg_map['SYNTHSEG_MAP'][part]
                out_arr[in_arr== og_value] = new_region_val

        out_nii = nib.Nifti1Image(out_arr.astype(np.uint8), ref_header.get_sform(), ref_header)
        nib.save(out_nii, op_file_path)
        return "ok"
    except Exception as e:
         print(f"failed! due to {e}")


def resample_og_size(inp_file_path:str, op_file_path:str, tmp_file_path:str):
    try:
        stat_img = image.load_img(inp_file_path, dtype="float32")
        temp_img = image.load_img(tmp_file_path, dtype="float32")
        resampled_stat_img = resample_to_img(stat_img, temp_img, interpolation='nearest')
        resampled_stat_img.to_filename(op_file_path)   
        return "ok"
    except Exception as e:
        print( f"failed! due to {e}") 
