from tabulate import tabulate
import os
from datetime import datetime

# Import relatif simple pour article (car article n'importe pas facture, donc pas de risque)
# from . import article
from .article import mes_Articles

# --- NOTE IMPORTANTE : ON NE MET PAS 'from . import vente' ICI ---
# On le mettra plus bas, à l'intérieur des fonctions, pour éviter l'erreur.

mes_Factures = {}

class Facture:
    compteur_id = 0
    def __init__(self, id_vente, prix_total, date_facture=None):
        self.id_facture = Facture.compteur_id
        self.id_vente = id_vente
        self.prix_total = prix_total
        self.date_facture = datetime.now().strftime("%d/%m/%Y %H:%M") if date_facture is None else date_facture
        Facture.compteur_id += 1

def calculateTTC(prix_total, taux_tva=0.20):
    return prix_total * (1 + taux_tva)

def calculateHT(prix_total, taux_tva=0.20):
    return prix_total / (1 + taux_tva)

def calculateTVA(prix_total, taux_tva=0.20):
    return prix_total - calculateHT(prix_total, taux_tva)

def generateFacture(facture, liste_ventes_details):
    # ... (Votre code de génération de facture reste identique ici) ...
    # Copiez-collez votre fonction generateFacture existante ici
    # Juste pour l'exemple, je mets le début :
    ht = calculateHT(facture.prix_total)
    tva = calculateTVA(facture.prix_total)
    ttc = calculateTTC(facture.prix_total)
    
    lignes_produits = ""
    for item in liste_ventes_details:
        nom = item['nom'][:20]
        qte = item['quantite_vendue']
        pu = item['prix_unitaire']
        total_ligne = item['prix_total']
        lignes_produits += f"{nom:<20} {qte:>3} x {pu:>8.0f} | {total_ligne:>10.0f} FCFA\n"

    template = f"""
============================================================
                     FACTURE CLIENT
============================================================
N° Facture : {facture.id_facture}
Date       : {facture.date_facture}
------------------------------------------------------------
DESCRIPTION               QTÉ x P.U.      |   TOTAL
------------------------------------------------------------
{lignes_produits}
------------------------------------------------------------
TOTAL H.T.                                | {ht:>10.0f} FCFA
TVA (20%)                                 | {tva:>10.0f} FCFA
============================================================
TOTAL À PAYER (TTC)                       | {ttc:>10.0f} FCFA
============================================================
"""
    print(template)
    now = os.path.dirname(__file__)
    dossier = os.path.join(now, "..", "factures_clients") # Dossier corrigé
    if not os.path.exists(dossier): 
        os.makedirs(dossier)
    with open(os.path.join(dossier, f"facture_{facture.id_facture}.txt"), "w", encoding="utf-8") as f:
        f.write(template)

def addFacture(new_facture):
    mes_Factures[new_facture.id_facture] = {
        'id_facture': new_facture.id_facture,
        'id_vente': new_facture.id_vente,
        'prix_total': new_facture.prix_total,
        'date_facture': new_facture.date_facture
    }
    # Note: generateFacture nécessite désormais une liste de détails. 
    # Si on ajoute une facture simple sans détails, on ne peut pas l'appeler directement sans adapter.
    # Pour l'instant, on laisse comme ça.

def generateFacturesForAllVentes():
    # --- IMPORT DÉCALÉ ICI POUR ÉVITER L'ERREUR ---
    from .vente import mes_Ventes, calculateTotalPrice 
    # -----------------------------------------------
    
    for id_vente, details in mes_Ventes.items():
        prix_total = calculateTotalPrice(details['id_article'], details['quantite_vendue'])
        facture = Facture(id_vente, prix_total)
        addFacture(facture)





# from tabulate import tabulate  # Pour formater les tableaux dans les fichiers texte
# import os  #Pour gérer les chemins de fichiers
# from datetime import datetime  # Pour gérer les dates de vente

# # import article  # module pour accéder à  mes_Articles(Dictionnaire des articles)
# from . import article
# from . import vente
# from .article import mes_Articles
# from .vente import mes_Ventes, mes_Possibles_Ventes, Vente, addVente, calculateTotalPrice
# from .facture import generateFacture

# # Dictionnaire pour stocker les factures
# mes_Factures = {}

# class Facture:
#     compteur_id = 0
#     def __init__(self, id_vente, prix_total, date_facture=None, facture_ht=None, facture_tva=None, facture_ttc=None):
#         self.id_facture = Facture.compteur_id
#         self.facture_ht = facture_ht
#         self.facture_tva = facture_tva
#         self.facture_ttc = facture_ttc
#         self.id_vente = id_vente
#         self.prix_total = prix_total
#         self.date_facture = datetime.now().strftime("%d/%m/%Y %H:%M") if date_facture is None else date_facture
#         Facture.compteur_id += 1


