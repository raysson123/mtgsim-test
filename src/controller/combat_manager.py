class CombatManager:
    def __init__(self):
        self.attackers = []
        self.blockers = []

    def declare_attacker(self, card, target_player):
        if not card.tapped:
            card.tapped = True
            self.attackers.append({"card": card, "target": target_player})

    def resolve_combat_damage(self):
        for attack_info in self.attackers:
            attacker = attack_info["card"]
            target = attack_info["target"]
            
            # Calcula dano
            damage = attacker.power
            
            # Aplica dano ao jogador (A lógica de commander está dentro do take_damage do Player)
            target.take_damage(damage, source_card=attacker)
            
            print(f"{attacker.name} causou {damage} de dano a {target.name}.")

        # Limpa combate
        self.attackers = []
        self.blockers = []