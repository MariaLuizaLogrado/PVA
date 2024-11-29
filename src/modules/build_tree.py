from .knot import Knot

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
    
    def compute_all_trees(self):
        self.raiz_nose = [self.build_tree(min_tree) for min_tree in self.min_trees_nose]
        self.raiz_mouth = [self.build_tree(min_tree) for min_tree in self.min_trees_mouth]
        self.raiz_left_eye = [self.build_tree(min_tree) for min_tree in self.min_trees_left_eye]
        self.raiz_right_eye = [self.build_tree(min_tree) for min_tree in self.min_trees_right_eye]