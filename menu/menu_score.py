import tkinter as tk
import json

class Scores(tk.Toplevel):
    __slots__=["master"]

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.title("Gestion des parties")
        self.resizable(height=True, width=True)
        self.widgets()

    def widgets(self):
        '''
        Création des widgets un à un et insertion grâce aux fonctions grid()
        '''
        # supprimer tous les widgets
        for widget in self.winfo_children():
            widget.destroy()
        # en-tetes
        tk.Label(self, text="Partie", font=("Arial", 14, "bold")).grid(row=0, column=0)
        tk.Label(self, text="Taille", font=("Arial", 14, "bold")).grid(row=0, column=1)
        tk.Label(self, text="Etage", font=("Arial", 14, "bold")).grid(row=0, column=2)
        tk.Label(self, text="Score", font=("Arial", 14, "bold")).grid(row=0, column=3)


        # scores
        for i, (id, data) in enumerate(self.master.games.items()):
            tk.Label(self, text=data["nom"], font=("Arial", 12)).grid(row=i+1, column=0)
            tk.Label(self, text=data["taille"], font=("Arial", 12)).grid(row=i+1, column=1)
            tk.Label(self, text=data["etage"], font=("Arial", 12)).grid(row=i+1, column=2)
            tk.Label(self, text=data["score"], font=("Arial", 12)).grid(row=i+1, column=3)


