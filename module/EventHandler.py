from module.Office import Office
from module.Player import Player


class EventHandler:
    def __init__(self, player: Player, office: Office) -> None:
        self.player = player
        self.office = office
        self.animatonics = []

        self.__is_mask_on = False
        self.__is_light_on = False
        self.__is_pc_on = False
        self.__is_door_close = False

        self.__is_facing_front = True

    @property
    def is_facing_front(self):
        return self.__is_facing_front

    @property
    def is_pc_on(self):
        return self.__is_pc_on

    def add_animatonics(self, animatonics: list):
        self.animatonics.extend(animatonics)

    def toggle_mask(self):
        self.__is_mask_on = not self.__is_mask_on
        self.player._receive_event(self.__is_mask_on)

    def toggle_light(self):
        self.__is_light_on = not self.__is_light_on

    def toggle_door(self):
        if not self.__is_facing_front:
            return

        self.__is_door_close = not self.__is_door_close
        self.office._receive_event("Door")

    def toggle_pc(self):
        if self.__is_facing_front:
            return

        self.__is_pc_on = not self.__is_pc_on

    def turn_left(self):
        if self.__is_facing_front:
            return

        self.__is_facing_front = True
        self.office._receive_event("Turn Left")

    def turn_right(self):
        if not self.__is_facing_front:
            return

        self.__is_facing_front = False
        self.office._receive_event("Turn Right")

    def try_kill_player(self, animatonic_name):
        if animatonic_name == "BirdMan":
            if not self.__is_mask_on:
                self.lock_gameplay()
                return True

        if animatonic_name == "MrHappy":
            if self.__is_pc_on:
                self.lock_gameplay()
                return True

        if animatonic_name == "TempCharacter":
            if not self.__is_light_on:
                self.lock_gameplay()
                return True

        return False

    def lock_gameplay(self):
        for animatonic in self.animatonics:
            animatonic.freeze()

        if self.__is_mask_on:
            self.toggle_mask()
