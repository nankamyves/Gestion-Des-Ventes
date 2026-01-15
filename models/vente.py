# from tabulate import tabulate  # Pour formater les tableaux dans les fichiers texte
# import os  # Pour gérer les chemins de fichiers
# from datetime import datetime  # Pour gérer les dates de vente

# # import article  # module pour accéder à  mes_Articles(Dictionnaire des articles)
# from . import article
# from .article import mes_Articles

# # import facture  # module pour accéder à  mes_Factures(Dictionnaire des factures)
# from . import facture
# from .facture import mes_Factures, Facture, generateFacture, calculateTotalPrice


from tabulate import tabulate
import os
from datetime import datetime

# Imports relatifs (le point . signifie "dans le même dossier")
from . import article
from .article import mes_Articles

# On importe facture normalement ici
from . import facture
from .facture import mes_Factures, Facture, generateFacture

# Dictionnaire pour stocker les ventes
mes_Ventes = {}

# Dictionnaire pour stocker les possibles ventes(Ce sont les ventes en attente de confirmation)
mes_Possibles_Ventes = {}

class Vente:
    compteur_id = 0
    def __init__(self, id_article, quantite_vendue, id_vente=None, prix_total=None, date_vente=None):
        # Si un id_vente est fourni, on l'utilise, sinon on prend le compteur
        if id_vente is not None:
            self.id_vente = id_vente
        else:
            self.id_vente = Vente.compteur_id
            Vente.compteur_id += 1
        self.id_vente = Vente.compteur_id
        self.id_article = id_article
        self.quantite_vendue = quantite_vendue
        self.date_vente = datetime.now().strftime("%d/%m/%Y %H:%M") if date_vente is None else date_vente

# Fonction pour afficher les ventes
def displayVentes():
    for id_vente, details in mes_Ventes.items():
        print(f"ID Vente: {id_vente}, ID Article: {details['id_article']}, Quantité Vendue: {details['quantite_vendue']}, Date de Vente: {details['date_vente']}\n")


#Calcul des quantités d'articles restantes
def RestArticleQuantity(id_article, quantite_vendue):
    res = article.mes_Articles[id_article]['quantite'] - quantite_vendue
    return res


# Fonction pour le calcul du prix total d'une vente
def calculateTotalPrice(id_article, quantite_vendue):
    prix_unitaire = article.mes_Articles[id_article]['prix']
    prix_total = prix_unitaire * quantite_vendue
    return prix_total


# Fonction pour ajouter une nouvelle vente
def addVente(new_vente):
    # Je récupère le reste probable après la vente
    reste_apres_vente = RestArticleQuantity(new_vente.id_article, new_vente.quantite_vendue)
    if (reste_apres_vente < 0):
        print(f"Vente impossible : stock insuffisant pour l'article ID {new_vente.id_article}-{article.mes_Articles[new_vente.id_article]['nom']}\n")
        res = input("Voulez-vous vendre le reste du stock disponible ? (y/n) : ")
        if res.lower() == 'y':
            # Vendre le reste du stock
            new_vente.quantite_vendue = article.mes_Articles[new_vente.id_article]['quantite']
            # Mettre à jour le stock de l'article à 0
            article.mes_Articles[new_vente.id_article]['quantite'] = 0
            # Ajouter la vente
            # mes_Ventes[new_vente.id_vente] = {
            #     'id_vente': new_vente.id_vente,
            #     'id_article': new_vente.id_article,
            #     'nom': article.mes_Articles[new_vente.id_article]['nom'],
            #     'quantite_vendue': new_vente.quantite_vendue, 
            #     'date_vente': new_vente.date_vente,
            # }
            return addVente(new_vente)  # Appel récursif pour ajouter la vente avec la quantité ajustée
        else:
            print("La vente est annulée !\n")
            return 0  # Retourne 0 si la vente est annulée
    else:
        # Ajouter la nouvelle vente aux données existantes
        total_price = calculateTotalPrice(new_vente.id_article, new_vente.quantite_vendue)
        print(f"Prix total de la vente : {total_price} \n")
        mes_Ventes[new_vente.id_vente] = {
            'id_vente': new_vente.id_vente,
            'id_article': new_vente.id_article,
            'nom': article.mes_Articles[new_vente.id_article]['nom'],
            'quantite_vendue': new_vente.quantite_vendue, 
            'date_vente': new_vente.date_vente,
        }
        print(f"Vente effectuée : {new_vente.quantite_vendue} unités de l'article ID {new_vente.id_article}-{article.mes_Articles[new_vente.id_article]['nom']}")
        headers = ["ID Ventes", "ID Article","Nom De L'article", "Quantite Vendue", "Date Vente"]
        données = []
        # print("Dossier de travail actuel :", os.getcwd())
        now = os.path.dirname(__file__)
        chemin_fichier = os.path.join(now, "..", "ventes.txt")
        chemin_final = os.path.abspath(chemin_fichier)
    
        for id_vente, details in mes_Ventes.items():
            données.append([
                id_vente, 
                details['id_article'], 
                details['nom'], 
                details['quantite_vendue'],
                details['date_vente'],
        ])

        # Générer le tableau
        tableau_visuel = tabulate(données, headers, tablefmt="grid")

        # Écrire (remplacer) les données dans le fichier
        with open(chemin_final, "w", encoding="utf-8") as f:
            f.write(tableau_visuel)

        print(f"Vente effectuée...")
        return total_price # Retourne le prix réel de la vente effectuée



