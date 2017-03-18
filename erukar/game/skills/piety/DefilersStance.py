from erukar.engine.model.Skill import Skill

class DefilersStance(Skill):
    '''
    Using the Defiler's Stance allows the usage of Demonic Source. While active, Demonic Energy is
    displayed below ArcEnergy in stats. Typically, Demonic Energy does not regenerate unless someone
    Consecrates an area through Holy Water, the Consecration Conversion Word, or through Altars
    or the Natural Divinity anomaly.

    Altars and the Natural Divinity anomaly naturally regenerate a certain amount of Demonic Energy.

    In higher levels of Defiler's Stance, you also gain efficiency bonuses to casting spells based
    on Demonic Energy. 
    '''
    Name = 'Defiler\'s Stance'

    def demonic_energy_available(level):
        return min(25*min(2,level) + 10*max(0,level-2), 100)

    def divine_damage_vulnerability(level):
        return 65 - 5*(level-1)

    def demonic_energy_generation(level):
        return 2 * max(0,level-6)

    def demonic_word_efficiency_bonus(level):
        return 5 * max(0,level-4)

    def current_level_description(self):
        return ''.join([
            DefilersStance.demonic_energy_description(self.level),
            DefilersStance.energy_generation_description(self.level),
            DefilersStance.eff_bonus_description(self.level),
            DefilersStance.vulnerability_description(self.level),
        ])

    def demonic_energy_description(level):
        energy_available = DefilersStance.demonic_energy_available(level)
        if energy_available >= 100:
            return 'Allows full usage of environmental Demonic Energy. '
        if energy_available > 0:
            return 'Allows usage of {}% of environmental Demonic Energy. '.format(energy_available)
        return ''

    def energy_generation_description(level):
        generated = DefilersStance.demonic_energy_generation(level)
        if generated > 0:
            return 'Creates {} environmental Demonic Energy per turn. '.format(generated)
        return ''

    def eff_bonus_description(level):
        bonus = DefilersStance.demonic_word_efficiency_bonus(level)
        if bonus > 0:
            return 'Words based on Demonic Energy receive a {}% efficiency bonus. '.format(bonus)
        return ''

    def vulnerability_description(level):
        vulnerability = DefilersStance.divine_damage_vulnerability(level)
        return 'Incurs a natural {}% vulnerability to Divine Damage. '.format(vulnerability)
