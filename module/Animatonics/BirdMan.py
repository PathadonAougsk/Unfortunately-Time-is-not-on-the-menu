from pathlib import Path

import pygame

from module.Animation import Animation
from module.Animatonics.Animatonic import AnimatonicSystem
from module.Player import Player


class BirdMan(AnimatonicSystem):
    def __init__(self, screen, aggro_rate, target: Player, eventhandler, x, y) -> None:
        super().__init__(screen, target, eventhandler, aggro_rate)

        Appear_path = Path.cwd() / "Assets" / "BirdMan" / "Appear.png"
        Jump_scare_path = Path.cwd() / "Assets" / "BirdMan" / "Jump_scare.png"

        self.prep_animation = (
            Animation(Appear_path).set_sprites_frame(90, 64).set_output(400, 300)
        )
        self.prep_animation.load_sprite(3, 4, 2)

        self.jump_animation = (
            Animation(Jump_scare_path)
            .set_sprites_frame(200, 128)
            .set_output(2000, 1800)
        )
        self.jump_animation.load_sprite(3, 3, 2)

        self.current_animation = self.prep_animation
        self._max_state = 3

        self._prep_tick, self._jump_tick, self._reset_tick = 0, 0, 0

    def update_behavior(self):
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
            self.current_animation.draw_sprite(self.screen, 0, 0, True)
            return

        self.current_animation.draw_sprite(self.screen, 600, 100)

    def __run_animation(self, func, tick_attr, delay=200, reverse=False):
        current_tick = pygame.time.get_ticks()
        last_tick = getattr(self, tick_attr)

        if current_tick - last_tick > delay:
            setattr(self, tick_attr, current_tick)

            finished = self.current_animation.animate(reverse=reverse)

            if finished:
                func()
