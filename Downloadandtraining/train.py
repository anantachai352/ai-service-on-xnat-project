import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
from keras import layers
from keras.optimizers import Adam
from keras.layers.core import Dense
from keras.layers import GlobalAveragePooling2D
from keras import Model
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping
import PIL
from UploadFile import uploadFile


# Initialize a variable
default_epochs = 1000
default_batch_size = 32
default_lr = 0.00001

# Get values ​​via input() or use default values
epochs = input(f"Set epochs [default is {default_epochs}]: ") or default_epochs
batch_size = input(f"Set batch size [default is {default_batch_size}]: ") or default_batch_size
learning_rate = input(f"Set learning rate [default is {default_lr}]: ") or default_lr

epochs = int(epochs)
batch_size = int(batch_size)
learning_rate = float(learning_rate)

# Show value
print('config epochs is:', epochs)
print('config batch size is:', batch_size)
print('config learning rate is:', epochs)

# Parameter config
image_size = (224, 224)
seed = 1
num_classes = 2

# Set the path of the dataset
train_dir = "train"
val_dir = "val"
test_dir = "test"

# set GPU
os.environ['CUDA_VISIBLE_DEVICES'] = '1' # เลือกใช้ GPU ตัวที่ 0

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


class VGG16Model(tf.Module):
    def __init__(self, num_classes=2):
        super(VGG16Model, self).__init__()
        self.pretrained_model = tf.keras.applications.VGG16(include_top=False,
                                                            input_shape=(224, 224, 3),
                                                            pooling=None)  
        for layer in self.pretrained_model.layers:
            layer.trainable = True
        
        self.pooling_layer = GlobalAveragePooling2D()
        self.fc1 = Dense(4096, activation='relu')
        self.fc2 = Dense(4096, activation='relu')
        self.fc3 = Dense(num_classes, activation='softmax')
    
    def __call__(self, inputs):
        x = self.pretrained_model(inputs)
        x = self.pooling_layer(x)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        return x

inputs = tf.keras.Input(shape=(224, 224, 3))
vgg16_layer = VGG16Model(num_classes=num_classes)
outputs = vgg16_layer(inputs)
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

def save_model():
    # Create folder
    folder = 'model'
    os.makedirs(folder, exist_ok=True)

    # file name
    filename = 'pneumoniaVGG16_v'
    file_extension = '.h5'
    i = 1

    while os.path.isfile(os.path.join(folder, f"{filename}{i}{file_extension}")):
        i += 1
    filepath = os.path.join(folder, f"{filename}{i}{file_extension}")
    filename = f"{filename}{i}{file_extension}"

    # save model 
    model.save(filepath)

    return folder, filename

folder, filename = save_model()
print('folder is ', folder)
print('filename is', filename)

score = model.evaluate(
    test,
    steps=test.n // test.batch_size
)
print("Test loss:", score[0])
print("Test accuracy:", score[1])


# upload file.
uploadFile(folder, filename)








