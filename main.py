from views.app import MainView
from controller.app_controller import AppController

if __name__ == "__main__":
    # 1. Création de la vue
    app = MainView()
    
    # 2. Création du contrôleur en lui passant la vue
    controller = AppController(app)
    
    # 3. Injection du contrôleur dans la vue (pour les callbacks des boutons)
    app.set_controller(controller)
    
    # 4. Lancement
    app.mainloop()