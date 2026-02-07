class RulesEngine:
    @staticmethod
    def check_state_based_actions(player):
        """
        Verifica condições de derrota baseadas nas regras do Commander.
        Retorna True se o jogador perdeu.
        """
        # 1. Vida a 0 ou menos
        if player.life <= 0:
            print(f"{player.name} foi eliminado (0 de vida).")
            return True

        # 2. Dano de Comandante (21 ou mais de um único comandante)
        for cmd_id, damage in player.commander_damage_taken.items():
            if damage >= 21:
                print(f"{player.name} foi eliminado (21+ de dano de comandante).")
                return True

        # 3. Veneno (10 contadores)
        if player.poison_counters >= 10:
            print(f"{player.name} foi eliminado (Veneno).")
            return True
            
        return False

    @staticmethod
    def validate_deck_rules(deck_list):
        """
        Valida se o deck segue as regras de construção do Commander.
        """
        # Regra: 100 Cartas (99 + 1 ou 98 + 2)
        if len(deck_list) != 100:
            print(f"AVISO: Deck tem {len(deck_list)} cartas. Commander exige 100.")
            # return False # Pode ser apenas um aviso por enquanto

        # Regra: Singleton (Apenas 1 cópia de cada, exceto terrenos básicos)
        counts = {}
        basic_lands = ["Plains", "Island", "Swamp", "Mountain", "Forest", "Wastes", 
                       "Snow-Covered Plains", "Snow-Covered Island", "Snow-Covered Swamp", 
                       "Snow-Covered Mountain", "Snow-Covered Forest"]
        
        for card_name in deck_list:
            if card_name in counts:
                counts[card_name] += 1
            else:
                counts[card_name] = 1
                
        for card_name, count in counts.items():
            # Verifica se não é terreno básico e tem mais de 1 cópia
            is_basic = any(basic in card_name for basic in basic_lands)
            if count > 1 and not is_basic:
                 print(f"AVISO: Carta '{card_name}' tem {count} cópias. Commander é Singleton.")
        
        return True