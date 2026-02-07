import os

def criar_pastas():
    # Estrutura base que o seu novo código vai exigir
    pastas = [
        "config",                           # Configurações do sistema
        "data/cards",                        # Base de dados JSON das cartas
        "data/decks/user_decks",             # Decks que você criar
        "data/decks/imported",               # Decks baixados/completos
        "data/cache",                        # Dados temporários de sessão
        "assets/cards/generic",              # Imagens comuns (Terrenos)
        "assets/ui",                         # Ícones e botões
        "src/controller",
        "src/model",
        "src/view",
        "src/utils"
    ]

    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
        print(f"✅ Pasta pronta: {pasta}")

if __name__ == "__main__":
    criar_pastas()