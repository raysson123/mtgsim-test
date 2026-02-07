import pygame

class UIComponents:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        centro_x = largura // 2
        
        # --- Configuração de Layout do Menu Principal ---
        largura_btn = 350
        altura_btn = 55
        espacamento = 75
        inicio_y = 280

        # Botões Principais
        self.btn_jogar = pygame.Rect(centro_x - largura_btn//2, inicio_y, largura_btn, altura_btn)
        self.btn_colecao = pygame.Rect(centro_x - largura_btn//2, inicio_y + espacamento, largura_btn, altura_btn)
        self.btn_meus_decks = pygame.Rect(centro_x - largura_btn//2, inicio_y + espacamento*2, largura_btn, altura_btn)
        self.btn_sair = pygame.Rect(centro_x - largura_btn//2, inicio_y + espacamento*3, largura_btn, altura_btn)

        # --- BOTÕES DA TELA DE COLEÇÃO (ATUALIZADO) ---
        self.btn_voltar_colecao = pygame.Rect(20, 20, 120, 40)
        self.btn_prox_pagina = pygame.Rect(largura - 140, altura // 2 - 20, 120, 40)
        self.btn_prev_pagina = pygame.Rect(20, altura // 2 - 20, 120, 40)
        
        # Área central para exibir as cartas em grid
        self.area_grid_colecao = pygame.Rect(150, 100, largura - 300, altura - 200)

        # --- Componentes da Tela de Cadastro (Meus Decks) ---
        self.campo_nome_deck = pygame.Rect(centro_x - 150, 200, 300, 45)
        self.btn_selecionar_arquivo = pygame.Rect(centro_x - 150, 280, 300, 50)
        self.btn_salvar_deck = pygame.Rect(centro_x - 100, 400, 200, 60)
        self.btn_voltar_menu = pygame.Rect(30, 30, 120, 40)

        # --- Componentes do Jogo ---
        self.btn_proxima_fase = pygame.Rect(largura - 180, altura - 80, 150, 50)
        self.btn_manter_mao = pygame.Rect(centro_x - 210, altura // 2 + 100, 200, 60)
        self.btn_fazer_mulligan = pygame.Rect(centro_x + 10, altura // 2 + 100, 200, 60)

    def desenhar_botao_menu(self, surface, rect, texto, fonte):
        """Desenha um botão estilizado com efeito de hover."""
        pos_mouse = pygame.mouse.get_pos()
        cor_fundo = (60, 60, 65) if rect.collidepoint(pos_mouse) else (30, 30, 35)
        cor_borda = (100, 100, 255) if rect.collidepoint(pos_mouse) else (70, 70, 70)

        sombra = rect.copy()
        sombra.x += 3
        sombra.y += 3
        pygame.draw.rect(surface, (10, 10, 10), sombra, border_radius=10)

        pygame.draw.rect(surface, cor_fundo, rect, border_radius=10)
        pygame.draw.rect(surface, cor_borda, rect, 2, border_radius=10)

        txt_surf = fonte.render(texto, True, (230, 230, 230))
        txt_rect = txt_surf.get_rect(center=rect.center)
        surface.blit(txt_surf, txt_rect)

    def desenhar_campo_texto(self, surface, rect, texto, ativo, fonte):
        """Desenha campos de entrada de texto."""
        cor = (255, 255, 255) if ativo else (100, 100, 100)
        pygame.draw.rect(surface, (20, 20, 20), rect, border_radius=5)
        pygame.draw.rect(surface, cor, rect, 2, border_radius=5)
        
        txt_surf = fonte.render(texto, True, (200, 200, 200))
        surface.blit(txt_surf, (rect.x + 10, rect.y + (rect.height//2 - txt_surf.get_height()//2)))