class EventHandler:
    def __init__(self) -> None:
        self.is_mask_on = False
        self.is_light_on = False
        self.is_pc_on = False
        self.is_door_close = False

        self._is_facing_office = True

    def toggle_mask(self):
        self.is_mask_on = not self.is_mask_on

    def toggle_light(self):
        self.is_light_on = not self.is_light_on

    def toggle_door(self):
        if not self._is_facing_office:
            return

        self.is_door_close = not self.is_door_close

    def toggle_pc(self):
        if self._is_facing_office:
            return

        self.is_pc_on = not self.is_pc_on

    def turn_to_office(self):
        self._is_facing_office = True

    def turn_to_backroom(self):
        self._is_facing_office = False

    def finnish_turn(self):
        self._is_facing_office = not self._is_facing_office

    def try_kill_player(self, animatonic_name):
        if animatonic_name == "MrHappy":
            if self.is_pc_on:
                return True

        if animatonic_name == "MrTemp":
            if not self.is_light_on:
                return True

        return False