# # Fonction pour afficher les factures
# def displayFactures():
#     for id_facture, details in mes_Factures.items():
#         print(f"ID Facture: {id_facture}, ID Vente: {details['id_vente']}, Prix Total: {details['prix_total']}, Date de Facture: {details['date_facture']}\n")


# # Fonction pour générer une facture formatée dans un fichier texte
# def generateFacture(facture, liste_ventes_details):
#     """
#     facture : instance de la classe Facture
#     liste_ventes_details : liste de dictionnaires contenant les infos des produits
#     """
#     # Calculs monétaires (basés sur vos fonctions existantes)
#     ht = calculateHT(facture.prix_total)
#     tva = calculateTVA(facture.prix_total)
#     ttc = calculateTTC(facture.prix_total)
    
#     # 1. Construction dynamique de la liste des produits
#     lignes_produits = ""
#     for item in liste_ventes_details:
#         # Format : Nom du produit | Qté x Prix Unitaire | Total ligne
#         nom = item['nom'][:20] # Limite à 20 caractères
#         qte = item['quantite_vendue']
#         pu = item['prix_unitaire']
#         total_ligne = item['prix_total']
        
#         lignes_produits += f"{nom:<20} {qte:>3} x {pu:>8.0f} | {total_ligne:>10.0f} FCFA\n"

#     # 2. Template de la facture
#     template = f"""
# ============================================================
#                      FACTURE CLIENT
# ============================================================
# N° Facture : {facture.id_facture}
# Date       : {facture.date_facture}
# ------------------------------------------------------------
# DESCRIPTION               QTÉ x P.U.      |   TOTAL
# ------------------------------------------------------------
# {lignes_produits}
# ------------------------------------------------------------
# TOTAL H.T.                                | {ht:>10.0f} FCFA
# TVA (20%)                                 | {tva:>10.0f} FCFA
# ============================================================
# TOTAL À PAYER (TTC)                       | {ttc:>10.0f} FCFA
# ============================================================
#               Merci de votre fidélité !
# ============================================================
# """

#     # Affichage Console
#     print(template)

#     # Sauvegarde Fichier
#     now = os.path.dirname(__file__)
#     dossier = os.path.join(now, "..", "factures.txt")
#     if not os.path.exists(dossier): 
#         os.makedirs(dossier)
    
#     with open(os.path.join(dossier, f"facture_{facture.id_facture}.txt"), "w", encoding="utf-8") as f:
#         f.write(template)



# # Fonction pour ajouter une nouvelle facture
# def addFacture(new_facture):
#     mes_Factures[new_facture.id_facture] = {
#         'id_facture': new_facture.id_facture,
#         'id_vente': new_facture.id_vente,
#         'prix_total': new_facture.prix_total,
#         'date_facture': new_facture.date_facture
#     }
#     # Générer la facture (fichier texte)
#     generateFacture(new_facture)


# # Fonction pour le calcul du TTC d'une facture
# def calculateTTC(prix_total, taux_tva=0.20):
#     ttc = prix_total * (1 + taux_tva)
#     return ttc  

# # Fonction pour le calcul du HT d'une facture
# def calculateHT(prix_total, taux_tva=0.20):
#     ht = prix_total / (1 + taux_tva)
#     return ht

# # Fonction pour le calcul de la TVA d'une facture
# def calculateTVA(prix_total, taux_tva=0.20):
#     tva = prix_total - calculateHT(prix_total, taux_tva)
#     return tva

# # Fonction pour générer des factures pour toutes les ventes confirmées dans un fichier texte
# def generateFacturesForAllVentes():
#     for id_vente, details in mes_Ventes.items():
#         prix_total = calculateTotalPrice(details['id_article'], details['quantite_vendue'])
#         facture = Facture(
#             id_vente = id_vente,
#             prix_total = prix_total,
#             date_facture = datetime.now().strftime("%d/%m/%Y %H:%M")
#         )
#         addFacture(facture)


# # Fonction pour générer une facture pour une vente spécifique
# def generateFactureForVente(id_vente):
#     if id_vente in mes_Ventes:
#         details = mes_Ventes[id_vente]
#         prix_total = calculateTotalPrice(details['id_article'], details['quantite_vendue'])
#         facture = Facture(
#             id_vente = id_vente,
#             prix_total = prix_total,
#             date_facture = datetime.now().strftime("%d/%m/%Y %H:%M")
#         )
#         addFacture(facture)
#     else:
#         print(f"Aucune vente trouvée avec l'ID {id_vente}\n")



