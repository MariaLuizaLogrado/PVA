import numpy as np
from .catmull_rom_t import CatmullRomT
import matplotlib.pyplot as plt

class ComputeSplines:
    def __init__(self, 
                 sorted_coord_nose, sorted_coord_mouth, sorted_coord_left_eye, sorted_coord_right_eye,
                #  new_longest_path_nose, new_longest_path_mouth, new_longest_path_left_eye,  new_longest_path_right_eye, 
                #  nodes_nose, nodes_mouth, nodes_left_eye, nodes_right_eye, 
                #  nose_dict, mouth_dict, left_eye_dict, right_eye_dict,
                #  idx_nose, idx_mouth, idx_left_eye, idx_right_eye
                 ):
        
        # self.new_longest_path_nose = new_longest_path_nose
        # self.new_longest_path_mouth = new_longest_path_mouth
        # self.new_longest_path_left_eye = new_longest_path_left_eye
        # self.new_longest_path_right_eye = new_longest_path_right_eye

        # self.nodes_nose = nodes_nose
        # self.nodes_mouth = nodes_mouth
        # self.nodes_left_eye = nodes_left_eye
        # self.nodes_right_eye = nodes_right_eye

        # self.nose_dict = nose_dict
        # self.mouth_dict = mouth_dict
        # self.left_eye_dict = left_eye_dict
        # self.right_eye_dict = right_eye_dict

        # self.idx_nose = idx_nose
        # self.idx_mouth = idx_mouth
        # self.idx_left_eye = idx_left_eye
        # self.idx_right_eye = idx_right_eye
        self.sorted_coord_nose = sorted_coord_nose
        self.sorted_coord_mouth = sorted_coord_mouth
        self.sorted_coord_left_eye = sorted_coord_left_eye
        self.sorted_coord_right_eye = sorted_coord_right_eye

    def compute_splines(self, points_sorted):
        # coordenadas_novos_caminhos = {}

        # for j in range(len(new_longest_path)):

        #     indices = new_longest_path[j]
        #     filteredNos = [nodes[j][i] for i in indices]
        #     coordenadas_caminho = [dict[i] for i in filteredNos]
        #     coordenadas_novos_caminhos[idx[j]] = coordenadas_caminho
        #     print(coordenadas_novos_caminhos) 

        all_X = []
        all_Y = []
        all_control_x = []
        all_control_y = []

        # # Loop sobre cada chave em coordenadas_novos_caminhos
        # for idx, (key, value) in enumerate(coordenadas_novos_caminhos.items()):

        #     # Extraindo as coordenadas x e y
        #     coordenadas = coordenadas_novos_caminhos[key]
        #     control_x = [coord[0] for coord in coordenadas]
        #     control_y = [coord[1] for coord in coordenadas]
        #     print(control_x)

        for componente in points_sorted:

            control_x = [coord[0] for coord in componente]
            control_y = [coord[1] for coord in componente]

            # Adicionando pontos fantasmas
            control_x.insert(0, control_x[0] - 0.1)
            control_x.append(control_x[-1] + 0.1)
            control_y.insert(0, control_y[0] - 0.1)
            control_y.append(control_y[-1] + 0.1)

            T = 1
            t = np.arange(0, 1.1, 0.5)
            # t = np.zeros(1)
            N = len(control_x)

            interpolated_points = np.zeros((len(t), 2))
            X = np.zeros((len(t), N - 3))
            Y = np.zeros((len(t), N - 3))

            vx = np.zeros((N - 3, 4))
            vy = np.zeros((N - 3, 4))
            for i in range(N - 3):
                vx[i, :] = control_x[i:i + 4]
                vy[i, :] = control_y[i:i + 4]

            S = vx.shape

            # Construindo os dados de interpolação
            for i in range(S[0]):
                vx1 = vx[i, :]
                vy1 = vy[i, :]
                q_aux = CatmullRomT(vx1, vy1, T).q
                # q_aux = catmull.q
                for j in range(len(t)):
                    interpolated_points[j] = q_aux(t[j])
                X[:, i] = interpolated_points[:, 0]
                Y[:, i] = interpolated_points[:, 1]

            # Acumula os pontos de controle e trajetórias completas
            all_X.append(X)
            all_Y.append(Y)
            all_control_x.append(control_x)
            all_control_y.append(control_y)
            # all_colors.append(color)

        return all_X, all_Y, all_control_x, all_control_y
    
    def compute_all_splines(self):

        self.all_X_nose, self.all_Y_nose, self.all_control_x_nose, self.all_control_y_nose = self.compute_splines(self.sorted_coord_nose
                                                                                                                #  self.new_longest_path_nose,
                                                                                                                #   self.nodes_nose, self.nose_dict,
                                                                                                                #   self.idx_nose
                                                                                                                  )
        
        self.all_X_mouth, self.all_Y_mouth, self.all_control_x_mouth, self.all_control_y_mouth = self.compute_splines(self.sorted_coord_mouth
                                                                                                                    #   self.new_longest_path_mouth,
                                                                                                                    #   self.nodes_mouth,
                                                                                                                    #   self.mouth_dict, 
                                                                                                                    #   self.idx_mouth
                                                                                                                      )
        
        self.all_X_left_eye, self.all_Y_left_eye, self.all_control_x_left_eye, self.all_control_y_left_eye = self.compute_splines(self.sorted_coord_left_eye
                                                                                                                                #   self.new_longest_path_left_eye,
                                                                                                                                #   self.nodes_left_eye, 
                                                                                                                                #   self.left_eye_dict, 
                                                                                                                                #   self.idx_left_eye
                                                                                                                                  )
        
        self.all_X_right_eye, self.all_Y_right_eye, self.all_control_x_right_eye, self.all_control_y_right_eye = self.compute_splines(self.sorted_coord_right_eye
                                                                                                                                #   self.new_longest_path_right_eye,
                                                                                                                                #     self.nodes_right_eye, 
                                                                                                                                #     self.right_eye_dict, 
                                                                                                                            #    self.idx_right_eye
                                                                                                                               )


def plot_splines(all_X, all_Y, all_control_x, all_control_y, name):
    
    colors = ['blue', 'red', 'green', 'gray', 'orange', 'black', 'purple', 'pink', 'brown', 'cyan', 'yellow', 'magenta']
    plt.figure(figsize=(12, 10))

    for i, (X, Y, control_x, control_y) in enumerate(zip(all_X, all_Y, all_control_x, all_control_y)):
        color = colors[i]
        # Plotando os pontos de controle
        plt.plot(control_x, control_y, "o", color=color)
        # Plotando a spline (interpolação) completa
        plt.plot(X, Y, color=color)


    # Definindo título, rótulos e legendas
    plt.title('Interpolação Catmull-Rom - Trajetórias Completas e Pontos de Controle')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    # plt.legend()
    plt.grid(True)
    plt.gca().invert_yaxis()
    plt.savefig(f'./exemplos/08_spline_plot_{name}.png')
    plt.show()