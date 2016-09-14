from erukar.engine.commands.Command import Command
import erukar

class Levelup(Command):
    OverridesUntilSuccess = True
    aliases = ['level', 'levelup']
    attributes = ['strength','dexterity','vitality','acuity','sense','resolve']
    Welcome = "Congratulations, you are now Level {}. You have {} points to spend."
    Help = "1.\tAdd <points> to <stat>: Add specified number of points to an attribute. If the number you specify is greater than your total remaining for allocation, this command will allocate the remainder of your points into <stat>.\n2.\tRemove <points> from <stat>: Remove a specified number of pre-allocated points from an attribute. If the number you specify is great enough to attempt to subtract from your pre-existing attribute score, this will remove all pre-allocate points for said stat.\n3.\tStatus: Show the current breakdown of pre-allocated scores compared to before pre-allocation.\n4.\tConfirm: Lock-in preallocation of stats. A confirmation will prompt you to commit or cancel.\n5.\tCancel: Cancel preallocation of stats. A confirmation will prompt you to commit or cancel."
    NoPoints = "You cannot allocate points because you do not have any points to spend."
    AddingTooMuch = 'You specified {}, but only have {} points to spend. Proceding with the lower value.'
    RemovingTooMuch = "You specified {}, but this would subtract too many points. Re-allocating to your initial value. You now have {} points to spend."

    def __init__(self):
        super().__init__()
        self.num_points = 0
        self.initial_state = {}
        self.future_state = {}
        self.subcommands = [
            ('add ', self.add_points),
            ('remove ', self.remove_points),
            ('status', self.status),
            ('confirm', self.confirm),
            ('cancel', self.cancel),
            ('yes', self.yes),
            ('no', self.no)]

    def execute(self, *_):
        self.target = self.find_player().lifeform()
        self.num_points = 15*len([x for x in self.target.afflictions if isinstance(x, erukar.engine.effects.NeedsInitialization)])
        self.num_points += len([x for x in self.target.afflictions if isinstance(x, erukar.engine.effects.ReadyToLevel)])
        if self.num_points is 0:
           return self.succeed(self.NoPoints)

        # Welcome
        if not self.context or not isinstance(self.context.context, erukar.engine.commands.executable.Levelup):
            self.initial_state = {x:self.target.get(x) for x in self.attributes}
            self.future_state = self.initial_state.copy()
            return self.fail(self.Welcome.format(self.target.level, self.num_points))

        # Copy context status
        self.num_points = self.context.context.num_points
        self.future_state = self.context.context.future_state
        self.initial_state = self.context.context.initial_state

        return self.determine_subcommand()

    def determine_subcommand(self):
        '''Determines what subcommand is to be executed based on payload'''
        payload = self.payload()
        for subcmd in self.subcommands:
            if subcmd[0] in payload:
                return subcmd[1](payload.replace(subcmd[0],''))

        return self.help()

    def determine_stat_and_points(self, payload, keyword):
        '''Use a keyword to figure out what attribute and how much is to be modified'''
        amount, stat = [0, 'strength']
        if keyword in payload:
            amount, stat = payload.split(keyword)
            if not amount.isdigit() or stat not in self.attributes:
                return ['strength', 0]
            return stat, int(amount)
        else: # no keyword specified, we have to make a guess.
            vals = payload.split(' ')
            amount = int(next((x for x in vals if x.isdigit()), '0'))
            stat = next((x for x in vals if x in self.attributes), 'strength')
        return stat, amount

    def add_points(self, payload):
        '''Add a specific number of points to an attribute'''
        result = ''
        stat, amount = self.determine_stat_and_points(payload,' to ')
        if self.num_points < amount:
            result = self.AddingTooMuch.format(amount, self.num_points)
            amount = self.num_points

        self.num_points -= amount
        self.future_state[stat] += amount
        result = result + '{} now at {}, was {} (+{}). You now have {} points to spend.'.format(stat, self.future_state[stat], self.initial_state[stat], self.future_state[stat]-self.initial_state[stat], self.num_points)
        return self.fail(result)

    def remove_points(self, payload):
        '''Remove a specific number of points from an attribute'''
        self.subcommand = 'remove '
        result = ''
        stat, amount = self.determine_stat_and_points(payload,' from ')
        difference = self.future_state[stat] - self.initial_state[stat]
        if difference < amount:
            self.num_points += difference
            self.future_state[stat] = self.initial_state[stat]
            return self.fail(self.RemovingTooMuch.format(amount, self.num_points))

        self.future_state[stat] -= amount
        self.num_points += amount
        return self.fail('Removing {} from {}. You now have {} points to spend.'.format(amount, stat, self.num_points))

    def status(self, *_):
        '''Provide a status breakdown, including attribute values and the current points to spend'''
        stats = '\n'.join(['{:10}: {} (+{}, was {})'.format(x, self.future_state[x], self.initial_state[x]-self.future_state[x], self.initial_state[x]) for x in self.attributes])

        return self.fail('{}\n\nYou have {} points to spend.'.format(stats, self.num_points))

    def help(self, *_):
        return self.fail(self.Help)

    def yes(self, *_):
        '''Confirm a Confirmation or Cancelation'''
        if self.context.context.subcommand is 'confirm':
            return self.complete()
        if self.context.context.subcommand is 'cancel':
            return self.succeed('Aborting Level Up attribute allocation.')
        return self.fail('Unrecognized "yes" command')

    def complete(self):
        for x in self.attributes:
            setattr(self.target, x, self.future_state[x])
        self.target.max_health += (4 + self.target.vitality)
        self.target.health += (4 + self.target.vitality)
        self.target.afflictions = [x for x in self.target.afflictions \
                            if (not isinstance(x, erukar.engine.effects.ReadyToLevel) and not isinstance(x, erukar.engine.effects.NeedsInitialization))]
        return self.succeed('Your Level Up attribute allocation is now LOCKED.')

    def no(self, *_):
        return self.fail('Returning to level up process.')

    def confirm(self, *_):
        self.subcommand = 'confirm'
        return self.fail('Are you sure you want to lock in this allocation? (yes or no)')

    def cancel(self, *_):
        self.subcommand = 'cancel'
        return self.fail('Are you sure you want to abort this allocation? You will lose all progress. (yes or no)')
