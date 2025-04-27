import cv2
import numpy as np

class Canny:
    def __init__(self, mouth, nose, left_eye, right_eye):
        self.mouth = mouth
        self.nose = nose
        self.left_eye = left_eye
        self.right_eye = right_eye

    def edge_detection(self, image):
        return cv2.Canny(image, 150, 200)
    
    def coordenates(self, edge):
        coord = np.argwhere(edge == 255)

        return {i: tuple(coord)[::-1] for i, coord in enumerate(coord)}
    
    def compute_all_edges(self):
        self.mouth_edge = self.edge_detection(self.mouth)
        self.nose_edge = self.edge_detection(self.nose)
        self.left_eye_edge = self.edge_detection(self.left_eye)
        self.right_eye_edge = self.edge_detection(self.right_eye)

        self.mouth_dict = self.coordenates(self.mouth_edge)
        self.nose_dict = self.coordenates(self.nose_edge)
        self.left_eye_dict = self.coordenates(self.left_eye_edge)
        self.right_eye_dict = self.coordenates(self.right_eye_edge)

def display_canny(image, name="example_image"):
    dir = "exemplos"
    cv2.imwrite(dir + "/" + name + ".png", image)