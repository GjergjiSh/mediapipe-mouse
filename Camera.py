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

    #if your screen is 1280x720p you can't move the mouse to the point (1280, 720),
    # the "maximum" point that it accepts
    # it's actually (screenWidth - 1, screenHeight - 1) or (1279, 719)p in this case.
    screen_w -= 1
    screen_h -= 1

    prev_locx, prev_locy = 0,0
    curr_locx, curr_locy = 0,0

    downsize_var = 100 #pixels
    smooth_var = 7

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

            # Map downsized rectangle pixel range to screen range
            icx = np.interp(cx, (downsize_var, cam.cap_w-downsize_var), (0,screen_w))
            icy = np.interp(cy, (downsize_var, cam.cap_h-downsize_var), (0,screen_h))

            # Smoothen mapped values to avoid shaky mouse
            curr_locx = prev_locx + (icx - prev_locx) / smooth_var
            curr_locy = prev_locy + (icy - prev_locy) / smooth_var

            autopy.mouse.move(curr_locx,curr_locy)

            if click:
                autopy.mouse.click()

            # Track smoothed values
            prev_locx, prev_locy = curr_locx,curr_locy

        #print(cx, cy, click)
        cam.display_frame(frame)
