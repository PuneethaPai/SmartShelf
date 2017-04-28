from keras.applications import imagenet_utils
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
from extract_rack import TrainSetGeneartor as ts
from PIL import Image

preprocess = imagenet_utils.preprocess_input
import cv2
import numpy as np


class Presentation(ts):
    def __init__(self, videoPath, windowWidth, windowHeight):
        ts.__init__(self, videoPath, windowWidth, windowHeight)
        self.model = self.load_model()

    def screen_play(self):
        while 1:
            success, frame = self._video.read()
            if not success:
                break
            frame = cv2.resize(frame, (self._windowWidth, self._windowHeight), interpolation=cv2.INTER_AREA)
            croppendFrameSet = self._get_frame_set(frame)
            processed_images = self.preprocess_prediction_images(croppendFrameSet)
            key = cv2.waitKey(1) & 0xFF
            step_predict = self.model.predict_classes(np.asarray(processed_images))
            print step_predict
            if step_predict[0] == 0:
                cv2.rectangle(frame, self._rackReferenceSet[0][0], self._rackReferenceSet[0][1], (0, 0, 255), 3)
            if step_predict[1] == 0:
                cv2.rectangle(frame, self._rackReferenceSet[1][0], self._rackReferenceSet[1][1], (0, 0, 255), 3)
            if step_predict[2] == 0:
                cv2.rectangle(frame, self._rackReferenceSet[2][0], self._rackReferenceSet[2][1], (0, 0, 255), 3)
            if key == ord("q"):
                break
            cv2.imshow("Smart Shelf", frame)

    def preprocess_prediction_images(self, imageSet):
        imageList = []
        for image in imageSet:
            image=cv2.resize(image,(32,64),interpolation=cv2.INTER_AREA)
            opencv_imageData = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_im=Image.fromarray(opencv_imageData)
            image=img_to_array(pil_im)
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
tt = Presentation("../Demo_With_People.mp4",400, 500)
tt.process_extract()
# tt.process_save()
tt.screen_play()
