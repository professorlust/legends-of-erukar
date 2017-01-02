from erukar.engine.lifeforms.Enemy import Enemy
import erukar, random

class Lich(Enemy):
    BriefDescription = "a lich  "

    def __init__(self, random=True):
        super().__init__("Lich", random)
        # Now personality
        self.str_ratio = 0.05
        self.dex_ratio = 0.1
        self.vit_ratio = 0.05
        self.acu_ratio = 0.4
        self.sen_ratio = 0.25
        self.res_ratio = 0.15
        self.define_level(40)
        self.spells = [
            erukar.game.magic.predefined.Disorient(),
            erukar.game.magic.predefined.AcidBurst(),
            erukar.game.magic.predefined.FireBurst(),
            erukar.game.magic.predefined.IceBurst(),
            erukar.game.magic.predefined.ElectricalBurst(),
            erukar.game.magic.predefined.ShadowBurst()
        ]
        self.conditions.append(erukar.game.conditions.magical.Undead(self))

    def perform_turn(self):
        targets = list(self.viable_targets(self.current_room))
        if len(targets) > 0:
            return self.cast_a_spell(targets[0])
        return self.maybe_move_somewhere()

    def cast_a_spell(self, target):
        cast = erukar.engine.commands.executable.Cast()
        cast.sender_uid = self.uid

        choice_val = random.random()
        if self.health < self.max_health/2:
            choice_val += 0.3

        if choice_val < 0.2:
            spell_alias = 'Disorient'
        elif choice_val < 0.6:
            spell_alias = 'Shadow Burst'
        elif choice_val < 0.7:
            spell_alias = 'Fire Burst'
        elif choice_val < 0.8:
            spell_alias = 'Ice Burst'
        elif choice_val < 0.9:
            spell_alias = 'Acid Burst'
        else:
            spell_alias = 'Electrical Burst'

        cast.user_specified_payload = '{} on {}'.format(spell_alias, target.alias())
        return cast