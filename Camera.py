import cv2
import sys
import Hands

class Camera():
    camera_index : int
    video_cap : cv2.VideoCapture

    def __init__(self, camera_index=0, cap_w=640, cap_h=480) -> None:
        self.camera_index = camera_index,
        self.video_cap = cv2.VideoCapture(0)

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

if __name__ == '__main__':
    cam =  Camera(camera_index=0)
    detector = Hands.HandDetector()

    while True:
        frame = cam.capture_frame()
        detector.click_detected(frame)

        cam.display_frame(frame)
