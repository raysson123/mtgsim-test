import pygame
import sys
from src.model.game_session import GameSession
from src.view.scene_manager import SceneManager
from src.controller.input_handler import InputHandler
from src.view.ui_components import UIComponents
from src.view.assets_mgr import AssetsManager
from src.view.table_manager import TableManager
from src.model.turn_manager import TurnManager
from src.controller.combat_manager import CombatManager

class GameApp:
    def __init__(self):
        # 1. Inicialização do Pygame (A Janela)
        pygame.init()
        info = pygame.display.Info()
        self.largura, self.altura = info.current_w, info.current_h
        self.tela = pygame.display.set_mode((self.largura, self.altura), pygame.RESIZABLE)
        pygame.display.set_caption("MTG Commander Simulator - Pro")
        self.relogio = pygame.time.Clock()
        self.executando = True

        # 2. Inicialização dos Utilitários Base
        self.assets_mgr = AssetsManager()
        self.fontes = {
            'titulo': pygame.font.SysFont("Arial", 64, bold=True),
            'menu': pygame.font.SysFont("Arial", 28, bold=True),
            'vida': pygame.font.SysFont("Arial", 36, bold=True),
            'fase': pygame.font.SysFont("Arial", 22, bold=True)
        }
        self.ui = UIComponents(self.largura, self.altura)

        # 3. Inicialização dos Dados (Model)
        # GameSession guarda: jogadores, decks, quem é o jogador local, etc.
        self.session = GameSession() 
        
        # Managers de Lógica
        self.table_mgr = TableManager(self.largura, self.altura, self.assets_mgr)
        self.turn_mgr = TurnManager()
        self.combat_mgr = CombatManager()

        # 4. Inicialização do Visual (View) e Controlo (Controller)
        # O SceneManager sabe desenhar o Menu, Jogo ou Coleção baseado no estado da session
        self.scene_manager = SceneManager(self) 
        
        # O InputHandler processa os cliques e altera a session
        self.handler = InputHandler(self) 

    def run(self):
        """O Loop Principal do Jogo (The Game Loop)"""
        while self.executando:
            # A. Processar Entrada (Teclado/Mouse)
            eventos = pygame.event.get()
            self.handler.processar_eventos(eventos)

            # B. Atualizar Lógica (Update)
            # Aqui você pode chamar self.session.update() ou lógica de IA
            self.update_game_logic()

            # C. Desenhar na Tela (Draw)
            self.tela.fill((15, 15, 20)) # Limpa tela
            self.scene_manager.desenhar_cena_atual() # Desenha a tela certa
            pygame.display.flip() # Atualiza monitor

            # D. Controlar FPS
            self.relogio.tick(60)

        pygame.quit()
        sys.exit()

    def update_game_logic(self):
        """Centraliza atualizações que não dependem de cliques (ex: animações, IA)."""
        if self.session.estado_atual == "jogo":
            # Exemplo: Se tiver IA jogando, chama aqui
            pass