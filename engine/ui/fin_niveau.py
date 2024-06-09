import tkinter as tk


class FinNiveau(tk.Tk):
    """Fenêtre affichée lorsque le joueur termine un étage."""

    __slots__ = ["score", "etage_suivant", "title_label", "score_label", "restart_button", "quit_button"]

    def __init__(self, score: int) -> None:
        """
        Initialise une instance de la classe FinNiveau.

        Args:
            score (int): Le score du joueur.

        Returns:
            None
        """
        # appeler le constructeur de la classe mère
        super().__init__()

        # configuration de la fenêtre
        self.title("Etage terminé")
        self.geometry("300x200")

        # score du joueur
        self.score = score

        # est ce que le joueur veut continuer à jouer
        self.etage_suivant = False

        # Titre de la fenêtre en gros
        self.title_label = tk.Label(self, text="Etage terminé", font=("Arial", 24))
        self.title_label.pack(side=tk.TOP, pady=20)

        # Score du joueur en petit en italique
        self.score_label = tk.Label(self, text=f"Score: {self.score}", font=("Arial", 12, "italic"))
        self.score_label.pack(side=tk.TOP, pady=10, padx=10)

        # Bouton pour recommencer
        self.restart_button = tk.Button(self, text="Etage suivant", command=self.suivant)
        self.restart_button.pack(side=tk.LEFT, pady=10, padx=40)

        # Bouton pour quitter
        self.quit_button = tk.Button(self, text="Quitter", command=self.quit)
        self.quit_button.pack(side=tk.LEFT, pady=5)

    def suivant(self):
        """
        Passe au niveau suivant.

        Cette méthode met à jour la variable `etage_suivant` à True, ce qui indique que le joueur souhaite passer au niveau suivant.
        Ensuite, elle détruit l'objet courant.

        """

        self.etage_suivant = True
        self.destroy()

    def quit(self):
        """
        Ferme la fenêtre actuelle.
        """
        self.destroy()

    def get_user_input(self) -> bool:
        """
        Cette méthode permet d'obtenir l'entrée de l'utilisateur.

        Elle exécute la boucle principale de l'interface utilisateur et retourne la valeur de l'attribut `etage_suivant`.

        :return: Un booléen indiquant si l'utilisateur a choisi de passer à l'étage suivant.
        """
        self.mainloop()
        return self.etage_suivant
    
