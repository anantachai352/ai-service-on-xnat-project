# VXNAT-based pulmonary x-ray prediction program for pneumonia patients.

## **แผนการดำเนินงาน**

Status :

    ✅ = Clear
    📌 = In progress
    ⁉️ = Something wrong
|       | Topics                                                                                                                                                                                                                                                                                                                                                                              | Percent                               | Status |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- | ------ |
| **1** | **วางแผนการแก้ปัญหาเรื่องการแยก class บน vxnat**<br><br>- สร้างปลั๊กอินสำหรับการแยก class บน vxnat<br>- ปลั๊กอินสามารถ convert DICOM to JPEG ได้ เพื่อความสะดวกในการ training                                                                                                                                                                                                       | 100%                                  | ✅      |
| **2** | **ออกแบบการเขียน REST API สำหรับการ download ภาพจาก xnat**<br><br>- สำหรับการ download ภาพใช้เป็น REST API<br>- เขียนโปรแกรมสำหรับการแยก class เข้าไปในแต่ละโฟลเดอร์ สำหรับการนำไป training<br><br>Train<br><br>    |-normal<br>    |-pneumonia<br><br>Val<br><br>    |-normal<br>    |-pneumonia<br><br>Test<br><br>    |-normal<br>    |-pneumonia                                | 100%                                  | ✅      |
| **3** | **ออกแบบการ training ภาพที่ได้รับจาก vxnat** <br><br>- ใช้ Tensorflow  framework<br>- ใช้ Resnet50 เป็น model สำหรับการ test <br>- ออกแบบให้สามารถ save model ออกมาเป็น version เพื่อง่ายต่อการจัดการ<br><br>ออกแบบให้มีการ upload model ขึ้นไปเก็บไว้บน google drive เพื่อสะดวกในการเรียกใช้งาน<br><br>- ใช้ google drive api ในการ upload                                         | 100% <br><br><br><br><br>        100% | ✅      |
| **4** | **ออกแบบการ download model มาใช้งาน**<br><br>- ใช้ google drive api ในการ download<br>- เขียนโปรแกรมกำหนดให้ดึงไฟล์ model เวอร์ชั่นล่าสุด โดยอิงจากเวลาการ upload<br><br>**ออกแบบการสร้าง AI ทำนายผลโรค Pneumonia ด้วยรูปถ่ายทางการทางการแพทย์**<br><br>- เขียนโปรแกรมเรียกใช้ model ที่ได้ทำการ download มา<br>- เขียนโปรแกรมทำงานผลภาพ โดยการบันทึกเป็น DICOM ที่มีการใส่ Puttext | 100% <br><br><br><br>        100%     | ✅      |
| **5** | **ออกแบบการนำโปรแกรมขึ้นไปเป็นปลั๊กอิน AI service บน vxnat**<br><br>- เขียนโปรแกรมสร้าง scan เพื่อใช้ rest api ส่งรูปการทำนายเข้าไปเก็บ<br><br>**แพ็คโปรแกรมเป็น docker image สำหรับสร้างปลั๊กอินบน xnat** <br><br>- build docker image<br>- ออกแบบการสื่อสารระหว่าง docker กับ vxnat ด้วย json file<br>- ทดสอบการใช้งาน                                                            | 100% <br><br><br>        100%         | ✅      |
| **6** | **ออกแบบและทำการทดลองโปรแกรมโดยรวม**<br><br>- ประสิทธิภาพในการใช้งาน<br><br>**บันทึกผลและทำเอกสารโครงงาน**                                                                                                                                                                                                                                                                          | 100% <br><br><br>        100%         | 📌     |



# **Technical Report**

**Demo Video :**

https://www.youtube.com/watch?v=HDvdCnHQDgc&


