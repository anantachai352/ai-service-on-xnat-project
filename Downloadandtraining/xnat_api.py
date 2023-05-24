import requests
import os
import zipfile
import random
import shutil

def api_images_from_xnat(xnat_url, user, password, project_id):
    folder = 'Zipdata'
    os.makedirs(folder, exist_ok=True)
    

    # Authenticate with the XNAT server and get the JSESSIONID cookie
    auth_url = f'http://{xnat_url}/data/JSESSION'
    auth_response = requests.post(auth_url, auth=(user, password))
    jsessionid = auth_response.cookies.get('JSESSIONID')


    # Get all subjects for the project
    subjects_url = f'http://{xnat_url}/data/archive/projects/{project_id}/subjects'
    response = requests.get(subjects_url, cookies={'JSESSIONID': jsessionid}, stream=True)
    subjects_json = response.json()

    print(f'Loading images from {project_id}...')

    # print(subjects_json)
    # Loop through all subjects and download DICOM files
    for subject in subjects_json['ResultSet']['Result']:

        subject_id = subject['ID']
        # print(subject_label)
        subject_sessions_url = f"http://{xnat_url}/data/projects/{project_id}/subjects/{subject_id}/experiments"
        response = requests.get(subject_sessions_url, cookies={'JSESSIONID': jsessionid}, stream=True)
        subject_sessions_json = response.json()
        # print(subject_sessions_json)
        for session in subject_sessions_json['ResultSet']['Result']:
            session_id = session['ID']
            # print(session_id)
            session_scans_url = f"http://{xnat_url}/data/experiments/{session_id}/scans"
            response = requests.get(session_scans_url, cookies={'JSESSIONID': jsessionid}, stream=True)
            session_scans_json = response.json()
            # print(session_scans_json)
            for scan in session_scans_json['ResultSet']['Result']:
                scan_id = scan['ID']
                # print(scan_id)
                scan_files_url = f"http://{xnat_url}/data/archive/projects/{project_id}/subjects/{subject_id}/experiments/{session_id}/scans/{scan_id}/resources/pneumonia_label/files?format=zip"
                response = requests.get(scan_files_url, cookies={'JSESSIONID': jsessionid}, stream=True)
                # print(response)
                zip_file = os.path.join(folder, f"{subject_id}.zip") 
                with open(zip_file, 'wb') as f:
                    f.write(response.content)
                
                # with zipfile.ZipFile(zip_file) as zf:
                #     print(zf.namelist)
    return folder



def unzip(zip_folder):
    class1 = 'normal'
    class2 = 'pneumonia'

    #Create 3 folders
    folder1 = 'train'
    folder2 = 'val'
    folder3 = 'test'

    folder_paths = [folder1, folder2, folder3]

    for folder_path in folder_paths:
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            print(f"{folder_path} has been deleted.")
        else:
            print(f"{folder_path} could not be deleted because it is not a folder or does not exist.")


    os.makedirs(folder1, exist_ok=True)
    os.makedirs(os.path.join(folder1, class1), exist_ok=True)
    os.makedirs(os.path.join(folder1, class2), exist_ok=True)

    os.makedirs(folder2, exist_ok=True)
    os.makedirs(os.path.join(folder2, class1), exist_ok=True)
    os.makedirs(os.path.join(folder2, class2), exist_ok=True)

    os.makedirs(folder3, exist_ok=True)
    os.makedirs(os.path.join(folder3, class1), exist_ok=True)
    os.makedirs(os.path.join(folder3, class2), exist_ok=True)

    # Read all image filenames from a folder
    files = os.listdir(zip_folder)
    # print(files)

    # Random files and divide them into groups based on a certain percentage
    random.shuffle(files)
    total_files = len(files)
    # print(total_files)
    folder1_files = files[:int(total_files*0.7)]
    # print(folder1_files)
    folder2_files = files[int(total_files*0.7):int(total_files*0.85)]
    # print(folder2_files)
    folder3_files = files[int(total_files*0.85):]
    # print(folder3_files)

    count_1 = 0
    count_2 = 0
    count_3 = 0 

    ## For the train folder
    for files in folder1_files:
        count_1 += 1
        # print(files)
        zip_file = zipfile.ZipFile(zip_folder + '/' +files, 'r')
        # print(zip_file)
        
        for file_list in zip_file.namelist():
            # print(file_list)
            filename = os.path.basename(f'{file_list}')
            print(filename)
            if file_list.endswith('0.jpeg'):
                image_data = zip_file.read(file_list)
                # save images
                with open(folder1 + '/' + class1 + '/' + filename, 'wb') as image_file:
                    image_file.write(image_data)
                
            elif file_list.endswith('1.jpeg'):
                image_data = zip_file.read(file_list)
                # save images
                with open(folder1 + '/' + class2 + '/' + filename, 'wb') as image_file:
                    image_file.write(image_data)
                    
        zip_file.close()


    ## For the validation folder
    for files in folder2_files:
        count_2 += 1
        # print(files)
        zip_file = zipfile.ZipFile(zip_folder + '/' +files, 'r')
        # print(zip_file)
        

        for file_list in zip_file.namelist():
            # print(file_list)
            filename = os.path.basename(f'{file_list}')
            print(filename)
            if file_list.endswith('0.jpeg'):
                image_data = zip_file.read(file_list)
                # save images
                with open(folder2 + '/' + class1 + '/' + filename, 'wb') as image_file:
                    image_file.write(image_data)
                
            elif file_list.endswith('1.jpeg'):
                image_data = zip_file.read(file_list)
                # save images
                with open(folder2 + '/' + class2 + '/' + filename, 'wb') as image_file:
                    image_file.write(image_data)
                    
        zip_file.close()
    

    ## For the test folder
    for files in folder3_files:
        count_3 += 1
        # print(files)
        zip_file = zipfile.ZipFile(zip_folder + '/' +files, 'r')
        # print(zip_file)
        
        for file_list in zip_file.namelist():
            # print(file_list)
            filename = os.path.basename(f'{file_list}')
            print(filename)
            if file_list.endswith('0.jpeg'):
                image_data = zip_file.read(file_list)
                # save images
                with open(folder3 + '/' + class1 + '/' + filename, 'wb') as image_file:
                    image_file.write(image_data)
                
            elif file_list.endswith('1.jpeg'):
                image_data = zip_file.read(file_list)
                # save images
                with open(folder3 + '/' + class2 + '/' + filename, 'wb') as image_file:
                    image_file.write(image_data)
                    
        zip_file.close()
    
    num = count_1 + count_2 + count_3
    print('Total files : ', num)
    print(f'Train : ', count_1)
    print(f'Validataion : ', count_2)
    print(f'Test : ', count_3)
