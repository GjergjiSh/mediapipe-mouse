import cv2
import sys
from numpy.lib import utils
import Hands
import autopy
import numpy as np
import Utils as utls

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

if __name__ == '__main__':
    cam =  Camera()
    detector = Hands.HandDetector()

    screen_w, screen_h = autopy.screen.size()
    print(screen_h, screen_w)
    screen_w -= 1
    screen_h -= 1
    downsize_var = 100 #pixels


    while True:
        frame = cam.capture_frame()

        utls.draw_rectangle(
            frame,
            (downsize_var,downsize_var),
            (cam.cap_w-downsize_var, cam.cap_h-downsize_var),
            utls.PURPLE,
            thickness=3)

        (cx, cy, click) = detector.click_detected(frame)

        if ((cx is not None) and (cy is not None)):
            icx = np.interp(cx, (downsize_var, cam.cap_w-downsize_var), (0,screen_w))
            icy = np.interp(cy, (downsize_var, cam.cap_h-downsize_var), (0,screen_h))

            autopy.mouse.move(icx,icy)

        #print(cx, cy, click)
        cam.display_frame(frame)
