import cv2
import numpy as np

class Canny:
    def __init__(self, mouth, mouth_x, mouth_y,
                 nose, nose_x, nose_y,
                 left_eye, left_eye_x, left_eye_y,
                 right_eye, right_eye_x, right_eye_y
                #  mid_point 
                 ):
        self.mouth = mouth
        self.mouth_x = mouth_x
        self.mouth_y = mouth_y

        self.nose = nose
        self.nose_x = nose_x
        self.nose_y = nose_y

        self.left_eye = left_eye
        self.left_eye_x = left_eye_x
        self.left_eye_y = left_eye_y

        self.right_eye = right_eye
        self.right_eye_x = right_eye_x
        self.right_eye_y = right_eye_y

        # self.mid_point = mid_point


    def edge_detection(self, image):
        return cv2.Canny(image, 150, 200)
    
    def coordenates(self, edge, x, y):
        coord = np.argwhere(edge == 255)
        sum = np.array([y,x])
        coord_sum = coord + sum
        # print(coord_sum)

        # coord_mid = coord_sum - self.mid_point

        # print(coord_mid)

        # return {i: tuple(coord_mid)[::-1] for i, coord_mid in enumerate(coord_mid)}
        return {i: tuple(coord_sum)[::-1] for i, coord_sum in enumerate(coord_sum)}
    
    def compute_all_edges(self):
        self.mouth_edge = self.edge_detection(self.mouth)
        self.nose_edge = self.edge_detection(self.nose)
        self.left_eye_edge = self.edge_detection(self.left_eye)
        self.right_eye_edge = self.edge_detection(self.right_eye)

        self.mouth_dict = self.coordenates(self.mouth_edge, self.mouth_x, self.mouth_y)
        self.nose_dict = self.coordenates(self.nose_edge, self.nose_x, self.nose_y)
        self.left_eye_dict = self.coordenates(self.left_eye_edge, self.left_eye_x, self.left_eye_y)
        self.right_eye_dict = self.coordenates(self.right_eye_edge, self.right_eye_x, self.right_eye_y)

def display_canny(image, name="example_image"):
    dir = "exemplos"
    cv2.imwrite(dir + "/" + name + ".png", image)