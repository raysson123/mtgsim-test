import os
from src.model.deck_loader import DeckLoader
from src.model.deck_serializer import DeckSerializer # <--- Novo Import

class DeckBuilderController:
    def __init__(self, assets_mgr):
        self.assets_mgr = assets_mgr
        self.caminho_txt_temp = ""
        self.lista_cartas_temp = []
        self.nome_deck_temp = ""

    def iniciar_importacao(self, caminho_arquivo, nome_deck):
        """Passo 1: Lê o TXT temporariamente para extrair a lista."""
        self.caminho_txt_temp = caminho_arquivo
        self.nome_deck_temp = nome_deck
        
        try:
            self.lista_cartas_temp = DeckLoader.load_from_txt(caminho_arquivo)
            return True
        except Exception as e:
            print(f"Erro ao ler deck: {e}")
            return False

    def finalizar_cadastro(self, commander_name, tela, fonte):
        """Passo 2: Converte para JSON e Baixa as imagens."""
        nome_arquivo = self.nome_deck_temp.strip().lower().replace(" ", "_")
        
        # 1. AQUI A MUDANÇA: Usamos o Serializer para criar o JSON estruturado
        DeckSerializer.salvar_deck_json(
            nome_arquivo, 
            self.nome_deck_temp, 
            commander_name, 
            self.lista_cartas_temp
        )
        
        # 2. Prepara lista para download (Scryfall precisa de lista plana de nomes)
        lista_download = [commander_name] + [c for c in self.lista_cartas_temp if c != commander_name]
        
        # 3. Baixa imagens e dados técnicos (data/cards/...)
        self.assets_mgr.baixar_deck_completo(
            nome_arquivo, 
            lista_download, 
            tela, 
            fonte
        )
        
        # Limpeza
        self.caminho_txt_temp = ""
        self.lista_cartas_temp = []