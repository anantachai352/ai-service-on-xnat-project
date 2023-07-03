## Training Images From VXNAT
The program will download images from VXNAT using the REST API. Then, it will randomly split the images into train, val, and test sets in a 70-15-15 ratio, storing them in the 'train', 'val', and 'test' folders respectively. Next, it will separate the classes into 'normal' and 'pneumonia' for training using the TensorFlow framework and the ResNet50 model. Once the training is completed, the program will upload the trained model to Google Drive using the Google Drive API.



