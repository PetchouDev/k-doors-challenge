# This code is released into the Public Domain.
from math import sqrt
from random import random, randrange, choice, randint

class CaseCarte:  
    """Classe représentant une case de la carte du donjon."""

    __slots__ = ['sqr']

    def __init__(self, sqr):
        """
        Initialise une instance de la classe MapGeneration.

        Args:
            sqr (int): La valeur du côté du carré.

        Returns:
            None
        """
        self.sqr = sqr

    def get_ch(self):
            """
            Renvoie le caractère représentant la case.
            
            Returns:
                str: Le caractère représentant la case.
            """
            return self.sqr
    
    def get_digit(self):
        """
        Renvoie l'index correspondant au caractère actuel dans la liste des caractères possibles.
        
        Retourne :
        - 0 pour le caractère '#'
        - 1 pour le caractère '.'
        - 2 pour le caractère '+'
        - 3 pour le caractère 'E'
        - 4 pour le caractère 'S'
        - 5 pour le caractère '-'
        - 6 pour le caractère 'M'
        - 7 pour le caractère 'C'
        
        Retourne :
        - L'index correspondant au caractère actuel dans la liste des caractères possibles.
        """
        return ('#', '.', '+', 'E', 'S', '-', 'M', 'C').index(self.get_ch())

class PieceCarte:
    """Classe représentant une salle du donjon."""

    __slots__ = ['row', 'col', 'height', 'width']

    def __init__(self, r, c, h, w):
        """
        Initialise un objet de la classe MapGeneration.

        :param r: Le nombre de lignes de la carte.
        :type r: int
        :param c: Le nombre de colonnes de la carte.
        :type c: int
        :param h: La hauteur de la carte.
        :type h: int
        :param w: La largeur de la carte.
        :type w: int
        """
        self.row = r
        self.col = c
        self.height = h
        self.width = w