[https://youtu.be/HDvdCnHQDgc](https://youtu.be/HDvdCnHQDgc)

 **Flow diagram :**

![](https://paper-attachments.dropboxusercontent.com/s_7787865C7FAB426CF3D08B3DFD1DC042F998D51D6B0FF1E674EE2778F2C8DB49_1684767709723_project-Page-1.drawio+3.png)


 
 
 จาก Flow diagram จะเห็นว่ามีการเปลี่ยนแปลงไม่มีการใช้ฟังก์ชั่น XNAT Machine Learning เหมือน Flow diagram เดิม เนื่องจากการใช้งาน XNAT Machine Learning นั้นใช้งานค่อยข้างยาก ข้อจำกัดในการใช้งานเยอะ และใช้ทรัพยากรของเครื่องในการที่จะ training model ค่อยข้างเยอะ ทำให้ผมได้ทำการตัดในส่วนของ XNAT Machine Learning ออกและเปลี่ยนแผนงานใหม่เป็น ดังนี้ 
 
ผมจะทำการแยกอธิบายเป็นส่วนๆ ตาม Flow diagram โดยเริ่มจากส่วนที่ 1 

![](https://paper-attachments.dropboxusercontent.com/s_7787865C7FAB426CF3D08B3DFD1DC042F998D51D6B0FF1E674EE2778F2C8DB49_1684767735193_project-Page-1.drawio+6.png)


ในส่วนที่ 1 จะเป็น VXNAT โดยในส่วนนี้ผมได้ทำการเตรียมข้อมูลเพื่อที่จะนำข้อมูลไป train แต่ในการเตรียมข้อมูลนี้ผมจะไม่ใช้ OHIF-XNAT Viewer ในการ label แล้ว เนื่องจากผมไม่ได้ใช้ตัวของฟังก์ชั่น XNAT Machine Learning แล้ว แต่ผมจะทำให้มัน basic มากขึ้นโดยการใช้เป็น classification แทน ซึ่งในการที่จะแยกคลาส ผมได้ทำการสร้าง plugin สำหรับใช้ run ในการแยกคลาสแบบง่ายๆ ขึ้นมา โดยจะมีหน้าตาดังรูป

![](https://paper-attachments.dropboxusercontent.com/s_7787865C7FAB426CF3D08B3DFD1DC042F998D51D6B0FF1E674EE2778F2C8DB49_1683616024979_Screenshot+from+2023-05-09+14-06-02.png)


ในส่วนนี้ผมจะให้ user ได้ทำการใส่เลขในการระบุคลาส โดยผมได้ทำการระบุ Required ไว้ด้านล่างว่า 0 = Normal, 1 = Pneumonia ซึ่งจะสามรถใส่ได้แค่ 0  หรือ 1 เท่านั้น 
พอทำการระบุคลาสแล้วกด Run Container ในตัว plugin นี้จะทำการแปลง DICOM เป็น JPEG โดยในการ save รูปเป็น JPEG นั้นจะทำการเพิ่มเลขคลาสที่ได้ทำการระบุไว้ในท้ายชื่อไฟล์นั้นๆ ดังรูป

![](https://paper-attachments.dropboxusercontent.com/s_7787865C7FAB426CF3D08B3DFD1DC042F998D51D6B0FF1E674EE2778F2C8DB49_1683616422248_Screenshot+from+2023-05-09+14-13-25.png)


และนี่คือส่วนของ VXNAT ที่จะใช้ในการแยกคลาสของภาพถ่ายทางการแพทย์ครับ
ในส่วนนี้สามารถดู code ได้จาก :
https://github.com/anantachai352/ai-service-on-xnat-project/tree/main/Class_label


----------

ต่อไปจะเป็นส่วนของการดึงข้อมูลไปเตรียมสำหรับการ training 

![](https://paper-attachments.dropboxusercontent.com/s_7787865C7FAB426CF3D08B3DFD1DC042F998D51D6B0FF1E674EE2778F2C8DB49_1684767753371_project-Page-1.drawio+7.png)


ผมได้ทำการเขียน python โดยใช้ **REST API** ในการดึงข้อมูลออกมาจาก VXNAT server โดยจะทำการดึงรูป JPEG ที่ได้ทำการแยกคลาสไว้แล้วออกมาครับ ดังภาพ diagram ครับ

![](https://paper-attachments.dropboxusercontent.com/s_7787865C7FAB426CF3D08B3DFD1DC042F998D51D6B0FF1E674EE2778F2C8DB49_1683617832856_api.drawio.png)


ใน Project ของ VXNAT จะมีหลาย Subject และในแต่ละ Subject ก็จะมี Session และ Scan ไปเรื่อยๆครับ ในส่วนของรูปภาพจะอยู่ในส่วนด้านในสุดครับ ผมเขียนโปรแกรมโดยใช้แค่ Project ID เพื่อที่จะทำการดึงภาพ JPEG ทั้งหมดที่อยู่ใน Project ครับ เนื่องจากเราสร้าง Project ขึ้นมาเพื่อที่จะเก็บข้อมูลอยู่แล้ว โดยผมจะทำการสุ่มไฟล์รูปที่ดึงมาทั้งหมดเข้าไปเก็ยไว้ในแต่ละโฟลเดอร์ โดยจะแบ่งออกเป็น Train 70%, Validation 15% และ Test 15% 

แต่ในแต่ละโฟลเดอร์จะมีโฟลเดอร์สำหรับแยกคลาสอีก ก็คือ normal และ pneumonia รูปแบบการจัดโฟลเดอร์จะเป็นแบบนี้ครับ
Train        70%

    |-normal
    |-pneumonia

Val           15%

    |-normal
    |-pneumonia

Test          15%

    |-normal
    |-pneumonia

โดยผมเขียนโปรแกรมโดยใช้ชื่อตัวสุดท้ายของแต่ละไฟล์ที่ได้ทำการแยกคลาสมาเป็น 0 กับ 1 เป็นเงื่อนไขในการแยกไฟล์ไปในแต่ละโฟลเดอร์ครับ อันนี้ก็จะเสร็จสิ้นการเตรียมไฟล์ของผมครับ
โดยผมจะทำการแบ่ง **code** เป็นส่วนๆ ดังนี้ 

**ส่วนที่ 1 :** 

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
        for subject in subjects_json\['ResultSet'\]['Result']:
    
            subject_id = subject['ID']
            # print(subject_label)
            subject_sessions_url = f"http://{xnat_url}/data/projects/{project_id}/subjects/{subject_id}/experiments"
            response = requests.get(subject_sessions_url, cookies={'JSESSIONID': jsessionid}, stream=True)
            subject_sessions_json = response.json()
            # print(subject_sessions_json)
            for session in subject_sessions_json\['ResultSet'\]['Result']:
                session_id = session['ID']
                # print(session_id)
                session_scans_url = f"http://{xnat_url}/data/experiments/{session_id}/scans"
                response = requests.get(session_scans_url, cookies={'JSESSIONID': jsessionid}, stream=True)
                session_scans_json = response.json()
                # print(session_scans_json)
                for scan in session_scans_json\['ResultSet'\]['Result']:
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

ฟังก์ชั่น ***api_images_from_xnat***  ****เป็นฟังก์ชั่นสำหรับการใช้ REST API ทำการ download ภาพจาก VXNAT โดยจุดสำคัญในส่วนนี้คือ url, user, password และ project id เนื่องจากผมจะทำการ download ภาพจากทั้ง project เพราะฉะนั้นใช้เพียง project id ก็เพียงพอสำหรับการ download 

    สำหรับการ download ภาพด้วยฟังก์ชั่น ***api_images_from_xnat***  ผลลัพธ์ที่ได้จะเป็นไฟล์ ***Zip*** ดังนั้นผลจึง

ต้องมี folder สำหรับเก็บไฟล์ Zip ไว้ก่อน แล้วให้ฟังก์ชั่นทำการ ***return*** ชื่อ folder ออกมาเพื่อเอาไปใช้งานในฟังก์ชันถัดไป

**ส่วนที่ 2 :**

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

ฟังก์ชั่น ***unzip*** เป็นฟังก์ชั่นสำหรับทำการนำไฟล์รูปภาพจากไฟล์ Zip มาทำการบันทึกตาม folder ที่กำหนด โดยจะมี 3 โฟลเดอร์ได้แก่ train, val และ test โดยมีอัตตราส่วน 70-15-15 ตามลำดับ โดยในแบ่งภาพไปยังแต่ละโฟลเดอร์จะทำการสุ่มแบ่งเข้าไป 

    นอกจากนี้เมื่อภาพเข้าไปแต่ละโฟลเดอร์แล้วจะทำการแบ่ง ***Class*** ออกเป็น normal กับ pneumonia โดย

จะใช้วิธีการเช็คหลังชื่อรูปว่าเป็นตัวเลขอะไร ถ้าเป็นเลข 0 จะแยกไปยังโฟลเดอร์ของ normal ถ้าเป็นเลข 1 จะแยกไปยังโฟลเดอร์ของ pneumonia 

    ในส่วนนี้ก็จะเป็นการจบกระบวนการ download ภาพด้วย REST API และเตรียมภาพ dataset ให้พร้อม

สำหรับการนำไป training ด้วยวิธีการจัดโฟลเดอร์และแยกคลาส


----------

ต่อไปจะเป็นส่วนของการ **Training** ครับ

![](https://paper-attachments.dropboxusercontent.com/s_7787865C7FAB426CF3D08B3DFD1DC042F998D51D6B0FF1E674EE2778F2C8DB49_1684767770805_project-Page-1.drawio+8.png)


โดยผมจจะใช้ tensorflow ในการ train ครับ ข้อมูลผมได้ทำการจัดแยกโฟลเดอร์ไว้เรียบร้อยแล้วก็สามารถระบุ path แล้วนำมา train ได้เลยครับ ผมจะใช้ resnet50 เป็นโมเดลพื้นฐานในการ train ครับ
จากนั้นผมทำการ upload model ขึ้นไปยัง google drive เพื่อใช้เป็นที่จัดเก็บ model บนคลาวด์ ซึ่งจะสามารถเรีอกใช้ model ได้จากทุกที่ถ้ามี internet โดยผมจะแบ่ง code ออกเป็นส่วนๆ 
**ส่วนที่ 1 :**

    # Configure for image resizing and augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )
    
    # Generator for train set
    train = train_datagen.flow_from_directory(
        train_dir,
        target_size=image_size,
        batch_size=batch_size,
        shuffle = True,
        class_mode='categorical'
    )
    
    
    # Configure image scaling for validation set and test set
    val_datagen = ImageDataGenerator(rescale=1./255)
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Generator for validation set
    val = val_datagen.flow_from_directory(
        val_dir,
        target_size=image_size,
        batch_size=batch_size,
        shuffle = True,
        class_mode='categorical'
    )
    
    # Generator for test set
    test = test_datagen.flow_from_directory(
        test_dir,
        target_size=image_size,
        batch_size=batch_size,
        shuffle = True,
        class_mode='categorical'
    )
    
    resize_and_rescale = tf.keras.Sequential([
      layers.Resizing(224, 224),
      layers.Rescaling(1./255)
    ])
    
    data_augmentation = tf.keras.Sequential([
      layers.RandomFlip("horizontal"),
      layers.RandomRotation(0.2),
    ])
    
    class_names = list(train.class_indices.keys())
    print(class_names)
    
    
    class Resnet50Model(tf.Module):
        def __init__(self, num_classes=10):
            super(Resnet50Model, self).__init__()
            self.pretrained_model = tf.keras.applications.ResNet50(include_top=False,
                                                                   input_shape=(224, 224, 3),
                                                                   pooling='avg')
            for layer in self.pretrained_model.layers:
                resize_and_rescale,
                data_augmentation,
                layer.trainable = True   
            self.flatten = Flatten()
            self.fc1 = Dense(512, activation='relu')
            self.fc2 = Dense(num_classes, activation='softmax')
        
        def __call__(self, inputs):
            x = self.pretrained_model(inputs)
            x = self.flatten(x)
            x = self.fc1(x)
            x = self.fc2(x)
            return x
    
    inputs = tf.keras.Input(shape=(224, 224, 3))
    resnet50_layer = Resnet50Model(num_classes=num_classes)
    outputs = resnet50_layer(inputs)
    model = Model(inputs=inputs, outputs=outputs)
    
    # Set Early stopping
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    
    # compile และ train model
    model.compile(optimizer = Adam(learning_rate = learning_rate), loss='categorical_crossentropy', metrics=['accuracy'], run_eagerly=True)
    model.summary()
    history = model.fit(
                train,
                steps_per_epoch=train.n // train.batch_size,
                epochs=epochs,
                validation_data=val,
                validation_steps=val.n // val.batch_size,
                shuffle=True,
                callbacks=[early_stopping]
    )
    ส่วนของการ ***training*** ในส่วนนี้ผมจะทำการเรียกภาพและ class จากโฟล์เดอร์ dataset ที่ได้ทำการ

เตรียมไว้ในฟังก์ชั่น ***unzip*** ออกมาใช้งานโดยใช้ฟังก์ชั่น ***flow_from_directory()*** ของ tensorflow ทำการเก็บข้อมูลไว้ในตัวแปล ***train, val*** และ ***test*** ตามลำดับ จากนั้นเรียกใช้งาน Resnet50 model เพื่อใช้สำหรับการ training และมีการใช้ฟังก์ชั่น ***EarlyStopping()*** ของ tensorflow ในการหยุดการ training เมื่อค่า ***validataion loss*** มีค่าคงที่ จากนั้นก็จะเข้าสู่กระบวนการ training 

**ส่วนที่ 2 :**

    def save_model():
        # Create folder
        folder = 'model'
        os.makedirs(folder, exist_ok=True)
    
        # file name
        filename = 'pneumoniaRESNET50_v'
        file_extension = '.h5'
        i = 1
    
        while os.path.isfile(os.path.join(folder, f"{filename}{i}{file_extension}")):
            i += 1
        filepath = os.path.join(folder, f"{filename}{i}{file_extension}")
        filename = f"{filename}{i}{file_extension}"
    
        # save model 
        model.save(filepath)
    
        return folder, filename
    
    ฟังก์ชั่น ***save_model*** เป็นฟังก์ชั่นสำหรับการ save model โดยจะมีการเช็คชื่อ model ที่อยู่ในโฟลเดอร์

สำหรับการ save ถ้ามีชื่อ model อยู่แล้วจะเพิ่มเลขของเวอร์ชั่นที่อยู่ด้านหลังของชื่อไปเรื่อยๆโดยจะเรื่มจากเวอร์ชั่นที่ 1 

    สำหรับฟังก์ชันนี้ถูกสร้างขึ้นเพื่อจัดการกับ  version ของ model ไม่ให้มีการบันถึง model ทับกับไฟล์เดิมทีมี

อยู่ก่อนแล้ว 

**ส่วนที่ 3 :** 

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
    ฟังก์ชั่น ***uploadFile*** เป็นฟังก์ชั่นสำหรับการอัปโหลด model ไปเก็บไว้ที่ google drive โดยส่วนสำคัญของ

ฟังก์ชั่นนี้คือโค๊ดในส่วนของ ***CLIENT_SECRET_FILE*** ซึ่งจะเป็นตัวแปรสำหรับเก็บไฟล์ ***token*** ของ google drive api จะอยู่ในรูปของ json โดยสามารถศึกษาเพิ่มเติมเพื่อที่จะรับ token ได้จาก https://developers.google.com/drive/api/guides/about-sdk

    ส่วนสำคัญส่วนที่ 2 ที่จำเป็นต้องมีคือ folder id ในส่วนนี้ต้องทำการสร้างโฟลเดอร์สำหรับการนำข้อมูลไป

จัดเก็บบน google drive ก่อน จากนั้น google drive จะทำการ generate ****folder id มาให้ โดยการเข้าไปยังโฟลเดอร์นั้น แล้วดูที่ ***URL*** ก็จะพบกับ folder id

    เมื่อมีทั้งส่องอย่างครบแล้วเราก็จะสามารถทำการ upload model ขึ้นไปยัง google drive ได้ โดยการระบุที่

อยู่ model ที่จะทำการ upload ขึ้นไป จากนั้นก็ทำการ upload โดยใช้ฟังชั่น ***MediaFileUpload*** เมื่อเราทำการ upload ครั้งแรก google จะให้เราทำการ login google และมีคำถามเกี่ยวกับความปลอดภัย เมื่อเราทำการยืนยัน จะมีไฟล์ ***token_drive_v3.pickle*** มาให้สำหรับการ login โดยอัตโนมัติที่ไม่ต้องทำการยืนยันความปลอดภัยอีก

ในส่วนนี้สามารถดู code ได้จาก :
https://github.com/anantachai352/ai-service-on-xnat-project/tree/main/Downloadandtraining


----------

ต่อไปในส่วนของ **Docker AI Services** 



![](https://paper-attachments.dropboxusercontent.com/s_7787865C7FAB426CF3D08B3DFD1DC042F998D51D6B0FF1E674EE2778F2C8DB49_1684767790083_project-Page-1.drawio+9.png)


ในส่วนนี้ผมได้สร้างโปรแกรมทดสอบไว้บน localhost โดยที่ยังไม่ได้ทำการแพ็คเป็น docker image 
โดยตัวของโปรแกรมจะทำการ download model จาก google drive ด้วย google drive api โดยจะเลือก model เวอร์ชั่นล่าสุดที่ทำการ upload ขึ้นไปบน google drive จากนั้นตัวโปรแกรมจะเรียก model มาใช้ในการทำนายผลลัพธ์ภาพถ่ายทางการแพทย์ โดย output ที่ได้ออกมาจะเป็น DICOM ที่มีการ puttext ผลลัพธ์การทำนายไว้ โดยจะแบ่ง code ออกเป็นส่วนๆ ดังนี้
**ส่วนที่ 1 :**

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
    ฟังก์ชั่น ***DownloadModel*** เป็นฟังก์ชั่นสำหรับดาวน์โหลด model จาก google drive โดยใช้งาน google

 drive api ส่วนที่สำคัญที่ต้องมีคือ ***CLIENT_SECRET_FILE*** กับ ***foder id*** เช่นเดียวกับฟังก์ชั่น uploadFile 

     เมื่อเชื่อมต่อกับ google drive ได้แล้วโปรแกรมจะทำการอ่านชื่อไฟล์ model ล่าสุดที่ได้ทำการ upload ขึ้น

ไปโดยจะใช้ ***Time*** เป็นข้อกำหนด จากนั้นทำการเก็บชื่อไว้ในตัวแปร ***file_name*** และเก็บ ID ไว้ในตัวแปร ***file_id*** 

    ทุกอย่างพร้อมก็จะสามารถดาวน์โหลด model ได้ ก่อนจะดาวน์โหลดโปรแกรมจะทำการเช็คชื่อไฟล์ใน

โฟลเดอร์ที่จัดกับ model บนเครื่องกับชื่อไฟล์ที่อ่านได้จาก google drive ว่ามีการตรงกันหรือไม่ ถ้าชื่อตรงกันจะไม่ทำการดาวน์โหลด เนื่องจากการดาวน์โหลด model แต่ละครั้งนั้นค่อยข้างใช้เวลาการดาวน์โหลดที่ค่อยข้างนาน ขึ้นอยู่กับอินเทอร์เน็ตของผู้ใช้จึงมีเงื่อนไขนี้เข้ามาช่วย

ส่วนที่ 2 :

    def dcm_to_arr(dcm_file):
    
        ds = dcmread(dcm_file, force=True)
        arr = ds.pixel_array
        print("test shape :",arr.shape)
        img = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
        
        return  img
    
    def predicttion(img_arr, model_path):
        print('Model path is:', model_path)
        # load model
        model = load_model(model_path)
        # print("max & min", np.amax(img_arr), np.amin(img_arr))
    
        #image normalization 16 bit to 8 bit 
        image_normali = mapRange(value=img_arr, inMin=np.amin(img_arr) ,inMax=np.amax(img_arr), outMin=0.0, outMax=255.0)
        # print("image normalization max & min :", np.amax(image_normali), np.amin(image_normali))
        # print("image normalization dtype:", image_normali.dtype)
        new_image = image_normali.astype(np.uint8)
        # print("image normalization new dtype:", new_image.dtype)    
    
        # image resize
        img_resize = cv2.resize(img_arr, (224, 224))
        print("resize :", img_resize.shape)
        image_reshape = img_resize.reshape(1, 224, 224, 3)
        print("reshape :", image_reshape.shape)  
       
        # predict image
        pred = model.predict(image_reshape)
        classes = ['normal', 'pneumonia']
        conf = pred[0]
        # print(conf)
        idx = np.argmax(conf)
        # print(idx)
        label = classes[idx]
        # print(label)
        labels = "{}: {:.2f}%".format(label, conf[idx] * 100)
        print(labels)
    
    
        # putText
        if idx == 0 :
            text_size = (img_arr.shape[0]/100) * 0.13
            image = cv2.putText(new_image, labels, (50, 120), 2, text_size, (0, 255, 0), cv2.LINE_4)
            image = cv2.putText(new_image, '(development version)', (50, 160), 2, 1, (0, 255, 0), cv2.FONT_HERSHEY_DUPLEX)
        elif idx ==1 :
            text_size = (img_arr.shape[0]/100) * 0.13
            image = cv2.putText(new_image, labels, (50, 120), 2, text_size, (0, 0, 255), cv2.LINE_4)
            image = cv2.putText(new_image, '(development version)', (90, 160), 2, 1, (0, 0, 255), cv2.FONT_HERSHEY_DUPLEX)
        
        return image 

เป็นการทำนายผลภาพจาก model ในส่วนนี้จะมี 2 ฟังก์ชั่นหลักๆ คือฟังก์ชั่น ***dcm_to_arr*** ฟังก์ชั่นที่ใช้สำหรับแปลงข้อมูล DICOM เป็นรูปภาพเพื่อให้สามารถนำไปทำนายผลได้ กับฟังก์ชั่น ***predicttion*** เป็นฟังก์ชั่นสำหรับการนำ model ที่ได้ทำการดาวน์โหลดมาจาก google drive มาทำนายผลภาพ 
ในส่วนนี้สามารถดู code ได้จาก :
https://github.com/anantachai352/ai-service-on-xnat-project/tree/main/ai_service

