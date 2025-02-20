######################################################################################################
## Etapa 0: Importando as bibliotecas necessárias
######################################################################################################
import os
import time

from concurrent.futures import ThreadPoolExecutor
from modules.image import Image, display_image
from modules.detection import Detection, plot_detection
from modules.canny import Canny
from modules.adjacency_matrix import AdjacencyMatrix
from modules.connected_components import ConnectedComponents, highlight_components
from modules.mst import MinimunSpanningTree
from modules.build_tree import BuildTree, plot_logest_path
from modules.compute_splines import ComputeSplines, plot_splines

import cv2
from typing import Optional, Dict

def initialize_camera(camera_index: int = 0) -> Optional[cv2.VideoCapture]:
    """
    Initialize the camera with error handling
    
    Parameters:
        camera_index (int): Camera device index
    Returns:
        cv2.VideoCapture or None: Initialized camera object
    """
    try:
        cam = cv2.VideoCapture(camera_index)
        if not cam.isOpened():
            print("Could not open webcam")
            return None
            
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        return cam
    except Exception as e:
        print(f"Error initializing camera: {e}")
        return None
    
def process_image(img_frame):
    try:
        start_step1 = time.time()
        print("Etapa 1: Leitura da imagem")
        img = Image()
        img.set_image(img_frame)
        end_step1 = time.time()


        # Etapa 2: Detecção de características
        print("Etapa 2: Detecção de características")
        detection = Detection(img.gray_image)
        detection.compute_all_detections()
        end_step2 = time.time()

        return detection


        # Etapa 3: Detecção de bordas
        print("Etapa 3: Detecção de bordas")
        canny = Canny(detection.mouth.img, detection.nose.img, detection.left_eye.img, detection.right_eye.img)
        canny.compute_all_edges()
        end_step3 = time.time()


        # Etapa 4: Criação das matrizes de adjacência
        print("Etapa 4: Criação das matrizes de adjacência")
        adjacency_matrix = AdjacencyMatrix(canny.mouth_dict, canny.nose_dict, canny.left_eye_dict, canny.right_eye_dict)
        adjacency_matrix.compute_all_matrices()
        end_step4 = time.time()

        # Etapa 5: Cálculo de componentes conectados para cada matriz
        print("Etapa 5: Cálculo de componentes conectados para cada matriz")
        components_results = ConnectedComponents(adjacency_matrix.nose_adjacency_matrix, adjacency_matrix.mouth_adjacency_matrix, adjacency_matrix.left_eye_adjacency_matrix, adjacency_matrix.right_eye_adjacency_matrix)
        components_results.compute_all_components()
        components_results.compute_main_cc()
        end_step5 = time.time()
        # Etapa 6: Cálculo da árvore geradora mínima
        print("Etapa 6: Cálculo da árvore geradora mínima")
        mst = MinimunSpanningTree(components_results.dic_main_nose_cc, components_results.dic_main_mouth_cc, components_results.dic_main_left_eye_cc, components_results.dic_main_right_eye_cc,
                                  adjacency_matrix.nose_adjacency_matrix, adjacency_matrix.mouth_adjacency_matrix, adjacency_matrix.left_eye_adjacency_matrix, adjacency_matrix.right_eye_adjacency_matrix)
        mst.compute_all_mst()
        end_step6 = time.time()
        # Etapa 7: Construção da árvore e poda
        print("Etapa 7: Construção da árvore e poda")
        tree = BuildTree(mst.min_trees_nose, mst.min_trees_mouth, mst.min_trees_left_eye, mst.min_trees_right_eye)
        tree.compute_all_trees()
        end_step7 = time.time()
        # Etapa 8: Splines
        print("Etapa 8: Splines")
        splines = ComputeSplines(tree.new_longest_path_nose, tree.new_longest_path_mouth, tree.new_longest_path_left_eye, tree.new_longest_path_right_eye,
                                 mst.nodes_nose, mst.nodes_mouth, mst.nodes_left_eye, mst.nodes_right_eye,
                                 canny.nose_dict, canny.mouth_dict, canny.left_eye_dict, canny.right_eye_dict,
                                 mst.idx_nose, mst.idx_mouth, mst.idx_left_eye, mst.idx_right_eye)
        splines.compute_all_splines()
        end_step8 = time.time()

        

        #print(f"Processado: {file_path}")
        print(f"Tempo1 {end_step1 - start_step1}\nTempo2 {end_step2 - end_step1}\nTempo3 {end_step3 - end_step2}\nTempo4 {end_step4 - end_step3}\nTempo5 {end_step5 - end_step4}\nTempo6 {end_step6 - end_step5}\nTempo7 {end_step7 - end_step6}\nTempo8 {end_step8 - end_step7}")
        return img, detection, canny, adjacency_matrix, components_results, mst, tree, splines

    except Exception as e:
        print(f"Erro:{e}")
        return None

    
cam = initialize_camera(0)
if cam is None:
    raise ValueError("Failed to initialize camera")

while True:
    ret, img = cam.read()
    if not ret:
        print("Failed to grab frame")
        continue

    #image = cv2.imread('./image/pedro.jpg')
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    detection = process_image(img)
    if detection is not None:
        if detection.face is not None:
            x, y, w, h = detection.face.x, detection.face.y, detection.face.w, detection.face.h
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        if detection.nose is not None:
            x, y, w, h = detection.face.x + detection.nose.x, detection.face.y + detection.nose.y, detection.nose.w, detection.nose.h
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if detection.mouth is not None:
            x, y, w, h = detection.face.x + detection.mouth.x, detection.face.y + detection.mouth.y, detection.mouth.w, detection.mouth.h
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        if detection.left_eye is not None:
            x, y, w, h = detection.face.x + detection.left_eye.x, detection.face.y + detection.left_eye.y, detection.left_eye.w, detection.left_eye.h
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)
        if detection.right_eye is not None:
            x, y, w, h = detection.face.x + detection.right_eye.x, detection.face.y + detection.right_eye.y, detection.right_eye.w, detection.right_eye.h
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)

    cv2.imshow("Webcam", img)

    if cv2.waitKey(100) & 0xff == 27:  # ESC key
        break