import os
import shutil
from src.model.deck_loader import DeckLoader
from src.model.deck_data_manager import DeckDataManager

class DeckBuilderController:
    def __init__(self, assets_mgr):
        self.assets_mgr = assets_mgr
        self.caminho_txt_temp = ""
        self.lista_cartas_temp = []
        self.nome_deck_temp = ""

    def iniciar_importacao(self, caminho_arquivo, nome_deck):
        """Passo 1: Lê o arquivo e prepara para a escolha do comandante."""
        self.caminho_txt_temp = caminho_arquivo
        self.nome_deck_temp = nome_deck
        
        # Carrega a lista do TXT
        try:
            self.lista_cartas_temp = DeckLoader.load_from_txt(caminho_arquivo)
            return True # Sucesso
        except Exception as e:
            print(f"Erro ao ler deck: {e}")
            return False

    def finalizar_cadastro(self, commander_name, tela, fonte):
        """Passo 2: Salva tudo e inicia o download."""
        nome_pasta = self.nome_deck_temp.strip().lower().replace(" ", "_")
        
        # 1. Define caminhos
        path_deck = os.path.join("data", "decks", "user_decks")
        os.makedirs(path_deck, exist_ok=True)
        
        # 2. Copia o TXT para o sistema do jogo
        dest_txt = os.path.join(path_deck, f"{nome_pasta}.txt")
        shutil.copy(self.caminho_txt_temp, dest_txt)
        
        # 3. Salva os metadados (Quem é o Commander?)
        DeckDataManager.salvar_metadata(nome_pasta, self.nome_deck_temp, commander_name)
        
        # 4. Prepara lista de download (Commander primeiro)
        lista_final = [commander_name] + [c for c in self.lista_cartas_temp if c != commander_name]
        
        # 5. Chama o AssetsManager apenas para executar o trabalho braçal de download
        self.assets_mgr.baixar_deck_completo(
            nome_pasta, 
            lista_final, 
            tela, 
            fonte
        )
        
        # Limpa memória temporária
        self.caminho_txt_temp = ""
        self.lista_cartas_temp = []