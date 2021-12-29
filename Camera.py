import cv2
import sys

class Camera():
    camera_index : int
    video_cap : cv2.VideoCapture
    cap_w : int
    cap_h : int

    def __init__(self, camera_index=0, cap_w=640, cap_h=480) -> None:
        self.camera_index = camera_index,
        self.video_cap = cv2.VideoCapture(0)

        self.cap_w = cap_w
        self.cap_h = cap_h

        self.video_cap.set(3,cap_w)
        self.video_cap.set(4,cap_h)


    def capture_frame(self):
        ret, frame = self.video_cap.read()
        if ret:
            return frame
        else:
            print('Failed to capture frame')

        return None

    def display_frame(self, frame) -> None:
        if frame is not None:
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) == ord('q'):
                print('Exiting...')
                sys.exit(0)
        else:
            print('Camera frame is empty')
            sys.exit(-1)