from extract_rack import TrainSetGeneartor as ts
import cv2

class Presentation(ts):
    def __init__(self, videoPath, windowWidth, windowHeight):
        ts.__init__(self,videoPath, windowWidth, windowHeight)

    def extract(self):
        self.process_extract()

    def screen_play(self):
        # count = 0
        while 1:
            success, frame = self._video.read()
            # croppendFrameSet = self._get_frame_set(frame)
            #(rack1,rack2,rack3)=model.predict(cropedFrameSet)

            if not success:
                break
            frame = cv2.resize(frame, (self.windowWidth, self.windowHeight), interpolation=cv2.INTER_AREA)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("1"):
                cv2.rectangle(frame,self._rackReferenceSet[0][0],self._rackReferenceSet[0][1],(255,0,0),3)
            elif key == ord("2"):
                cv2.rectangle(frame, self._rackReferenceSet[1][0], self._rackReferenceSet[1][1], (255, 0, 0), 3)
            elif key==ord("3"):
                cv2.rectangle(frame, self._rackReferenceSet[2][0], self._rackReferenceSet[2][1], (255, 0, 0), 3)
            elif key==ord("q"):
                break
            cv2.imshow("Smart Shelf",frame)

            # self._write_to_disk(croppendFrameSet, count)
            # self._show_images(croppendFrameSet)
            # count += 1
tt=Presentation("../video.mp4", 350, 512)
tt.extract()
tt.screen_play()