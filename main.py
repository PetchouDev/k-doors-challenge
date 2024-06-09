from menu.menu_principal import MenuPrincipal

if __name__ == "__main__":
    
    # boucle infinie pour relancer le menu principal après la fin d'une partie 
    # l'évènement de sortie de du menu à été écrasé par sys.exit() pour éviter une boucle infinie
    while True: 
        app= MenuPrincipal()
        app.mainloop()