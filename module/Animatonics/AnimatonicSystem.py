import pygame
from numpy.random.mtrand import randint

from module.Animation import Animation


class AnimatonicSystem:
    All_Animatonics = []

    def __init__(self, screen, target, event_handler, aggro_rate) -> None:
        self.target = target
        self.aggro_rate = aggro_rate

        self._aggro = 0
        self._currentlyAttack = False
        self._state, self._max_state = 0, 1

        self._frozen = False
        self.__event_handler = event_handler
        self.screen = screen

    def try_to_move(self):
        if self._frozen:
            return False

        if randint(0, 10) >= 100 - self._aggro:
            self._state += 1
            self._aggro = 0
            return True

        self._aggro += self.aggro_rate

    def freeze(self):
        self._frozen = True

    def unfreeze(self):
        self._frozen = False

    def __prepare_attack(self):
        pass

    @classmethod
    def _attack(cls):
        return ("Attack", cls.__name__)

    @classmethod
    def _reset(cls):
        return ("Reset", cls.__name__)

    def _run_animation(self, animation, func, tick_attr, delay=200, reverse=False):
        current_tick = pygame.time.get_ticks()
        last_tick = getattr(self, tick_attr)

        if current_tick - last_tick > delay:
            setattr(self, tick_attr, current_tick)

            finished = animation.animate(reverse=reverse)

            if finished:
                return func()

    def _gameover(self):
        pass
