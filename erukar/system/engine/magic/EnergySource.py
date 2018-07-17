from erukar.system.engine import MagicEffect


class EnergySource(MagicEffect):
    '''
    All spells start with an Energy Source, and there can only be one
    per spell chain. This can be Arcane Energy, Blood, or Divinity.
    Potions have their own sources which are predefined and not usable
    in spell chains.
    The EnergySource used takes a finite value of Arcane Energy and uses
    that to establish kwargs like power and percentage.

    The enact function is not used in EnergySource; instead use the source
    method. This returns a Success or Failure and established kwargs
    '''
    def source(self, caster, cmd, mutator):
        return False, None
