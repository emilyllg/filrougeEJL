# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 14:56:37 2024

@author: Formation
"""
import numpy as np
from Board import Board

class Game(object):
    
    def __init__(self):
        
        self.board = Board(1,8,True)
        self.isover=False
        
        
        
        
    def set_difficulty(self, level):
        """
        Définit la difficulté sans interaction utilisateur, pour l'interface graphique.
        Entry : level String
        Returns : None
        """
        if level == 'facile': 
            self.board.difficulty = 1
            self.board.n = 8
        elif level == 'moyen':
            self.board.difficulty = 2
            self.board.n = 14
        elif level == 'difficile':
            self.board.difficulty = 3
            self.board.n = 20
                

    def PlaceMines(self):
        """
        PlaceMines place aléatoirement des mines sur le plateau en prenant en compte la taille du plateau.
        le nombre de mines est de nombre total de postitions // 2.
        Entrée : l'objet game actuel
        Sortie : self.board mis à jour et coordonnées des bombes placées sur le plateau list<(int,int)>

        """

        
        b=self.board.n

        
        totalpos=(b)**2

        if self.board.difficulty==1: 
            self.board.m=b+1
        if self.board.difficulty==2: 
            self.board.m=b+b//4
        if self.board.difficulty==3: 
            self.board.m=b+b//2
        randI = np.random.choice(totalpos,self.board.m, replace=False)
        
        # Convertir les indices aplatis en coordonnées 2D (x, y)
        coordinates = [(index // b, index % b) for index in randI]
        print(coordinates)
        for c in coordinates :
            self.board.listecases[c[0]][c[1]].hint=100
            self.board.listecases[c[0]][c[1]].ismine=True
        self.board.display_board()

        return coordinates 
        
    
    def SetHints(self, coordinates): 
        """
        Incrémente les indices des cases autour des mines pour indiquer le nombre de mines adjacentes.
        Entrée : liste de coordonnées des mines.
        Sortie : Plateau mis à jour avec indices
        """

        for c in coordinates: 

            for dx in [-1, 0, 1]:  
                for dy in [-1, 0, 1]: 

                    if dx == 0 and dy == 0:
                        continue
                    
                    new_x, new_y = c[0] + dx, c[1] + dy
    

                    if 0 <= new_x < self.board.n and 0 <= new_y < self.board.n:

                        if self.board.listecases[new_x][new_y].hint != 100:
                            self.board.listecases[new_x][new_y].hint += 1  
    
        self.board.display_board()
        return "Hints mis à jour"

    def input_coords(self):
        """
        Demande à l'utilisateur d'entrer des coordonnées pour choisir une case.
        Retourne un tuple (x, y) correspondant aux coordonnées choisies.
        """
        x=0
        y=0

        user_input = input("Entrez les coordonnées sous la forme 'x, y' : ")
        x, y = map(int, user_input.split(','))  # Convertir l'entrée en deux entiers

        if 0 <= x < self.board.n and 0 <= y < self.board.n:
            return x, y
                    
        else:
            print(f"Coordonnées hors limites, veuillez entrer des valeurs entre 0 et {self.board.n - 1}.")

                


                

    def reveal1case(self,x,y): 
        """Révèle une seule case.
        Entry : coordonnées x int et y int de la case 
        Sortie : attribut isrevealed de la case modifié à True"""
        
        self.board.listecases[x][y].isrevealed=True
        

    def revealALLcase(self,x,y): 
        """Révèle tout le plateau.
        Entry : coordonnées x int et y int  
        Sortie : attribut isrevealed de toutes les cases modifié à True"""
        
        for i in range(self.board.listecases.shape[0]):
            for j in range(self.board.listecases.shape[1]):
                self.board.listecases[i][j].isrevealed=True
                self.board.listecases[i][j].ismine=False
        
        return 'z' 
 
    def propagation(self, x, y):
        """
        Révèle toutes les cases connectées ayant hint == 0, et arrête la propagation aux cases avec hint > 0.
        Entry : coordonéées x int y int de la case cliquée 
        Sortie : plateau mis à jour en suivant les règles de révélation de case de la fonction propagation.
        """

        def is_valid(nx, ny):
            return 0 <= nx < self.board.n and 0 <= ny < self.board.n and not self.board.listecases[nx][ny].isrevealed
    

        if self.board.listecases[x][y].isrevealed:
            return
    

        if self.board.listecases[x][y].ismine==False: 
            self.board.listecases[x][y].isrevealed = True
    

        if self.board.listecases[x][y].hint > 0:
            return
    
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:  
                    nx, ny = x + dx, y + dy

                    if is_valid(nx, ny):
                        self.propagation(nx, ny)

        
        
        
    
    def CaseChoice(self,x,y):
        """ Déclenche selon l'attribut de la case choisie la fonction correspondante du jeu . 
        Entry : Coordonnées x int y int de la case choisie. 
        Returns : None
        """
        if self.board.listecases[x][y].isrevealed:
            print("Case déjà révélée.")
            return
        if self.board.listecases[x][y].ismine: 
              print("perdu")
              self.revealALLcase(x,y)
              self.board.isrevealed=True
              self.isover=True
              self.board.display_board()            
              
        elif self.board.listecases[x][y].hint==0  : 

            self.propagation(x,y)
            self.board.display_board()
            
        else : 

            self.reveal1case(x,y)
            self.board.display_board()
            

                
    def start_game(self):
        """Initialise le placement de bombes et d'indices sur un plateau. 
        Entry :plateau du jeu actuel
        Sortie : plateau du jeu actuel mis à jour."""
        # Initialisation du jeu
        coordinates = self.PlaceMines()
        self.SetHints(coordinates)
        
        """jeu en console"""
    
    # def input_difficulty(self):
    #     """
        
    #     """
    #     user_input = input("Choisir un niveau de difficiluté  'facile',ou'moyen'ou'difficile' : ")
    #     if user_input=='facile': 
    #         self.board.difficulty=1
    #         self.board.n=8
    #     if user_input=='moyen':
    #         self.board.difficulty=2
    #         self.board.n=14
    #     if user_input=='difficile':
    #         self.board.difficulty=3
    #         self.board.n=20
    #     if ValueError:
    #         print("Entrée invalide.")
        
    #     print('taille plateau', self.board.n)
    #     return self.board.n,self.board.difficulty
    # def setup_game(self):
    #     # """Permet de choisir entre jouer directement ou de changer le niveau."""
    #     # choix = input("jouer (1) ou changer de niveau (2) ? ")

    #     # if choix == "1":
    #     #     # Initialisation par défaut
    #     #     x, y = G.input_coords()
    #     #     coord = G.PlaceMines()
    #     #     G.SetHints(coord)
    #     #     G.CaseChoice(x, y)
    #     # elif choix == "2":
    #     #     # Choix du niveau de difficulté et de la taille du plateau
    #     #     taille, level = G.input_difficulty()
    #     #     G= Game(level, False,taille, False)
    #     #     coord = G.PlaceMines()
    #     #     G.SetHints(coord)
    #     #     x, y = self.input_coords()
    #     #     G.board.display_board()
    #     # else:
    #     #     print("Choix non valide. Veuillez entrer 1 ou 2.")
    #     #     self.setup_game()
    #     board=Board(1,8,False)
    #     g=Game(1, False,board,True)
    #     difficulty,isover,n,isrevealed
        
    #     return g 
    
        # # Boucle de jeu principale
        # while not self.isover:  
        #     try:
        #         # Demande des coordonnées et applique l'action
        #         x, y = self.input_coords()
        #         print(self.board.listecases[x][y].isrevealed)
        #         # Vérifier si la case est déjà révélée
        #         if self.board.listecases[x][y].isrevealed:
        #             print("Case déjà révélée.")
        #             continue  # Sortir sans effectuer d'autres actions si la case est déjà révélée
                
        #         self.CaseChoice(x, y)
                
        #         # Vérifie si la partie est gagnée
        #         if self.isover:
        #             print("Vous avez perdu!")
        #             break  # Sortir de la boucle si le joueur a gagné
        #         elif all(case.isrevealed or case.ismine for row in self.board.listecases for case in row):
        #             print("Vous avez gagné!")
        #             self.isover = True  

    
        #     except IndexError:
        #         print("Coordonnées hors limites. Essayez de nouveau.")
        #     except Exception as e:
        #         print(f"Une erreur est survenue : {e}")
