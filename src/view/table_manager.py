import pygame

class TableManager:
    def __init__(self, largura, altura, assets_mgr=None):
        """
        Gerencia o layout da mesa, dividindo a tela em quadrantes para os jogadores.
        Agora aceita assets_mgr para poder desenhar fundos ou elementos visuais se necessário.
        """
        self.largura = largura
        self.altura = altura
        self.assets_mgr = assets_mgr
        self.quadrantes = {}
        
        # Define layout padrão inicial (4 jogadores)
        self.ajustar_layout(4)

    def ajustar_layout(self, total_jogadores):
        """Calcula os retângulos (Rect) para cada jogador baseado na quantidade."""
        self.quadrantes = {}
        mid_x = self.largura // 2
        mid_y = self.altura // 2
        
        if total_jogadores == 2:
            # Layout 1x2 (Cima/Baixo)
            self.quadrantes[1] = pygame.Rect(0, 0, self.largura, mid_y)          # Oponente (Topo)
            self.quadrantes[0] = pygame.Rect(0, mid_y, self.largura, mid_y)      # Você (Baixo)
            
        elif total_jogadores >= 3:
            # Layout 2x2 (Quadrantes)
            # Slot 0: Você (Inferior Esquerdo)
            self.quadrantes[0] = pygame.Rect(0, mid_y, mid_x, mid_y)
            
            # Slot 1: Oponente 1 (Superior Esquerdo)
            self.quadrantes[1] = pygame.Rect(0, 0, mid_x, mid_y)
            
            # Slot 2: Oponente 2 (Superior Direito)
            self.quadrantes[2] = pygame.Rect(mid_x, 0, mid_x, mid_y)
            
            # Slot 3: Oponente 3 (Inferior Direito - se houver)
            self.quadrantes[3] = pygame.Rect(mid_x, mid_y, mid_x, mid_y)

    def draw_layout(self, screen, active_player_index):
        """Desenha as linhas divisórias da mesa e destaca o turno atual."""
        # Cor das linhas
        cor_linha = (50, 50, 50)
        espessura = 3
        
        # Linha Vertical Central
        pygame.draw.line(screen, cor_linha, (self.largura // 2, 0), (self.largura // 2, self.altura), espessura)
        
        # Linha Horizontal Central
        pygame.draw.line(screen, cor_linha, (0, self.altura // 2), (self.largura, self.altura // 2), espessura)
        
        # Destaque do Jogador Ativo (Borda Colorida no Quadrante)
        if active_player_index in self.quadrantes:
            rect_ativo = self.quadrantes[active_player_index]
            pygame.draw.rect(screen, (100, 100, 0), rect_ativo, 2) # Amarelo para quem está jogando

    def get_player_quadrant(self, slot_index):
        """Retorna o Rect do quadrante de um jogador específico."""
        return self.quadrantes.get(slot_index, pygame.Rect(0,0,100,100))