from pathlib import Path

import pygame
from numpy.random.mtrand import randint

from module.Animation import Animation
from module.Player import Player


class AnimatonicSystem:
    All_Animatonics = []

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls.All_Animatonics.append(instance)
        return instance

    def __init__(self, screen, target, event_handler, aggro_rate) -> None:
        self.target = target
        self.aggro_rate = aggro_rate

        self._aggro = 0
        self._currentlyAttack = False
        self._state, self._max_state = 0, 1

        self._frozen = False
        self.__event_handler = event_handler
        self.screen = screen

    @classmethod
    def attack_avaiable(cls):
        for animatonic in cls.All_Animatonics:
            if animatonic._currentlyAttack:
                return False
        return True

    def try_to_move(self):
        if self._frozen:
            return

        if randint(0, 10) >= 100 - self._aggro:
            self._state += 1
            self._aggro = 0
            return

        self._aggro += self.aggro_rate

    def freeze(self):
        self._frozen = True

    def unfreeze(self):
        self._frozen = False

    def update_behavior(self):
        pass

    def __prepare_attack(self):
        pass

    def _attack(self):
        result = self.__event_handler.try_kill_player(self.__class__.__name__)
        if not result:
            self._state = -1
            return

        self._state = -2

    def _jumpscare(self):
        pass

    def _reset(self):
        self.unfreeze()
        self._state = 0


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

        print(need_to_exist_in_frame)
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


class MrHappy(AnimatonicSystem):
    def __init__(self, screen, aggro_rate, target: Player, eventhandler, x, y) -> None:
        super().__init__(screen, target, eventhandler, aggro_rate)

        Appear_path = Path.cwd() / "Assets" / "MrHappy" / "Prepare.png"
        Jump_scare_path = Path.cwd() / "Assets" / "MrHappy" / "Jump_scare.png"

        self.prep_animation = (
            Animation(Appear_path)
            .set_sprites_frame(256, 256)
            .set_output(256 * 3, 256 * 3)
        )

        self.prep_animation.load_sprite(1, 8, gap_px=2)

        self.jump_animation = (
            Animation(Jump_scare_path)
            .set_sprites_frame(256, 256)
            .set_output(256 * 3, 256 * 3)
        )

        self.jump_animation.load_sprite(1, 5, gap_px=2)

        self.current_animation = self.prep_animation
        self._max_state = 3

        self._prep_tick, self._jump_tick, self._reset_tick = 0, 0, 0

    def interrupt(self):
        self._reset()
        self.current_animation = self.prep_animation
        self.current_animation.frame = 0

    def update_behavior(self, need_to_exist_in_frame=False):
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

        if need_to_exist_in_frame:
            self.current_animation.draw_sprite(self.screen, 0, 0, center=True)

    def __run_animation(self, func, tick_attr, delay=200, reverse=False):
        current_tick = pygame.time.get_ticks()
        last_tick = getattr(self, tick_attr)

        if current_tick - last_tick > delay:
            setattr(self, tick_attr, current_tick)

            finished = self.current_animation.animate(reverse=reverse)

            if finished:
                func()
