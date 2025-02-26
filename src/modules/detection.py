import cv2
import time

class FaceFeature:
    def __init__(self, img, x, y, w, h):
        self.img = img
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class Detection:
    def __init__(self, gray_image):
        self.gray_image = gray_image
        self.face = None
        self.nose = None
        self.mouth = None
        self.left_eye = None
        self.right_eye = None

    def detect_face(self):
        face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(self.gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40,50))

        for (x,y,w,h) in faces:
            return FaceFeature(self.gray_image[y:y+h, x:x+w], x, y, w, h)
        
        return None
        
    def detect_nose(self):
        nose_cascade = cv2.CascadeClassifier('models/haarcascade_mcs_nose.xml')
        noses = nose_cascade.detectMultiScale(self.face.img[self.right_eye.y:(self.mouth.y + self.mouth.h), self.left_eye.x:(self.right_eye.x+self.right_eye.w)], scaleFactor=1.1, minNeighbors=5, minSize=(40,50))
        for (x,y,w,h) in noses:
            x += self.left_eye.x
            y += self.right_eye.y
            return FaceFeature(self.face.img[y:y+h, x:x+w], x, y, w, h)

        return None
    
    def detect_mouth(self):
        mouth_cascade = cv2.CascadeClassifier('models/haarcascade_mcs_mouth.xml')
        mouths = mouth_cascade.detectMultiScale(self.face.img[self.left_eye.y+self.left_eye.h:, :], scaleFactor=1.1, minNeighbors=5, minSize=(40,50))
        for (x,y,w,h) in mouths:
            y += self.left_eye.y + self.left_eye.h
            return FaceFeature(self.face.img[y:y+h, x:x+w], x, y, w, h)

        
        return None #, face_without_mouth
    
    def detect_eyes(self):
        eye_cascade = cv2.CascadeClassifier('models/haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(self.face.img, scaleFactor=1.1, minNeighbors=5, minSize=(40,50))
        if len(eyes) >= 2:
            eyes = sorted(eyes, key=lambda x: x[0])
            x1, y1, w1, h1 = eyes[0]
            x2, y2, w2, h2 = eyes[1]
            return FaceFeature(self.face.img[y1:y1+h1, x1:x1+w1], x1, y1, w1, h1), FaceFeature(self.face.img[y2:y2+h2, x2:x2+w2], x2, y2, w2, h2)

        else:
            print("Olhos não detectados")
        
        return None, None


        
    def compute_all_detections(self):

        self.face = self.detect_face()
        if self.face is None:
            print("Face não detectada")
            return
        
        self.left_eye, self.right_eye = self.detect_eyes()
        if self.left_eye is None or self.right_eye is None:
            print("Olhos não detectados")
            return


        self.mouth = self.detect_mouth()
        if self.mouth is None:
            print("Boca não detectada")
            return
        

        self.nose = self.detect_nose()
        if self.nose is None:
            print("Nariz não detectado")
            return

        # print(f"Face detection: {end_face - start}\nNose detection: {end_nose - end_face}\nMouth detection: {end_mouth - end_nose}\nEye detection: {end_eye - end_mouth}")

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