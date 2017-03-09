from erukar.engine.magic.SpellWord import SpellWord
from erukar.engine.model.Damage import Damage
from erukar.engine.inventory.SpellAttack import SpellAttack
import erukar, random

class DamageOverTime(SpellWord):
    DamageRange = (0, 10)
    DamageScalar = 1.0
    DamageOffset = 0
    DamageDuration = 4
    DamageOverTimeEfficacy = 0.5

    DamageDescription = "{alias|target} is consumed by a pulsing energy!"
    DamageShouldScale = False
    DamageName = 'nonelemental'
    DamageMod = 'acuity'

    PotionName = 'Prolonged Poison'
    PotionPriceMultiplier = 5.0

    Name = 'Recurring Damage'
    Description = 'A punctuary word which releases destructive energy in bursts at regular intervals. While each damage burst is less potent than a Source Damage burst, the Recurring Damage total is often higher. The question a mage must ask is if they have the time for Recurring Damage to reach its full potential.'
    Flavor = 'A recent advancement in arcana, the "Augment Weapon" magic was developed at the Sidernes Academy in Luinden, Iuria as part of research conducted by Arcanist Felwin Bougarde. The research was based in part on pre-Theocracy battlemages whose legendary abilities to bind the elements to their items was once forgotten.'

    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        super().on_cast(command, lifeform, parameters)
        
        self.append_for_all_in_room(self.mutate(self.DamageDescription))
        rd_condition = erukar.game.conditions.negative.DamageOverTime(self.target, self.caster)
        rd_condition.damage = [Damage(
            name = self.DamageName,
            damage_range = self.DamageRange, 
            mod = self.DamageMod,
            dist_and_params = (random.uniform, (0,1)),
            scales = self.DamageShouldScale
        )]
        rd_condition.duration = int(self.DamageDuration * efficacy)
        rd_condition.damage_efficacy = self.DamageOverTimeEfficacy
        self.target.conditions.append(rd_condition)

        return parameters
