import tkinter as tk 
from tkinter import *
from tkinter import scrolledtext

class Information(tk.Toplevel):
    __slots__=["master", "width","height"]

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
        
        self.resizable(height = False, width = False)
        
        #self.creer_widgets()

    def creer_widgets(self):
        """
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=50, height=20, font=("Times New Roman", 14))
        self.text_area.pack()
        self.text_area.insert(tk.INSERT,"Quelques statistiques sur les villes :" +'\n')
        self.text_area.insert(tk.INSERT,"-------------------------------------------" +'\n')
        """      

        photo= PhotoImage(file='menu/Credits.png')
        label = Label(self.master, image=photo)
        label.pack()

