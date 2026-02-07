import json
import os
from src.model.deck_serializer import DeckSerializer

class DeckLoader:
    @staticmethod
    def load_from_txt(file_path):
        """Mantemos para ler o arquivo de importação inicial."""
        card_list = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    # Lógica simples de parse "1 Sol Ring"
                    parts = line.split(" ", 1)
                    if len(parts) == 2 and parts[0].isdigit():
                        qty = int(parts[0])
                        name = parts[1]
                    else:
                        qty = 1
                        name = line
                    
                    for _ in range(qty):
                        card_list.append(name)
        except: return []
        return card_list

    @staticmethod
    def load_deck_for_game(nome_arquivo_json):
        """
        NOVO: Lê o JSON do deck e retorna a lista plana para o Player usar.
        Ex: Retorna ['Sol Ring', 'Mountain', 'Mountain', ...]
        """
        data = DeckSerializer.carregar_deck_json(nome_arquivo_json)
        if not data:
            return []
            
        lista_final = []
        
        # 1. Adiciona Comandante (geralmente vai para zona de comando, mas o Player separa depois)
        if "commander_zone" in data:
            for item in data["commander_zone"]:
                lista_final.append(item["name"])
                
        # 2. Adiciona Mainboard
        if "mainboard" in data:
            for item in data["mainboard"]:
                qtd = item.get("quantity", 1)
                nome = item.get("name", "Unknown")
                for _ in range(qtd):
                    lista_final.append(nome)
                    
        return lista_final