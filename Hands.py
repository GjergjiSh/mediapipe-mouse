import cv2
import mediapipe as mp
import math

class HandDetector():
    detection_confidence : float
    track_confidence : float
    
    max_hands : int
    hand : mp.solutions.hands.Hands

    line_color : tuple
    dot_color : tuple
    line_thickness : float
    dot_thickness : float

    click_distance : float

    def __init__(self, detection_confidence=0.5, track_confidence=0.2, click_distance=25) -> None:
        self.max_hands = 1
        self.click_distance = click_distance        

        self.detection_confidence = detection_confidence
        self.track_confidence = track_confidence

        self.mp_hand_solution = mp.solutions.hands
        self.hand = mp.solutions.hands.Hands(
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.track_confidence
        )

        self.dot_color = (0,150,255)
        self.line_color = (124,55,174)
        self.line_thickness = 8
        self.dot_thickness = 5

    def click_detected(self, img, draw_line=True, draw_all_landmarks=False) -> bool:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hand.process(img_rgb)
        hand_landmark_list = []

        h , w , c = img.shape

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]

            for id, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x*w), int(lm.y*h)
                hand_landmark_list.append([id, cx, cy])
            
            if (len(hand_landmark_list) != 0):

                # thumb coordiantes
                l_x1, l_y1 = hand_landmark_list[4][1], hand_landmark_list[4][2]
                # pointer finger coordinates
                l_x3, l_y3 = hand_landmark_list[8][1], hand_landmark_list[8][2]
                # center between pointer finger and thumb
                cx , cy = ((l_x1 + l_x3) // 2) , ((l_y1 + l_y3) // 2)

                finger_distance = math.hypot(l_x1-l_x3, l_y1-l_y3)

                if draw_line:
                    cv2.circle(img, (l_x1,l_y1), self.dot_thickness, self.dot_color, cv2.FILLED)
                    cv2.circle(img, (l_x3,l_y3), self.dot_thickness, self.dot_color, cv2.FILLED)

                    cv2.line(img, (l_x1,l_y1), (l_x3,l_y3), self.line_color, self.line_thickness)

                    if finger_distance < self.click_distance:
                        cv2.circle(img, (cx,cy), self.dot_thickness, (0,255,0), cv2.FILLED)

                if draw_all_landmarks:
                    self.draw_all_lms(img, results)
            
                return True
        else:
            return False

    def draw_all_lms(self, img, results) -> None:
        for hand_lms in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                img, 
                hand_lms, 
                mp.solutions.hands.HAND_CONNECTIONS
             )