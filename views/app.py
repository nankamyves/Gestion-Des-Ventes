import tkinter as tk
from tkinter import ttk, messagebox

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion Supermarché - MVC")
        self.geometry("900x600")
        self.controller = None
        self.tree_art = None  # Initialisation par défaut
        self.tree_panier = None
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Treeview", rowheight=25)
        self.style.configure("TButton", padding=6, font=('Helvetica', 10))

        # --- Page d'accueil (Splash Screen) ---
        self.welcome_frame = tk.Frame(self, bg="#2c3e50")
        self.welcome_frame.pack(fill="both", expand=True)
        
        lbl_welcome = tk.Label(self.welcome_frame, text="Bienvenue dans le Gestionnaire", 
                               font=("Arial", 24, "bold"), fg="white", bg="#2c3e50")
        lbl_welcome.pack(expand=True)
        
        btn_enter = tk.Button(self.welcome_frame, text="Accéder à l'application", 
                              command=self.show_dashboard, font=("Arial", 12), bg="#e74c3c", fg="white")
        btn_enter.pack(pady=20)

        # Redirection automatique après 3 secondes
        self.after(3000, self.show_dashboard)

        # --- Dashboard (Caché au début) ---
        self.dashboard_frame = tk.Frame(self)

    def set_controller(self, controller):
        self.controller = controller

    def show_dashboard(self):
        # On annule le rappel automatique s'il existe pour éviter le double appel
        if hasattr(self, '_after_id'):
            self.after_cancel(self._after_id)
            
        if self.dashboard_frame.winfo_ismapped(): # Si déjà affiché, on ne fait rien
            return
        self.welcome_frame.pack_forget()
        self.dashboard_frame.pack(fill="both", expand=True)
        self.setup_dashboard()
        # Charger les données APRÈS que les widgets soient créés
        if self.controller:
            self.controller.refresh_article_list()

    def setup_dashboard(self):
        # Création des onglets
        notebook = ttk.Notebook(self.dashboard_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Onglet 1: Gestion Stock (Articles)
        self.tab_stock = tk.Frame(notebook)
        notebook.add(self.tab_stock, text="Gestion du Stock")
        self.setup_stock_tab()

        # Onglet 2: Ventes (Caisse)
        self.tab_vente = tk.Frame(notebook)
        notebook.add(self.tab_vente, text="Caisse & Facturation")
        self.setup_vente_tab()

        # Onglet 3: Historique
        self.tab_history = tk.Frame(notebook)
        notebook.add(self.tab_history, text="Historique Ventes")
        self.setup_history_tab()

    # ---------------- UI STOCK ----------------
    def setup_stock_tab(self):
        # Formulaire
        frame_form = tk.LabelFrame(self.tab_stock, text="Nouvel Article", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_form, text="Nom:").grid(row=0, column=0)
        self.ent_nom = tk.Entry(frame_form)
        self.ent_nom.grid(row=0, column=1, padx=5)

        tk.Label(frame_form, text="Prix:").grid(row=0, column=2)
        self.ent_prix = tk.Entry(frame_form)
        self.ent_prix.grid(row=0, column=3, padx=5)

        tk.Label(frame_form, text="Qté:").grid(row=0, column=4)
        self.ent_qty = tk.Entry(frame_form)
        self.ent_qty.grid(row=0, column=5, padx=5)
        
        tk.Label(frame_form, text="Limite:").grid(row=0, column=6)
        self.ent_lim = tk.Entry(frame_form)
        self.ent_lim.grid(row=0, column=7, padx=5)

        btn_add = ttk.Button(frame_form, text="Ajouter", command=self.action_add_article)
        btn_add.grid(row=0, column=8, padx=10)

        # Tableau
        columns = ("ID", "Nom", "Prix", "Quantité", "Seuil Limite")
        self.tree_art = ttk.Treeview(self.tab_stock, columns=columns, show="headings")
        for col in columns:
            self.tree_art.heading(col, text=col)
            self.tree_art.column(col, width=100)
        self.tree_art.pack(fill="both", expand=True, padx=10, pady=10)

    def action_add_article(self):
        if self.controller:
            self.controller.ajouter_article(
                self.ent_nom.get(), self.ent_prix.get(), 
                self.ent_qty.get(), self.ent_lim.get()
            )
            # Clear entries
            self.ent_nom.delete(0, tk.END)
            self.ent_prix.delete(0, tk.END)
            self.ent_qty.delete(0, tk.END)
            self.ent_lim.delete(0, tk.END)

    def update_articles_table(self, data):
        if self.tree_art and self.tree_art.winfo_exists():
            for i in self.tree_art.get_children():
                self.tree_art.delete(i)
            for row in data:
                self.tree_art.insert("", "end", values=row)

    # ---------------- UI VENTE ----------------
    def setup_vente_tab(self):
        # Zone Haut : Ajout au panier
        frame_top = tk.Frame(self.tab_vente, pady=10)
        frame_top.pack()

        tk.Label(frame_top, text="ID Article:").pack(side="left", padx=5)
        self.ent_id_vente = tk.Entry(frame_top, width=10)
        self.ent_id_vente.pack(side="left", padx=5)

        tk.Label(frame_top, text="Quantité:").pack(side="left", padx=5)
        self.ent_qty_vente = tk.Entry(frame_top, width=10)
        self.ent_qty_vente.pack(side="left", padx=5)

        btn_panier = ttk.Button(frame_top, text="Ajouter au panier", command=self.action_add_panier)
        btn_panier.pack(side="left", padx=10)

        # Zone Milieu : Panier
        lbl_panier = tk.Label(self.tab_vente, text="Panier en cours (Ventes possibles)", font=("Arial", 12, "bold"))
        lbl_panier.pack(pady=5)

        cols = ("Ref Vente", "Article", "Qté Demandée")
        self.tree_panier = ttk.Treeview(self.tab_vente, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree_panier.heading(c, text=c)
        self.tree_panier.pack(fill="x", padx=20)

        # Zone Bas : Validation
        btn_validate = tk.Button(self.tab_vente, text="VALIDER LA FACTURE & PAYER", 
                                 bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                                 command=self.action_valider_tout)
        btn_validate.pack(pady=20, fill="x", padx=50)

    def action_add_panier(self):
        if self.controller:
            self.controller.ajouter_au_panier(self.ent_id_vente.get(), self.ent_qty_vente.get())
            self.ent_id_vente.delete(0, tk.END)
            self.ent_qty_vente.delete(0, tk.END)

    def update_panier_table(self, data):
        for i in self.tree_panier.get_children():
            self.tree_panier.delete(i)
        for row in data:
            self.tree_panier.insert("", "end", values=row)

    def action_valider_tout(self):
        if self.controller:
            self.controller.valider_vente_globale()

    def afficher_facture_popup(self):
        messagebox.showinfo("Facture", "La facture a été générée et sauvegardée dans le dossier 'factures_clients'.")

    # ---------------- UI HISTORIQUE ----------------
    def setup_history_tab(self):
        btn_refresh = ttk.Button(self.tab_history, text="Actualiser l'historique", command=self.load_history_text)
        btn_refresh.pack(pady=5)

        self.text_history = tk.Text(self.tab_history, font=("Consolas", 10))
        self.text_history.pack(fill="both", expand=True, padx=10, pady=10)

    def load_history_text(self):
        if self.controller:
            content = self.controller.lire_historique_fichier()
            self.text_history.delete("1.0", tk.END)
            self.text_history.insert("1.0", content)  