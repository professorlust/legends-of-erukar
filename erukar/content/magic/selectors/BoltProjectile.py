from erukar.system.engine import Selector
import random


class BoltProjectile(Selector):
    YouEvaded = '{caster} creates a ball of {_type_descriptor} and '\
        'hurls it at you as a bolt of {_type} energy, but you are '\
        'able to dodge it just in time.'
    TheyEvaded = 'You fire a bolt of {_type} energy at {target}, but '\
        '{target_pronoun} is able to dodge it just in time.'
    YouWereHit = '{caster} fires a bolt of {_type_descriptor} at you, '\
        'slamming you with {_type} energy!'
    TheyWereHit = 'You fire a bolt of {_type} energy at {target} and '\
        'hit {target_object_pronoun}!'

    def was_evaded(mutator, caster, target, cmd):
        acu = caster
        adj = 25 - mutator.energy*0.5
        roll = int(random.uniform(*mutator.power_range(5, 25)))
        total = roll + adj + acu
        return total <= target.evasion()

    def append_evasion_results(caster, target, cmd, mutator):
        damage_type = mutator.get('damage_type', 'arcane')
        args = {
            'caster': caster.alias(),
            'target': target.alias(),
            '_type': damage_type,
            '_type_descriptor': BoltProjectile.descriptor(damage_type),
            'target_pronoun': 'he',
            'target_object_pronoun': 'him'
        }
        cmd.log(caster, BoltProjectile.TheyEvaded.format(**args))
        cmd.log(target, BoltProjectile.YouEvaded.format(**args))

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
