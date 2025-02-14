
import matplotlib.pyplot as plt
from scipy.sparse.csgraph import connected_components

class ConnectedComponents:
    def __init__(self, nose_adjacency_matrix, mouth_adjacency_matrix, left_eye_adjacency_matrix, right_eye_adjacency_matrix):
        self.nose_adjacency_matrix = nose_adjacency_matrix
        self.mouth_adjacency_matrix = mouth_adjacency_matrix
        self.left_eye_adjacency_matrix = left_eye_adjacency_matrix
        self.right_eye_adjacency_matrix = right_eye_adjacency_matrix
        self.n_components = None
        self.labels = None


    def compute_all_components(self):
        self.nose_n_components, self.nose_labels = connected_components(self.nose_adjacency_matrix)
        self.mouth_n_components, self.mouth_labels = connected_components(self.mouth_adjacency_matrix)
        self.left_eye_n_components, self.left_eye_labels = connected_components(self.left_eye_adjacency_matrix)
        self.right_eye_n_components, self.right_eye_labels = connected_components(self.right_eye_adjacency_matrix)

    def main_cc(self, labels):
        connected_components_labels = {}

        for i in range(len(labels)):
            if labels[i] not in connected_components_labels:
                connected_components_labels[labels[i]] = [i]
            else:
              connected_components_labels[labels[i]].append(i)
    

        componentNodeCount = {}

        for i in connected_components_labels.keys(): 
            componentNodeCount[i] = len(connected_components_labels[i]) 

        
        maxNodeComponent = max(componentNodeCount, key=componentNodeCount.get)

        componentsToRemove = []

        for key in componentNodeCount.keys(): 
            if componentNodeCount[key] < round(0.2 * componentNodeCount[maxNodeComponent]): 
                componentsToRemove.append(key) 


        for key in componentsToRemove: 
            del componentNodeCount[key]

        listMainComponents = componentNodeCount.keys()

        
        dicMainComponents = {}

        for key in listMainComponents: 
            dicMainComponents[key] = connected_components_labels[key] 

        return dicMainComponents
    
    def compute_main_cc(self):
        self.dic_main_nose_cc = self.main_cc(self.nose_labels)
        self.dic_main_mouth_cc = self.main_cc(self.mouth_labels)
        self.dic_main_left_eye_cc = self.main_cc(self.left_eye_labels)
        self.dic_main_right_eye_cc = self.main_cc(self.right_eye_labels)



def highlight_components(carac_dict, dic_main_carac_cc):
    '''
    Function to plot the main connected components of the face features
    
    Parameters:
    carac_dict (dict): dictionary containing the coordinates of the face features
    dic_main_carac_cc (dict): dictionary containing the main connected components of the face features
    
    Example:
    highlight_components(results[0][2].left_eye_dict, results[0][4].dic_main_left_eye_cc)
    '''
    main_coord = list(carac_dict.values())
    colors = ['blue', 'red', 'green', 'gray', 'orange', 'black', 'purple', 'pink', 'brown', 'cyan', 'yellow', 'magenta']
    plt.figure(figsize=(12, 10))

    for color,label in enumerate(dic_main_carac_cc.keys()): # Iterar sobre as chaves do dicionário que contém os principais componentes conectados
        for idx in dic_main_carac_cc[label]: # Iterar sobre os nós dos componentes conectados
            i, j = main_coord[idx] # Obter as coordenadas dos pontos
            # print(i, j, idx)
            plt.scatter(i, j, color=colors[color%len(colors)])  # Plotar os pontos filtrados

    plt.title("Pontos das Componentes Conectadas")
    plt.xlabel("Coluna")
    plt.ylabel("Linha")
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.show()