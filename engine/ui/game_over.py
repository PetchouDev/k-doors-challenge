import tkinter as tk

from PIL import ImageTk
import PIL.Image


class GameOver(tk.Tk):
    """Fenêtre affichée lorsque le joueur perd la partie."""

    __slots__ = ["score", "recommencer", "image_path", "image", "image_width", "image_height", "photo", "canvas", "score_label", "restart_button", "quit_button"]  

    def __init__(self, score: int) -> None:
        """
        Initialise la fenêtre de Game Over.

        Args:
            score (int): Le score du joueur.

        Returns:
            None
        """
        # appeler le constructeur de la classe mère
        super().__init__()

        # configuration de la fenêtre
        self.title("Game Over")
        self.geometry("520x470")
        self.resizable(height=False, width=False)

        # score du joueur
        self.score = score

        # est ce que le joueur veut recommencer
        self.recommencer = False
        self.image_path = "ressources/menu/Game_over.png"

        # Charger l'image et obtenir ses dimensions
        self.image = PIL.Image.open(self.image_path)
        self.image_width, self.image_height = self.image.size
        self.photo = ImageTk.PhotoImage(self.image)

        # Créer un Canvas avec la taille de l'image
        self.canvas = tk.Canvas(self, width=self.image_width, height=self.image_height, bg="black", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Afficher l'image sur le Canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Score du joueur en petit en italique
        self.score_label = tk.Label(self, text=f"Score: {self.score}", font=("Arial", 12, "italic"), bg="black", fg="white")
        self.canvas.create_window(self.image_width // 2, self.image_height * 0.65, window=self.score_label)

        # Bouton pour recommencer
        self.restart_button = tk.Button(self, text="Recommencer", command=self.restart, bg="black", fg="white")
        self.canvas.create_window(self.image_width // 3, self.image_height * 0.9, window=self.restart_button)

        # Bouton pour quitter
        self.quit_button = tk.Button(self, text="Quitter", command=self.quit, bg="black", fg="white")
        self.canvas.create_window(2 * self.image_width // 3, self.image_height * 0.9, window=self.quit_button)

    def restart(self):
        """
        Redémarre le jeu en définissant la variable 'recommencer' sur True et en détruisant la fenêtre actuelle.
        """
        self.recommencer = True
        self.destroy()

    def quit(self):
        """
        Ferme la fenêtre du jeu.
        """
        self.destroy()

    def get_user_input(self) -> bool:
        self.mainloop()
        return self.recommencer
