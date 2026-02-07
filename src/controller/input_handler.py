import pygame
from tkinter import filedialog
# Importe o novo controlador
from src.controller.deck_builder_controller import DeckBuilderController

class InputHandler:
    def __init__(self, game):
        self.game = game
        # Instancia o controlador específico de cadastro
        self.deck_builder = DeckBuilderController(self.game.assets_mgr)

    # ... processar_eventos e handle_menu (MANTÉM IGUAL) ...

    def handle_cadastro(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            ui = self.game.ui
            pos = evento.pos
            
            self.game.input_ativo_deck = ui.campo_nome_deck.collidepoint(pos)
            
            if ui.btn_selecionar_arquivo.collidepoint(pos):
                caminho = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
                if caminho: self.game.caminho_arquivo_selecionado = caminho
            
            # --- AQUI ESTA A MUDANÇA ---
            if ui.btn_salvar_deck.collidepoint(pos):
                if self.game.input_nome_deck and self.game.caminho_arquivo_selecionado:
                    # O InputHandler pede para o DeckBuilderController trabalhar
                    sucesso = self.deck_builder.iniciar_importacao(
                        self.game.caminho_arquivo_selecionado, 
                        self.game.input_nome_deck
                    )
                    
                    if sucesso:
                        # Pega a lista processada pelo controller para exibir na tela
                        self.game.lista_temp_cadastro = self.deck_builder.lista_cartas_temp
                        self.game.estado_atual = "selecao_commander"
            
            if ui.btn_voltar_menu.collidepoint(pos):
                self.game.estado_atual = "menu"
        
        # ... teclado igual ...

    def handle_selecao_commander(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_y = evento.pos[1]
            indice = (mouse_y - 150) // 35
            lista = self.game.lista_temp_cadastro
            
            if 0 <= indice < len(lista):
                commander_name = lista[indice]
                
                # O InputHandler manda o Controller finalizar
                self.deck_builder.finalizar_cadastro(
                    commander_name, 
                    self.game.tela, 
                    self.game.fontes['menu']
                )
                
                self.game.atualizar_lista_decks()
                self.game.estado_atual = "menu"