# Fonction pour ajouter une possible vente
def addPossibleVente(new_possible_vente):
    # Ajouter la nouvelle possible vente aux données existantes
    mes_Possibles_Ventes[new_possible_vente.id_vente] = {
        'id_vente': new_possible_vente.id_vente,
        'id_article': new_possible_vente.id_article,
        'quantite_vendue': new_possible_vente.quantite_vendue, 
        'date_vente': new_possible_vente.date_vente,
    }
    print(f"Possible vente ajoutée : {new_possible_vente.quantite_vendue} unités de l'article ID {new_possible_vente.id_article}\n")


# Fonction pour afficher les possibles ventes
def displayPossibleVentes():
    for id_vente, details in mes_Possibles_Ventes.items():
        print(f"ID Vente: {id_vente}, ID Article: {details['id_article']}, Quantité Vendue: {details['quantite_vendue']}, Date de Vente: {details['date_vente']}\n")


# Fonction pour vider les possibles ventes après confirmation ou annulation
def clearPossibleVentes():
    mes_Possibles_Ventes.clear()
    print("Toutes les possibles ventes ont été confirmées et le tableau a été vidé.\n")


# Fonction pour ajouter chaque vente contenue dans les possibles ventes au tableau des ventes confirmées
# et générer une facture globale pour toutes ces ventes
def confirmPossibleVentes():
    total_facture = 0
    details_pour_facture = []
    
    # On boucle sur les ventes en attente
    for id_v, details in mes_Possibles_Ventes.items():
        # Récupération des infos de l'article
        info_art = article.mes_Articles[details['id_article']]
        
        # Création et ajout de la vente
        vente_obj = Vente(details['id_article'], details['quantite_vendue'], id_vente=id_v)
        prix_reel = addVente(vente_obj) 
        
        if prix_reel > 0:
            total_facture += prix_reel
            # On prépare la ligne pour la facture
            details_pour_facture.append({
                'nom': info_art['nom'],
                'quantite_vendue': vente_obj.quantite_vendue,
                'prix_unitaire': info_art['prix'],
                'prix_total': prix_reel
            })
    
    # Génération de la facture globale si au moins une vente a réussi
    if total_facture > 0:
        nouvelle_facture = Facture(id_vente="MULTIPLE", prix_total=total_facture)
        generateFacture(nouvelle_facture, details_pour_facture)
    
    clearPossibleVentes()



#    def confirmPossibleVentes():
#     total_general = 0
#     for id_vente, details in mes_Possibles_Ventes.items():
#         vente = Vente(
#             id_vente = id_vente,
#             id_article = details['id_article'],
#             quantite_vendue = details['quantite_vendue'],
#             date_vente = details['date_vente']
#         )
#         prix_de_cette_vente = addVente(vente)
#         total_general += prix_de_cette_vente
#     clearPossibleVentes()
#     print(f"Total général des ventes confirmées : {total_general}\n")
#     return total_general