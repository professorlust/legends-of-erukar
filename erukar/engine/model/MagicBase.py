from erukar.engine.model.Describable import Describable
import erukar

class MagicBase(Describable):
    def on_cast(self, command, caster, parameters=None, efficacy=1.0):
        self.cmd = command
        self.caster = caster
        self.set_parameters(parameters)

    def set_parameters(self, parameters):
        '''Attempt to set parameters to the object. Sometimes this
        can fail, so it's wrapped in a try/catch to continue.'''
        if not parameters: return
        for param in parameters:
            try: setattr(self, param, parameters[param])
            except: pass

    def append_result(self, uid, msg):
        if self.cmd:
            self.cmd.append_result(uid, msg)

    def append_for_others_in_room(self, msg):
        if not self.cmd: return
        for content in self.caster.current_room.contents:
            if isinstance(content, erukar.engine.lifeforms.Lifeform) and content is not self.caster:
                self.cmd.append_result(content.uid, msg)

    def append_for_all_in_room(self, msg):
        if not self.cmd: return
        for content in self.caster.current_room.contents:
            if isinstance(content, erukar.engine.lifeforms.Lifeform):
                self.cmd.append_result(content.uid, msg)

