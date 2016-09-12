from erukar.engine.commands.Command import Command

class ResponseCommand(Command):
    '''
    Used when responding to context. Never executable.
    CMD         Context         Implied CMD     Rationale
    ================================================================================
    Attack      Target          Attack          Simplify next turn's attack with shortened "attack"
    Close       Target          Open            Can use "open" to open the same door
    Drop        Target          Give            Pick something up rapidly
    Equip       Inventory       Unequip         It is possible that the inventory command was called before; don't break continuity
    Give        Inventory       Give            See Equip
    Inspect     ???             Inspect
    Inventory   Inventory       Inspect         See Equip
    Join        N/A             N/A
    Map         N/A             N/A
    Move        Direction       Move            Allows you to keep using "move" to keep moving in the same direction
    Open        Target          Close           See Close
    Quit        N/A             N/A
    Stats       Stats           Stats           Allows the user to inspect stat scores further
    Take        Target          Drop            Allows the user to drop accidentally taken items easily
    Unequip     Target          Equip           Simplify re-equip if it was done on accident
    Use         Target          Use             Keep using
    '''
    pass

