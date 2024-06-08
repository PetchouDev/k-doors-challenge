import pygame

import pathlib

from engine.ui.tilemap import Tilemap
from engine.utils.vector import Vector
from random import randint

from game.constantes import (
    PLAYER_SPEED, FRAME_RATE, DEAD_ZONE, DEBUG, NB_EMPLACEMENTS_INVENTAIRE, TAILLE_BORDURE_INVENTAIRE, 
    DISTANCE_AGRO_MONSTRES, DISTANCE_AGRO_STOP_MONSTRES, DISTANCE_ATTAQUE_MONSTRE, RECUl_DEGATS_ATTAQUANT,
    NB_COEUR_MAX, VIE_JOUEUR_DEFAUT, SOUNDS, DISTANCE_ATTAQUE_JOUEUR, GHOST, DISTANCE_POUR_RAMASSER_OBJET,
    RECUL_DEGATS_ATTAQUEE)
from game.game import Game
from datetime import datetime, timedelta

from game.entites import Joueur, Gobelin, ObjetAuSol
from game.objets import Arme, Epee, Coeur, Potion, Cle, Prop, Consommable, Botte
from math import exp

from typing import Optional, List
import traceback
from .utils import resize

from engine.ui.game_over import GameOver
from engine.ui.fin_niveau import FinNiveau



PATH = pathlib.Path(__file__).parent.parent

HEART = pygame.image.load("ressources/objects/heart.png")
HEART = pygame.transform.scale(HEART, (32, 32))
HEART.set_colorkey((255, 255, 255))

BLACK_HEART = pygame.image.load("ressources/objects/black_heart.png")
BLACK_HEART = pygame.transform.scale(BLACK_HEART, (32, 32))
BLACK_HEART.set_colorkey((255, 255, 255))

BOTTE = pygame.image.load("ressources/objects/botte.png")   
BOTTE = pygame.transform.scale(BOTTE, (32, 32))
BOTTE.set_colorkey((255, 255, 255))

# set the key repeat
pygame.key.set_repeat(1, 20) # allow holding after 1ms, repeat every 20ms => 50 fps

attente_prochaine_attaque = None

