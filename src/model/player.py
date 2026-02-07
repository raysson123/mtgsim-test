class Player:
    def __init__(self, name, deck_list):
        self.name = name
        self.life = 40  # Regra Commander: Começa com 40 de vida
        self.deck = deck_list
        self.hand = []
        self.battlefield = []
        self.graveyard = []
        self.exile = []
        self.command_zone = []  # Onde fica o Comandante no início
        
        # Rastreia dano de comandante recebido.
        # Chave: ID do Comandante Oponente, Valor: Dano acumulado
        self.commander_damage_taken = {} 
        self.poison_counters = 0 # Contadores de Veneno (10 = Derrota)
        
        self.has_played_land_this_turn = False
        self.mana_pool = {"W": 0, "U": 0, "B": 0, "R": 0, "G": 0, "C": 0}

    def take_damage(self, amount, source_card=None):
        self.life -= amount
        
        # Regra: Dano de Comandante
        if source_card and getattr(source_card, "is_commander", False):
            cmd_id = source_card.id
            if cmd_id not in self.commander_damage_taken:
                self.commander_damage_taken[cmd_id] = 0
            self.commander_damage_taken[cmd_id] += amount