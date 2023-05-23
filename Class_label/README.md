## Label Pneumonia Class On VXNAT
This program is used to build a Docker image for deploying it as a plugin to detect Pneumonia on VXNAT.

## Usage
1. Clone the [ai-service-on-xnat-project](https://github.com/anantachai352/ai-service-on-xnat-project) repository 

< $ git clone https://github.com/anantachai352/ai-service-on-xnat-project >

2. Navigate to the 'Class_label' folder.

< $ cd /ai-service-on-xnat-project/Class_label >

3. Build docker image

<$ docker build -t class_label .>

4. Copy the code from the ***command.json*** file and paste it into the JSON file on VXNAT to establish communication between VXNAT and the Docker image.