from erukar.engine.lifeforms.Enemy import Enemy
import erukar, random

class IurianCleric(Enemy):
    BriefDescription = "an Iurian Cleric"
    RandomizedArmor = [
        ('left', 'erukar.game.inventory.armor.shields'),
        ('feet', 'erukar.game.inventory.armor.chest'),
        ('chest', 'erukar.game.inventory.armor.boots'),
        ('head', 'erukar.game.inventory.armor.helm')
    ]
    RandomizedWeapons = ['right' ]

    def __init__(self):
        super().__init__("Iurian Cleric")
        self.strength = int(random.uniform(2, 5))
        self.dexterity = int(random.uniform(1, 4))
        self.vitality = int(random.uniform(4, 6))
        self.acuity = int(random.uniform(2, 3))
        self.sense = int(random.uniform(2, 5))
        self.resolve = int(random.uniform(1, 3))
        self.spells = [erukar.game.magic.predefined.Heal()]
        self.define_level(5)
        self.name = "Iurian Cleric"
        self.randomize_equipment()
        self.set_vision_results('You see a {alias}.','You see a {alias}. {describe}',(0,1))
        self.set_sensory_results('You hear movement.','You hear a {alias}.',(0, 1))
        self.set_detailed_results('There is a Iurian Cleric wielding {describe_weapon}.', 'There is a Iurian Cleric wearing {describe_armor} and wielding {describe_weapon}')

    def perform_turn(self):
        if self.health < (self.max_health / 2):
            return self.heal_self()
        targets = list(self.viable_targets(self.current_room))
        if len(targets) > 0:
            return self.do_attack(targets)
        return self.maybe_move_somewhere()

    def heal_self(self):
        cast = erukar.engine.commands.executable.Cast()
        cast.sender_uid = self.uid
        cast.user_specified_payload = 'Heal'
        return cast
