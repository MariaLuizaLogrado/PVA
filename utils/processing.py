######################################################################################################
## STEP 2: USANDO HAAR CASCADE PARA DETECTAR CARACTERÍSTICAS FACIAIS
######################################################################################################

# Função que recebe uma imagem colorida como entrada e retorna a mesma imagem convertida para escala de cinza
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Converter a imagem de um espaço de cores RGB para escala de cinza
    return gray

# Função que usará um modelo para detectar o rosto de uma pessoa
def detect_faces(image, face_classifier):
    faces = face_classifier.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 50))
    return faces

# Função que usará um modelo para detectar os olhos de uma pessoa
def detect_eyes(image, eyes_classifier):
    eyes = eyes_classifier.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 50))
    return eyes

# Função que usará um modelo para detectar o nariz de uma pessoa
def detect_noses(image, nose_classifier):
    noses = nose_classifier.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 50))
    return noses

# Função que usará um modelo para detectar a boca de uma pessoa
def detect_mouths(image, mouth_classifier):
    mouths = mouth_classifier.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 50))
    return mouths

# Função que irá nos retornar os contornos de uma imagem
def apply_canny(image):
    edges = cv2.Canny(image, 150, 200)
    return edges

# Função que plotará imagens
def plots(figura, title=''):
    plt.figure(figsize=(20,10))
    plt.imshow(figura, cmap='gray')
    plt.axis('off')
    plt.title(title)
    plt.show()

# Função que aleatoriza 
def retirando_pixels(mEdges, thresh):
    lCoord = [] # Lista para armazenar as coordenddas dos pixels de interesse

    for i in range(mEdges.shape[0]):
        for j in range(mEdges.shape[1]):
            if mEdges[i][j] == 255: # Verificando se o ponto encontrado corresponde ao pixel 255
                lCoord.append((i,j)) # Adicionando a coordenada desse pixel encontrado no lCoord
    mainCoord = lCoord.copy() # Copiando a lista de coordenadas dos pontos (coordenadas dos pixels de interesse)
    random.shuffle(lCoord) # Aleatorizando a ordem das coordenadas dos pontos

    times = thresh # Definando um limiar para zerarmos os pixels

    #for i,t in zip(lCoord, range(times)): # Zipamos a lista de coordenadas com o limiar para definirmos um 'critério de parada' no laço
    #        mEdges[i[0]][i[1]] = 0 # Zerando os pixels 255

    return mEdges, mainCoord

# Função que fará o processamento de imagem e nos retornará os contornos das características
def process_image(image_path, face_classifier, eyes_classifier, nose_classifier, mouth_classifier):
    image = cv2.imread(image_path) # Lendo a imagem
    processed_image = preprocess_image(image) # Pré-processando a imagem (convertendo para escala de cinza)
    faces = detect_faces(processed_image, face_classifier) # Detectando o rosto na imagem

    for (x, y, w, h) in faces:
        face_roi = processed_image[y:y+h, x:x+w] # Recortando a região de interesse (Roi) do rosto
        noses = detect_noses(face_roi, nose_classifier) # Detectando o nariz na região de interesse do rosto

        for (nx, ny, nw, nh) in noses:
            nose_roi = face_roi[ny:ny+nh, nx:nx+nw] # Recortando a região de interesse (Roi) do nariz
            # plots(nose_roi, title="ROI Nariz") # Plotando a região de interesse do nariz
            nariz_contornos = apply_canny(nose_roi) # Aplicando o detector de bordas de Canny na região de interesse do nariz
            # plots(nariz_contornos, title="Contornos com Canny")
            newNoseEdges, mainCoord_nose = retirando_pixels(nariz_contornos, 100)

    return nariz_contornos, mainCoord_nose
