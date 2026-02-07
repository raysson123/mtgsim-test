import json
import os
import datetime

class DeckSerializer:
    @staticmethod
    def salvar_deck_json(nome_arquivo, nome_display, commander, lista_cartas):
        """
        Recebe uma lista simples de strings (cartas) e salva um JSON estruturado.
        """
        # Caminho da pasta
        caminho_pasta = os.path.join("data", "decks", "user_decks")
        os.makedirs(caminho_pasta, exist_ok=True)
        caminho_arquivo = os.path.join(caminho_pasta, f"{nome_arquivo}.json")

        # Processa a lista de cartas para o formato {name, quantity}
        # No Commander geralmente é 1 de cada, mas o código fica pronto para outros formatos
        cartas_estruturadas = []
        contagem = {}
        
        for carta in lista_cartas:
            # Remove o comandante da lista principal se ele estiver lá duplicado
            if carta == commander: continue 
            
            if carta in contagem:
                contagem[carta] += 1
            else:
                contagem[carta] = 1

        for carta, qtd in contagem.items():
            cartas_estruturadas.append({"name": carta, "quantity": qtd})

        # Monta o Objeto Final
        dados_deck = {
            "metadata": {
                "name": nome_display,
                "commander": commander,
                "format": "Commander",
                "created_at": str(datetime.date.today())
            },
            "commander_zone": [
                {"name": commander, "quantity": 1}
            ],
            "mainboard": cartas_estruturadas
        }

        # Salva no disco
        try:
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados_deck, f, indent=4)
            return True
        except Exception as e:
            print(f"Erro ao serializar deck: {e}")
            return False

    @staticmethod
    def carregar_deck_json(nome_arquivo):
        """
        Lê o JSON e retorna um dicionário com os dados.
        Aceita o nome do arquivo (ex: 'meu_deck') ou caminho completo.
        """
        if not nome_arquivo.endswith(".json"):
            nome_arquivo += ".json"
            
        # Tenta achar o arquivo em user_decks ou imported
        caminho = os.path.join("data", "decks", "user_decks", nome_arquivo)
        if not os.path.exists(caminho):
            caminho = os.path.join("data", "decks", "imported", nome_arquivo)
            
        if os.path.exists(caminho):
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao ler JSON: {e}")
        return None