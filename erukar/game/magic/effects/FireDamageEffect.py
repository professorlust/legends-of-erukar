class FireDamageEffect(SpellEffect):
    DamageRange = (0, 10)

    def on_cast(self, lifeform, parameters=None, efficacy=1.0):
        '''Inflicts a random amount of fire damage to something, defaulting to the caster'''
        target = self.get_target(lifeform, parameters)

        acuity = lifeform.calculate_effective_stat('acuity')
        damages = [Damage('fire', self.DamageRange, acuity, random.uniform, (0,1))]
