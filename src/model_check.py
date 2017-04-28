from extract_rack import TrainSetGeneartor as ts
from keras.models import model_from_json
from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array,ImageDataGenerator
from keras.preprocessing.image import load_img
datagen=ImageDataGenerator(rescale=1./255)
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
print model.evaluate_generator(test_generator,1844)
print model.predict_generator(test_generator, 1844)