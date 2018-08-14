from .MagicEffect import MagicEffect
from .SpellMutator import SpellMutator
import erukar


class SpellInstance:
    '''Class which is basically just a way for spells to
    maintain parity from effect to effect'''
    NoSource = 'Your spell fails! You must begin a spell chain with an '\
        'Energy Source.'

    def __init__(self, chain=None):
        self.chain = chain if chain and isinstance(chain, list) else []

    def cmd_execute(self, cmd, caster=None):
        if len(self.chain) < 1:
            return
        caster = caster or cmd.args['player_lifeform']
        target = cmd.args.get('interaction_target', caster)
        mutator = SpellMutator(cmd.args.get('kwargs', {}))
        self.execute(caster, target, cmd, mutator)

    def execute(self, caster, target, cmd, mutator):
        if not SpellInstance.is_source(self.chain[0]):
            cmd.log(caster, self.NoSource)
            return
        # Attempt to source
        success, kwargs = self.chain[0]().source(caster, cmd, mutator)
        if success:
            self.run_chain(caster, target, cmd, mutator)

    def run_chain(self, caster, target, cmd, mutator):
        index = 1
        for effect in self.chain[1:]:
            index += 1
            if SpellInstance.is_selector(effect):
                self.split(caster, effect(), self.chain[index:], cmd, mutator)
                return
            mutator = effect().enact(caster, target, cmd, mutator)

    def split(self, caster, selector, chain, cmd, mutator):
        all_targets = set(selector.applicable_targets(caster, cmd, mutator))
        new_source = erukar.system.engine.SplitEnergySource
        new_chain = [new_source] + chain
        mutator.remove('target')
        for target in all_targets:
            mut_copy = mutator.copy()
            mut_copy.evasion = selector.evasion
            selector.adjust_energy(len(all_targets), mut_copy)
            subinstance = SpellInstance(new_chain)
            subinstance.execute(caster, target, cmd, mut_copy)

    def is_source(link):
        return issubclass(link, erukar.system.engine.EnergySource)

    def is_selector(link):
        return issubclass(link, erukar.system.engine.Selector)
