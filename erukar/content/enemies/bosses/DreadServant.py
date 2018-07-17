from erukar.system.engine import BasicAI, SpellInstance, SpellCasting
from erukar.system.engine import ActivateAbility
from .undead.Skeleton import Skeleton
from ..templates.Undead import Undead
from erukar.content.inventory import Shortsword, Buckler
from erukar.content.modifiers import Steel, Oak
from erukar.content.magic import ArcaneEnergySource, Daemomorph, RadialArea
from erukar.content.magic import InflictCondition, InflictDamage, Summon
from erukar.content.conditions.magical import HealthDrain, Wither


class DreadServant(Undead):
    ClassName = 'Dread Servant'
    ClassLevel = 4

    def init_stats(self):
        self.strength = 0
        self.dexterity = 2
        self.vitality = 1
        self.acuity = 3
        self.sense = 1
        self.resolve = 4

    def init_personality(self):
        self.ai_module = DreadServantAi(self)
        self.str_ratio = 0.05
        self.dex_ratio = 0.2
        self.vit_ratio = 0.05
        self.acu_ratio = 0.3
        self.sen_ratio = 0.1
        self.res_ratio = 0.3
        self.stat_points = 8

    def init_inventory(self):
        self.left = Buckler(modifiers=[Oak])
        self.right = Shortsword(modifiers=[Steel])
        self.inventory = [self.left, self.right]


class DreadServantAi(BasicAI):
    NecroticLinkCooldown = 5
    SummonGuardsCooldown = 6
    PutrefyingBlastCooldown = 7

    def __init__(self, puppet):
        super().__init__(puppet)
        self.necrotic_link_cooldown = 0
        self.summon_cooldown = 0
        self.putrefying_blast_cooldown = 0

    def perform_turn(self):
        if self.desperately_needs_to_heal():
            return self.do_heal()
        if self.should_do_summon():
            return self.do_summon()
        if self.is_in_dangerous_proximity():
            return self.move_somewhere_safe()
        if self.necrotic_link_can_be_used():
            return self.use_necrotic_link()
        if self.putrefying_blast_can_be_used():
            return self.use_putrefying_blast()
        if self.needs_to_heal():
            return self.do_heal()
        target, _ = self.check_for_enemies_in_range()
        if target:
            return self.create_attack(target, self.puppet.right)
        return self.idle()

    def desperately_needs_to_heal(self):
        return self.puppet.health < 0.10 * self.puppet.maximum_health()

    def needs_to_heal(self):
        return self.puppet.health < 0.50 * self.puppet.maximum_health()

    def summon(self):
        instance = SpellInstance([
            ArcaneEnergySource,
            Summon
        ])
        kwargs = {
            'summon_type': Skeleton
        }
        return instance, kwargs

    def should_do_summon(self):
        return self.has_sufficient_energy()\
            and self.summon_cooldown <= 0

    def do_summon(self):
        self.summon_cooldown = self.SummonGuardsCooldown
        spell, kwargs = self.summon()
        cmd = self.create_command(ActivateAbility)
        cmd.args['abilityModule'] = SpellCasting.__module__
        cmd.args['spell'] = spell
        cmd.args['kwargs'] = kwargs
        return cmd

    def sacrifice(self):
        pass

    def do_heal(self):
        pass

    def is_in_dangerous_proximity(self):
        return False

    def move_somewhere_safe(self):
        pass

    def necrotic_link(self):
        instance = SpellInstance([
            ArcaneEnergySource,
            Daemomorph,
            InflictCondition
        ])
        kwargs = {
            'type': HealthDrain
        }
        return instance, kwargs

    def necrotic_link_can_be_used(self):
        return self.has_sufficient_energy()\
                and self.necrotic_link_cooldown <= 0

    def use_necrotic_link(self):
        self.necrotic_link_cooldown = self.NecroticLinkCooldown
        spell, kwargs = self.necrotic_link()
        for enemy in self.check_for_enemies_in_range(self.NecroticLinkRange):
            cmd = self.create_command(ActivateAbility)
            cmd.args['abilityModule'] = SpellCasting.__module__
            cmd.args['interaction_target'] = enemy.uuid
            cmd.args['spell'] = spell
            cmd.args['kwargs'] = kwargs
            return cmd

    def putrefying_blast(self):
        instance = SpellInstance([
            ArcaneEnergySource,
            Daemomorph,
            RadialArea,
            InflictCondition,
            InflictDamage
        ])
        kwargs = {
            'type': Wither
        }
        return instance, kwargs

    def putrefying_blast_can_be_used(self):
        return self.has_sufficient_energy()\
                and self.putrefying_blast_cooldown <= 0

    def use_putrefying_blast(self):
        self.putrefying_blast_cooldown = self.PutrefyingBlastCooldown
        spell, kwargs = self.putrefying_blast()
        cmd = self.create_command(ActivateAbility)
        cmd.args['abilityModule'] = SpellCasting.__module__
        cmd.args['spell'] = spell
        cmd.args['kwargs'] = kwargs
        return cmd

    def has_sufficient_energy(self):
        aae = self.puppet.allocated_arcane_energy()
        return self.puppet.arcane_energy <= aae
