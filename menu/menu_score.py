import tkinter as tk
import json

class menu_score(tk.Toplevel):
    __slots__=["master", "width","height","saisie","score", "nom", "saisie2"]

    def __init__(self, master, width, height):  
        """
        Initialise un objet FenetreAvecGraphique avec le widget maitre et les dimensions spécifiéesde la fenêtre.

        Args:
            width (int): Largeur de la fenêtre.
            height(int): Hauteur de la fenêtre.
        """
        super().__init__()
        self.master = master
        self.height = height
        self.width = width
        self.saves = self.master.games
        self.title("Tableau des scores")
        
        self.resizable(height = True, width = True)
        self.widgets()


    def widgets(self):
        
        # en-tetes
        tk.Label(self, text="Partie", font=("Arial", 14, "bold")).grid(row=0, column=0)
        tk.Label(self, text="Score", font=("Arial", 14, "bold")).grid(row=0, column=1)

        # scores
        for i, (id, data) in enumerate(self.saves.items()):
            tk.Label(self, text=data["nom"], font=("Arial", 12)).grid(row=i+1, column=0)
            tk.Label(self, text=data["score"], font=("Arial", 12)).grid(row=i+1, column=1)

