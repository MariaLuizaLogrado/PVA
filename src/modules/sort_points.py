import matplotlib.pyplot as plt
import numpy as np

class SortPoints:
    def __init__(self, new_longest_path_nose, new_longest_path_mouth,  new_longest_path_left_eye, new_longest_path_right_eye,
                 nodes_nose, nodes_mouth, nodes_left_eye, nodes_right_eye,
                 nose_dict, mouth_dict, left_eye_dict, right_eye_dict):
        
        self.new_longest_path_nose = new_longest_path_nose
        self.new_longest_path_mouth = new_longest_path_mouth
        self.new_longest_path_left_eye = new_longest_path_left_eye
        self.new_longest_path_right_eye = new_longest_path_right_eye

        self.nodes_nose = nodes_nose
        self.nodes_mouth = nodes_mouth
        self.nodes_left_eye = nodes_left_eye
        self.nodes_right_eye = nodes_right_eye

        self.nose_dict = nose_dict
        self.mouth_dict = mouth_dict
        self.left_eye_dict = left_eye_dict
        self.right_eye_dict = right_eye_dict

    def access_coord(self, indices, listas, dic_coord):
        points_longest_path = []
        for i, sub_indices in enumerate(indices):
            lista = listas[i]
            points_longest_path.append([lista[idx] for idx in sub_indices])

        coord_longest_path = []
        for lista in points_longest_path:
            points = [dic_coord[i] for i in lista if i in dic_coord]
            coord_longest_path.append(points)
        return coord_longest_path
    
    def sort_points(self, lista):
        # Função para compare points
        def compare(p1, p2):
            if p1[0] == p2[0]:  # Se as coordenadas X forem iguais, compare as coordenadas Y
                return p1[1] < p2[1]
            return p1[0] < p2[0]
        
        # Verificar o first e o último ponto da lista
        first = lista[0]
        last = lista[-1]
        
        if compare(last, first):  # Se o último ponto for "menor" que o first, inverte a lista
            lista.reverse()
        
        return lista
    
    def compute_all_coordenates(self):
        # Acessar as coordenadas
        coord_nose = self.access_coord(self.new_longest_path_nose, self.nodes_nose, self.nose_dict)
        coord_mouth = self.access_coord(self.new_longest_path_mouth, self.nodes_mouth, self.mouth_dict)
        coord_left_eye = self.access_coord(self.new_longest_path_left_eye, self.nodes_left_eye, self.left_eye_dict)
        coord_right_eye = self.access_coord(self.new_longest_path_right_eye, self.nodes_right_eye, self.right_eye_dict)

        # Ordenar os pontos
        self.sorted_coord_nose = [self.sort_points(coords) for coords in coord_nose]
        self.sorted_coord_mouth = [self.sort_points(coords) for coords in coord_mouth]
        self.sorted_coord_left_eye = [self.sort_points(coords) for coords in coord_left_eye]
        self.sorted_coord_right_eye = [self.sort_points(coords) for coords in coord_right_eye]

def plot_sorted_points(sorted, name):
    # Plotando os pontos e conectando-os
    plt.figure(figsize=(12, 10))
    colors = ['blue', 'red', 'green', 'gray', 'orange', 'black', 'purple', 'pink', 'brown', 'cyan', 'yellow', 'magenta']

    for grupo, color in zip(sorted, colors):
        x_vals = [p[0] for p in grupo]
        y_vals = [p[1] for p in grupo]
        
        # Plota os pontos
        plt.plot(x_vals, y_vals, marker='o', markersize=5, color=color)
        
        # Adiciona as setas para indicar a ordem dos pontos
        for i in range(len(grupo) - 1):
            plt.annotate('', xy=(x_vals[i+1], y_vals[i+1]), xytext=(x_vals[i], y_vals[i]),
                        arrowprops=dict(facecolor=color, edgecolor=color, arrowstyle='->', lw=2))

    # Personaliza o gráfico
    plt.title('Visualização da Ordem dos Pontos')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.savefig(f'./exemplos/07_sorted_points_{name}.png')
    plt.show()
