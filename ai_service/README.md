## AI Service For Predicting Pneumonia
The program will download the model from Google Drive using the Google Drive API. Then, it will use the model to predict medical images of patients with pneumonia. The output will be in the form of DICOM files that include the predictions made by the model.

## Prerequisites
The user must have a Google account and enable the Google Drive API to obtain a token for connecting to Google Drive. The token will be in the form of a ***JSON*** file that the user needs to download and add to the program's working directory. For more information, please refer to https://developers.google.com/drive/api/guides/about-sdk.

## Usage
1. Clone the [ai-service-on-xnat-project](https://github.com/anantachai352/ai-service-on-xnat-project) repository 

```bash
$ git clone https://github.com/anantachai352/ai-service-on-xnat-project
```

2. Navigate to the ***'ai_service'*** folder.

```bash
$ cd /ai-service-on-xnat-project/ai_service
```

3. Create environment

```bash
$ python3 -m venv env 
```
4. Install environment 

```bash
$ pip install -r req.txt
```
5. Run script ***main.py***
```bash
$ python3 main.py
```
