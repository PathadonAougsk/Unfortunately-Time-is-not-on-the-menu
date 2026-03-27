from module.EventHandler import EventHandler


class AnimatonicController:
    def __init__(self, animatonics: dict, event_handler: EventHandler) -> None:

        self.animatonics = animatonics
        self.event_handler = event_handler

        self.states = {name: 0 for name in animatonics}

    def process(self):
        print("MrHappy", self.states["MrHappy"])
        print("MrTemp", self.states["MrTemp"])

        for name, animatonic in self.animatonics.items():
            if not self.is_valid(name) and animatonic.mode == "idle":
                continue

            if animatonic.try_to_move():
                self.states[name] += 1

            event = animatonic.behavior(self.states[name])
            if event:
                self.internal_process(event)

    def render(self):
        for name, animatonic in self.animatonics.items():
            if not self.is_valid(name) and animatonic.mode == "prep":
                continue
            animatonic.draw()

    def force_character_state(self, name, state):
        self.states[name] = state

    def internal_process(self, event):
        event_type, character_name = event

        if event_type not in ["Attack", "Reset"]:
            return

        if event_type == "Attack":
            for name, animatonic in self.animatonics.items():
                animatonic.freeze()

            if self.event_handler.try_kill_player(character_name):
                self.animatonics[character_name].jumpscare()
                return "Attack!"

            self.force_character_state(character_name, -1)

        elif event_type == "Reset":
            animatonic = self.animatonics[character_name]
            for name, animatonic in self.animatonics.items():
                animatonic.unfreeze()

            self.force_character_state(character_name, 0)

    def is_valid(self, name):
        if name == "MrHappy":
            if self.event_handler._is_facing_office:
                return False
            if not self.event_handler.is_pc_on:
                if self.states[name] == 3:
                    self.force_character_state(name, 0)
                    self.animatonics[name].interrupt()
                return False
            return True

        if name == "MrTemp":
            if not self.event_handler._is_facing_office:
                return False
            return True

        return True
