from ctypes import ArgumentError
import HandDetector as hdet
import Camera as cam
import pyautogui
import Utils as utls
import numpy as np
import sys
import argparse


def main(dvar,svar,verbose,display):
    pyautogui.PAUSE = 0

    camera =  cam.Camera()
    detector = hdet.HandDetector()
    screen_w, screen_h = pyautogui.size()
    print('Screen size: {}x{}'.format(screen_w, screen_h))

    # if your screen is 1280x720p you can't move the mouse to the point (1280, 720),
    # the "maximum" point that it accepts
    # it's actually (screenWidth - 1, screenHeight - 1) or (1279, 719)p in this case.
    screen_w -= 1
    screen_h -= 1

    prev_locx, prev_locy = 0,0
    curr_locx, curr_locy = 0,0

    print('Virtual Controller Area: {}x{}'.format(camera.cap_w-dvar, camera.cap_h-dvar))

    while True:
        frame = camera.capture_frame()

        utls.draw_rectangle(
            frame,
            (dvar,dvar),
            (camera.cap_w-dvar, camera.cap_h-dvar),
            utls.PURPLE,
            thickness=3)

        (cx, cy, click) = detector.track_fingers(frame)
        if verbose:
            print(cx,cy,click)

        if ((cx is not None) and (cy is not None)):

            # Map downsized rectangle pixel range to screen range
            icx = np.interp(cx, (dvar, camera.cap_w-dvar), (0,screen_w))
            icy = np.interp(cy, (dvar, camera.cap_h-dvar), (0,screen_h))

            # Smoothen mapped values to avoid shaky mouse
            curr_locx = prev_locx + (icx - prev_locx) / svar
            curr_locy = prev_locy + (icy - prev_locy) / svar

            pyautogui.moveTo(screen_w-curr_locx,curr_locy)

            if click:
                pyautogui.mouseDown(button='left')
            else:
               pyautogui.mouseUp(button='left')

            # Track smoothed values
            prev_locx, prev_locy = curr_locx,curr_locy

        #print(cx, cy, click)
        if display:
            camera.display_frame(frame)


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        '-dvar',
        metavar='--dvar',
        type=int,
        default=75,
        help='Set size of virtual control area relative to screen size' )

    arg_parser.add_argument(
        '-svar',
        metavar='--svar',
        default=5,
        type=float,
        help='Used to smoothen mouse movement. The higher the value, the smoother but slower movement of the mouse pointer' )

    arg_parser.add_argument(
        '-verbose',
        metavar='--verbose',
        type=bool,
        default=False,
        help='Print Coordinates of mouse for debugging')

    arg_parser.add_argument(
        '-display',
        metavar='--display',
        type=bool,
        default=True,
        help='Turn video display on/off' )

    args = arg_parser.parse_args()


    dvar = args.dvar
    svar = args.svar
    verbose = args.verbose
    display = args.display

    try:
        main(dvar,svar,verbose,display)
    except KeyboardInterrupt:
        print('Exiting...')
        sys.exit(-1)