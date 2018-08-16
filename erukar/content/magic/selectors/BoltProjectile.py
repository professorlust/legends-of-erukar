from erukar.system.engine import Selector
import random


class BoltProjectile(Selector):
    YouBasic = '{caster} channels {source} to fire a bolt of '\
        '{type} energy at you ({roll} attack).'
    TheyBasic = 'You channel {source} to fire a bolt of {type} '\
        'energy at {target} ({roll} attack).'
    YouWereHit = 'The bolt hits you!'
    TheyWereHit = 'The bolt hits!'
    YouEvaded = 'You dodge the bolt!'
    TheyEvaded = 'It dodges the bolt.'

    def was_evaded(self, mutator, caster, target, cmd):
        acu = caster.acuity
        adj = 25 - mutator.energy*0.5
        roll = int(random.uniform(*mutator.power_range(5, 25)))
        total = roll + adj + acu
        BoltProjectile.append_results(caster, target, cmd, mutator, total)
        return BoltProjectile._evaded(total, target)

    def _evaded(total, target):
        return total <= target.evasion()

    def append_results(caster, target, cmd, mutator, roll):
        damage_type = mutator.get('damage_type', 'arcane')
        args = {
            'source': 'blood magic',
            'caster': caster.alias(),
            'target': target.alias(),
            'type': damage_type,
            'roll': roll
        }
        cmd.log(caster, BoltProjectile.YouBasic.format(**args))
        cmd.log(target, BoltProjectile.TheyBasic.format(**args))
        if BoltProjectile._evaded(roll, target):
            cmd.log(caster, BoltProjectile.TheyEvaded.format(**args))
            cmd.log(target, BoltProjectile.YouEvaded.format(**args))
            return
        cmd.log(caster, BoltProjectile.TheyWereHit.format(**args))
        cmd.log(target, BoltProjectile.YouWereHit.format(**args))

    def descriptor(_type):
        if _type == 'fire':
            return random.choice([
                'flames',
                'fire',
                'embers',
            ])
        if _type == 'ice':
            return random.choice([
                'frost',
                'ice crystals',
                'snow',
            ])
        if _type == 'electric':
            return random.choice([
                'lightning',
                'sparks',
                'plasma'
            ])
        if _type == 'aqueous':
            return random.choice([
                'water',
                'steam',
                'acid',
            ])
        if _type == 'arcane':
            return random.choice([
                'arcane energies'
            ])
        if _type == 'force':
            return random.choice([
                'visual distortion',
                'rapidly vibrating energy',
                'concussive force'
            ])
        if _type == 'divine':
            return random.choice([
                'pure light',
                'radiance',
                'purity',
            ])
        if _type == 'demonic':
            return random.choice([
                'darkness',
                'shadows',
                'black flame'
            ])
        return _type
