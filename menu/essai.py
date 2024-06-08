import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def start_game():
    messagebox.showinfo("Démarrer le jeu", "Le jeu commence !")

def open_options():
    messagebox.showinfo("Options", "Options du jeu.")

def quit_game():
    root.quit()

# Initialiser la fenêtre principale
root = tk.Tk()
root.title("Menu de Jeu Vidéo")
root.geometry("225x225")

# Charger l'image de fond
image_path = "menu/fond_menu.png"
background_image = Image.open(image_path)
background_photo = ImageTk.PhotoImage(background_image)

# Créer un canvas pour l'image de fond
canvas = tk.Canvas(root, width=225, height=225)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Créer un label de titre
title_label = tk.Label(root, text="Mon Jeu Vidéo", font=("Helvetica", 24, "bold"), bg="#2c3e50", fg="white")
title_label_window = canvas.create_window(300, 100, window=title_label)

# Fonction pour styliser les boutons
def create_button(text, command):
    button = tk.Button(root, text=text, font=("Helvetica", 14), width=15, height=2, bg="#3498db", fg="white", bd=0, command=command, activebackground="#2980b9", activeforeground="white")
    return button

# Créer les boutons du menu
play_button = create_button("Jouer", start_game)
options_button = create_button("Options", open_options)
quit_button = create_button("Quitter", quit_game)

# Ajouter les boutons au canvas
canvas.create_window(225//2, 225//2, window=play_button)
canvas.create_window(225//2, 225//2+30, window=options_button)
canvas.create_window(225//2, 225//2+60, window=quit_button)

# Lancer la boucle principale de l'application
root.mainloop()