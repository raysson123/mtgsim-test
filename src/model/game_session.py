# src/model/game_session.py
class GameSession:
    def __init__(self):
        self.jogadores_ativos = []
        self.jogador_local = None
        self.decks_disponiveis = []
        self.indice_deck_selecionado = 0
        
        # Estado atual global
        self.estado_atual = "menu" 
        
        # Managers que persistem
        self.turn_mgr = None
        self.combat_mgr = None
        self.assets_mgr = None