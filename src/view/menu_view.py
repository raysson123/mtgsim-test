import pygame

class MenuView:
    def __init__(self, tela, ui, fontes):
        self.tela = tela
        self.ui = ui
        self.fontes = fontes

    def exibir_menu_principal(self):
        """Renderiza a interface do menu principal."""
        # Título com efeito simples
        txt_titulo = self.fontes['titulo'].render("MTG SIMULATOR", True, (255, 255, 255))
        pos_titulo = (self.tela.get_width()//2 - txt_titulo.get_width()//2, 100)
        self.tela.blit(txt_titulo, pos_titulo)

        # Botões conforme o novo modelo
        self.ui.desenhar_botao_menu(self.tela, self.ui.btn_jogar, "JOGAR", self.fontes['menu'])
        self.ui.desenhar_botao_menu(self.tela, self.ui.btn_colecao, "COLEÇÃO DE CARTAS", self.fontes['menu'])
        self.ui.desenhar_botao_menu(self.tela, self.ui.btn_meus_decks, "MEUS DECKS", self.fontes['menu'])
        self.ui.desenhar_botao_menu(self.tela, self.ui.btn_sair, "SAIR", self.fontes['menu'])

    def exibir_tela_cadastro(self, nome_deck, input_ativo, arquivo_selecionado):
        """Interface para Meus Decks (Cadastro)."""
        # Título da tela
        txt_t = self.fontes['menu'].render("CADASTRO DE NOVO DECK", True, (200, 200, 200))
        self.tela.blit(txt_t, (self.tela.get_width()//2 - txt_t.get_width()//2, 100))

        # Campo de Nome
        label_nome = self.fontes['fase'].render("Nome do Deck:", True, (150, 150, 150))
        self.tela.blit(label_nome, (self.ui.campo_nome_deck.x, self.ui.campo_nome_deck.y - 25))
        self.ui.desenhar_campo_texto(self.tela, self.ui.campo_nome_deck, nome_deck, input_ativo, self.fontes['menu'])

        # Seleção de Ficheiro
        txt_arq = os.path.basename(arquivo_selecionado) if arquivo_selecionado else "Nenhum arquivo .txt selecionado"
        self.ui.desenhar_botao_menu(self.tela, self.ui.btn_selecionar_arquivo, "BUSCAR .TXT", self.fontes['menu'])
        
        txt_info_arq = self.fontes['fase'].render(txt_arq, True, (0, 200, 0) if arquivo_selecionado else (150, 50, 50))
        self.tela.blit(txt_info_arq, (self.ui.btn_selecionar_arquivo.x, self.ui.btn_selecionar_arquivo.y + 60))

        # Salvar e Voltar
        self.ui.desenhar_botao_menu(self.tela, self.ui.btn_salvar_deck, "SALVAR E BAIXAR", self.fontes['menu'])
        self.ui.desenhar_botao_menu(self.tela, self.ui.btn_voltar_menu, "VOLTAR", self.fontes['fase'])

import os # Necessário para os.path.basename