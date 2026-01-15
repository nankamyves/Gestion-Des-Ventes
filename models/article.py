from tabulate import tabulate  # Pour formater les tableaux dans les fichiers texte
import os  #Pour gérer les chemins de fichiers

# from . import article

# Dictionnaire pour stocker les articles
mes_Articles = {}

class Article:
    compteur_id = 0
    def __init__(self, nom, prix, quantite, stock_limite):
        self.id_article = Article.compteur_id
        self.nom = nom
        self.prix = prix
        self.quantite = quantite
        self.stock_limite = stock_limite
        Article.compteur_id += 1

    def __str__(self):
        return f"Article(ID: {self.id_article}, Nom: {self.nom}, Prix: {self.prix}, Quantité: {self.quantite}, stock_limite: {self.stock_limite})"


# Fonction pour afficher les articles
def displayArticles():
    for id_article, details in mes_Articles.items():
        print(f"ID: {id_article}, Nom: {details['nom']}, Prix: {details['prix']}, Quantité: {details['quantite']}, stock_limite: {details['stock_limite']}\n")



# Fonction pour ajouter un nouvel article à un tableau stocké dans un fichier texte
# new_article est une liste contenant les infos l'article à ajouter
def addArticle(new_article):

    # Ajouter le nouvel article aux données existantes
    mes_Articles[new_article.id_article] = {
        'id_article':new_article.id_article,
        'nom':new_article.nom, 
        'prix':new_article.prix, 
        'quantite':new_article.quantite,
        'stock_limite':new_article.stock_limite,
    }
    
    headers = ["Identifiants", "Nom", "Prix Unitaire", "Quantité en stock"]
    données = []
    # print("Dossier de travail actuel :", os.getcwd())
    now = os.path.dirname(__file__)
    chemin_fichier = os.path.join(now, "..", "articles.txt")
    chemin_final = os.path.abspath(chemin_fichier)
 
    for id_article, details in mes_Articles.items():
        données.append([
            id_article, 
            details['nom'], 
            details['prix'], 
            details['quantite'],
            details['stock_limite'],
    ])

    # Générer le tableau
    tableau_visuel = tabulate(données, headers, tablefmt="grid")

    # Écrire (remplacer) les données dans le fichier
    with open(chemin_final, "w", encoding="utf-8") as f:
        f.write(tableau_visuel)


# Suppression dun article par son ID
def removeArticle(id_article):
    if id_article in mes_Articles:
        del mes_Articles[id_article]
        print(f"Article avec l'ID : {id_article} a été supprimé !!")
    else:
        print(f"Aucun article trouvé avec l'ID {id_article} !!")


# Modification d'un article par son ID
def updateArticle(id_article, new_nom=None, new_prix=None, new_quantite=None, new_stock_limite=None):
    if id_article in mes_Articles:
        if new_nom is not None:
            mes_Articles[id_article]['nom'] = new_nom
        if new_prix is not None:
            mes_Articles[id_article]['prix'] = new_prix
        if new_quantite is not None:
            mes_Articles[id_article]['quantite'] = new_quantite
        if new_stock_limite is not None:
            mes_Articles[id_article]['stock_limite'] = new_stock_limite
        print(f"L'article avec l'ID : {id_article} a été modifié !!")
    else:
        print(f"Aucun article trouvé avec l'ID {id_article} !!")
        res = input("Voulez-vous ajouter un nouvel article avec cet ID ?\nEntrez 'y' pour ajouter, ou 'n' pour annuler : ")
        if res.lower() == 'y':
            nom = input("Entrez le nom de l'article : ")
            prix = float(input("Entrez le prix de l'article : "))
            quantite = int(input("Entrez la quantité en stock : "))
            stock_limite = int(input("Entrez le stock limite : "))
            new_article = Article(nom, prix, quantite, stock_limite)
            addArticle(new_article)
            print("Nouvel article ajouté avec succès !")
        else:
            print("Aucun article n'a été ajouté.")


#charger_articles_depuis_fichier pour actualiser le dictionnaire mes_Articles à partir du fichier articles.txt
def charger_articles_depuis_fichier():
    """Charge les données du fichier articles.txt dans le dictionnaire mes_Articles"""
    now = os.path.dirname(__file__)
    chemin_final = os.path.abspath(os.path.join(now, "..", "articles.txt"))
    
    mes_Articles.clear() # On vide pour éviter les doublons au rechargement
    
    if os.path.exists(chemin_final):
        with open(chemin_final, "r", encoding="utf-8") as f:
            lignes = f.readlines()
            
        for ligne in lignes:
            # On ignore les lignes de décoration (+---+) et l'en-tête
            if "+" in ligne or "Identifiants" in ligne or not ligne.strip():
                continue
            
            # Parsing: | 0 | Produit A | 10.5 | 100 | 20 |
            parties = [p.strip() for p in ligne.split("|") if p.strip()]
            
            if len(parties) >= 5: # ID, Nom, Prix, Qté, Limite
                try:
                    id_art = int(parties[0])
                    nom = parties[1]
                    prix = float(parties[2])
                    qty = int(parties[3])
                    limite = int(parties[4])
                    
                    # Reconstruction de l'objet
                    # Astuce: On ne réutilise pas Article() directement pour éviter d'incrémenter le compteur auto inutilement
                    # Ou on ajuste le compteur après
                    mes_Articles[id_art] = {
                        'id_article': id_art,
                        'nom': nom, 'prix': prix, 'quantite': qty, 'stock_limite': limite
                    }
                    # Mettre à jour le compteur de classe pour qu'il reparte du bon ID
                    if id_art >= Article.compteur_id:
                        Article.compteur_id = id_art + 1
                except ValueError:
                    continue


# Fonction pour sauvegarder les articles dans le fichier articles.txt
def saveArticlesToFile():
    path = os.path.abspath("articles.txt")
    with open(path, "w", encoding="utf-8") as f:
        for id_art, d in mes_Articles.items():
            line = f"{id_art};{d['nom']};{d['prix']};{d['quantite']};{d['stock_limite']}\n"
            f.write(line)

# # Mes tests d'utilisation
# a = Article("Produit A", 10.5, 100, 20)
# b = Article("Produit B", 10.5, 50, 30)
# c = Article("Produit C", 1.5, 20, 10)

# addArticle(a)
# addArticle(b)
# addArticle(c)
# print("Le tableau a été mis à jour !")
# print("mes_Articles :", mes_Articles)

# displayArticles()
# # removeArticle(0)
# # print("Après suppression de l'article avec l'ID 0 :")
# # print("mes_Articles :", mes_Articles)
# updateArticle(1,new_nom=None, new_prix=12.0, new_quantite=10, new_stock_limite=None)
# print("Après modification de l'article avec l'ID 1 :")
# displayArticles()