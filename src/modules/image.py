import cv2

class Image:
    def __init__(self, path):
        self.path = path
        self.image = None
        self.gray_image = None

    def reading_image(self):
        self.image = cv2.imread(self.path)
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

import matplotlib.pyplot as plt
def display_image(image):
    plt.figure(figsize=(12, 10))
    plt.imshow(image)
    plt.axis('off')
    plt.show()

    