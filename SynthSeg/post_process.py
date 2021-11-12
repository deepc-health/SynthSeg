import json
import numpy as np
import nibabel as nib
from nilearn.image import resample_to_img
from nilearn import image
import yaml

def store_labels_json(mapping_path:str):
    with open(mapping_path, "r") as stream:
        seg_map = yaml.full_load(stream)

    with open("./data/dcmqi-template.json") as json_data:
        data_dict=json.load(json_data)
    seg_atrributes_list = []

    temp_dict = data_dict["segmentAttributes"][0]
    for new_regions in seg_map['Regions']:
        temp_dict["labelID"] = new_regions['seg value']
        temp_dict["SegmentDescription"] = new_regions['seg name']
        seg_atrributes_list.append(temp_dict.copy())

    data_dict["segmentAttributes"] = seg_atrributes_list 

    json_object = json.dumps(data_dict, indent = 4)
    with open(f"./out/matter_seg/labels.json", "w") as outfile:
        outfile.write(json_object)
    
    seg_atrributes_list = []
    for key, value in seg_map['SYNTHSEG_MAP'].items():
        temp_dict["labelID"] = value
        temp_dict["SegmentDescription"] = key
        temp_dict["SegmentAlgorithmType"] = "AUTOMATIC"
        seg_atrributes_list.append(temp_dict.copy())

    data_dict["segmentAttributes"] = seg_atrributes_list 

    json_object = json.dumps(data_dict, indent = 4)
    with open(f"./out/anatomy_seg/labels.json", "w") as outfile:
        outfile.write(json_object)

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
