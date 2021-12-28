import mediapipe as mp
import cv2

GREEN = (0,255,0)
RED = (0,0,255)
BLUE = (255,0,0)
WHITE = (255,255,255)


def draw_line(img, p1 , p2,  color, thickness) -> None:
    cv2.line(img, p1, p2, color, thickness)

def draw_circle(img, center ,color, thickness)-> None:
    cv2.circle(img, center, thickness, color, cv2.FILLED)


def draw_hand_landmarks(img, results) -> None:
    for hand_lms in results.multi_hand_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            img,
            hand_lms,
            mp.solutions.hands.HAND_CONNECTIONS
        )