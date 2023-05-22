import os
import io
from Google import Create_Service
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
import httplib2
from tqdm import tqdm
import time
from IPython.display import display


def uploadFile(folder, filename):
    CLIENT_SECRET_FILE = 'client_secret_75469628766-mcsp2blgek6u9g587sl6dsani4ekvpao.apps.googleusercontent.com.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # Upload File
    folder_id = '1kDl7wfNCSZcTJkIboqLk4tU1g72G9TC2'
    file_name = filename
    mime_type = 'application/x-hdf5'

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    file_size = os.path.getsize(f'{folder}/{filename}')
    # print(file_size)


    media = MediaFileUpload(f'{folder}/{file_name}', mimetype=mime_type, resumable=True, chunksize=1024*1024)
    http = httplib2.Http(timeout=600) 

    request = service.files().create(media_body=media, body=file_metadata, fields='id')
    progress_bar = tqdm(total=file_size, desc='Uploading', unit='bytes')
    response = None 
    start_time = time.time()

    while response is None:
         status, response = request.next_chunk()
         if status:
            uploaded_size = status.resumable_progress
            upload_speed = uploaded_size / (time.time() - start_time)
            time_left = (file_size - uploaded_size) / upload_speed
            progress_bar.set_postfix({'Speed': f'{upload_speed:.2f} bytes/s', 'Time Left': f'{time_left:.2f} seconds'})
            progress_bar.update(uploaded_size - progress_bar.n)
         time.sleep(0.1)

    progress_bar.close()
    print('Upload complete.')


