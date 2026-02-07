import os
import sys
import pygame
import tkinter as tk
from tkinter import filedialog

# --- [CONFIGURAÇÃO DE CAMINHOS E IMPORTS] ---
diretorio_raiz = os.path.dirname(os.path.abspath(__file__))
if diretorio_raiz not in sys.path:
    sys.path.insert(0, diretorio_raiz)

try:
    from src.view.assets_mgr import AssetsManager
    from src.view.table_manager import TableManager 
    from src.view.ui_components import UIComponents  
    from src.view.menu_view import MenuView
    from src.view.collection_view import CollectionView  # <--- NOVA IMPORTAÇÃO
    from src.model.deck_loader import DeckLoader
    from src.model.player import Player
    from src.model.turn_manager import TurnManager 
    from src.controller.rules_engine import RulesEngine
    from src.controller.ai_engine import AIEngine
    from src.controller.input_handler import InputHandler
    from src.controller.combat_manager import CombatManager
except Exception as e:
    print(f"Erro ao importar módulos internos: {e}")
    sys.exit(1)

class MTGGame:
    def __init__(self):
        pygame.init()
        # Tkinter escondido para os diálogos de arquivo
        self.root = tk.Tk()
        self.root.withdraw()
        
        # Configuração de Janela
        info = pygame.display.Info()
        self.largura, self.altura = info.current_w, info.current_h
        self.tela = pygame.display.set_mode((self.largura, self.altura), pygame.RESIZABLE)
        pygame.display.set_caption("MTG Commander Simulator - Pro")
        
        # --- Componentes Principais ---
        self.ui = UIComponents(self.largura, self.altura)
        self.assets_mgr = AssetsManager()
        
        # Passamos assets_mgr para o TableManager poder desenhar cartas corretamente
        self.table_mgr = TableManager(self.largura, self.altura, self.assets_mgr)
        
        self.turn_mgr = TurnManager()
        self.combat_mgr = CombatManager()
        
        self.fontes = {
            'titulo': pygame.font.SysFont("Arial", 64, bold=True),
            'menu': pygame.font.SysFont("Arial", 28, bold=True),
            'vida': pygame.font.SysFont("Arial", 36, bold=True),
            'fase': pygame.font.SysFont("Arial", 22, bold=True)
        }
        
        # --- Inicialização das Views ---
        self.menu_view = MenuView(self.tela, self.ui, self.fontes)
        self.collection_view = CollectionView(self.tela, self.ui, self.assets_mgr, self.fontes) # <--- INICIALIZA COLEÇÃO
        self.handler = InputHandler(self)
        
        # --- Estados do Jogo ---
        self.estado_atual = "menu"
        self.executando = True
        self.relogio = pygame.time.Clock()
        
        # --- Dados de Sessão ---
        self.jogadores_ativos = []
        self.jogador_local = None
        self.total_jogadores_selecionado = 4 
        self.decks_disponiveis = []
        self.indice_deck_selecionado = 0
        self.nome_sala = ""
        self.input_ativo_sala = False
        
        # Cadastro
        self.input_nome_deck = ""
        self.caminho_arquivo_selecionado = ""
        self.input_ativo_deck = False

        # Inicializa a lista de decks
        self.atualizar_lista_decks()

    def atualizar_lista_decks(self):
        """Procura decks nas pastas de dados (User e Imported)."""
        pastas = [
            os.path.join("data", "decks", "user_decks"),
            os.path.join("data", "decks", "imported")
        ]
        
        self.decks_disponiveis = []
        for caminho in pastas:
            if os.path.exists(caminho):
                for item in os.listdir(caminho):
                    # Remove extensões para mostrar apenas o nome
                    nome = item.replace(".txt", "").replace(".json", "")
                    if nome not in self.decks_disponiveis:
                        self.decks_disponiveis.append(nome)
        
        if not self.decks_disponiveis:
            self.decks_disponiveis = ["Nenhum Deck Encontrado"]

    def iniciar_jogo(self):
        """Prepara e inicia a partida."""
        if not self.decks_disponiveis or self.decks_disponiveis[0] == "Nenhum Deck Encontrado": 
            print("Nenhum deck disponível para jogar!")
            return
        
        # Pega o deck selecionado (Por enquanto o primeiro da lista ou o índice 0)
        nome_deck_origem = self.decks_disponiveis[self.indice_deck_selecionado]
        nome_pasta_deck = nome_deck_origem.lower().replace(" ", "_")
        
        # Tenta localizar o arquivo do deck
        caminho_txt = os.path.join("data", "decks", "user_decks", f"{nome_pasta_deck}.txt")
        if not os.path.exists(caminho_txt):
            caminho_txt = os.path.join("data", "decks", "imported", nome_pasta_deck, "decklist.txt")

        if os.path.exists(caminho_txt):
            print(f"Carregando deck: {nome_pasta_deck}")
            lista_nomes = DeckLoader.load_from_txt(caminho_txt)
            
            # Pré-carregamento visual (garante que as imagens existem)
            self.assets_mgr.baixar_deck_completo(nome_pasta_deck, lista_cartas=lista_nomes, 
                                               tela=self.tela, fonte=self.fontes['menu'])
            
            # Configura a Mesa
            self.table_mgr.ajustar_layout(self.total_jogadores_selecionado)
            self.jogadores_ativos = []
            self.combat_mgr.limpar_combate()

            for i in range(self.total_jogadores_selecionado):
                is_bot = (i != 0)
                p = Player("Você" if i == 0 else f"Bot {i}", lista_nomes)
                p.shuffle()
                # Draw inicial passando o contexto do deck para carregar imagens certas
                p.draw(self.assets_mgr, 7, deck_name=nome_pasta_deck)
                
                if i == 0: self.jogador_local = p
                self.jogadores_ativos.append({'player': p, 'slot': i, 'is_bot': is_bot})
            
            self.turn_mgr.em_mulligan = True 
            self.estado_atual = "jogo"
        else:
            print(f"Erro: Arquivo do deck não encontrado em {caminho_txt}")

    def update(self):
        if self.estado_atual == "jogo":
            pos_mouse = pygame.mouse.get_pos()
            nome_deck_folder = self.decks_disponiveis[self.indice_deck_selecionado].lower().replace(" ", "_")

            # Resolução de Combate
            fase_atual = self.turn_mgr.get_fase_atual()
            if fase_atual == "DAMAGE" and self.combat_mgr.fila_ataque:
                self.combat_mgr.resolver_dano_total(self.jogadores_ativos, RulesEngine)

            for item in self.jogadores_ativos:
                p = item['player']
                quad = self.table_mgr.get_player_quadrant(item['slot'])
                
                # IA joga
                if item['is_bot'] and not self.turn_mgr.em_mulligan:
                    AIEngine.pensar_e_jogar(item, self.assets_mgr, nome_deck_folder, 
                                         self.turn_mgr, self.combat_mgr, self.jogadores_ativos)
                
                # Jogador Local organiza mesa
                if p == self.jogador_local:
                    p.organize_battlefield(quad.width, quad.height, quad.x, quad.y)
                    p.organize_hand(quad.width, quad.height, quad.x, quad.y)

    def draw(self):
        self.tela.fill((15, 15, 15))
        
        # --- DESENHO DOS ESTADOS ---
        if self.estado_atual == "menu":
            self.menu_view.exibir_menu_principal() # Novo menu simplificado
            
        elif self.estado_atual == "cadastro":
            self.menu_view.exibir_tela_cadastro(self.input_nome_deck, self.input_ativo_deck, 
                                              self.caminho_arquivo_selecionado)
        
        elif self.estado_atual == "colecao":
            self.collection_view.exibir() # <--- DESENHA A COLEÇÃO
            
        elif self.estado_atual == "jogo":
            self.table_mgr.draw_layout(self.tela, self.turn_mgr.indice_jogador_ativo)
            
            nome_deck_folder = self.decks_disponiveis[self.indice_deck_selecionado].lower().replace(" ", "_")
            
            for item in self.jogadores_ativos:
                p = item['player']
                
                # Desenha cartas passando o deck_folder correto para o AssetsManager
                for c in p.battlefield + (p.hand if p == self.jogador_local else []):
                    c.draw(self.tela, self.assets_mgr, nome_deck_folder)

            # Botões de HUD (Fase e Mulligan)
            self.ui.desenhar_botao_arredondado(self.tela, (0, 80, 150), self.ui.btn_proxima_fase, 
                                             self.turn_mgr.get_fase_atual(), self.fontes['fase'])
            
            if self.turn_mgr.em_mulligan:
                overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                self.tela.blit(overlay, (0,0))
                self.ui.desenhar_botao_arredondado(self.tela, (34, 177, 76), self.ui.btn_manter_mao, "MANTER", self.fontes['menu'])
                self.ui.desenhar_botao_arredondado(self.tela, (180, 50, 50), self.ui.btn_fazer_mulligan, "MULLIGAN", self.fontes['menu'])

        pygame.display.flip()

    def run(self):
        while self.executando:
            self.handler.processar_eventos(pygame.event.get())
            self.update()
            self.draw()
            self.relogio.tick(60)
        pygame.quit()

if __name__ == "__main__":
    MTGGame().run()