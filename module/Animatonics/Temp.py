from pathlib import Path

import pygame

from module.Animation import Animation
from module.Animatonics.Animatonic import AnimatonicSystem
from module.Player import Player


class TempCharacter(AnimatonicSystem):
    def __init__(self, screen, aggro_rate, target: Player, eventhandler, x, y) -> None:
        super().__init__(screen, target, eventhandler, aggro_rate)

        Appear_path = Path.cwd() / "Assets" / "TempCharacter" / "Appear.png"
        Jump_scare_path = Path.cwd() / "Assets" / "TempCharacter" / "Jump_scare.png"

        self.prep_animation = (
            Animation(Appear_path)
            .set_sprites_frame(64 * 2, 64 * 2)
            .set_output(300, 300)
        )
        self.prep_animation.load_sprite(1, 7)

        self.jump_animation = (
            Animation(Jump_scare_path)
            .set_sprites_frame(64 * 2, 64 * 2)
            .set_output(2000, 2000)
        )
        self.jump_animation.load_sprite(1, 8)

        self.current_animation = self.prep_animation
        self._max_state = 3

        self._prep_tick, self._jump_tick, self._reset_tick = 0, 0, 0

    def update_behavior(self, need_to_exist_in_frame=True):
        if self._state == self._max_state:
            self.current_animation = self.prep_animation
            if not self._frozen:
                self.freeze()
            self.__run_animation(self._attack, "_prep_tick")

        elif self._state == -1:
            self.current_animation = self.prep_animation
            self.__run_animation(self._reset, "_reset_tick", reverse=True)

        elif self._state == -2:
            self.current_animation = self.jump_animation
            self.__run_animation(self._jumpscare, "_jump_tick", delay=100)
            self.current_animation.draw_sprite(self.screen, -250, 0, True)
            return

        if need_to_exist_in_frame:
            self.current_animation.draw_sprite(self.screen, 120, 0, True)

    def __run_animation(self, func, tick_attr, delay=300, reverse=False):
        current_tick = pygame.time.get_ticks()
        last_tick = getattr(self, tick_attr)

        if current_tick - last_tick > delay:
            setattr(self, tick_attr, current_tick)

            finished = self.current_animation.animate(reverse=reverse)

            if finished:
                func()
