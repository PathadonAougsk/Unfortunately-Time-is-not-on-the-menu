class EventHandler:
    def __init__(self) -> None:
        self.__is_mask_on = False
        self.__is_light_on = False
        self.__is_pc_on = False
        self.__is_door_close = False

        self.__is_facing_front = True

    @property
    def is_facing_front(self):
        return self.__is_facing_front

    def toggle_mask(self):
        self.__is_mask_on = not self.__is_mask_on
        return ("Mask", self.__is_mask_on)

    def toggle_light(self):
        self.__is_light_on = not self.__is_light_on
        return ("Light", self.__is_light_on)

    def toggle_door(self):
        if not self.__is_facing_front:
            return

        self.__is_door_close = not self.__is_door_close
        return ("Door", self.__is_door_close)

    def toggle_pc(self):
        if self.__is_facing_front:
            return

        self.__is_pc_on = not self.__is_pc_on
        return ("Pc", self.__is_pc_on)

    def request_left(self):
        if self.__is_facing_front:
            return

        return ("Facing front", not self.__is_facing_front)

    def request_right(self):
        if not self.__is_facing_front:
            return

        return ("Facing front", not self.__is_facing_front)

    def summbit_order(self):
        if not self.__is_pc_on:
            return

        return ("Sumbit Order", True)

    def finnish_turn(self):
        self.__is_facing_front = not self.__is_facing_front

    def try_kill_player(self, animatonic_name):
        if animatonic_name == "BirdMan":
            if not self.__is_mask_on:
                return ("Kill", True)

        if animatonic_name == "MrHappy":
            if self.__is_pc_on:
                return ("Kill", True)

        if animatonic_name == "TempCharacter":
            if not self.__is_light_on:
                return ("Kill", True)

        return ("Kill", False)
