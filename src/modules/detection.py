import cv2

class Detection:
    def __init__(self, gray_image):
        self.gray_image = gray_image
        self.face = None
        self.nose = None
        self.mouth = None
        self.left_eye = None
        self.right_eye = None

    def detect_faces(self):
        face_cascade = cv2.CascadeClassifier('models\haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(self.gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 50))
        for (x, y, w, h) in faces:
            self.face = self.gray_image[y:y+h, x:x+w]

    def detect_nose(self):
        nose_cascade = cv2.CascadeClassifier('models\haarcascade_mcs_nose.xml')
        nose_model = nose_cascade.detectMultiScale(self.face, scaleFactor=1.1, minNeighbors=5, minSize=(40, 50))
        for (x, y, w, h) in nose_model:
            self.nose = self.face[y:y+h, x:x+w]

    def detect_mouth(self):
        mouth_cascade = cv2.CascadeClassifier('models\haarcascade_mcs_mouth.xml')
        # mouth_model = mouth_cascade.detectMultiScale(self.face, scaleFactor=1.5, minNeighbors=15, minSize=(40, 50))
        mouth_model = mouth_cascade.detectMultiScale(self.face, scaleFactor=1.1, minNeighbors=5, minSize=(40, 50))
        for (x, y, w, h) in mouth_model:
            self.mouth = self.face[y:y+h, x:x+w]

    def detect_eyes(self):
        eyes_cascade = cv2.CascadeClassifier('models\haarcascade_eye.xml')
        eyes_model = eyes_cascade.detectMultiScale(self.face, scaleFactor=1.1, minNeighbors=5, minSize=(40, 50))
        # Verificar se ao menos dois olhos foram detectados
        if len(eyes_model) >= 2:
            # Ordena os olhos pela posição horizontal (x), para tentar separar em esquerdo e direito
            eyes_model = sorted(eyes_model, key=lambda x: x[0])
            
            # Assume que o primeiro é o olho esquerdo e o segundo é o olho direito
            lx, ly, lw, lh = eyes_model[0]
            rx, ry, rw, rh = eyes_model[1]
            
            self.left_eye = self.face[ly:ly+lh, lx:lx+lw]
            self.right_eye = self.face[ry:ry+rh, rx:rx+rw]