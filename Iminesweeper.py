# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 11:00:34 2024

@author: Emily-Jane
"""

import sys
import random
from Board import Board
from Game import Game
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMenu
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout,QComboBox
)

class Iminesweeper(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game  
        self.initUI()
        
    def change_difficulty(self):
        """"
        Change le niveau de difficulté du jeu et réinitialise le plateau de jeu en conséquence.
        Cette méthode est appelée lorsque l'utilisateur sélectionne un nouveau niveau de difficulté
        à partir du menu déroulant.
        Entry: self
        Return:  None
        """
        # Obtenir le niveau de difficulté choisi
        difficulty = self.difficulty_combo.currentText().lower()  # Convertir en minuscule pour correspondre à set_difficulty
        self.game.set_difficulty(difficulty)  # Appel à la méthode Game pour définir la difficulté
        
        # Réinitialiser le plateau de jeu avec la nouvelle taille et difficulté

        self.game.board = Board(self.game.board.difficulty, self.game.board.n, False)
    
        # Mettre en place les mines et les indices pour le nouveau plateau
        self.game.PlaceMines()
        self.game.SetHints(self.game.PlaceMines())
        
        # Créer la grille de boutons pour la difficulté choisie
        self.create_grid()
    
    def initUI(self):
        """"
        Initialise l'interface utilisateur pour le jeu Démineur.
        Entry: self
        Return: None

        """
        self.setWindowTitle("Démineur")
        
        main_layout = QVBoxLayout()

    # Sélection du niveau de difficulté
        difficulty_layout = QHBoxLayout()
        difficulty_label = QLabel("Niveau de difficulté :")
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Facile", "Moyen", "Difficile"])
        self.difficulty_combo.currentIndexChanged.connect(self.change_difficulty)
        
        difficulty_layout.addWidget(difficulty_label)
        difficulty_layout.addWidget(self.difficulty_combo)
        
        # Ajout sélection difficulté layout principal
        main_layout.addLayout(difficulty_layout)

        # Layout  grille
        self.grid_layout = QGridLayout()
        main_layout.addLayout(self.grid_layout)
        
        self.setLayout(main_layout)
        self.show()
        
        # Charger la grille pour la difficulté par défaut
        self.change_difficulty()


    def create_grid(self):
        """Crée les boutons pour la grille de jeu et les ajoute à la mise en page.
        Entry: self
        Return: None
        """
        # Effacer les boutons précédents de la grille
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Créer les boutons pour le nouveau plateau
        self.buttons = {}
        for x in range(self.game.board.n):
            for y in range(self.game.board.n):
                button = QPushButton("")
                button.setFixedSize(40, 40)
                button.clicked.connect(lambda _, x=x, y=y: self.reveal(x, y))
                
                # Activer le menu contextuel pour gérer le clic droit
                button.setContextMenuPolicy(Qt.CustomContextMenu)
                button.customContextMenuRequested.connect(self.show_context_menu)

                self.grid_layout.addWidget(button, x, y)
                self.buttons[(x, y)] = button
    
    
    
    
    def show_context_menu(self, pos):
       """Affiche un menu contextuel pour marquer ou retirer un drapeau.
       Entry: 
           -pos : QPoint
            La position du clic droit dans la fenêtre.
    
        Return: None
       """
       button = self.sender()  
       x, y = next(((i, j) for (i, j), b in self.buttons.items() if b == button), (None, None))
       
       if x is None or y is None:
           return  

       case = self.game.board.listecases[x][y]
       
       # menu contextuel avec option correspondante
       menu = QMenu(self)
       if case.isflagged:
           action_toggle_flag = menu.addAction("Retirer le drapeau")
       else:
           action_toggle_flag = menu.addAction("Marquer avec un drapeau")
       
       action = menu.exec_(self.mapToGlobal(pos))
       
       # verification
       if action == action_toggle_flag:
           if case.isflagged:
               reply = QMessageBox.question(
                   self, "Retirer le drapeau", 
                   "Voulez-vous retirer le drapeau ?", 
                   QMessageBox.Yes | QMessageBox.No
               )
               if reply == QMessageBox.No:
                   return

           self.toggle_flag(x, y)




    def toggle_flag(self, x, y):
            """Ajoute ou retire un drapeau de la case spécifiée.
            Entry : x,y position 
            Return : None """
            case = self.game.board.listecases[x][y]
            

            if case.isrevealed:
                QMessageBox.warning(self, "Attention", "Vous ne pouvez pas modifier un drapeau sur une case déjà révélée.")
                return
    
            case.isflagged = not case.isflagged  
    
            button = self.buttons[(x, y)]
            if case.isflagged:
                button.setText("🚩")
                button.setStyleSheet("background-color: yellow;")
            else:
                button.setText("")
                case.isrevealed=False
                button.setStyleSheet("background-color: lightgray;")
    


    def check_win_condition(self):
        """Vérifie si toutes les cases non-minées ont été révélées."""
        for row in self.game.board.listecases:
            for case in row:
                if not case.ismine and not case.isrevealed:
                    return False
        return True


    def reveal(self, x, y):
        """
        Révèle la case à la position (x, y) sur le plateau de jeu.
        x: int 
        y: int 
        """

        if self.game.board.listecases[x][y].isflagged:
            QMessageBox.warning(self, "Attention", "Vous ne pouvez pas révéler une case marquée avec un drapeau.")
            return
        
        if self.game.board.listecases[x][y].isrevealed:
            QMessageBox.warning(self, "Attention", "Case déjà révélée.")
            return
        
        self.game.CaseChoice(x, y)
        self.update_board()
    
        if self.game.isover:
            self.game_over()
            
        elif self.check_win_condition():
            self.win_game()

    def win_game(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Victoire")
        msg_box.setText("Vous avez gagné ! Félicitations !")
        msg_box.exec_()
        self.reset_game()  

    def update_board(self):
        """Met à jour l'affichage du plateau après chaque action."""
        for x in range(self.game.board.n):
            for y in range(self.game.board.n):
                case = self.game.board.listecases[x][y]
                button = self.buttons[(x, y)]
                if case.isrevealed:
                    # Afficher une mine, un indice ou une case vide
                    if case.ismine:
                        button.setText("💣")
                        button.setStyleSheet("background-color: red;")
                    elif case.hint > 0:
                        button.setText(str(case.hint))
                        button.setStyleSheet("background-color: lightgray;")
                    else:
                        button.setText("")  # Case vide
                        button.setStyleSheet("background-color: lightgray;")
                    button.setEnabled(False)

    def game_over(self):
        """Affiche une boîte de dialogue lorsque le joueur touche une mine, indiquant que le jeu est terminé.
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Game Over")
        msg_box.setText("Vous avez touché une mine! Voulez-vous rejouer ?")
        replay_button = msg_box.addButton("Rejouer", QMessageBox.AcceptRole)
        quit_button = msg_box.addButton("Quitter", QMessageBox.RejectRole)
        
        msg_box.exec_()
        

        if msg_box.clickedButton() == replay_button:
            self.reset_game()  
        elif msg_box.clickedButton() == quit_button:
            self.close()  
    
    def reset_game(self):
        """Réinitialise le jeu en recréant une nouvelle instance de Game et en redémarrant la grille."""
        self.game = Game()  
        self.game.start_game()  
        self.create_grid()  
        


# Code principal pour lancer l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    g=Game()
    g.start_game()
    # Lancer l'interface graphique
    ex = Iminesweeper(g)
    sys.exit(app.exec_())

