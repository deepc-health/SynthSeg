import os
import numpy as np
import nibabel as nib
from nilearn.image import resample_to_img
from nilearn import image
import yaml


def anatomy_seg(inp_file_path:str, op_file_path:str, mapping_path:str):
    try:
        nii = nib.load(inp_file_path)
        ref_header = nii.header
        in_arr = nii.get_fdata()  
        out_arr = np.zeros_like(in_arr, dtype=np.uint8)
        
        with open(mapping_path, "r") as stream:
            seg_map = yaml.full_load(stream)

        for new_regions in seg_map.keys():
            if "SEG_MAP" not in new_regions:
                new_seg = seg_map[new_regions]
                for part in new_seg.keys():
                    og_value = seg_map["SEG_MAP"][part]
                    new_value = new_seg[part]
                    out_arr[in_arr== og_value] = new_value

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
