import numpy as np
from keras.models import load_model
from pydicom import dcmread
import cv2


def dcm_to_arr(dcm_file):

    ds = dcmread(dcm_file, force=True)
    arr = ds.pixel_array
    print("test shape :",arr.shape)
    img = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    
    return  img

def mapRange(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

def predicttion(img_arr, model_path):
    print('Model path is:', model_path)
    # load model
    model = load_model(model_path)
    print("max & min", np.amax(img_arr), np.amin(img_arr))

    #image normalization 16 bit to 8 bit 
    image_normali = mapRange(value=img_arr, inMin=np.amin(img_arr) ,inMax=np.amax(img_arr), outMin=0.0, outMax=255.0)
    print("image normalization max & min :", np.amax(image_normali), np.amin(image_normali))
    print("image normalization dtype:", image_normali.dtype)
    new_image = image_normali.astype(np.uint8)
    print("image normalization new dtype:", new_image.dtype)    

    # image resize
    img_resize = cv2.resize(img_arr, (224, 224))
    print("resize :", img_resize.shape)
    image_reshape = img_resize.reshape(1, 224, 224, 3)
    print("reshape :", image_reshape.shape)  
   
    # predict image
    pred = model.predict(image_reshape)
    classes = ['normal', 'pneumonia']
    conf = pred[0]
    print(conf)
    idx = np.argmax(conf)
    print(idx)
    label = classes[idx]
    print(label)
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






    

 

