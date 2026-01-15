from tkinter import messagebox
from models.article import Article, addArticle, mes_Articles, charger_articles_depuis_fichier
from models.vente import mes_Possibles_Ventes, confirmPossibleVentes, addPossibleVente, Vente, RestArticleQuantity
import os

class AppController:
    def __init__(self, view):
        self.view = view
        self.charger_donnees_initiales()

    def charger_donnees_initiales(self):
        # Chargement des articles au démarrage
        charger_articles_depuis_fichier()
        self.refresh_article_list()

    def ajouter_article(self, nom, prix, quantite, limite):
        try:
            prix = float(prix)
            quantite = int(quantite)
            limite = int(limite)

            if prix < 0 or quantite < 0 or limite < 0:
                messagebox.showerror("Erreur", "Les valeurs ne peuvent pas être négatives.")
                return

            new_article = Article(nom, prix, quantite, limite)
            addArticle(new_article)
            self.refresh_article_list()
            messagebox.showinfo("Succès", "Article ajouté avec succès !")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides.")

    def ajouter_au_panier(self, id_article, quantite_demandee):
        try:
            id_article = int(id_article)
            quantite_demandee = int(quantite_demandee)

            if quantite_demandee <= 0:
                messagebox.showerror("Erreur", "La quantité doit être supérieure à 0.")
                return

            if id_article not in mes_Articles:
                messagebox.showerror("Erreur", "ID Article introuvable.")
                return

            # Vérification du stock
            stock_actuel = mes_Articles[id_article]['quantite']
            if quantite_demandee > stock_actuel:
                messagebox.showwarning("Stock Insuffisant", f"Seulement {stock_actuel} unités disponibles.")
                return

            # Ajout aux possibles ventes
            # Note: Ici on simplifie l'usage de Vente pour le panier temporaire
            vente_temp = Vente(id_article, quantite_demandee)
            addPossibleVente(vente_temp)
            
            self.refresh_panier_list()
        except ValueError:
            messagebox.showerror("Erreur", "Format de quantité invalide.")

    def valider_vente_globale(self):
        if not mes_Possibles_Ventes:
            messagebox.showinfo("Info", "Le panier est vide.")
            return

        # Validation et Génération de facture
        confirmPossibleVentes()
        
        # Vérification des alertes stock après vente
        self.verifier_alertes_stock()
        
        self.refresh_article_list()
        self.refresh_panier_list()
        self.view.afficher_facture_popup() # Feedback visuel

    def verifier_alertes_stock(self):
        alertes = []
        for id_art, details in mes_Articles.items():
            if details['quantite'] <= details['stock_limite']:
                alertes.append(f"{details['nom']} (Reste: {details['quantite']})")
        
        if alertes:
            msg = "ATTENTION - STOCK CRITIQUE :\n" + "\n".join(alertes)
            messagebox.showwarning("Alerte Stock", msg)

    def get_articles_data(self):
        """Retourne une liste de tuples pour l'affichage tableau"""
        data = []
        for id_art, d in mes_Articles.items():
            data.append((id_art, d['nom'], f"{d['prix']} FCFA", d['quantite'], d['stock_limite']))
        return data

    def get_panier_data(self):
        data = []
        for id_v, d in mes_Possibles_Ventes.items():
            nom_art = mes_Articles[d['id_article']]['nom']
            data.append((id_v, nom_art, d['quantite_vendue']))
        return data


    def lire_historique_fichier(self):
        # Forcer le chemin absolu à la racine du projet
        path = os.path.join(os.getcwd(), "ventes.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return "Aucun historique trouvé dans ventes.txt"

    # def lire_historique_fichier(self):
    #     """Lit le fichier ventes.txt pour l'afficher"""
    #     content = "Aucun historique disponible."
    #     now = os.path.dirname(__file__)
    #     path = os.path.join(now, "..", "ventes.txt") # Ajuster selon votre structure
    #     # Dans votre structure, le controller est dans /controllers, donc remonter 2 fois ?
    #     # Assumons que main.py lance tout, le chemin relatif dépend du CWD.
    #     # Utilisons un chemin relatif robuste:
    #     path = os.path.abspath("ventes.txt")
        
    #     if os.path.exists(path):
    #         with open(path, "r", encoding="utf-8") as f:
    #             content = f.read()
    #     return content

    # def refresh_article_list(self):
    #     self.view.update_articles_table(self.get_articles_data())

    def refresh_article_list(self):
        # On vérifie si l'attribut tree_art existe dans la vue avant de l'utiliser
        if hasattr(self.view, 'tree_art'):
            self.view.update_articles_table(self.get_articles_data())

    def refresh_panier_list(self):
        self.view.update_panier_table(self.get_panier_data())

    # Méthodes de gestion des articles(supprimer_article, modifier_article)
    def supprimer_article(self, id_article):
        if id_article in mes_Articles:
            del mes_Articles[id_article]
            self.refresh_article_list()
            messagebox.showinfo("Succès", "Article supprimé.")

    def modifier_article(self, id_art, nouveau_nom, nouveau_prix):
        if id_art in mes_Articles:
            mes_Articles[id_art]['nom'] = nouveau_nom
            mes_Articles[id_art]['prix'] = float(nouveau_prix)
            self.refresh_article_list()

    # Méthode pour annuler le panier
    def annuler_panier(self):
        from models.vente import clearPossibleVentes
        clearPossibleVentes()
        self.refresh_panier_list()
        messagebox.showinfo("Panier", "Ventes en attente annulées.")
