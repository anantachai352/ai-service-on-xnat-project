import os
import argparse
import pydicom
from downloadFile import DownloadModel
from predict import dcm_to_arr, predicttion
from imgTOdcm import image_To_dicom
import requests


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--dir_image", type=str, required=True, help="path to input image")
parser.add_argument("-o", "--dir_output", type=str, required=True, help="path to output image")
cfg = vars(parser.parse_args())


if __name__ == "__main__":

    path_input = cfg["dir_image"]
    print("Input dirs: ", path_input)
    path_output = cfg["dir_output"]
    print("Output dirs:", path_output)
    base_dicom = "base.dcm" #base.dcm
    os.makedirs(path_output, exist_ok=True)

    # Download model by google drive api
    model = DownloadModel()
    print('Model path is ', model)


    for filename in os.listdir(path_input):
        f = os.path.join(path_input, filename)
        name = filename.rsplit('.', maxsplit=1)[0]
            
        if f.endswith(".dcm"):
            image_arr = dcm_to_arr(f)
            arr_pred = predicttion(image_arr, model)
            dcm_out = image_To_dicom(base_dicom, arr_pred)
            output_path = os.path.join(path_output, name+".dcm")
            pydicom.filewriter.dcmwrite(output_path, dcm_out, write_like_original=False)
            # break
        