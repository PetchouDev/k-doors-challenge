# Libraries de la bibliothèque standard
from typing import List
import importlib
import json

# Modules locaux
from engine.generation import GenerateurCarte
from engine.ui.porte import Porte
from engine.utils import Vector
from .entites import Entite, Joueur, Gobelin, ObjetAuSol

from .objets import Cle, Prop



OFFSET_PLACEMENT_X = 400
OFFSET_PLACEMENT_Y = 300

class Game:
    """Représente un étage du jeu. Cette classe est principalement utiliser
    pour simplifier la sauvegarde du jeu en réunissant tout le contenu dans 
    une seule classe."""

    __slots__ = ("numero", "nb_cles", "etage", "nb_cles_recuperees", "entites", "matrice", "score", "joueur", "taille_matrice", "nom", "start", "end", "portes")

    def __init__(self, numero: int, nom: str, etage:int=1, taille_matrice:int=50,  nb_cles:int=0, nb_cles_recuperees:int=0, entites: List[Entite] = [], matrice: List[List[int]] = None, score:int=0, portes:List[Porte] = []) -> None:
        """
        Initialise un objet de la classe Game.

        Args:
            numero (int): Le numéro du jeu.
            nom (str): Le nom du jeu.
            etage (int, optional): L'étage du jeu. Par défaut 1.
            taille_matrice (int, optional): La taille de la matrice du jeu. Par défaut 50.
            nb_cles (int, optional): Le nombre total de clés dans le jeu. Par défaut 0.
            nb_cles_recuperees (int, optional): Le nombre de clés récupérées par le joueur. Par défaut 0.
            entites (List[Entite], optional): La liste des entités présentes dans le jeu. Par défaut [].
            matrice (List[List[int]], optional): La matrice représentant le jeu. Par défaut None.
            score (int, optional): Le score du joueur. Par défaut 0.
            portes (List[Porte], optional): La liste des portes présentes dans le jeu. Par défaut [].
        """
        
        self.numero = numero
        self.etage = etage
        self.nom = nom
        self.taille_matrice = taille_matrice
        self.nb_cles = nb_cles
        self.nb_cles_recuperees = nb_cles_recuperees
        self.etage = etage

        self.entites = entites
        self.portes = portes
        try:
            self.joueur = [entite for entite in entites if entite.__class__.__name__ == "Joueur"][0]
        except IndexError:
            self.joueur = Joueur("Joueur", 100, Vector(0, 0))
            self.entites.append(self.joueur)
        self.matrice = matrice

        self.start = None
        self.end = None

        

        if matrice:
            self.find_start_end()
        else:
            self.generate_map()
        
        #self.joueur.position = self.start * 32
        
        self.score = score

    def find_start_end(self) -> None:
        """
        Recherche et définit les coordonnées du point de départ et du point d'arrivée dans la matrice.
        """

        for y in range(len(self.matrice)):
            for x in range(len(self.matrice[0])):
                case = self.matrice[y][x]

                if case == 3:
                    self.end = Vector(x, y)
                elif case == 4:
                    self.start = Vector(x, y)

                if self.end and self.start: # arrêter la recherche si trouvé
                    return
    
    def generate_map(self) -> None:
        """
        Génère la carte du jeu en utilisant un générateur de carte.
        Initialise la matrice de jeu avec les éléments générés.
        Ajoute les portes, l'arrivée, le départ, les gobelins et les clés aux entités du jeu.
        """
    
        dg = GenerateurCarte(self.taille_matrice, self.taille_matrice, coef_difficulte=self.etage)
        dg.generate_map()
        dg.print_map()
        self.matrice = dg.get_for_game()

        self.matrice= self.generer_contour_noir(self.matrice)

        for y in range(len(self.matrice)):
            for x in range(len(self.matrice[0])):
                case = self.matrice[y][x]

                if case == 2:
                    porte = Porte(x, y)
                    self.portes.append(porte)


                elif case == 3:
                    self.end = Vector(x, y)
                    # créer un prop pour la sortie
                    prop = Prop("Arrivée", "ressources/objects/exit.png")
                    self.entites.append(ObjetAuSol(prop, Vector((x-2)*32, (y+2)*32), collectible=False))

                elif case == 4:
                    self.start = Vector(x, y)
                    # créer un prop pour l'entrée
                    prop = Prop("Départ", "ressources/objects/flag.png")
                    self.entites.append(ObjetAuSol(prop, Vector((x-2)*32, (y+2)*32), collectible=False))

                elif case == 6:
                    self.entites.append(Gobelin(Vector(x*32, y*32)))
                    self.matrice[y][x] = 1

                elif case == 7:
                    cle = Cle(1)
                    self.entites.append(ObjetAuSol(cle, Vector(x*32, y*32), True))
                    self.nb_cles += 1
                    self.matrice[y][x] = 1

    def generer_contour_noir(self, matrice:List[List[int]]) -> tuple[List[List[int]], Vector, Vector]:
        """
        Génère un contour noir autour de la matrice donnée et effectue des modifications sur la matrice.

        Args:
            matrice (List[List[int]]): La matrice d'entiers représentant le jeu.

        Returns:
            tuple[List[List[int]], Vector, Vector]: Un tuple contenant la matrice modifiée avec le contour noir,
            les coordonnées du point de départ et les coordonnées du point d'arrivée.

        """
        #  ajouter un cadre de 3 autour de la matrice pour éviter les sorties de la carte et rendre l'affichage des bords plus propre
        matrice = [[0, 0, 0] + row + [0, 0, 0] for row in matrice]
        matrice = [[0 for _ in range(len(matrice[0]))] for _ in range(3)] + matrice + [[0 for _ in range(len(matrice[0]))] for _ in range(3)]

        square = [[0 for _ in range(len(matrice[0]) * 2)] for _ in range(len(matrice) * 2)]

        for i, row in enumerate(matrice):
            for j, col in enumerate(row):
                square[i*2][j*2] = col
                square[i*2][j*2+1] = col
                square[i*2+1][j*2] = col
                square[i*2+1][j*2+1] = col

        # Pour les cases qui sont des entités ou des objets, on ne garde que la case du haut à gauche
        for i, row in enumerate(square):
            for j, col in enumerate(row):
                if col in [3, 4, 6, 7]:
                    square[i+1][j] = 1
                    square[i][j+1] = 1
                    square[i+1][j+1] = 1
                    if col == 3:
                        self.end = (i, j)
                    elif col == 4:
                        self.start = (i, j)
                        print("ENTREE : ", i, j)

        return square

    def from_json(data_json: dict) -> None:
        """
        Crée un objet Game à partir d'un dictionnaire JSON.

        Args:
            data_json (dict): Le dictionnaire JSON contenant les données du jeu.

        Returns:
            Game: L'objet Game créé à partir des données JSON.
        """
        
        module_entites = importlib.import_module("game.entites") # Importe le module entites
        # Pour chaque entité, on importe la classe correspondante et on crée l'objet
        entites=[getattr(module_entites, classe).from_json(entite) for classe, entite in data_json["entites"]]
        portes = [Porte.from_json(porte) for porte in data_json["portes"]]

        return Game(
            numero=data_json["numero"], 
            nom=data_json["nom"],
            etage=data_json["etage"],
            taille_matrice=data_json["taille_matrice"],
            nb_cles=data_json["nb_cles"],
            nb_cles_recuperees=data_json["nb_cles_recuperees"],
            entites=entites,
            portes=portes,
            matrice=data_json["matrice"],
            score=data_json["score"],
        )
    
    def to_json(self) -> dict:
        """
        Convertit l'objet en un dictionnaire JSON.

        Retourne un dictionnaire contenant les attributs de l'objet sous forme de clés et leurs valeurs correspondantes.
        Les attributs inclus sont : 'numero', 'nom', 'etage', 'taille_matrice', 'nb_cles', 'nb_cles_recuperees', 'entites',
        'portes', 'matrice' et 'score'.

        Returns:
            dict: Un dictionnaire contenant les attributs de l'objet sous forme de clés et leurs valeurs correspondantes.
        """
        return {
            "numero": self.numero,
            "nom": self.nom,
            "etage": self.etage,
            "taille_matrice": self.taille_matrice,
            "nb_cles": self.nb_cles,
            "nb_cles_recuperees": self.nb_cles_recuperees,
            "entites": [(entite.__class__.__name__, entite.to_json()) for entite in self.entites],
            "portes": [porte.to_json() for porte in self.portes],
            "matrice": self.matrice,
            "score": self.score
        }
    
    def save(self) -> None:
            """
            Sauvegarde les données du jeu dans un fichier JSON.

            :return: None
            """
            data_json = self.to_json()
            with open(f"data/{self.nom}.json", "w") as f:
                json.dump(data_json, f, indent=4)
