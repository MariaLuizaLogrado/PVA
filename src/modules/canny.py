import cv2
import numpy as np

class Canny:
    def __init__(self, mouth, nose, left_eye, right_eye):
        self.mouth = mouth
        self.nose = nose
        self.left_eye = left_eye
        self.right_eye = right_eye

    def edge_detection(self):
        self.mouth_edge = cv2.Canny(self.mouth, 150, 200)
        self.nose_edge = cv2.Canny(self.nose, 150, 200)
        self.left_eye_edge = cv2.Canny(self.left_eye, 150, 200)
        self.right_eye_edge = cv2.Canny(self.right_eye, 150, 200)

    def coordenates(self):
        mouth_coord = np.argwhere(self.mouth_edge == 255)
        nose_coord = np.argwhere(self.nose_edge == 255)
        left_eye_coord = np.argwhere(self.left_eye_edge == 255)
        right_eye_coord = np.argwhere(self.right_eye_edge == 255)

        self.mouth_dict = {tuple(coord): i for i, coord in enumerate(mouth_coord)}
        self.nose_dict = {tuple(coord): i for i, coord in enumerate(nose_coord)}
        self.left_eye_dict = {tuple(coord): i for i, coord in enumerate(left_eye_coord)}
        self.right_eye_dict = {tuple(coord): i for i, coord in enumerate(right_eye_coord)}