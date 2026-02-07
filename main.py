import sys
import os

# Configura o caminho para encontrar a pasta src
diretorio_raiz = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, diretorio_raiz)

# Importa apenas o Motor
from src.core.game_app import GameApp

if __name__ == "__main__":
    try:
        app = GameApp()
        app.run()
    except Exception as e:
        print(f"Erro Crítico: {e}")
        # Aqui poderia salvar um log de erro