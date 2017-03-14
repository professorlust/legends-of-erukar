class Skill:
    Descriptions = [
        'Basic Description per level here'
    ]
    Name = 'Default Skill Name'

    def __init__(self):
        self.level = 1

    def is_viable_for(self, *_):
        return False

    def persistible_attributes(self):
        return []

    def on_skills(self):
        title = '{}, Level {}'.format(self.Name, self.level)
        current_level = self.current_level_description()
        next_level = self.next_level_description()
        return '\n'.join([title, '-'*16, current_level, 'Next Level: {}'.format(next_level)])

    def current_level_description(self):
        return self.Descriptions[self.level-1]

    def next_level_description(self):
        return 'None' if self.level >= len(self.Descriptions) else self.Descriptions[self.level]

