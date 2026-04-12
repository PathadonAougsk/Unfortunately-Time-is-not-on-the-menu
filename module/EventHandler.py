import pygame


class EventHandler:
    def __init__(self) -> None:
        self.is_mask_on = False
        self.is_pc_on = False
        self.is_door_close = False
        self.is_sumbit = False

        self._is_facing_office = True
        self.is_game_over = False
        self.is_reset = False
        self.score = 0

        self._door_close_start = 0
        self._door_locked_until = 0
        self._door_max_close = 5000  # ms before lockout

    @property
    def is_door_locked(self):
        return pygame.time.get_ticks() < self._door_locked_until

    def toggle_mask(self):
        self.is_mask_on = not self.is_mask_on

    def toggle_light(self):
        self.is_light_on = not self.is_light_on

    def toggle_door(self):
        if not self._is_facing_office:
            return
        if self.is_door_locked:
            return

        if self.is_door_close:
            self.is_door_close = False
            self._door_close_start = 0
        else:
            self.is_door_close = True
            self._door_close_start = pygame.time.get_ticks()

    def update_door(self):
        if not self.is_door_close:
            return
        if pygame.time.get_ticks() - self._door_close_start > self._door_max_close:
            self.is_door_close = False
            self._door_close_start = 0
            self._door_locked_until = pygame.time.get_ticks() + 10000

    def toggle_pc(self):
        if self._is_facing_office:
            return

        self.is_pc_on = not self.is_pc_on

    def turn_to_office(self):
        self._is_facing_office = True

    def turn_to_backroom(self):
        self._is_facing_office = False

    def sumbit_order(self):
        self.is_sumbit = not self.is_sumbit

    def finnish_turn(self):
        self._is_facing_office = not self._is_facing_office

    def try_kill_player(self, animatonic_name):
        if animatonic_name == "MrHappy":
            if self.is_pc_on:
                return True

        if animatonic_name == "MrTemp":
            if not self.is_mask_on:
                return True

        if animatonic_name == "MrBall":
            if not self.is_door_close:
                return True

        return False

    def gameover(self):
        if self.is_game_over:
            return

        self.is_game_over = True
        self.is_reset = True

    def go_to_menu(self):
        self.is_game_over = False
        self.is_reset = False
        self.is_mask_on = False
        self.is_light_on = False
        self.is_pc_on = False
        self.is_door_close = False
        self._door_close_start = 0
        self._door_locked_until = 0
        self._is_facing_office = True
        self.score = 0
