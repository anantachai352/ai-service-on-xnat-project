## Training Images From VXNAT
The program will download images from VXNAT using the REST API. Then, it will randomly split the images into train, val, and test sets in a 70-15-15 ratio, storing them in the 'train', 'val', and 'test' folders respectively. Next, it will separate the classes into 'normal' and 'pneumonia' for training using the TensorFlow framework and the ResNet50 model. Once the training is completed, the program will upload the trained model to Google Drive using the Google Drive API.

## Prerequisites

1. Prior to using the program, users should install xnat-docker-compose and run it to activate the xnat-server. For additional information, please refer to https://github.com/NrgXnat/xnat-docker-compose.
2. The user needs to know the ***URL*** of the VXNAT server, as well as the ***username*** and ***password*** for logging in and accessing the system.

## Usage
1. Clone the [ai-service-on-xnat-project](https://github.com/anantachai352/ai-service-on-xnat-project) repository 

```bash
$ git clone https://github.com/anantachai352/ai-service-on-xnat-project
```

2. Navigate to the 'Class_label' folder.

```bash
$ cd /ai-service-on-xnat-project/Downloadandtraining
```

3. Create environment
```bash
$ python3 -m venv env 
```
4. Install environment 
```bash
$ pip install -r req.txt
```
5. Run script ***scipt.sh***
```bash
$ sh scipt.sh
```
