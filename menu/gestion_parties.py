import tkinter as tk
from tkinter import messagebox

import os, pathlib, json

PATH = pathlib.Path(__file__).parent.parent.absolute()

class GestionParties(tk.Toplevel):
    """
        Initialise un objet GestionParties avec le widget maitre et les dimensions spécifiées de la fenêtre.

        
    """
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

            # bouton de suppression
            tk.Button(self, text="Supprimer", font=("Arial", 12), command=lambda: self.supprimer_partie(id)).grid(row=i+1, column=4, columnspan=2)

            # bouton pour lance la partie
            tk.Button(self, text="Lancer", font=("Arial", 12), command=lambda: self.lancer_partie(id)).grid(row=i+1, column=6, columnspan=2)

    def supprimer_partie(self, id):
        """
          fonction qui supprime la partie correspondant à l'id
          :paramètres: id: entier représentant l'identité de la partie
          :return:
        """
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette partie?"):
            # supprimer le fichier de sauvegarde
            os.remove(f"{PATH}/data/{self.master.games[id]['nom']}.json")

            # mettre à jour la liste des parties
            del self.master.games[id]

            # mettre à jour le fichier de sauvegarde
            with open(f"{PATH}/data/saves.json", "w") as f:
                json.dump(self.master.games, f)

            # mettre à jour l'affichage
            self.widgets()

    def lancer_partie(self, id):
        """
          fonction qui lance la partie
          :paramètres: id : entier représentant l'identité de la partie
          :return:
          """

        self.master.start_game(id)
