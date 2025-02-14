from .knot import Knot
import matplotlib.pyplot as plt
import numpy as np

class BuildTree:
    def __init__(self, min_trees_nose, min_trees_mouth,  min_trees_left_eye, min_trees_right_eye):
        
        self.min_trees_nose = min_trees_nose

        self.min_trees_mouth = min_trees_mouth

        self.min_trees_left_eye = min_trees_left_eye

        self.min_trees_right_eye = min_trees_right_eye

    def build_tree(self, min_trees):
        abertos = []  
        n_nos = len(min_trees) 
        if n_nos > 0: 
            raiz = Knot(0) 
            abertos.append(raiz) 

        proximo_no = 0 
        while proximo_no < len(abertos): 
            no = abertos[proximo_no] 
            proximo_no += 1
            for j in range(n_nos): 
                if min_trees[no.idx, j] == 1:
                    ja_visitou = False 
                    for i in range(proximo_no):
                        if abertos[i].idx == j:
                            ja_visitou = True 
                            break
                    if not ja_visitou:
                        filho = Knot(j) 
                        abertos.append(filho)
                        no.filhos.append(filho)
        return raiz
    

    def prunning_tree(self, raiz):
        if len(raiz.filhos) == 0: # Condição base (nó folha)
            return 1, [raiz.idx], 1, [raiz.idx] # Se o nó não tiver filhos, sua altura é 0 e seu caminho é ele mesmo
        else: # Caso recursivo (nó com filhos)
            for filho in raiz.filhos: 
                # print('filho:', filho.idx)
                filho.altura, filho.caminho_altura_maxima, filho.tamanho_caminho_maximo, filho.caminho_maximo = self.prunning_tree(filho) # Para cada filho do nó atual, a função é chamada recursivamente, retornando a altura e o caminho para cada um dos filhos.

            if len(raiz.filhos) == 1:
                if raiz.filhos[0].altura + 1 > raiz.filhos[0].tamanho_caminho_maximo:
                    tamanho_caminho_maximo = raiz.filhos[0].altura + 1
                    caminho_maximo = [raiz.idx] + raiz.filhos[0].caminho_altura_maxima
                else:
                    tamanho_caminho_maximo = raiz.filhos[0].tamanho_caminho_maximo
                    caminho_maximo = raiz.filhos[0].caminho_maximo
            else:
                raiz.filhos.sort(key=lambda x: x.altura, reverse=True)
                tamanho_caminho_maximo = raiz.filhos[0].altura + raiz.filhos[1].altura + 1
                uma_parte_do_caminho = raiz.filhos[0].caminho_altura_maxima.copy()
                uma_parte_do_caminho.reverse()
                caminho_maximo = uma_parte_do_caminho + [raiz.idx] + raiz.filhos[1].caminho_altura_maxima
                for filho in raiz.filhos: 
                    if filho.tamanho_caminho_maximo > tamanho_caminho_maximo:
                        tamanho_caminho_maximo = filho.tamanho_caminho_maximo 
                        caminho_maximo = filho.caminho_maximo

            no_altura_maxima = raiz.filhos[0] # max(raiz.filhos, key=lambda x: x.altura) # Entre todos os filhos, o código encontra aquele que tem a maior altura (o caminho mais longo até uma folha).

            return no_altura_maxima.altura + 1, [raiz.idx] + no_altura_maxima.caminho_altura_maxima, tamanho_caminho_maximo, caminho_maximo # A altura retornada é incrementada em 1, pois estamos subindo um nível na árvore, e o caminho máximo é atualizado para incluir o nó atual (raiz.idx) na frente da lista.
             

    def compute_all_trees(self):
        self.raiz_nose = [self.build_tree(min_tree) for min_tree in self.min_trees_nose]
        self.raiz_mouth = [self.build_tree(min_tree) for min_tree in self.min_trees_mouth]
        self.raiz_left_eye = [self.build_tree(min_tree) for min_tree in self.min_trees_left_eye]
        self.raiz_right_eye = [self.build_tree(min_tree) for min_tree in self.min_trees_right_eye]

        self.longest_path_nose = [self.prunning_tree(raiz)[3] for raiz in self.raiz_nose]
        self.longest_path_mouth = [self.prunning_tree(raiz)[3] for raiz in self.raiz_mouth]
        self.longest_path_left_eye = [self.prunning_tree(raiz)[3] for raiz in self.raiz_left_eye]
        self.longest_path_right_eye = [self.prunning_tree(raiz)[3] for raiz in self.raiz_right_eye]


def plot_logest_path(dic_coords, longest_path, nodes):
  # Criar a figura
  plt.figure(figsize=(12, 10))

  coord = dic_coords
  colors = ['blue', 'red', 'green', 'gray', 'orange', 'black', 'purple', 'pink', 'brown', 'cyan', 'yellow', 'magenta']

  for j in range(len(longest_path)):

    ordem = longest_path[j]
    highlight_indices = nodes[j]


    # Obter coordenadas destacadas na ordem definida
    coords_destacados = [key for key, idx in coord.items() if idx in highlight_indices]
    coords_ordenados = [coords_destacados[i] for i in ordem if i < len(coords_destacados)]

    # Separar X e Y
    x_ordem, y_ordem = zip(*coords_ordenados)

    # Plotar cada ponto e conectar com linhas
    for i in range(len(x_ordem) - 1):
        plt.plot([y_ordem[i], y_ordem[i + 1]], [x_ordem[i], x_ordem[i + 1]], f'o-', linewidth=2, color = colors[j])  # Traçando a linha
        plt.annotate(f'{i}', (y_ordem[i], x_ordem[i]), textcoords="offset points", xytext=(0,5), ha="center", color='black')  # Anotando o número do nó

    # Plotar o último ponto
    plt.annotate(f'{len(x_ordem) - 1}', (y_ordem[-1], x_ordem[-1]), textcoords="offset points", xytext=(0,5), ha="right", color='black')

  # Melhorias na visualização
  plt.gca().invert_yaxis()
  plt.grid(True, linestyle="--", alpha=0.5)
  plt.xlabel("Coordenada X")
  plt.ylabel("Coordenada Y")
  plt.title("Maiores Caminhos")

  # Mostrar o gráfico
  return plt.show()