import cv2

refPt = []


class TrainSetGeneartor(object):
    def __init__(self, video_path, windowWidth, windowHeight):
        self.__video = cv2.VideoCapture(video_path)
        self.__rack_reference_set = []
        self.__croping = False
        self.windowHeight = windowHeight
        self.windowWidth = windowWidth
        self.__first_frame = self._get_first_frame()

    def _get_first_frame(self):
        success, frame = self.__video.read()
        return cv2.resize(frame, (self.windowWidth, self.windowHeight), interpolation=cv2.INTER_AREA)

    def _mouse_handler(self, event, x, y, flags, params):
        global refPt
        if event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(x, y)]
            self.__croping = True
        elif event == cv2.EVENT_LBUTTONUP:
            refPt.append((x, y))
            self.__croping = False
            cv2.rectangle(self.__first_frame, refPt[0], refPt[1], (0, 255, 0), 2)
            cv2.imshow(params[0], self.__first_frame)

    def _generate_dataset_for_a_rack(self, rackName):
        clone = self.__first_frame.copy()
        cv2.namedWindow(rackName)
        cv2.setMouseCallback(rackName, self._mouse_handler, param=[rackName])
        while True:
            cv2.imshow(rackName, self.__first_frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("r"):
                self.__first_frame = clone.copy()
            elif key == ord("c"):
                self.__rack_reference_set.append(refPt)
                break

    def _get_frame_set(self, frame):
        frameSet = []
        for refPt in self.__rack_reference_set:
            cropped_frame = frame[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            frameSet.append(cropped_frame)
        return frameSet

    def _write_to_disk(self, croppedFrameSet, count):
        for index, frame in enumerate(croppedFrameSet):
            cv2.imwrite("rack" + str(index + 1) + "/frame" + str(count) + ".jpg", frame)

    def _show_images(self, croppedFrameSet):
        for index, frame in enumerate(croppedFrameSet):
            cv2.imshow("rack" + str(index + 1), frame)
            if cv2.waitKey(1) and 0xFF == ord("q"):
                break

    def _crop_and_save(self):
        count = 0
        while 1:
            success, frame = self.__video.read()
            if not success:
                break
            frame = cv2.resize(frame, (self.windowWidth, self.windowHeight), interpolation=cv2.INTER_AREA)
            croppend_frame_set = self._get_frame_set(frame)
            self._write_to_disk(croppend_frame_set, count)
            self._show_images(croppend_frame_set)
            count += 1

    def process(self):
        self._generate_dataset_for_a_rack(rackName="rack 1")
        self._generate_dataset_for_a_rack(rackName="rack 2")
        self._generate_dataset_for_a_rack(rackName="rack 3")
        self._crop_and_save()


tt = TrainSetGeneartor("video.mp4", 350, 512)
tt.process()
