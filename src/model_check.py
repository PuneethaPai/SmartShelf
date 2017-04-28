from extract_rack import TrainSetGeneartor as ts
from keras.models import model_from_json
from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array,ImageDataGenerator
from keras.preprocessing.image import load_img
datagen=ImageDataGenerator(rescale=1./255)
import numpy as np
import os
import cv2
from PIL import Image
test_data_dir='../data/test'


def load_model():
    json_file = open('model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model/model.h5")
    print("Loaded model from disk")
    # evaluate loaded model on test data
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return loaded_model

test_generator = datagen.flow_from_directory(
        test_data_dir,
        target_size=(64,32),
        batch_size=32,
        class_mode='binary')
model=load_model()
# print model.evaluate_generator(test_generator,1844)
path = "/Users/surajus/Office Work/April/SmartShelf/data/predict"
image_lit=os.listdir(path)
setImage=[]
for image in image_lit:
    keras_imageData = load_img(path + "/" + image, target_size=(64, 32))
    opencv_imageData= cv2.imread(path + "/" + image)
    # print "keras",keras_imageData
    # opencv_imageData= cv2.resize(opencv_imageData,(32,64),interpolation=cv2.INTER_AREA)
    opencv_imageData=cv2.cvtColor(opencv_imageData,cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(opencv_imageData)
    pil_im=pil_im.resize((32,64))
    # print imageData.shape
    keras_data=img_to_array(keras_imageData)
    # out = pil_im.transpose(Image.ROTATE_270)
    data=img_to_array(pil_im)
    print "opencv",data
    print "keras",keras_data
    setImage.append(data)
    cv2.imshow("image",data)
    # cv2.waitKey(10000)
data=np.asarray(setImage)
# image2 = load_img("../test_full.jpg", target_size=(64,32))
# image1 = img_to_array(image1)
# image2 = img_to_array(image2)
print model.predict_classes(data)
# print model.predict_generator(test_generator, 1844)