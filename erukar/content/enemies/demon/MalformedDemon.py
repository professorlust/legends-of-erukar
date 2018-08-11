from erukar.system.engine import BasicAI, Enemy, SpellInstance
from erukar.system.engine import SpellCasting, ActivateAbility
from erukar.content.inventory import Claws
from erukar.content.magic import BloodSource, Pyromorph, InflictDamage
import erukar


class MalformedDemon(Enemy):
    BriefDescription = "a malformed demon"
    Probability = 1
    ClassName = "Malformed Demon"
    ClassLevel = 2

    def init_stats(self):
        self.dexterity = 1
        self.vitality = 0
        self.strength = 0
        self.resolve = 2
        self.sense = 2
        self.acuity = 1

    def init_personality(self):
        self.ai_module = MalformedDemonAi(self)
        self.str_ratio = 0.4
        self.dex_ratio = 0.2
        self.vit_ratio = 0.1
        self.acu_ratio = 0.0
        self.sen_ratio = 0.15
        self.res_ratio = 0.15
        self.stat_points = 8

    def init_inventory(self):
        self.left = Claws()
        self.right = Claws()
        self.inventory = [self.left, self.right]

    def init_skills(self):
        self.skills.append(erukar.SpellCasting())
        self.skills.append(erukar.BloodMagic())


class MalformedDemonAi(BasicAI):
    PyroblastCooldown = 3
    PyroblastRange = 4

    def __init__(self, puppet):
        super().__init__(puppet)
        self.pyroblast_cooldown = 0

    def perform_turn(self):
        if self.can_pyroblast():
            cmd = self.do_pyroblast()
            if cmd:
                return cmd
        return super().perform_turn()

    def can_pyroblast(self):
        return self.puppet.health > 10 and self.pyroblast_cooldown == 0

    def do_pyroblast(self):
        self.pyroblast_cooldown = self.PyroblastCooldown
        spell, kwargs = MalformedDemonAi.pyroblast()
        for e_tuple in self.check_for_enemies_in_range(self.PyroblastRange):
            enemy = e_tuple[-1]
            cmd = self.create_command(ActivateAbility)
            cmd.args['abilityModule'] = SpellCasting.__module__
            cmd.args['interaction_target'] = enemy.uuid
            cmd.args['spell'] = spell
            cmd.args['kwargs'] = kwargs
            cmd.obs(
                self.puppet.coordinates,
                'Casting Pyroblast at {}!'.format(enemy.alias())
            )
            return cmd

    def tick(self, *_):
        if self.pyroblast_cooldown > 0:
            self.pyroblast_cooldown -= 1

    def pyroblast():
        instance = SpellInstance([
            BloodSource,
            Pyromorph,
            InflictDamage
        ])
        kwargs = {}
        return instance, kwargs
