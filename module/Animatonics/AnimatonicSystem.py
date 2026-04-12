import pygame
from numpy.random.mtrand import randint


class AnimatonicSystem:
    def __init__(self, screen, target, event_handler, aggro_rate) -> None:
        self.target = target
        self.aggro_rate = aggro_rate

        self._aggro = 0
        self._currentlyAttack = False
        self._state, self._max_state = 0, 1

        self._frozen = False
        self.__event_handler = event_handler
        self.screen = screen

    def try_to_move(self, score=0):
        if self._frozen:
            return False

        effective_rate = self.aggro_rate * (1.1 ** (score // 5))

        if randint(0, 10) >= 100 - self._aggro:
            self._state += 1
            self._aggro = 0
            return True

        self._aggro += effective_rate

    def reset_game_over(self):
        self._aggro = 0
        self._state = 0
        self.mode = "idle"

    def freeze(self):
        self._frozen = True

    def unfreeze(self):
        self._frozen = False

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
        self.__event_handler.gameover()
