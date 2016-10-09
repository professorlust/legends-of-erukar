from erukar.engine.model.Describable import Describable
import erukar

class MagicBase(Describable):
    def on_cast(self, command, lifeform, parameters=None, efficacy=1.0):
        self.cmd = command
        self.lifeform = lifeform

    def get_target(self, lifeform, parameters=None):
        target = lifeform
        if parameters is not None and 'target' in parameters:
            target = parameters['target']
        return target

    def append_result(self, uid, msg):
        '''Appends the result to the Command object if it exists'''
        if self.cmd:
            self.cmd.append_result(uid, msg)

    def append_for_others_in_room(self, msg):
        '''Appends the result to the Command object if it exists'''
        if not self.cmd: return
        for content in self.lifeform.current_room.contents:
            if isinstance(content, erukar.engine.lifeforms.Lifeform) and content is not self.lifeform:
                self.cmd.append_result(content.uid, msg)

