from erukar.system.engine import Skill

class ClericsStance(Skill):
    '''
    Using the Cleric's Stance allows the usage of Divine Source. While active, Divine Energy is
    displayed below ArcEnergy in stats. Typically, Divine Energy does not regenerate unless someone
    Consecrates an area through Holy Water, the Consecration Conversion Word, or through Altars
    or the Natural Divinity anomaly.

    Altars and the Natural Divinity anomaly naturally regenerate a certain amount of Divine Energy.

    In higher levels of Cleric's Stance, you also gain efficiency bonuses to casting spells based
    on Divine Energy. 
    '''
    Name = 'Cleric\'s Stance'

    def divine_energy_available(level):
        return min(25*min(2,level) + 10*max(0,level-2), 100)

    def demonic_damage_vulnerability(level):
        return 65 - 5*(level-1)

    def divine_energy_generation(level):
        return 2 * max(0,level-6)

    def divine_word_efficiency_bonus(level):
        return 5 * max(0,level-4)

    def current_level_description(self):
        return ''.join([
            ClericsStance.divine_energy_description(self.level),
            ClericsStance.energy_generation_description(self.level),
            ClericsStance.eff_bonus_description(self.level),
            ClericsStance.vulnerability_description(self.level),
        ])

    def divine_energy_description(level):
        energy_available = ClericsStance.divine_energy_available(level)
        if energy_available >= 100:
            return 'Allows full usage of environmental Divine Energy. '
        if energy_available > 0:
            return 'Allows usage of {}% of environmental Divine Energy. '.format(energy_available)
        return ''

    def energy_generation_description(level):
        generated = ClericsStance.divine_energy_generation(level)
        if generated > 0:
            return 'Creates {} environmental Divine Energy per turn. '.format(generated)
        return ''

    def eff_bonus_description(level):
        bonus = ClericsStance.divine_word_efficiency_bonus(level)
        if bonus > 0:
            return 'Words based on Divine Energy receive a {}% efficiency bonus. '.format(bonus)
        return ''

    def vulnerability_description(level):
        vulnerability = ClericsStance.demonic_damage_vulnerability(level)
        return 'Incurs a natural {}% vulnerability to Demonic Damage. '.format(vulnerability)
