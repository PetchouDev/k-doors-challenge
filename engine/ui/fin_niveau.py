import tkinter as tk


class FinNiveau(tk.Tk):
    def __init__(self, score: int) -> None:
        super().__init__()

        self.title("Etage terminé")
        self.geometry("300x200")

        self.score = score

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
        self.etage_suivant = True
        self.destroy()

    def quit(self):
        self.destroy()


    def get_user_input(self) -> bool:
        self.mainloop()
        return self.etage_suivant
    
