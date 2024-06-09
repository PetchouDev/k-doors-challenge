import tkinter as tk 


class Information(tk.Toplevel):
    """Classe pour afficher les informations de réalisation du projet dans une fenêtre tkinter."""

    __slots__=["master", "width","height"]

    def __init__(self, master, width, height) -> None:
        """
        Initialise un objet Information avec le widget maitre et les dimensions spécifiées de la fenêtre.

        Args:
            width (int): Largeur de la fenêtre.
            height(int): Hauteur de la fenêtre.
        """
        super().__init__()
        self.master = master
        self.height = height
        self.width = width
        
        self.resizable(height = False, width = False)


