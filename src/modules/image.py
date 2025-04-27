import cv2
from PIL import Image as PILImage

class Image:
    def __init__(self, path=""):
        self.path = path
        self.image = None
        self.gray_image = None
        self.open = None

    def reading_image(self):
        self.open = PILImage.open(self.path)
        # i want to save as png
        # self.open.save(self.path.replace('.jpg', '.png'))
        self.image = cv2.imread(self.path)
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def set_image(self, image):
        self.image = image
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

import matplotlib.pyplot as plt
def display_image(image, name="01_example_image"):
    dir = "exemplos"
    image.save(dir + "/" + name + ".png")



    