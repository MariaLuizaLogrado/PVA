import numpy as np 

class AdjacencyMatrix:
    def __init__(self, mouth_dict, nose_dict, left_eye_dict, right_eye_dict):
        self.mouth_dict = mouth_dict
        self.nose_dict = nose_dict
        self.left_eye_dict = left_eye_dict
        self.right_eye_dict = right_eye_dict

    @staticmethod
    def in_same_row_or_column(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return x1 == x2 or y1 == y2

    @staticmethod
    def in_diagonal(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return abs(x1 - x2) == abs(y1 - y2)

    @staticmethod
    def absolute_distance(point1, point2):
        x_dist = abs(point1[0] - point2[0])
        y_dist = abs(point1[1] - point2[1])
        return x_dist + y_dist

    def neighborhood(self, point1, point2, threshold):
        return self.absolute_distance(point1, point2) <= threshold

    def check_neighborhood(self, points, row_col_threshold = 1, diagonal_threshold = 2):
        points_list = list(points.items())
        connections = {}  # Dicionário para armazenar as ligações entre os points
        for id1, _ in points_list:
            connections[id1] = []  # Inicializa a lista de ligações para o ponto atual

        for id1, ponto1 in points_list:
            for id2, ponto2 in points_list[id1+1:]:
                # print(ponto1, ponto2)
                if self.in_same_row_or_column(ponto1, ponto2):  # Verificando se os points estão na mesma linha/coluna
                    if self.neighborhood(ponto1, ponto2, row_col_threshold):  # Verificando se as distâncias estão dentro do limite imposto
                        connections[id1].append(id2)  # Adicionar a ligação entre os points ao dicionário de ligações
                        connections[id2].append(id1)  # Adicionar a ligação entre os points ao dicionário de ligações

        for id1, ponto1 in points_list:
            for id2, ponto2 in points_list[id1+1:]:
                if self.in_diagonal(ponto1, ponto2):  # Evitar calcular a distância do ponto com ele mesmo
                    if self.neighborhood(ponto1, ponto2, diagonal_threshold):  # Verificando se as distâncias estão dentro do limite imposto
                        connections[id1].append(id2)  # Adicionar a ligação entre os points ao dicionário de ligações
                        connections[id2].append(id1)  # Adicionar a ligação entre os points ao dicionário de ligações

        return connections
    
    def adjacency_matrix(self, connections):
        n = max(connections.keys()) + 1
        matrix = np.zeros((n, n))

        for i, neighbors in connections.items():
            for j in neighbors:
                matrix[i, j] = 1
        
        return matrix


    def compute_all_matrices(self):
        # Computar as matrizes de adjacência para cada componente
        mouth_connections = self.check_neighborhood(self.mouth_dict)
        self.mouth_adjacency_matrix = self.adjacency_matrix(mouth_connections)

        nose_connections = self.check_neighborhood(self.nose_dict)
        self.nose_adjacency_matrix = self.adjacency_matrix(nose_connections)

        left_eye_connections = self.check_neighborhood(self.left_eye_dict)
        self.left_eye_adjacency_matrix = self.adjacency_matrix(left_eye_connections)

        right_eye_connections = self.check_neighborhood(self.right_eye_dict)
        self.right_eye_adjacency_matrix = self.adjacency_matrix(right_eye_connections)