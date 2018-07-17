from erukar.system.engine import TargetedAbility
from erukar.system.engine import Corpse, Dying, Dead
from erukar.ext.math import Navigator


class SpellCasting(TargetedAbility):
    Name = 'Spellcasting'
    ShowInLists = False

    def valid_at(self, cmd, loc):
        pass

    def perform(self, cmd):
        spell = cmd.args.get('spell', None)
        spell.cmd_execute(self)
