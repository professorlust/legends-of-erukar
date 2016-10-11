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
            if parameters['target'] is None:
                target = lifeform
        return target

    def append_result(self, uid, msg):
        if self.cmd:
            self.cmd.append_result(uid, msg)

    def append_for_others_in_room(self, msg):
        if not self.cmd: return
        for content in self.lifeform.current_room.contents:
            if isinstance(content, erukar.engine.lifeforms.Lifeform) and content is not self.lifeform:
                self.cmd.append_result(content.uid, msg)

    def append_for_all_in_room(self, msg):
        if not self.cmd: return
        for content in self.lifeform.current_room.contents:
            if isinstance(content, erukar.engine.lifeforms.Lifeform):
                self.cmd.append_result(content.uid, msg)

