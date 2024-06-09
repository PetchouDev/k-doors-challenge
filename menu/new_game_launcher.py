import tkinter as tk 
from tkinter import messagebox


class New_game(tk.Toplevel):
    """Classe pour afficher une fenêtre permettant de paramétrer une nouvelle partie dans une fenêtre tkinter."""

    __slots__=["master", "width","height", "saisie", "valeur_seuil","indication"]

    def __init__(self, master, width, height) -> None:
        """
        Initialise un objet New_game avec le widget maitre et les dimensions spécifiées de la fenêtre.

        Args:
            width (int): Largeur de la fenêtre.
            height(int): Hauteur de la fenêtre.
        """
        super().__init__()
        self.master = master
        self.height = height
        self.width = width
        
        self.resizable(height = False, width = False)
        
        self.creer_widgets()

    def creer_widgets(self) -> None:
        """
        Crée les widgets de la fenêtre de paramètres.

        Cette méthode crée et configure les différents widgets nécessaires pour la fenêtre de paramètres.
        Les widgets créés sont les suivants :
        - Un label pour indiquer de nommer le jeu.
        - Un champ de saisie pour le nom du jeu.
        - Une échelle pour ajuster la taille de la carte.
        - Un bouton pour valider les paramètres.

        """
        # Couleurs
        bg_color = "#2c3e50"
        fg_color = "#ecf0f1"  # Texte clair
        entry_bg = "#34495e"
        button_bg = "#2980b9"
        scale_bg = "#1abc9c"

        self.title("Paramètres")
        self.geometry("425x300")
        self.configure(bg=bg_color)

        # Label pour indiquer de nommer le jeu
        self.indication = tk.Label(self, text="Name your game", font=("Arial", 14), bg=bg_color, fg=fg_color)
        self.indication.grid(row=0, column=0, pady=10)

        # Champ de saisie pour le nom du jeu
        self.saisie = tk.Entry(self, font=("Arial", 12), bg=entry_bg, fg=fg_color, insertbackground=fg_color)
        self.saisie.grid(row=1, column=0, padx=10, pady=10)

        # Échelle pour ajuster la taille de la carte
        self.valeur_seuil = tk.DoubleVar()
        self.scale = tk.Scale(self, orient='horizontal', from_=50, to=150, resolution=1, tickinterval=50,length=400, label='Size of the map', variable=self.valeur_seuil, font=("Arial", 12), bg=bg_color, fg=fg_color, troughcolor=scale_bg, highlightbackground=bg_color)
        self.scale.grid(row=2, column=0, padx=10, pady=20)

        # Bouton pour valider les paramètres
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider_parametres, font=("Arial", 12), bg=button_bg, fg=fg_color)
        self.bouton_valider.grid(row=3, column=0, pady=20)

    def valider_parametres(self) -> None:
        """
        Valide les paramètres saisis pour le nouveau jeu.

        Cette méthode récupère le nom du jeu saisi par l'utilisateur et la taille de la carte choisie.
        Ensuite, elle affiche le nom du jeu et la taille de la carte dans la console.
        Si le nom du jeu est vide ou déjà utilisé, une boîte de dialogue d'erreur est affichée.
        Sinon, les guillemets doubles sont supprimés du nom du jeu pour éviter les injections de code.
        Enfin, la fenêtre actuelle est détruite et la méthode create_new_game() du maître est appelée pour créer un nouveau jeu avec les paramètres validés.

        Paramètres:
        - self: L'instance de la classe NewGameLauncher.

        Retour:
        - None
        """
        nom_jeu = self.saisie.get()
        taille_carte = int(self.valeur_seuil.get())
        print(f"Nom du jeu: {nom_jeu}")
        print(f"Taille de la carte: {taille_carte}")
        noms = [g.get('nom') for g in self.master.games.values()]
        if nom_jeu == "" or nom_jeu in noms:
            messagebox.showerror("Erreur", "Le nom du jeu est invalide ou déjà utilisé.")
        else:
            # supprimer les " du nom pour éviter les injections de code
            nom_jeu = nom_jeu.replace('"', "")
            self.destroy()
            self.master.create_new_game(nom_jeu, taille_carte)