class Runtime():
    def __init__(self, game:Optional[Game]=None, width=800, height=600):        
        # (re)initialize pygame module
        if pygame.get_init():
            pygame.quit()
        if pygame.mixer.get_init():
            pygame.mixer.quit()
        if pygame.font.get_init():
            pygame.font.quit()
        
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.font = pygame.font.SysFont("monospace", 20, bold=True)


        # Game contient toutes les informations sur l'étage actuel, et donc la partie
        # si game est None, alors on crée un nouvel étage
        self.game = game
        if not self.game:
            self.game = Game(1, "test")

        print("Sauvegarde : ", game.nom)
        
        self.player = self.game.joueur

            
        if self.game.start is None:
            self.game.generate_map()

        map = self.game.matrice
        entree = self.game.start
        sortie = self.game.end

        entree.x -= 2
        entree.y += 2

        sortie.x -= 2
        sortie.y += 2

        # screen creation
        self.display = pygame.display.set_mode((width, height))

        # définir le titre de la fenêtre
        pygame.display.set_caption("Tilemap")

        # store the width and height of the display
        self.width = width
        self.height = height

        # store the map
        self.map = Tilemap(map, entree, sortie)

        self.last_step = datetime.now()

        
        if not self.player:
            self.player = Joueur("Player", 100, Vector(0, 0))
            print("Joueur ajouté")
            self.game.entites.append(self.player)

        # placer le joueur au centre de l'écran
        self.player.rendered_position = Vector(self.width // 2, self.height // 2)
        print("--"*10)
        print("Position player")
        print(self.player.position)

        # si un nouveau joueur est créé, on le place à l'entrée
        if self.player.position.x==0:
            print("placing player")
            
            # si le joueur n'a pas de position, on le place à l'entrée
            self.player.position = entree * 32 - Vector(*self.display.get_size()) // 2

        print('Placing player on map')
        # placer la carte dans l'espace 
        self.map.draw(self.display, -self.player.position, self.game.portes)

        # placer le joueur au centre de l'écran
        print("Positionnement joueur sur l'écran")
        self.player.rect.center = self.width // 2, self.height // 2
        self.map.offset = -self.player.position

        # allow full screen display
        self.fullscreen = False

        # vérifier que le joueur a bien une épée
        print("Vérification de l'épée dans l'inventaire du joueur")
        epee = False
        for object in self.player.inventaire:
            if object.nom == "Épée":
                epee = True

        print("Épée trouvée : ", epee)
    
        if not epee:
            from game.objets import Epee
            self.player.ajouter_inventaire(Epee())
            print(self.player.inventaire)

        self.player.select_item(0)

        ## selectionner le premier objet de l'inventaire
        self.player.select_item(self.player.get_item_index("Épée"))
#
        # declaration de l'horloge
        self.clock = pygame.time.Clock()

        # etats des touches (permet un déplacement plus fluide et sur plus d'un axe par frame)
        self.states = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "object_use": False,
            "wheel": None
        }

        # musique en cours
        self.current_music = randint(0, len(SOUNDS["OST"]) - 1)

        # récupérer les chemins absolus des musiques
        self.ost = []
        for track in SOUNDS["OST"]:
            self.ost.append(PATH / "ressources" / "audio" / "ost" / track)

        
        #Préparation affichage inventaire
        self.text_afficher_inventaire = None
        self.text_inventaire_jusqua = None

        print("Initialisation terminée")    
    

    def toggle_fullscreen(self):
        # toggle the fullscreen mode
        self.fullscreen = not self.fullscreen

        # set the display mode to fullscreen
        if self.fullscreen:
            self = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self = pygame.display.set_mode((self.width, self.height))

        # return the display
        return self
    
    def update(self, corrected_movement, render_movement, offset, attaque=False):
        # draw the elements of the map
        try:
            self.map.draw(self.display, offset, portes=self.game.portes)

            if attaque:
                attaque = not self.utiliser_consommable()

            self.afficher_entites(attaque=attaque, corrected_movement=corrected_movement, render_movement=render_movement)

            self.afficher_inventaire()

            self.afficher_vie()

            # si le joueur est mort, créer une tombe; vider son inventaire et arrêter le jeu
            if self.player.vie <= 0:
                # ne garder que l'épée par défault et les clés
                self.player.inventaire = [item for item in self.player.inventaire if item.nom == "Épée" or item.nom == "Clé"]
                self.game.entites.append(ObjetAuSol(Prop("Tombe", "ressources/objects/grave.png"), self.player.position + 32*Vector(12.5, 9.5), collectible=False))
                return True
            self.afficher_fps()              
            if DEBUG:
                
                for porte in self.game.portes:
                    pygame.draw.line(pygame.display.get_surface(), (0, 0, 255), porte.rect.center, self.player.rect.center)

                # hitbox du joueur en violet
                pygame.draw.rect(self.display, (255, 0, 255), self.player.hitbox, 1)
            
            # Afficher le texte au dessus de la barre d'inventaire 
            # lorsqu'on change d'objet pour voir ce que c'est
            self.afficher_text_inventaire()
            
            # refresh the screen with
            pygame.display.flip()
            self.clock.tick(FRAME_RATE)

        except Exception as e:
            print('Erreur lors de la mise à jour de l\'écran')
            print(e)
            print(e.__cause__)
            print(traceback.format_exc())

        return False
    
    def utiliser_consommable(self):
        item = self.player.get_selected_item()
        if not isinstance(item, Consommable):
            return False
        
        item_utilise = item.utiliser(self.player)
        if item_utilise:
            pygame.mixer.Sound("ressources/audio/" + SOUNDS["soin"]).play()
            return True
        else:
            return False
            
    def afficher_text_inventaire(self):
        """Affiche le texte de l'inventaire
        
        Args:

        Retourne:

        """
        if self.text_afficher_inventaire is not None and \
                self.text_inventaire_jusqua is not None and \
                datetime.now() < self.text_inventaire_jusqua:
            
            TAILLE_SLOT = 10 # pourcentage de la hauteur de l'écran.
            TAILLE_SLOT /= 100
            PADDING = 10
            l_ecran, h_ecran = self.display.get_size()
            taille_inv = int(TAILLE_SLOT * h_ecran)
            pos = (
                l_ecran//2 - self.text_afficher_inventaire.get_width()//2, 
                h_ecran - PADDING - taille_inv - 30
                )
            self.display.blit(self.text_afficher_inventaire, pos)

    def afficher_joueur(self, corrected_movement, render_movement):

        # draw the player
        self.player.draw(render_movement, corrected_movement, self.display)

        # dessiner les éléments pour le debug
        if DEBUG:
            # tracer un trait entre le joueur et le centre de l'écran
            pygame.draw.line(self.display, (0, 0, 255), (self.width // 2, self.height // 2), self.player.rect.center, 1)

            # dessiner le rectangle du joueur
            pygame.draw.rect(self.display, (0, 255, 0), self.player.rect, 1)

            # Dessiner un rectangle vide pour la zone morte
            pygame.draw.rect(self.display, (255, 0, 0), (self.width // 2 - DEAD_ZONE[0], self.height // 2 - DEAD_ZONE[1], 2 * DEAD_ZONE[0], 2 * DEAD_ZONE[1]), 2)

    def etage_suivant(self):
        return FinNiveau(self.game.score).get_user_input()

    def start(self):
        # boucle de jeu
        print("Démarrage de la boucle de jeu")
        # condition d'arrêt
        self.running = True
        global attente_prochaine_attaque


        # mettre en attente les monstres pour éviter de se faire tuer au démarrage
        for entite in self.game.entites:
            if not isinstance(entite, Joueur) and entite.vitesse > 0:
                entite.en_attente = datetime.now() + timedelta(milliseconds=500)
        
        # boucle principale
        while self.running:
            # gestion de la musique
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(self.ost[self.current_music])
                pygame.mixer.music.play()
                self.current_music = (self.current_music + 1) % len(self.ost)
            
            # acquisition des événements
            for event in pygame.event.get():
                self.handle_event(event)

            attaque = False
            if self.states.get("object_use"):
                self.states["object_use"] = False
                item = self.player.get_selected_item()
                if item and item.nom == "Épée":
                    if (attente_prochaine_attaque is None or attente_prochaine_attaque < datetime.now()) and isinstance(self.player.get_selected_item(), Arme):
                        attaque=True
                        self.player.attaque = True
                        pygame.mixer.Sound("ressources/audio/" + SOUNDS["epee"]).play()
                        attente_prochaine_attaque = datetime.now() + timedelta(milliseconds=500)
                else:
                    attaque = True
            
            if not self.player.occupe and self.player.vie > 0:
                # calculer la vélocité du joueur
                player_movement = self.get_player_movement()

                # en déduire la velocité 
                player_movement *= (PLAYER_SPEED + self.player.buff_vitesse) / FRAME_RATE

                # vérifier si on peut ouvrir une porte
                self.map.verifier_portes(self.player, self.game.portes)

                # Vérifier les collisions
                corrected_movement = player_movement if GHOST else self.map.correct_movement(self.player, player_movement)

                # si le mouvement n'est pas nul et que le dernier pas date de plus de .35s
                if (corrected_movement.x != 0 or corrected_movement.y != 0) and self.last_step + timedelta(milliseconds=350) < datetime.now():
                    pygame.mixer.Sound("ressources/audio/" + SOUNDS["pas"]).play()
                    self.last_step = datetime.now()



                # répartir le déplacement entre le joueur et la carte pour que le joueur reste dans la zone morte
                rendered_movement, offset = self.process_movement(corrected_movement)

            else:
                corrected_movement = Vector(0, 0)
                rendered_movement = Vector(0, 0)
                offset = Vector(0, 0)
            
            # appliquer le déplacement et rafraichir l'écran
            game_over = self.update(corrected_movement=corrected_movement, render_movement=rendered_movement, offset=offset, attaque=attaque)
            if game_over:
                # dernière afficher les entités pour voir la tombe
                self.update(Vector(0, 0), Vector(0, 0), Vector(0, 0), False)

                # actualiser l'écran
                pygame.display.flip()
                

                # replacer le joueur à l'entrée
                self.player.position = Vector(0, 0)                         #
                                                                            #
                # réinitialiser la vie du joueur                            # Pas affiché directement mais nécessaire pour une nouvelle tentative
                self.player.vie_max =  self.player.vie = VIE_JOUEUR_DEFAUT  #
                                                                            #
                # réinitialiser la vitesse du joueur                        #      
                self.player.buff_vitesse = 0                                #

                # attendre .5s
                pygame.time.wait(500)
                
                # boite de dialogue de fin de partie
                fin_partie = GameOver(self.game.score)
                fin_partie.configure(bg="black")
                

                should_restart =fin_partie.get_user_input()

                

                if should_restart:
                    # quitter pygame 
                    self.stop()
                    # relancer la partie
                    return True
                else:
                    # quitter pygame 
                    self.stop()
                    # retour au menu
                    return False
                
            # si le joueur a atteint la sortie (moins de 32 pixels de distance)
            end_pos = self.game.end * 32 - Vector(*self.display.get_size()) // 2

            if self.player.position.distance_between(end_pos) <= 32:
                # jouer le son de la victoire
                pygame.mixer.Sound("ressources/audio/" + SOUNDS["victoire"]).play()

                # attendre .5s
                pygame.time.wait(500)

                # ajouter des points au score
                self.game.score += self.game.etage

                # augmenter la difficulté
                self.game.etage += 1   

                # savoir si le joueur veut continuer
                suivant = self.etage_suivant()

                # restaurer la vie du joueur
                self.player.vie = self.player.vie_max

                # réinitialiser sa position
                self.player.position = Vector(0, 0)

                # Ssupprimer les entités de l'étage actuel
                self.game.entites = [entite for entite in self.game.entites if isinstance(entite, Joueur)]

                # supprimer la carte de l'étage actuel
                self.game.matrice = []

                # si on veut continuer
                if suivant:
                    # quitter pygame 
                    self.stop()
                    return True
                
                # si on veut quitter
                else:
                    # quitter pygame 
                    self.stop()
                    return False
                
        return False


    def stop(self):
        self.running = False
        self.game.save()
        pygame.quit()

    # calculer le vecteur de déplacement du joueur et le déplacement de la carte
    def process_movement(self, player_movement: Vector):
        offset = Vector(0, 0)

        position = self.player.real_pos

        new_position = position + player_movement

        # si le joueur est trop à gauche
        if new_position.x < self.width // 2 - DEAD_ZONE[0]:
            # placer le joueur à la limite de la zone morte
            new_position.x = self.width // 2 - DEAD_ZONE[0]

        # si le joueur est trop à droite
        if new_position.x > self.width // 2 + DEAD_ZONE[0]:
            # placer le joueur à la limite de la zone morte
            new_position.x = self.width // 2 + DEAD_ZONE[0]

        # si le joueur est trop en haut
        if new_position.y < self.height // 2 - DEAD_ZONE[1]:
            # placer le joueur à la limite de la zone morte
            new_position.y = self.height // 2 - DEAD_ZONE[1]

        # si le joueur est trop en bas
        if new_position.y > self.height // 2 + DEAD_ZONE[1]:
            # placer le joueur à la limite de la zone morte
            new_position.y = self.height // 2 + DEAD_ZONE[1]

        # calculer le nouveau déplacement du joueur
        corrected_movement = new_position - position

        # calculer le déplacement de la carte
        offset = corrected_movement - player_movement

        return corrected_movement, offset

    # calculer le vecteur de déplacement du joueur
    def get_player_movement(self):
        player_movement = Vector(0, 0)
        if self.states["up"]:
            player_movement.y -= 1
        if self.states["down"]:
            player_movement.y += 1
        if self.states["left"]:
            player_movement.x -= 1
        if self.states["right"]:
            player_movement.x += 1

        return player_movement.normalize()

    def changement_slot_inv(self):
        """Récupère le changement de slot de l'inventaire et l'applique si besoin
        
        Args:

        Retourne:
        """
        if self.states["wheel"] != None:
            if len(self.player.inventaire) > 0:
                item_selected = self.player.get_selected_item()
                if item_selected:

                    index = self.player.inventaire.index(item_selected)
                else:
                    index = 0
                new_index = index + self.states["wheel"]
                if new_index < 0:
                    new_index = len(self.player.inventaire) - 1
                elif new_index >= len(self.player.inventaire):
                    new_index = 0
                
                self.player.select_item(new_index)

                item_selected = self.player.get_selected_item()
                self.text_afficher_inventaire = self.font.render(item_selected.label, True, (0, 0, 0))
                self.text_inventaire_jusqua = datetime.now() + timedelta(seconds=2)

            self.states["wheel"] = None
    
    def afficher_fps(self):
        """Afficher les fps sur l'écran
        
        Args:

        Retourne:

        """
        font = pygame.font.Font(None, 36)
        text = font.render(f"{int(self.clock.get_fps())} FPS", True, (0, 255, 0))
        self.display.blit(text, (10, 96))

    def afficher_inventaire(self):
        """Afficher l'inventaire du joueur sur l'écran
        
        Args:

        Retourne:

        """
        self.changement_slot_inv()

        NB_SLOT = NB_EMPLACEMENTS_INVENTAIRE
        TAILLE_SLOT = 10 # pourcentage de la hauteur de l'écran.
        TAILLE_SLOT /= 100
        PADDING = 10
        largeur_ecran, hauteur_ecran = self.display.get_size()
        taille_inv = int(TAILLE_SLOT * hauteur_ecran)

        pos = (
            largeur_ecran//2 - (taille_inv*NB_SLOT)//2,
            hauteur_ecran - taille_inv - PADDING
        ) #position coin gauche du rectangle de l'inventaire
        for i in range(NB_SLOT):
            if i == 0:
                start = pos
            else:
                start = [start[0] + taille_inv - taille_bordure, pos[1]]

            taille_bordure = TAILLE_BORDURE_INVENTAIRE

            if len(self.player.inventaire) > i:
                item = self.player.inventaire[i]
                try:
                    image: pygame.Surface = item.images.copy().get("common")
                except AttributeError:
                    image = item.image
                    image = resize(image, 1.7)
                    
                
                self.display.blit(image, (start[0] + 2, start[1] + 2))

                if item.est_selectionne:
                    taille_bordure *= 2
                
                if item.quantite > 1:
                    label = self.font.render(str(item.quantite), 1, (255,0,0))
                    self.display.blit(label, (start[0] +taille_inv//2 - 22, start[1] + taille_inv - 25))
            
            pygame.draw.rect(self.display, (220, 220, 220), (start, (taille_inv, taille_inv)), taille_bordure)



    def afficher_entites(self, attaque=False, corrected_movement=Vector(0, 0), render_movement=Vector(0, 0)):
        """Afficher toutes les entités sur l'écran (hors joueur)
        Calcule aussi les différentes attaques
        
        Args:
            offset (Vector): le déplacement de la carte

        Retourne:

        """
        entites = sorted(self.game.entites, key=lambda entite: entite.position.y)
        player_pos = self.player.real_pos

        entite_trouvee = False
        item = self.player.get_selected_item()
        attaque = attaque and item and item.nom=="Épée"

        for entite in entites:
            if isinstance(entite, Joueur):
                continue
            entite.draw(self.display, player_pos, self.map)
            if DEBUG:
                pygame.draw.rect(self.display, (255, 0, 0), entite.rect, 1)
            entite_pos = Vector(*entite.real_pos)
            distance = entite_pos.distance_between(Vector(*self.player.rect.center))

            # si l'entité est un monstre, on vérifie si le joueur est à portée
            if entite.vitesse > 0:
                entite_occupe = entite.occupe

                if attaque and distance <= DISTANCE_ATTAQUE_JOUEUR:
                    entite_trouvee = True
                    arme = self.player.get_selected_item()
                    if isinstance(arme, Arme):
                        pygame.mixer.Sound("ressources/audio/" + SOUNDS["epee"]).play()
                    attaque_reussie = self.player.attaquer(entite, arme.degats)
                    if not attaque_reussie:
                        self.player.en_attente = datetime.now() + timedelta(milliseconds=500)

                    if attaque_reussie:

                        if entite.vie <= 0:
                            self.looter(entite)
                            self.game.score += 1
                            self.game.entites.remove(entite)
                        else:
                            entite.en_attente = datetime.now() + timedelta(milliseconds=300)


                        
                        self.appliquer_recul(entite, self.player)
                

                elif not entite_occupe and distance <= DISTANCE_ATTAQUE_MONSTRE and self.player.vie > 0:
                    attaque = entite.attaquer(self.player, entite.degats)
                    if attaque:
                        # Appliquer recul sur les entités
                        self.appliquer_recul(self.player, entite)

                        
                        

                # si le joueur est à portée de l'entité, on la déplace
                elif not entite_occupe and DISTANCE_AGRO_STOP_MONSTRES < distance <= DISTANCE_AGRO_MONSTRES:
                    vector_to_player = (player_pos - entite_pos).normalize()
                    entite_movement = vector_to_player * PLAYER_SPEED / FRAME_RATE * entite.vitesse
                    entite.position = entite.position + entite_movement
                    # jouer le cri du goebelin avec 1/100 de chance
                    if entite.nom == "Gobelin" and randint(0, 100) == 1:
                        pygame.mixer.Sound("ressources/audio/" + SOUNDS["cri"]).play()


                # relier les entités au joueur
                if DEBUG:
                    pygame.draw.line(self.display, (255, 0, 0), self.player.rect.center, entite.rect.center, 1)

                        
                    
            elif entite.vitesse > -5: #Entité au sol (objet, clé, coffre)
                if distance <= DISTANCE_POUR_RAMASSER_OBJET:
                    est_ramasse = entite.ramasser(self.player)
                    if est_ramasse:
                        if isinstance(entite.objet, Cle):
                            self.game.score += 2
                            pygame.mixer.Sound("ressources/audio/" + SOUNDS["cle"]).play()
                        else:
                            pygame.mixer.Sound("ressources/audio/" + SOUNDS["soin"]).play()
                        self.game.entites.remove(entite)

        if self.player.vie > 0:
            self.afficher_joueur(corrected_movement=corrected_movement, render_movement=render_movement)
        
        if attaque and not entite_trouvee:
            self.player.en_attente = datetime.now() + timedelta(milliseconds=500)
    
    def afficher_vie(self):
        # afficher les coeurs noirs
        nb_coeurs = self.player.vie_max // 20
        for i in range(nb_coeurs):
            self.display.blit(BLACK_HEART, (10 + i * 33, 10))
        # afficher la santé du joueur
        vie = self.player.vie / 20
        for i in range(int(vie)):
            self.display.blit(HEART, (10 + i * 33, 10))
        
        # si le joueur à un nombre non entier de points de vie, on affiche un coeur partiel sur un coeur noir
        if vie % 1 != 0:
            width = vie % 1 * 32
            self.display.blit(HEART, (10 + int(vie) * 33, 10), (0, 0, width, 32))

        # En dessous, afficher la vitesse du joueur
        # 1 botte pour la vitesse de base
        self.display.blit(BOTTE, (10, 42))

        # ensuite, 1 botte pour un buff de 25 de vitesse
        for i in range(self.player.buff_vitesse // 25):
            self.display.blit(BOTTE, (10 + 33 + i * 33, 42))


        # en dessous, afficher le score en blanc
        label = self.font.render(f"Score : {self.game.score}", 1, (0, 0, 0))
        self.display.blit(label, (10, 74))
        
    def appliquer_recul(self, entite1, entite2):
        """Applique un recul à l'entité 1 suite à une attaque de l'entité 2
        
        Args:
            entite1 (Entite): L'entité qui subit le recul
            entite2 (Entite): L'entité qui attaque

        Retourne:

        """
        # Calcul du vecteur de recul
        recul = (entite1.real_pos - entite2.real_pos).normalize()
        

        if isinstance(entite1, Joueur):
            entite2.position -= recul*RECUl_DEGATS_ATTAQUANT
            player_movement = recul*RECUL_DEGATS_ATTAQUEE
        else:
            entite1.position += recul*RECUL_DEGATS_ATTAQUEE
            player_movement = Vector(0,0)

        corrected_movement = self.map.correct_movement(self.player, player_movement)


        # répartir le déplacement entre le joueur et la carte pour que le joueur reste dans la zone morte
        rendered_movement, _ = self.process_movement(corrected_movement)
        self.afficher_joueur(corrected_movement=corrected_movement, render_movement=rendered_movement)
    
    def looter(self, entite):
        """Permet de looter une entité
        
        Args:
            entite (Entite): L'entité à looter

        Retourne:

        """
        # si l'entité est le joueur, on ne fait rien
        if isinstance(entite, Joueur):
            return

        difficulte = self.game.etage
        loots_possibles = []

        #Epée
        #chance par défaut : 30% (-5 par niveau jusqu'à 5)
        #Chance calculée : entre 0 et chance_default/(i+1) (i allant de 0 à 9)
        #Dégats : random entre 5 et 5 + i*difficulte//2 (i allant de 0 à 9)

        proba_def = max(30 - 5*difficulte, 5)*10
        for i in range(10):
            degats = randint(5, 5+i*difficulte//2)
            
            proba = randint(0, int(proba_def/(i+1))) #de 0 à 1000
            epee = Epee(degats)
            loots_possibles.append({
                "proba": proba,
                "objet": epee,
                "vecteur": Vector(randint(10, 50), randint(10, 50))
            })
        
        #Consommables
        #Chance par défaut : 50% (-5 par niveau jusqu'à 10)
        #Chance calculée : entre 0 et chance_default/(i+1) (i allant de 0 à 9)
        #Quantité : random entre 1 et 1 + i*difficulte//2 (i allant de 0 à 9)

        consommables = (Potion, Coeur, Botte)
        proba_def = max(50 - 5*difficulte, 10)*10
        for i in range(10):
            conso = consommables[randint(0, len(consommables)-1)]
            quantite = 1 #randint(1, 1+i*difficulte//2)

            proba = randint(0, int(proba_def/(i+1))) #de 0 à 1000
            objet = conso(quantite)
            loots_possibles.append({
                "proba": proba,
                "objet": objet,
                "vecteur": Vector(randint(10, 50), randint(10, 50))
            })

        loots = []
        for loot in loots_possibles:
            if randint(0, 1000) < loot["proba"]:
                loots.append(loot)
        
        
        for loot in loots:
            self.game.entites.append(ObjetAuSol(loot["objet"], entite.position + loot["vecteur"]))
        


    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.stop()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_z:
                self.states["up"] = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.states["down"] = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_q:
                self.states["left"] = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.states["right"] = True
            if event.key == pygame.K_SPACE:
                self.states["object_use"] = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_z:
                self.states["up"] = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.states["down"] = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_q:
                self.states["left"] = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.states["right"] = False
        
        elif event.type == pygame.MOUSEWHEEL:
            self.states["wheel"] = event.y

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if DEBUG:
                    self.player.vie -= 5
                else:
                    self.states["object_use"] = True

            elif event.button == 3 and DEBUG:
                self.player.vie += 10




