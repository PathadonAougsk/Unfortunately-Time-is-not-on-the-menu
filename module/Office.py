from pathlib import Path

import pygame

from module.Animation import Animation


class Office:
    def __init__(self, screen) -> None:
        self.screen = screen
        self._state = 0

        front_side = Path.cwd() / "Assets" / "Office" / "front_side.png"
        back_side = Path.cwd() / "Assets" / "Office" / "back_side.png"
        door_animation = Path.cwd() / "Assets" / "Office" / "door_animation.png"

        self.front_side = (
            Animation(front_side)
            .set_sprites_frame(256, 256)
            .set_output(256 * 3, 256 * 3)
        )
        self.front_side.load_sprite(1, 1)

        self.back_side = (
            Animation(back_side)
            .set_sprites_frame(256, 256)
            .set_output(256 * 3, 256 * 3)
        )
        self.back_side.load_sprite(1, 6, gap_px=2)

        self.door = (
            Animation(door_animation)
            .set_sprites_frame(256, 256)
            .set_output(256 * 3, 256 * 3)
        )
        self.door.load_sprite(1, 10, gap_px=2)

        self.door_tick = pygame.time.get_ticks()
        self.back_tick = pygame.time.get_ticks()

        self.door_animating = False
        self.back_animating = False

        self.door_reverse = False
        self.back_reverse = False

    def update_behavior(self):
        if self._state == 0:
            self.front_side.draw_sprite(self.screen, 0, 0, True)
            self.__run_door_animation(delay=100)

            self.door.draw_sprite(self.screen, 0, 0, True)

        elif self._state == 1:
            self.__run_back_animation(delay=100)
            self.back_side.draw_sprite(self.screen, 0, 0, True)

    def __run_door_animation(self, delay=100):
        if not self.door_animating:
            return

        current_tick = pygame.time.get_ticks()

        if current_tick - self.door_tick > delay:
            self.door_tick = current_tick

            finished = self.door.animate(reverse=self.door_reverse)

            if finished:
                self.door_animating = False

    def __run_back_animation(self, delay=100):
        if not self.back_animating:
            return

        current_tick = pygame.time.get_ticks()

        if current_tick - self.back_tick > delay:
            self.back_tick = current_tick

            finished = self.back_side.animate(reverse=self.back_reverse)

            if finished:
                if self.back_reverse:
                    self._state = 0
                    self.back_reverse = False
                self.back_animating = False

    def _receive_event(self, type_of_event):
        if type_of_event == "Door" and not self.door_animating:
            self.door_reverse = not self.door_reverse
            self.door_animating = True

        elif type_of_event == "Turn Right":
            self._state = 1
            self.back_side.frame = 0
            self.back_animating = True

        elif type_of_event == "Turn Left":
            self.back_animating = True
            self.back_reverse = True
