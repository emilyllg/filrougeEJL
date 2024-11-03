# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 14:49:13 2024

@author: Formation
"""
import numpy as np
from case import Case

class Board(object):
    def __init__(self,difficulty,n,isrevealed):
        self.difficulty=difficulty
        self.n=n
        self.isrevealed=isrevealed
        self.listecases=self.CreateEmptyBoard()
        
        
    #création du tableau vide composé de cases. 
    def CreateEmptyBoard(self): 
            
        listcases=np.zeros((self.n, self.n), dtype=object)
        for i in range(listcases.shape[0]):
            for j in range(listcases.shape[1]):
                listcases[i][j]=Case(i,j,0,False,False)
        
        return listcases

    
 

    # Fonction pour afficher le tableau de manière stylisée
    def display_board(board):
        print("Plateau de jeu :")
        for row in board.listecases:
            line = []
            for case in row:
                if case.isrevealed:
                    if case.ismine:
                        line.append(" * ")  # Affiche une mine
                    else:
                        line.append(f" {case.hint} ")  # Affiche l'indice
                else:
                    line.append(" ? ")  # Case cachée
            print(" | ".join(line))
            print("-" * (len(row) * 4 - 1))  # Séparation entre les lignes

# tests
#board = Board.CreateEmptyBoard(5)

# Modification de quelques cases pour l'exemple
# board[1, 1].ismine = True
# board[2, 2].hint = 3
# board[2, 2].isrevealed = True
# board[3, 3].isrevealed = True
# board[3, 3].hint = 1

# Affichage du tableau stylisé
#display_board(board)
