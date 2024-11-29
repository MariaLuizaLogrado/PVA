class Knot:
    def __init__(self, idx, filhos=None):
        # Inicializa o nó com o índice 'idx' e uma lista de filhos. Se 'filhos' não for passado,
        # uma nova lista vazia é criada para evitar que uma mesma lista seja compartilhada entre instâncias.
        self.idx = idx
        self.filhos = filhos if filhos is not None else []