# src/controller/match_controller.py
from src.model.deck_loader import DeckLoader
from src.model.player import Player

class MatchController:
    @staticmethod
    def iniciar_partida(session, table_mgr, total_jogadores):
        """Configura jogadores, carrega decks e prepara a mesa."""
        nome_deck = session.decks_disponiveis[session.indice_deck_selecionado]
        lista_cartas = DeckLoader.load_deck_for_game(nome_deck)
        
        if not lista_cartas: return False

        # Configura Player e Bots... (código movido do main)
        session.jogadores_ativos = []
        for i in range(total_jogadores):
            p = Player(f"Player {i}", lista_cartas)
            # ... logica de shuffle e draw ...
            session.jogadores_ativos.append({'player': p, 'slot': i})
            
        session.estado_atual = "jogo"
        return True