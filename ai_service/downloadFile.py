import os
import io
from Google import Create_Service
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

def DownloadModel():

    # Create service
    CLIENT_SECRET_FILE = 'client_secret_75469628766-mcsp2blgek6u9g587sl6dsani4ekvpao.apps.googleusercontent.com.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    #Folder ID
    folder_id = '1kDl7wfNCSZcTJkIboqLk4tU1g72G9TC2'

    # Call the API to fetch the latest files.
    query = f"parents='{folder_id}' and mimeType!='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, orderBy="modifiedTime desc",pageSize=1, fields="nextPageToken, files(id, name, mimeType, createdTime, modifiedTime)").execute()

    # check file name
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['mimeType']}) - ID: {item['id']}")

    file_name = item['name']
    # print(file_name)
    file_id = item['id']
    # print(file_id)

    # Create folder
    folder = 'model'
    os.makedirs(folder, exist_ok=True)

    # Check the files in the folder
    file_list = os.listdir(folder)
    if file_list:
        for filename in file_list:
            if filename == file_name:
                print(f"{file_name} exists in the folder.")
                modelpath = f'{folder}/{file_name}'
                break
        else:
            print(f"{file_name} in the folder could not be found.")
    else:
        print(f"The file in the {folder} could not be found.")

        # Request the file content
        print(f'Downloading...{file_name}...')
        try:
            request = service.files().get_media(fileId=file_id)
            file = io.BytesIO(request.execute())

            # Save the file content
            with open(f'{folder}/{file_name}', 'wb') as f:
                f.write(file.getbuffer())
            print(f'Successfully downloaded file "{file_name}" from Google Drive')
            modelpath = f'{folder}/{file_name}'
        except HttpError as error:
            print(f'An error occurred: {error}')

    return modelpath

if __name__=="__main__":
    filename = DownloadModel()
    print(filename)