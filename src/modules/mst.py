import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree

class MinimunSpanningTree:
    def __init__(self,dic_main_nose_cc, dic_main_mouth_cc, dic_main_left_eye_cc, dic_main_right_eye_cc,
                 nose_adjacency_matrix, mouth_adjacency_matrix, left_eye_adjacency_matrix, right_eye_adjacency_matrix):
        self.dic_main_nose_cc = dic_main_nose_cc
        self.dic_main_mouth_cc = dic_main_mouth_cc
        self.dic_main_left_eye_cc = dic_main_left_eye_cc
        self.dic_main_right_eye_cc = dic_main_right_eye_cc

        self.nose_adjacency_matrix = nose_adjacency_matrix
        self.mouth_adjacency_matrix = mouth_adjacency_matrix
        self.left_eye_adjacency_matrix = left_eye_adjacency_matrix
        self.right_eye_adjacency_matrix = right_eye_adjacency_matrix

    def minimum_spanning_tree(self, dic_main_cc, adjacency_matrix):
        idx = list(dic_main_cc.keys())
        nodes = list(dic_main_cc.values())
        min_trees = []

        for i in range(len(nodes)):
            submatriz_adj = adjacency_matrix[np.ix_(nodes[i], nodes[i])]
            min_tree = minimum_spanning_tree(submatriz_adj).toarray().astype(int)
            min_tree += min_tree.T
            min_trees.append(min_tree)

        return idx, nodes, min_trees
    
    def compute_all_mst(self):
        self.idx_nose, self.nodes_nose, self.min_trees_nose = self.minimum_spanning_tree(self.dic_main_nose_cc, self.nose_adjacency_matrix)
        self.idx_mouth, self.nodes_mouth, self.min_trees_mouth = self.minimum_spanning_tree(self.dic_main_mouth_cc, self.mouth_adjacency_matrix)
        self.idx_left_eye, self.nodes_left_eye, self.min_trees_left_eye = self.minimum_spanning_tree(self.dic_main_left_eye_cc, self.left_eye_adjacency_matrix)
        self.idx_right_eye, self.nodes_right_eye, self.min_trees_right_eye = self.minimum_spanning_tree(self.dic_main_right_eye_cc, self.right_eye_adjacency_matrix)

