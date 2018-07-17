from erukar.system.engine.commands import Map, Inventory, Skills, Stats


class DifferentialMessageEngine:
    ''''
    The Differential Message Engine takes messages that need to be sent
    to real life players and minimizes them before they are sent out.
    This should reduce bandwidth drastically
    '''
    MapStateParams = [
        'minX',
        'minY',
        'height',
        'width',
        'pixel',
        'coordinates'
    ]
    MapTypesForDiff = ['rooms', 'actions', 'lighting']

    def __init__(self):
        self.state = {}

    def messages_for(self, instance, node, log):
        yield from self.game(instance, node, log)
        yield from self.map(node)
        yield from self.skills(node)
        yield from self.vitals(node)
        yield from self.inventory(node)

    def game(self, inst, node, log):
        char = node.lifeform()
        game_state = {
            'wealth': char.wealth,
            'log': log,
            'location': inst.dungeon.overland_location.alias(),
            'movementPoints': char.movement_allowed,
            'actionPoints': {
                'current': char.current_action_points,
                'reserved': char.reserved_action_points
            },
            'turnOrder': inst.turn_manager.frontend_readable_turn_order()[:4],
            'interactions': inst.get_interaction_results(node)
        }
        yield 'update state', game_state

    def map(self, node):
        cmd = node.create_command(Map)
        new = cmd.execute().result_for(node.uid)[0]
        yield from self.map_state_diff(node, new)
        for _type in self.MapTypesForDiff:
            yield from self._type_diff(node, _type, new[_type])
        actors = new['actors']
        yield 'update actors', actors

    def map_state_diff(self, node, new):
        map_state = {kw: new[kw] for kw in self.MapStateParams}
        state = self.get(node, 'map_state', {})
        coord_diff = self.diff(node, 'map_state', map_state, state)
        if coord_diff:
            yield 'update map state', coord_diff

    def _type_diff(self, node, _type, new):
        state = self.get(node, _type, {})
        diff = self.diff(node, _type, new, state)
        if diff:
            yield 'update {}'.format(_type), diff

    def inventory(self, node):
        state = self.get(node, 'inventory', {})
        cmd = node.create_command(Inventory)
        new = cmd.execute().result_for(node.uid)[0]
        diff = self.diff(node, 'inventory', new, state)
        if diff:
            yield 'set inventory', diff

    def skills(self, node):
        cmd = node.create_command(Skills)
        new = cmd.execute().result_for(node.uid)[0]
        state = self.get(node, 'skills', {})
        skills_diff = self.diff(node, 'skills', new, state)
        if skills_diff:
            yield 'update skills', skills_diff

    def vitals(self, node):
        cmd = node.create_command(Stats)
        new = cmd.execute().result_for(node.uid)[0]
        state = self.get(node, 'skills', {})
        skills_diff = self.diff(node, 'skills', new, state)
        if skills_diff:
            yield 'update vitals', new

    def get(self, node, state_type, default):
        node_state = self.state.get(node, {})
        if not node_state:
            self.state[node] = {}
        specific_state = node_state.get(state_type, default)
        if not specific_state:
            self.state[node][state_type] = default
        return specific_state

    def diff(self, node, _type, new, state):
        msg, state = self._dict_diffgen(node, new, state)
        self.state[node][_type] = state
        return msg

    def _dict_diffgen(self, node, msg, state):
        state = state or {}
        diff = {}
        for key in msg:
            if key not in state or not isinstance(msg[key], type(state[key])):
                state[key] = msg[key]
                diff[key] = msg[key]
                continue
            if isinstance(msg[key], dict):
                _diff, _state = self._dict_diffgen(node, msg[key], state[key])
                if _diff:
                    diff[key] = _diff
                state[key] = _state
                continue
            if msg[key] != state[key]:
                diff[key] = msg[key]
                state[key] = msg[key]
        return diff, state
