import pygame
import os
import requests
import json

class AssetsManager:
    def __init__(self):
        self.card_images = {}
        self.card_data_cache = {} 
        self.base_path = os.path.join("assets", "cards")
        
        # Cria as pastas base caso não existam
        if not os.path.exists(self.base_path):
            os.makedirs(os.path.join(self.base_path, "generic"), exist_ok=True)
        
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 14)

    def get_card_image(self, card_name, deck_name="generic"):
        """
        Retorna a imagem da carta usando a nova lógica de subpastas.
        """
        # Se já está na memória RAM, retorna direto (Alta Performance)
        if card_name in self.card_images:
            return self.card_images[card_name]

        # Tenta carregar do disco usando o nome do deck como pasta
        image = self.load_from_disk(card_name, deck_name)
        
        if image:
            self.card_images[card_name] = image
            return image
        
        # Se não achou em lugar nenhum, cria um placeholder
        return self.create_placeholder(card_name)

    def load_from_disk(self, card_name, deck_name):
        """Busca a imagem na pasta do deck ou na pasta generic."""
        # Normaliza o nome para o arquivo (ex: "Sol Ring" -> "sol_ring.jpg")
        clean_name = card_name.lower().replace(" ", "_")
        extensions = [".jpg", ".png", ".jpeg"]
        
        # Organiza a busca: 1º na pasta do deck, 2º na pasta generic
        search_folders = [deck_name.lower().replace(" ", "_"), "generic"]
        
        for folder in search_folders:
            folder_path = os.path.join(self.base_path, folder)
            for ext in extensions:
                img_path = os.path.join(folder_path, clean_name + ext)
                
                if os.path.exists(img_path):
                    try:
                        img = pygame.image.load(img_path).convert_alpha()
                        
                        # Tenta carregar o JSON de dados (agora em data/cards)
                        json_path = os.path.join("data", "cards", clean_name + ".json")
                        if os.path.exists(json_path):
                            with open(json_path, 'r', encoding='utf-8') as f:
                                self.card_data_cache[card_name] = json.load(f)
                        return img
                    except Exception as e:
                        print(f"Erro ao carregar {img_path}: {e}")
        return None

    def baixar_deck_completo(self, nome_deck, lista_cartas, tela, fonte):
        """
        Baixa imagens para assets/cards/[nome_deck] e JSONs para data/cards/
        """
        deck_folder = nome_deck.lower().replace(" ", "_")
        img_dir = os.path.join(self.base_path, deck_folder)
        data_dir = os.path.join("data", "cards")
        
        # Cria os diretórios necessários
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)
            
        total = len(lista_cartas)
        terrenos_basicos = ["plains", "swamp", "mountain", "forest", "island"]

        for i, card_name in enumerate(lista_cartas):
            clean_name = card_name.lower().replace(" ", "_")
            
            # Atualiza tela de carregamento
            tela.fill((30, 30, 30))
            texto = fonte.render(f"Processando: {card_name} ({i+1}/{total})", True, (255, 255, 255))
            tela.blit(texto, (tela.get_width()//2 - texto.get_width()//2, tela.get_height()//2))
            pygame.display.flip()
            
            # Decide se salva no deck ou no generic (se for terreno)
            subfolder = "generic" if any(t in clean_name for t in terrenos_basicos) else deck_folder
            caminho_img = os.path.join(self.base_path, subfolder, f"{clean_name}.jpg")
            caminho_json = os.path.join(data_dir, f"{clean_name}.json")
            
            if os.path.exists(caminho_img) and os.path.exists(caminho_json):
                continue
                
            try:
                # Busca no Scryfall
                url_api = f"https://api.scryfall.com/cards/named?exact={card_name}"
                resp = requests.get(url_api, timeout=5)
                
                if resp.status_code == 200:
                    data = resp.json()
                    
                    # Salva Dados em data/cards/
                    relevant_data = {
                        "name": data.get("name"),
                        "type_line": data.get("type_line"),
                        "oracle_text": data.get("oracle_text", ""),
                        "mana_cost": data.get("mana_cost", "")
                    }
                    with open(caminho_json, 'w', encoding='utf-8') as f:
                        json.dump(relevant_data, f, indent=4, ensure_ascii=False)
                    
                    # Baixa Imagem para assets/cards/[subfolder]/
                    if "image_uris" in data:
                        img_url = data["image_uris"]["normal"]
                        img_data = requests.get(img_url).content
                        with open(caminho_img, 'wb') as f:
                            f.write(img_data)
                
                pygame.time.wait(100) # Evita bloqueio da API (Rate limit)
                    
            except Exception as e:
                print(f"Erro ao baixar {card_name}: {e}")

            pygame.event.pump()

    def create_placeholder(self, text):
        surface = pygame.Surface((220, 300))
        surface.fill((40, 40, 40))
        pygame.draw.rect(surface, (100, 100, 100), (0, 0, 220, 300), 3)
        words = text.split()
        y = 100
        for word in words:
            txt_img = self.font.render(word, True, (200, 200, 200))
            surface.blit(txt_img, (110 - txt_img.get_width()//2, y))
            y += 25
        return surface