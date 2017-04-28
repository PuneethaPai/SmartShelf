from extract_rack import TrainSetGeneartor as ts
from keras.models import model_from_json
from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing.image import img_to_array,ImageDataGenerator
from keras.preprocessing.image import load_img
preprocess = imagenet_utils.preprocess_input
import cv2
import numpy as np

class Presentation(ts):
    def __init__(self, videoPath, windowWidth, windowHeight):
        ts.__init__(self,videoPath, windowWidth, windowHeight)
        self.model=self.load_model()

    def screen_play(self):
        while 1:
            success, frame = self._video.read()
            if not success:
                break
            frame = cv2.resize(frame, (self._windowWidth, self._windowHeight), interpolation=cv2.INTER_AREA)
            croppendFrameSet = self._get_frame_set(frame)
            processed_images=self.preprocess_prediction_images(croppendFrameSet)
            datagen = ImageDataGenerator(rescale=1. / 255)
            prediction_generator=datagen.flow(np.asarray(processed_images))
            key = cv2.waitKey(1) & 0xFF
            prediction = self.model.predict_generator(prediction_generator, len(processed_images))
            to_predict_image = np.expand_dims(processed_images[0], axis=0)
            step_predict=self.model.predict(to_predict_image)
            print step_predict
            # print prediction

            if key == ord("1"):
                cv2.rectangle(frame, self._rackReferenceSet[0][0], self._rackReferenceSet[0][1], (255, 0, 0), 3)
            elif key == ord("2"):
                cv2.rectangle(frame, self._rackReferenceSet[1][0], self._rackReferenceSet[1][1], (255, 0, 0), 3)
            elif key==ord("3"):
                cv2.rectangle(frame, self._rackReferenceSet[2][0], self._rackReferenceSet[2][1], (255, 0, 0), 3)
            elif key==ord("q"):
                break
            cv2.imshow("Smart Shelf",frame)

    def preprocess_prediction_images(self,imageSet):
        imageList=[]
        for image in imageSet:
            image= cv2.resize(image,(32,64),interpolation=cv2.INTER_AREA)
            image=np.asarray(image)
            # print image.shape
            # image = img_to_array(image)
            imageList.append(image)
        return imageList

    def load_model(self):
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


# model.predict(full)
tt=Presentation("../video.mp4", 350, 512)
tt.process_extract()
tt.screen_play()