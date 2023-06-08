from pydicom import dcmread
from PIL import Image
import cv2
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image_dir", type=str, required=True, help="path to input image")
parser.add_argument("-o", "--output_dir", type=str, required=True, help="path to output image")
parser.add_argument("-c", "--class_label", type=int, required=True, help="0 is normal, 1 is pneumonia")
cfg = parser.parse_args()

path_input = cfg.image_dir
path_output = cfg.output_dir
class_label = cfg.class_label

def dcm2jpeg(input_dir, output_dir, class_label):
    os.makedirs(output_dir, exist_ok=True)
    print("os.listdir(input_dir):", os.listdir(input_dir))
    for filename in os.listdir(input_dir):
        f = os.path.join(input_dir, filename)
        name = filename.rsplit('.', maxsplit=1)[0]

        if f.endswith(".dcm"):
            ds = dcmread(f, force=True)
            arr = ds.pixel_array
            print(arr.shape)
            if class_label == 0:
                dist = name + '_0' + '.jpeg'
            elif class_label == 1:
                dist = name + '_1' + '.jpeg'
            cv2.imwrite(os.path.join(output_dir, dist), arr)
            print("complete the process")
    
    return  output_dir

jpeg_convert = dcm2jpeg(path_input, path_output, class_label)