class GenerateurCarte:
    """Classe pour générer une carte de donjon."""

    __slots__ = ['MAX', 'width', 'height', 'leaves', 'dungeon', 'rooms', 'NB_CLE', 'COEF_DIFFICULTE', 'liste_SE']

    def __init__(self, w: int, h: int, nb_cle:int=6, coef_difficulte:int=1):
            """
            Initialise un objet de la classe MapGeneration.

            Paramètres:
                - w (int): La largeur de la carte.
                - h (int): La hauteur de la carte.
                - nb_cle (int): Le nombre de clés à placer sur la carte.
                - coef_difficulte (int): Le coefficient de difficulté de la carte.

            Returns:
                None
            """
            
            self.MAX = 15 # Cutoff for when we want to stop dividing sections
            self.width = int(w)
            self.height = int(h)
            self.leaves = []
            self.dungeon = [] # la grille
            self.rooms = []
            self.NB_CLE = nb_cle

            self.COEF_DIFFICULTE = coef_difficulte
            self.NB_CLE = max(self.COEF_DIFFICULTE, int(self.width / 30))


            for h in range(self.height):
                row = []
                for w in range(self.width):
                    row.append(CaseCarte('#'))

                self.dungeon.append(row)

    def random_split(self, min_row, min_col, max_row, max_col):
            """
            Effectue une division aléatoire de la section donnée en utilisant les coordonnées minimales et maximales spécifiées.
            
            Args:
                min_row (int): La coordonnée minimale de la ligne.
                min_col (int): La coordonnée minimale de la colonne.
                max_row (int): La coordonnée maximale de la ligne.
                max_col (int): La coordonnée maximale de la colonne.
            """
            
            # We want to keep splitting until the sections get down to the threshold
            seg_height = max_row - min_row
            seg_width = max_col - min_col        # j'indique la largeur et la hauteur de ma première feuille

            if seg_height < self.MAX and seg_width < self.MAX: # les salles seront de largeur et hauteur <= 14 : la limite MAX
                self.leaves.append((min_row, min_col, max_row, max_col)) 
            elif seg_height < self.MAX and seg_width >= self.MAX:       # Si c'est plus grand en largeur que le MAX, alors je coupe verticalement
                self.split_on_vertical(min_row, min_col, max_row, max_col)
            elif seg_height >= self.MAX and seg_width < self.MAX:          #Si c'est plus grand en hauteur que le MAX, alors je coupe horizontalement
                self.split_on_horizontal(min_row, min_col, max_row, max_col)
            else:                                               #Sinon, puisqu'on une hauteur et une largeur plus grandes que le MAX, alors on coupe verticalement ou horizontalement
                    if random() < 0.5:
                        self.split_on_horizontal(min_row, min_col, max_row, max_col)
                    else:
                        self.split_on_vertical(min_row, min_col, max_row, max_col)

    def split_on_horizontal(self, min_row, min_col, max_row, max_col):
        """
        Coupe la zone de génération horizontalement en deux parties.
        
        Args:
            min_row (int): La limite inférieure de la ligne.
            min_col (int): La limite inférieure de la colonne.
            max_row (int): La limite supérieure de la ligne.
            max_col (int): La limite supérieure de la colonne.
        """
        
        split = (min_row + max_row) // 2 + choice((-2, -1, 0, 1, 2))   # on prend la moyenne entre les limites min_row et max_row auquel on ajoute une valeur de bruit
        self.random_split(min_row, min_col, split, max_col) # Je coupe dans le premier espace : entre le min et la limite split
        self.random_split(split + 1, min_col, max_row, max_col)  # Je coupe dans le second espace : entre la limite split et et le max

    def split_on_vertical(self, min_row, min_col, max_row, max_col):  
        """
        Divise la zone rectangulaire spécifiée verticalement en deux parties.
        
        Args:
            min_row (int): La limite inférieure de la rangée.
            min_col (int): La limite inférieure de la colonne.
            max_row (int): La limite supérieure de la rangée.
            max_col (int): La limite supérieure de la colonne.
        """
        split = (min_col + max_col) // 2 + choice((-2, -1, 0, 1, 2)) # on prend la moyenne entre les limites min_col et max_col auquel on ajoute une valeur de bruit
        self.random_split(min_row, min_col, max_row, split)
        self.random_split(min_row, split + 1, max_row, max_col)

    def carve_rooms(self):
            """
            Creuse des salles dans le donjon en utilisant les feuilles générées précédemment.

            Chaque feuille représente une section du donjon dans laquelle une salle peut être creusée.
            La méthode sélectionne aléatoirement certaines feuilles et crée des salles à l'intérieur de ces sections.
            La taille des salles est déterminée en fonction de la taille de la section.

            Les salles sont représentées par des caractères '.' dans la matrice du donjon.

            Note: Cette méthode modifie directement la matrice du donjon et ajoute les salles à la liste des salles.

            """
            
            for leaf in self.leaves:
                # We don't want to fill in every possible room or the 
                # dungeon looks too uniform
                if random() > 0.80: continue
                section_width = leaf[3] - leaf[1]
                section_height = leaf[2] - leaf[0]

                # The actual room's height and width will be 60-100% of the 
                # available section. 
                room_width = round(randrange(60, 100) / 100 * section_width)
                room_height = round(randrange(60, 100) / 100 * section_height)

                # If the room doesn't occupy the entire section we are carving it from,
                # 'jiggle' it a bit in the square
                if section_height > room_height:
                    room_start_row = leaf[0] + randrange(section_height - room_height)
                else:
                    room_start_row = leaf[0]

                if section_width > room_width:
                    room_start_col = leaf[1] + randrange(section_width - room_width)
                else:
                    room_start_col = leaf[1]
        
                self.rooms.append(PieceCarte(room_start_row, room_start_col, room_height, room_width))
                for r in range(room_start_row, room_start_row + room_height):
                    for c in range(room_start_col, room_start_col + room_width):
                        self.dungeon[r][c] = CaseCarte('.')

    def are_rooms_adjacent(self, room1, room2): # room1 et room2 sont des objets PieceCarte
            """
            Vérifie si deux pièces adjacentes sont adjacentes l'une à l'autre.

            Args:
                room1 (PieceCarte): La première pièce.
                room2 (PieceCarte): La deuxième pièce.

            Returns:
                tuple: Un tuple contenant deux listes, la première liste contient les rangées adjacentes entre les deux pièces,
                       la deuxième liste contient les colonnes adjacentes entre les deux pièces.
            """
            
            adj_rows = []
            adj_cols = []
            for r in range(room1.row, room1.row + room1.height): # on regarde si les coordonnées en hauteur de room1 sont comprises entre les coordonnées max et min sur la hauteur de room2
                if r >= room2.row and r < room2.row + room2.height:
                    adj_rows.append(r)

            for c in range(room1.col, room1.col + room1.width): # même procédé, mais en largeur
                if c >= room2.col and c < room2.col + room2.width:
                    adj_cols.append(c)

            return (adj_rows, adj_cols)

    def distance_between_rooms(self, room1, room2):
        """
        Calcule la distance entre deux salles.

        Args:
            room1 (Room): La première salle.
            room2 (Room): La deuxième salle.

        Returns:
            float: La distance entre les centres des deux salles.
        """
        centre1 = (room1.row + room1.height // 2, room1.col + room1.width // 2)
        centre2 = (room2.row + room2.height // 2, room2.col + room2.width // 2)

        return sqrt((centre1[0] - centre2[0]) ** 2 + (centre1[1] - centre2[1]) ** 2) # distance entre les centres
    
    def carve_corridor_between_rooms(self, room1, room2, connections, dico_relation):
            """
            Crée un couloir entre deux salles dans la carte du donjon.

            Args:
                room1 (Room): La première salle.
                room2 (tuple): La deuxième salle, représentée par un tuple contenant la salle elle-même, 
                               les lignes ou colonnes disponibles pour le couloir et le type de couloir ('rows' ou 'cols').
                connections (dict): Un dictionnaire contenant les salles reliées entre elles.
                dico_relation (dict): Un dictionnaire contenant les relations entre les salles.

            Returns:
                None
            """
            
            # Je constitue mon dictionnaire connections, des salles reliées entre elles
            clef = self.centre(room1)
            value = self.centre(room2[0])
            

            if room2[2] == 'rows':
                row = choice(room2[1]) # je choisie une ligne parmi les lignes de room2
                # Figure out which room is to the left of the other
                if room1.col + room1.width < room2[0].col:
                    start_col = room1.col + room1.width
                    end_col = room2[0].col
                    
                    
                    if clef not in connections.keys():
                    
                        connections[clef]= []
                        connections[clef].append(value)
                        dico_relation[clef]= []
                        dico_relation[clef].append(value)
                    else:
                        connections[clef].append(value)
                        dico_relation[clef].append(value)

                
                
                
                
                else:
                    start_col = room2[0].col + room2[0].width
                    end_col = room1.col
                    
                    
                    
                    if clef not in connections.keys():
                    
                        connections[clef]= []
                        connections[clef].append(value)
                        dico_relation[clef]= []
                        dico_relation[clef].append(value)
                    else:
                        connections[clef].append(value)    
                        dico_relation[clef].append(value)    

               
               
               
                liste_passage = []               
                for c in range(start_col, end_col):
                    self.dungeon[row][c] = CaseCarte('-')
                    liste_passage.append((row,c))
                dico_relation[clef].append(liste_passage)    




                    



            else:  # Il se passe la même chose qu'au-dessus, sauf qu'ici on s'intéresse aux lignes
                col = choice(room2[1]) # Je choisie une colonne parmi les colonnes de room2
                # Figure out which room is above the other
                if room1.row + room1.height < room2[0].row:
                    start_row = room1.row + room1.height
                    end_row = room2[0].row


                    if clef not in connections.keys():
                    
                        connections[clef]= []
                        connections[clef].append(value)
                        dico_relation[clef]= []
                        dico_relation[clef].append(value)
                    else:
                        connections[clef].append(value) 
                        dico_relation[clef].append(value) 




                else:
                    start_row = room2[0].row + room2[0].height
                    end_row = room1.row

                    if clef not in connections.keys():
                    
                        connections[clef]= []
                        connections[clef].append(value)
                        dico_relation[clef]= []
                        dico_relation[clef].append(value) 
                    else:
                        connections[clef].append(value) 
                        dico_relation[clef].append(value) 



                liste_passage = []
                for r in range(start_row, end_row):
                    self.dungeon[r][col] = CaseCarte('-')
                    liste_passage.append((r,col))
                dico_relation[clef].append(liste_passage)
    
    def centre(self, room1):
        """
        Calcule le centre d'une pièce donnée.

        Args:
            room1 (Room): La pièce pour laquelle le centre doit être calculé.

        Returns:
            tuple: Un tuple contenant les coordonnées du centre de la pièce (ligne, colonne).
        """
        return (room1.row + room1.height // 2, room1.col + room1.width // 2)
    
    def find_closest_unconnect_groups(self, groups, room_dict, connections, dico_relation):
        """
        Trouve les groupes de salles les plus proches non connectés et crée un corridor entre eux.

        Args:
            groups (list): Une liste de groupes de salles.
            room_dict (dict): Un dictionnaire contenant les informations sur les salles.
            connections (list): Une liste de connexions entre les salles.
            dico_relation (dict): Un dictionnaire contenant les relations entre les salles.

        Returns:
            None
        """
        shortest_distance = 99999
        start = None
        start_group = None
        nearest = None

        for group in groups:
            for room in group:
                key = (room.row, room.col)
                for other in room_dict[key]:
                    if not other[0] in group and other[3] < shortest_distance:
                        shortest_distance = other[3]
                        start = room
                        nearest = other
                        start_group = group
        self.carve_corridor_between_rooms(start, nearest, connections, dico_relation)

        # Fusionner les groupes
        other_group = None
        for group in groups:
            if nearest[0] in group:
                other_group = group
                break

        start_group += other_group
        groups.remove(other_group)
        
    def connect_rooms(self):
            """
            Connecte les salles entre elles en créant des connexions entre les salles adjacentes.
            """

            groups = []
            room_dict = {}
            for room in self.rooms:
                
                key = (room.row, room.col)
                room_dict[key] = []
                for other in self.rooms:
                    other_key = (other.row, other.col)
                    if key == other_key: continue
                    adj = self.are_rooms_adjacent(room, other)
                    if len(adj[0]) > 0:
                        room_dict[key].append((other, adj[0], 'rows', self.distance_between_rooms(room, other)))
                    elif len(adj[1]) > 0:
                        room_dict[key].append((other, adj[1], 'cols', self.distance_between_rooms(room, other)))
            
                groups.append([room]) #On ajoute dans le tableau groups les salles qui sont adjacentes à d'autres
                
            connections = dict()
            dico_relation = dict()
            while len(groups) > 1:
                self.find_closest_unconnect_groups(groups, room_dict, connections, dico_relation)
            self.in_out(connections, dico_relation)

    def in_out(self, graphe, dico_relation):
        """
        Cette méthode identifie les pièces d'un graphe qui sont des entrées ou des sorties.
        
        Args:
            graphe (dict): Un dictionnaire représentant le graphe des pièces.
            dico_relation (dict): Un dictionnaire représentant les relations entre les pièces.
        
        Returns:
            None
        """
        liste=[]
        #Je regarde s'il y a des pièces reliées qu'une seule fois 
        for key in graphe.keys():
            compteur = 0
            for a in graphe.values():
                for z in a:
                    if (key == z) or (len(graphe[key])>1) : 
                        compteur +=1

            if compteur == 0:
                liste.append(key)

        for b in graphe.values():
            for val in b:
                compteur2 = 0
                compteur3 = 0
                for c, f in graphe.items():
                    if (val == c):
                        compteur2 +=1
                    for i in f : 
                        if (val == i ):
                            compteur3+=1

                if (compteur2 == 0) and (compteur3 == 1):
                    liste.append(val)
        
        # calcul de distance entre entrée et sortie; on prend le max
        max = -99999
        start= 0,0
        end = 0,0
        
        for coord in liste : 
            for a in liste:
                dist = sqrt((a[0] - coord[0]) ** 2 + (a[1] - coord[1]) ** 2)
                if dist > max : 
                    max = dist
                    start = a[0], a[1]
                    end =  coord[0], coord[1]
        
        # Je dessine
        if liste != []:
            self.dungeon [start[0]][start[1]]= CaseCarte('S')
            self.dungeon[end[0]][end[1]]= CaseCarte('E')   

        liste_SE = [(start[0],start[1]),(end[0],end[1])]
        self.liste_SE = liste_SE
        dico_salle = graphe.copy()
        self.placements_entitees(dico_salle, dico_relation)

    def placements_entitees(self, dico_salle, dico_relation):
        """ Description : 
            La fonction complète dico_salle en rajoutant les données inverses (avant : A -> B ; maintenant : A <-> B)
            Elle appelle la fonction get_path afin de trouver le plus court chemin entre le départ et l'entrée
            Elle appelle la fonction self.separation pour découper le plus court chemin obtenu

        Paramètres:
            - dico_salle (dict): dictionnaire qui indique quelle salle est reliée avec qui (graphe non orienté)
            - dico_relation (dict): dictionnaire qui indique quelle salle est reliée avec qui en précisant les coordonnées de la jointure (graphe non orienté)
        Retourne:
        
        """

        coord_S = self.liste_SE[0]
        coord_E = self.liste_SE[1]
        dico = dico_salle.copy()
        for k,v in dico_salle.items():
            for coord in v:
                if coord not in dico_salle.keys():
                    dico[coord] = [k]
        dico_salle = dico.copy()
        for k,v in dico_salle.items():
            for coord in v:
                for cle, valeur in dico_salle.items():
                    if coord == cle and k not in valeur:
                        valeur.append(k)
        chemin = []
        liste_chemin = self.get_path(self.affiche_largeur(coord_E, dico_salle)[0], coord_E, coord_S, chemin)
        liste_chemin.append(coord_E)
        self.separations(liste_chemin, dico_relation, dico_salle)
        self.placements_monstres()

    def placements_monstres(self):
        """
        Place des monstres aléatoirement dans le donjon.

        Parcourt chaque case du donjon et remplace les cases vides par des monstres
        en fonction d'une probabilité de difficulté.

        """
        for r in range(self.height):
            for c in range(self.width):
                if self.dungeon[r][c].get_ch() == ".":
                    proba = randint(0, 100)
                    if proba <= self.COEF_DIFFICULTE:
                        self.dungeon[r][c] = CaseCarte("M")

    def affiche_largeur(self, root, arbre):
        """
        Description : 
            Utilise le graphe des relations des salles pour déterminer à partir d'un point l'arbre de parenté

        Paramètres:
            - root (tuple): coordonnee de départ
            - arbre (dict): dictionnaire qui indique quelle salle est reliée avec qui (équivalent d'un graphe) 
        Retourne:
            - parent (dict): indique le parent de chaque coordonnée
            - liste_traitee (liste): indique quelles coordonnées apparaissant dans parent
        """
        parent = dict()
        liste_root = []
        liste_root.append(root)
        liste_traite =[]
        while len(liste_root) != 0:
            racine = liste_root[0]
            for c,v in arbre.items():
                if racine==c:
                    for j in v:
                        comp = 0
                        for i in liste_traite:
                            if j != i:
                                comp += 1
                        if comp == len(liste_traite):
                            sim = 0
                            for y in liste_root:
                                if j == y:
                                    sim += 1
                            if sim == 0:
                                liste_root.append(j)
                                parent[j] = racine
            liste_traite.append(liste_root[0])
            liste_root.remove(racine)
        return(parent, liste_traite)

    def get_path(self, G, root, lettre, chemin):
        """
            Description : 
            Utilise le dictionnaire de parenté pour trouver le plus court chemin entre 2 salles (fonction récursive)

            Paramètres:
                - G (dict): coordonnee de départ
                - root (tuple): coordonnée de départ 
                - lettre (tuple): coordonnée d'arrivée
                - chemin (liste): chemin reliant la salle de départ et d'arrivée
            Retourne:
                - chemin (liste): chemin reliant la salle de départ et d'arrivée
            """
        if lettre == root:
            return(0)
        else :
            for c,v in G.items():
                if lettre == c:
                    chemin.append(c)
                    p = self.get_path(G, root, v, chemin)
                    return(chemin)

    def separations(self, chemin, dico_relation, dico_salle):
        """
            Description : 
            Permet de déterminer le nombre de séparation à faire selon le nombre de clé


            Paramètres:
            - dico_salle (dict): dictionnaire qui indique quelle salle est reliée avec qui (graphe orienté)
            - dico_relation (dict): dictionnaire qui indique quelle salle est reliée avec qui en précisant les coordonnées de la jointure (graphe non orienté)
            - chemin (liste): chemin reliant la salle de départ et d'arrivée
            Retourne:
                
            """
        longueur = len(chemin)//(self.NB_CLE+1)
        for nb_sections in range(1, self.NB_CLE+1):
            self.sections(chemin, nb_sections, longueur, dico_relation, dico_salle)

    def sections(self, chemin, nb_sections, longueur, dico_relation, dico_salle):
        """
            Description : 
            Sépare le chemin entre l'arrivée et le départ en différente partie. Le nombre de partie dépend du nombre de cle
            Appelle la fonction placemnts_portes et placements_cle pour chaque partie du chemin reliant S et E

            Paramètres:
            - dico_salle (dict): dictionnaire qui indique quelle salle est reliée avec qui (graphe orienté)
            - dico_relation (dict): dictionnaire qui indique quelle salle est reliée avec qui en précisant les coordonnées de la jointure (graphe non orienté)
            - chemin (liste): chemin reliant la salle de départ et d'arrivée
            - nb_sections (int) : Numéro de la section traitée
            - longueure (int) : longueure min des sections 

            Retourne:
                
                """
        valeur_min = (nb_sections-1) * (longueur)
        valeur_max = (nb_sections * (longueur))-1
        self.placement_portes(valeur_max, chemin, dico_relation)
        petit_chemin = []
        for i in range(valeur_min, valeur_max+1):
            petit_chemin.append(chemin[i])
        self.placement_cles(petit_chemin, chemin, dico_salle)

    def placement_cles(self, petit_chemin, chemin, dico_salle):
        """
            Description : 
            Place une cle à l'intérieure du graphe délimité par la première et la dernière coordonnée de la section du chemin 

            Paramètres:
            - dico_salle (dict): dictionnaire qui indique quelle salle est reliée avec qui (graphe orienté)
            - chemin (liste): chemin reliant la salle de départ et d'arrivée
            - petit_chemin (liste) : chemin d'une section  
              
            Retourne:
                
                """
        dico_cle = dico_salle.copy()
        if petit_chemin[0] == chemin [0]:
            for k,v in dico_cle.items():
                if k == petit_chemin[-1]:
                    v.remove(chemin[len(petit_chemin)])
        elif petit_chemin[-1] == chemin [-1]:
            for k,v in dico_cle.items():
                if k == petit_chemin[0]:
                    v.remove(chemin[-len(petit_chemin)])
        else:
            i = 0
            while chemin[i] != petit_chemin[0]:
                i += 1
            for k,v in dico_cle.items():
                if k == petit_chemin[0]:
                    v.remove(chemin[i-1])
                if k == petit_chemin[-1]:
                    v.remove(chemin[i+len(petit_chemin)]) 

        liste_salle = self.affiche_largeur(petit_chemin[0], dico_cle)[1]
        nb_random = randint(0, len(liste_salle)-1)
        cle = liste_salle[nb_random]
        if cle == self.liste_SE[0]:
            row = cle [0] + 1
            col = cle [1] + 1
            self.dungeon[row][col] = CaseCarte('C')
        else:
            self.dungeon[cle[0]][cle[1]] = CaseCarte('C')

    def placement_portes(self, valeur_max, chemin, dico_relation):
        """
            Description : 
            Place une porte entre la jointure de deux sectiions du chemin 

            Paramètres:
            - dico_relation (dict): dictionnaire qui indique quelle salle est reliée avec qui en précisant les coordonnées de la jointure (graphe non orienté)
            - chemin (liste): chemin reliant la salle de départ et d'arrivée
            - valeur_max (int) : dernière valeure de la section de chemin 
              
            Retourne:
                
        """
        coord_1 = chemin[valeur_max]
        coord_2 = chemin[valeur_max + 1]
        for c,v in dico_relation.items():
            if c == coord_1:
                for i in range(0, len(v)):
                    if coord_2 == v[i]:
                        val_1 = v[i+1]
                        self.dungeon[val_1[0][0]][val_1[0][1]] = CaseCarte('+')
            elif c == coord_2:
                for i in range(0, len(v)):
                    if coord_1 == v[i]:
                        val_1 = v[i+1]
                        self.dungeon[val_1[0][0]][val_1[0][1]] = CaseCarte('+')    

    def generate_map(self):
        """
        Génère une carte en utilisant l'algorithme de génération de labyrinthe.
        
        Cette méthode divise la carte en plusieurs sections, crée des salles dans chaque section,
        puis connecte les salles entre elles pour former un labyrinthe.
        """
        
        self.random_split(1, 1, self.height - 1, self.width - 1) #min_row = 1 et min_col = 1 pour laisser une bordure
        self.carve_rooms()
        self.connect_rooms()

    def print_map(self):
            """
            Affiche la carte du donjon.
            
            Parcourt chaque case de la carte et affiche le caractère correspondant à cette case.
            """
            for r in range(self.height):
                row = ''
                for c in range(self.width):
                    row += self.dungeon[r][c].get_ch()
                print(row)

    def get_for_game(self):
        """Retourne le dongeon sous la forme d'une matrice. Remplace les #, . et + par des chiffres.
            
            # -> 0 : mur
            . -> 1 : sol
            + -> 2 : porte
            E -> 3 : sortie (end)
            S -> 4 : entrée (start)
            - -> 5 : passage
            M -> 6 : monstre
            C -> 7 : clef
        
        Returns:
            List[List[int]]: le dongeon sous forme de matrice
        """
        #self.print_map()
        new_dungeon = []
        for row in self.dungeon:
            new_row = []
            for sqr in row:
                sqr = sqr.get_ch()
                if sqr == '#':
                    new_row.append(0)
                elif sqr == '.':
                    new_row.append(1)
                elif sqr == '+':
                    new_row.append(2)
                elif sqr == 'E':
                    new_row.append(3)
                elif sqr == 'S':
                    new_row.append(4)
                elif sqr == '-':
                    new_row.append(5)
                elif sqr == 'M':
                    new_row.append(6)
                elif sqr == 'C':
                    new_row.append(7)
            new_dungeon.append(new_row)

        return new_dungeon

    def get_for_game2(self):
            """
            Cette méthode retourne une matrice modifiée pour le jeu.
            
            La méthode prend la matrice 'dungeon' existante et ajoute un cadre de 1 autour de la matrice pour éviter les sorties de la carte et rendre l'affichage des bords plus propre.
            Ensuite, elle crée une nouvelle matrice 'square' avec des dimensions deux fois plus grandes que la matrice 'dungeon'.
            Les caractères spécifiques dans la matrice 'dungeon' sont remplacés par des chiffres correspondants dans la matrice 'square'.
            Les caractères 'S', 'E', 'M' et 'C' sont remplacés par des chiffres spécifiques et entourés de points.
            Le caractère '+' est remplacé par des chiffres spécifiques et entouré de tirets.
            Les autres caractères sont remplacés par des chiffres correspondants.
            
            Returns:
                square (list): La matrice modifiée pour le jeu.
            """
            
            matrice = self.dungeon
            matrice = [[0] + row + [1] for row in matrice]
            matrice = [[0 for _ in range(len(matrice[0]))]] + matrice + [[0 for _ in range(len(matrice[0]))]]

            square = [[0 for _ in range(len(matrice[0]) * 2)] for _ in range(len(matrice) * 2)]

            sol = CaseCarte('.').get_digit()
            passage = CaseCarte('-').get_digit()

            for i, row in enumerate(matrice):
                for j, col in enumerate(row):
                    if isinstance(col, int):
                        continue
                    if col.get_ch() in ('S', 'E', 'M', 'C'):
                        square[i*2][j*2] = col.get_digit()
                        square[i*2][j*2+1] = sol
                        square[i*2+1][j*2] = sol
                        square[i*2+1][j*2+1] = sol
                    elif col.get_ch() == '+':
                        if self.dungeon[i][j-1].get_ch() == '-':
                            square[i*2][j*2] = passage
                            square[i*2][j*2+1] = col.get_digit()
                            square[i*2+1][j*2] = passage
                            square[i*2+1][j*2+1] = col.get_digit()
                        elif self.dungeon[i][j+1].get_ch() == '-':
                            square[i*2][j*2] = col.get_digit()
                            square[i*2][j*2+1] = passage
                            square[i*2+1][j*2] = col.get_digit()
                            square[i*2+1][j*2+1] = passage
                        elif self.dungeon[i-1][j].get_ch() == '-':
                            square[i*2][j*2] = col.get_digit()
                            square[i*2][j*2+1] = passage
                            square[i*2+1][j*2] = col.get_digit()
                            square[i*2+1][j*2+1] = passage
                        elif self.dungeon[i+1][j].get_ch() == '-':
                            square[i*2][j*2] = col.get_digit()
                            square[i*2][j*2+1] = col.get_digit()
                            square[i*2+1][j*2] = passage
                            square[i*2+1][j*2+1] = passage


                    else:
                        square[i*2][j*2] = col.get_digit()
                        square[i*2][j*2+1] = col.get_digit()
                        square[i*2+1][j*2] = col.get_digit()
                        square[i*2+1][j*2+1] = col.get_digit()

            return square
