import pygame
import os

class CollectionView:
    def __init__(self, tela, ui, assets_mgr, fontes):
        self.tela = tela
        self.ui = ui
        self.assets_mgr = assets_mgr
        self.fontes = fontes
        
        self.pagina_atual = 0
        self.cartas_por_pagina = 10  # 2 linhas de 5 cartas
        self.colunas = 5
        self.espacamento_x = 180
        self.espacamento_y = 250

    def exibir(self):
        """Renderiza a grade de cartas e botões de navegação."""
        # 1. Título e Fundo
        self.tela.fill((20, 20, 25))
        txt_t = self.fontes['titulo'].render("COLEÇÃO DE CARTAS", True, (255, 255, 255))
        self.tela.blit(txt_t, (self.tela.get_width()//2 - txt_t.get_width()//2, 30))

        # 2. Carregar lista de cartas (ficheiros JSON em data/cards)
        caminho_dados = os.path.join("data", "cards")
        if not os.path.exists(caminho_dados):
            os.makedirs(caminho_dados, exist_ok=True)
        
        todas_cartas = [f.replace(".json", "") for f in os.listdir(caminho_dados) if f.endswith(".json")]
        todas_cartas.sort() # Ordem alfabética

        # 3. Lógica de Paginação
        inicio = self.pagina_atual * self.cartas_por_pagina
        fim = inicio + self.cartas_por_pagina
        cartas_visiveis = todas_cartas[inicio:fim]

        # 4. Desenhar a Grade (Grid)
        x_inicial = self.ui.area_grid_colecao.x
        y_inicial = self.ui.area_grid_colecao.y

        for i, nome_carta in enumerate(cartas_visiveis):
            col = i % self.colunas
            lin = i // self.colunas
            
            x = x_inicial + (col * self.espacamento_x)
            y = y_inicial + (lin * self.espacamento_y)

            # Puxa a imagem (tenta generic primeiro)
            img = self.assets_mgr.get_card_image(nome_carta, deck_name="generic")
            if img:
                # Redimensiona para caber na grade
                img_p = pygame.transform.smoothscale(img, (160, 220))
                self.tela.blit(img_p, (x, y))
                
                # Nome da carta abaixo da imagem
                nome_p = self.fontes['fase'].render(nome_carta[:15], True, (200, 200, 200))
                self.tela.blit(nome_p, (x + 80 - nome_p.get_width()//2, y + 225))

        # 5. Desenhar Botões de Navegação
        self.ui.desenhar_botao_menu(self.tela, self.ui.btn_voltar_colecao, "VOLTAR", self.fontes['fase'])
        
        if len(todas_cartas) > fim:
            self.ui.desenhar_botao_menu(self.tela, self.ui.btn_prox_pagina, "PRÓX. >", self.fontes['fase'])
        
        if self.pagina_atual > 0:
            self.ui.desenhar_botao_menu(self.tela, self.ui.btn_prev_pagina, "< ANTER.", self.fontes['fase'])

        # Info de Página
        total_pags = (len(todas_cartas) // self.cartas_por_pagina) + 1
        txt_pag = self.fontes['fase'].render(f"Página {self.pagina_atual + 1} de {total_pags}", True, (100, 100, 100))
        self.tela.blit(txt_pag, (self.tela.get_width()//2 - txt_pag.get_width()//2, self.tela.get_height() - 50))claer