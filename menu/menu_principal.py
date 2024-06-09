# Libraries de la bibliothèque standard Python
import os, sys
import json
import tkinter as tk
from tkinter import *

# Bibliothèques tierces
from PIL import ImageTk
import PIL.Image

# Bibliothèques de l'application
from .new_game_launcher import New_game
from .information import Information
from .menu_score import Scores
from .gestion_parties import GestionParties

from game import Game
from engine.runtime import Runtime


class MenuPrincipal (tk.Tk):
    """Classe représentant le menu principal du jeu."""

    __slots__ = ("bouton_fermeture","fen_launcher","l_fen_launcher","h_fen_launcher","label1","nom","l_fen_score", "h_fen_score","fen_score","etiquette_titre","bouton_info","bouton_nouvelle","bouton_ancien_partie","bouton_score", "l_fen_info", "h_fen_info","etiquette_nom","zone", "score","canvas", "frame1", "new_game_data", "games")

    def __init__(self) -> None:
        """
        Méthode spéciale appelée lors de la création d'une instance de la classe MenuPrincipal.
        Initialise les attributs de la classe et configure la fenêtre principale du menu.
        """
        super().__init__()
        self.title("K'Doors   Challenge  ")
        self.resizable(height=False, width=False)
        self.creer_widgets()
        self.h_fen_info = 913
        self.l_fen_info = 905

        self.l_fen_score = 650
        self.h_fen_score = 650
        self.fen_score = None

        self.l_fen_launcher = 400
        self.h_fen_launcher = 400
        self.fen_launcher = None

        self.configure(bg="#2c3e50")

        try:
            self.games = json.load(open("data/saves.json", "r"))
        except FileNotFoundError:
            print("Fichier de sauvegarde introuvable, création d'un nouveau fichier")
            self.games = {}
            os.makedirs("data", exist_ok=True)
            json.dump(self.games, open("data/saves.json", "w"))
        except json.decoder.JSONDecodeError:
            print("Fichier de sauvegarde corrompu, création d'un nouveau fichier")
            self.games = {}
            os.makedirs("data", exist_ok=True)
            json.dump(self.games, open("data/saves.json", "w"))

        self.games = {int(k): v for k, v in self.games.items()}

        # supprimer les parties qui n'ont pas de fichier de sauvegarde lisible
        to_delete = []
        for id, data in self.games.items():
            try:
                json.load(open(f"data/{data['nom']}.json", "r"))
            except:
                to_delete.append(id)

        for id in to_delete:
            del self.games[id]

        del to_delete

        # cache de communication avec l'assistant de création de nouvelle partie
        self.new_game_data = None

        # attacher la fermerture de la fenêtre à la méthode quitter
        self.protocol("WM_DELETE_WINDOW", self.quitter)

    def creer_widgets(self) -> None:
        """
        Crée les widgets du menu principal.

        Cette méthode crée et place les différents boutons et étiquettes du menu principal.
        Elle configure également la géométrie de la fenêtre et affiche une image de fond.

        Args:
            self: L'instance de la classe MenuPrincipal.

        Returns:
            None
        """
        IMAGE_PATH = 'ressources/menu/fond_menu.png'
        WIDTH, HEIGTH = 690, 465

        self.geometry('{}x{}'.format(WIDTH, HEIGTH))
        pil_img = PIL.Image.open(IMAGE_PATH)
        img = ImageTk.PhotoImage(pil_img)

        lbl = tk.Label(self, image=img)
        lbl.img = img  # Keep a reference in case this code put is in a function. -> indispensable 
        lbl.grid(row=1, column=3)  

        self.bouton_fermeture = tk.Button(self, text="Quitter l'application",font=("Helvetica", 14), width=20, height=2, bg="#3498db", fg="white", bd=0,  activebackground="#2980b9", activeforeground="white")
        self.bouton_fermeture.bind('<Button-1>',self.quitter)
        self.bouton_fermeture.grid(row = 5, column = 5)

        self.bouton_info = tk.Button(self, text="Information de Réalisation",font=("Helvetica", 14), width=20, height=2, bg="#3498db", fg="white", bd=0,  activebackground="#2980b9", activeforeground="white")
        self.bouton_info.bind('<Button-1>', self.information)
        self.bouton_info.grid(row = 0, column = 5)

        self.bouton_nouvelle = tk.Button(self, text="Nouvelle Partie",font=("Helvetica", 14), width=15, height=2, bg="#3498db", fg="white", bd=0, activebackground="#2980b9", activeforeground="white")
        self.bouton_nouvelle.bind('<Button-1>', self.new_game)
        self.bouton_nouvelle.grid(row = 2, column = 3)
        
        self.bouton_ancien_partie = tk.Button(self,text="Parties précédentes",font=("Helvetica", 14), width=25, height=2, bg="#3498db", fg="white", bd=0,  activebackground="#2980b9", activeforeground="white")
        self.bouton_ancien_partie.bind('<Button-1>', self.gestion_parties)
        self.bouton_ancien_partie.grid (row=4,column=3)

        self.bouton_score = tk.Button(self, text="Tableau des scores",font=("Helvetica", 14), width=15, height=2, bg="#3498db", fg="white", bd=0,  activebackground="#2980b9", activeforeground="white")
        self.bouton_score.bind('<Button-1>', self.tableau_score)

        self.bouton_score.grid (row=5,column=0)

        self.etiquette_titre = tk.Label(self,text=" K'Doors   Challenge  ",  font=("Helvetica", 14, "bold"), bg="#2c3e50", fg="white")
        self.etiquette_titre.grid(row = 1, column = 3)
       
        
    def quitter(self, event=None) -> None:
        """
        fonction permettant de quitter proprement le programme
        :paramètres: 
        :return:
        """
        self.destroy()
        sys.exit()


    def tableau_score(self, event ) -> None:
        """
        fonction callback qui affiche le tableau des scores dans une nouvelle fenêtre tkinter
        :paramètres: event pour le lier au bouton "bouton_score"
        :return:
        """
        if (self.fen_score != None) :
            self.fen_score.destroy()
        self.fen_score = Scores(self)

    def information(self, event) -> None:

        """
        fonction callback qui affiche les informations de réalisation du projet, à partir d'une image .png, dans une nouvelle fenêtre tkinter
        :paramètres: event pour le lier au bouton "bouton_info"
        :return:
        """
        fen=Information(self, self.l_fen_info, self.h_fen_info )
        fen.geometry("913x905")
        fen.title("Credits")
        IMAGE_PATH = 'ressources/menu/Credits.png'
        
        pil_img = PIL.Image.open(IMAGE_PATH)
        img = ImageTk.PhotoImage(pil_img)

        label = tk.Label(fen, image=img)
        label.img = img  # Keep a reference in case this code put is in a function. -> indispensable 

        label.pack()
        
        fen.mainloop()

    def new_game(self, event) -> None:
        """
        fonction callback qui affiche une nouvelle fenêtre dans laquelle on peut paramétrer le nom et la taille de la carte de la nouvelle partie
        :paramètres: event pour le lier au bouton "bouton_nouvelle"
        :return:
        """
        if (self.fen_launcher != None) :
            self.fen_launcher.destroy()
        self.fen_launcher= New_game(self, self.l_fen_launcher, self.h_fen_launcher)
        

    def create_new_game(self, nom: str, size: int) -> None:
        """
          fonction qui crée une nouvelle partie correspondant 
          :paramètres: nom: string donnant le nom de la partie
                     : size : int donnant la taille de la carte de la nouvelle partie
          :return:
        """
        # récupérer un id unique
        id = 0
        while id in self.games:
            id += 1
        
        # créer une nouvelle partie
        game = Game(id, nom, etage=1, taille_matrice=int(size))

        # enregistrer la partie pour créer un fichier de sauvegarde
        game.save()

        # ajouter la partie à la liste des parties
        self.games[id] = {"nom": nom, "taille": size, "etage": 1, "score": 0}

        # enregistrer la liste des parties
        json.dump(self.games, open("data/saves.json", "w"))

        num = game.numero
        del game

        # lancer la partie
        self.start_game(num)

    def gestion_parties(self, event) -> None:
        """
        fonction callback qui affiche une nouvelle fenêtre dans laquelle on peut choisir de supprimer une ancienne partie ou rejouer à une ancienne partie
        :paramètres: event pour le lier au bouton "bouton_ancien_partie"
        :return:
        """
        
        GestionParties(self)

    def start_game(self, id: int) -> None:
        """
          fonction qui lance la partie correspondant à l'id
          :paramètres: id: entier représentant l'identité de la partie
          :return:
        """
        try:
            self.destroy()
        except Exception as e:
            print(e)

        # charger la partie
        game = Game.from_json(json.load(open(f"data/{self.games[id]['nom']}.json", "r")))

        # lancer la partie (et demander si on veut recommencer/continuer à la fin)
        restart = Runtime(game).start()

        # sauvegarder la partie
        game.save()

        # mettre à jour le fichier de sauvegarde
        self.games[id]["etage"] = game.etage
        self.games[id]["score"] = game.score
        json.dump(self.games, open("data/saves.json", "w"))

        # si on veut recommencer, on relance la partie
        if restart:
            del game # libérer la mémoire
            self.start_game(id)
