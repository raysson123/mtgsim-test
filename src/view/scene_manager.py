# src/view/scene_manager.py
class SceneManager:
    def __init__(self, game):
        self.game = game # Acesso aos componentes visuais

    def desenhar_cena_atual(self):
        estado = self.game.session.estado_atual
        tela = self.game.tela
        
        if estado == "menu":
            self.game.menu_view.exibir_menu_principal(...)
        elif estado == "jogo":
            self.game.table_mgr.draw_layout(...)
            # ... desenha HUD ...
        elif estado == "colecao":
            self.game.collection_view.exibir()