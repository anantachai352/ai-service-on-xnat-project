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
parser.add_argument("-pro", required=True, help="project_id")
parser.add_argument("-subj", required=True, help="subject_id")
parser.add_argument("-sess", required=True, help="session_id")
cfg = vars(parser.parse_args())
api_auth = ('admin', 'admin')

def create_subject(host, project_id, subject_id, session_id, scan_type, studyInstanceUID):
    scan_name = scan_type.replace(".", "_")

    url_path = f"{host}/data/projects/{project_id}/subjects/{subject_id}/experiments/{session_id}/scans/{scan_name}"
    print("scan_type: ", scan_type)
    auth = api_auth
    params = {'xsiType': 'xnat:crScanData',
              'UID': studyInstanceUID,
              'xnat:crScanData/type': scan_type,
              'series_description': scan_type,
              'xnat:crScanData/quality': 'usable'}
    res = requests.put(url_path, params=params, auth=auth)
    print("Create ai_result subject's status: ", res.status_code)


def upload_ai_result_dicom(host, project_id, subject_id, session_id, scan_type, file_path):
    scan_name = scan_type.replace(".", "_")
    
    ai_result_name = f"{subject_id}_{session_id.split('_')[-1]}_{file_path.split('/')[-1]}"
    url_path = f"{host}/data/projects/{project_id}/subjects/{subject_id}/experiments/{session_id}/scans/{scan_name}/resources/secondary/files/{ai_result_name}"


    auth = api_auth
    print("file_path: ", file_path)
    print(f"file exist?", os.path.exists(file_path))
    params = {ai_result_name: open(file_path, 'rb')}  # "multipart/form-data"

    res = requests.put(url_path, files=params, auth=auth)
    # print(res.text)
    print("Upload ai_result's status:", res.status_code)



def regenerate_ohif_database(host, project_id):
    url = f"{host}/xapi/viewer/projects/{project_id}"
    auth = api_auth
    res = requests.post(url, auth=auth)
    # print(res.text, res.status_code)


if __name__ == "__main__":

    path_input = cfg["dir_image"]
    print("dirs: ", path_input)
    host = 'http://192.168.43.59'
    path_output = cfg["dir_output"]
    project_id = cfg["pro"]
    subject_id = cfg["subj"]
    session_id = cfg["sess"]
    scan_AItype = "AI"
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
            seriesInstanceUID = dcm_out.SeriesInstanceUID
            create_subject(host, project_id, subject_id, session_id, scan_AItype, seriesInstanceUID)
            output_path = os.path.join(path_output, name+".dcm")
            pydicom.filewriter.dcmwrite(output_path, dcm_out, write_like_original=False)
            upload_ai_result_dicom(host, project_id, subject_id, session_id, scan_AItype, output_path)
            
    regenerate_ohif_database(host, project_id)
            
        