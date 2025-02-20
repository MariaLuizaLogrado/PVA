import cv2
import time

class Detection:
    def __init__(self, gray_image):
        self.gray_image = gray_image
        self.face = None
        self.nose = None
        self.mouth = None
        self.left_eye = None
        self.right_eye = None

    def detect(self, eyes_detection, path_model, gray_image, scale_factor, min_neighbors, min_size):
        if eyes_detection:
            cascade = cv2.CascadeClassifier(path_model)
            output = cascade.detectMultiScale(gray_image, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=min_size)
            if len(output) >= 2:
                output = sorted(output, key=lambda x: x[0])
                x1, y1, w1, h1 = output[0]
                x2, y2, w2, h2 = output[1]

                return gray_image[y1:y1+h1, x1:x1+w1], gray_image[y2:y2+h2, x2:x2+w2]

        else:
            cascade = cv2.CascadeClassifier(path_model)
            output = cascade.detectMultiScale(gray_image, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=min_size)
            for (x, y, w, h) in output:
                print(x, y, w, h) 
                return gray_image[y:y+h, x:x+w]
        
    def compute_all_detections(self):
        start = time.time()
        self.face = self.detect(False, 'models/haarcascade_frontalface_default.xml', self.gray_image, 1.3, 5, (30, 30))
        end_face = time.time()
        self.nose = self.detect(False, 'models/haarcascade_mcs_nose.xml', self.face, 1.1, 5, (40, 50))
        end_nose = time.time()  
        self.mouth = self.detect(False, 'models/haarcascade_mcs_mouth.xml', self.face, 1.1, 5, (40, 50))
        end_mouth = time.time()
        self.left_eye, self.right_eye = self.detect(True, 'models/haarcascade_eye.xml', self.face, 1.1, 5, (40, 50))
        end_eye = time.time()
        print(f"Face detection: {end_face - start}\nNose detection: {end_nose - end_face}\nMouth detection: {end_mouth - end_nose}\nEye detection: {end_eye - end_mouth}")

def plot_detection(image, detection_face, detection_nose, detection_mouth, detection_left_eye, detection_right_eye):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if detection_face is not None:
        x, y, w, h = detection_face
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    if detection_nose is not None:
        x, y, w, h = detection_nose
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    if detection_mouth is not None:
        x, y, w, h = detection_mouth
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    if detection_left_eye is not None:
        x, y, w, h = detection_left_eye
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 2)
    if detection_right_eye is not None:
        x, y, w, h = detection_right_eye
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 2)
        return image