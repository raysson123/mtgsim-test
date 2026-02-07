import os
import json
import shutil

class DataManager:
    @staticmethod
    def setup_directories():
        """Cria a estrutura de pastas se não existir"""
        paths = [
            "data/cache",
            "data/local/profiles",
            "data/decks/favorites",
            "data/decks/imported",
            "data/decks/user_decks"
        ]
        for path in paths:
            os.makedirs(path, exist_ok=True)

    @staticmethod
    def save_deck(deck_data, category="user_decks"):
        """Salva um deck na categoria escolhida"""
        filename = f"{deck_data['name'].lower().replace(' ', '_')}.json"
        path = f"data/decks/{category}/{filename}"
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(deck_data, f, indent=4)

    @staticmethod
    def clear_temp_data():
        """Limpa dados de sessões antigas"""
        cache_dir = "data/cache"
        for filename in os.listdir(cache_dir):
            file_path = os.path.join(cache_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Erro ao limpar cache: {e}")