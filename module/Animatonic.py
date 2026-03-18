from pathlib import Path

import pygame
from numpy.random.mtrand import randint

from module.Animation import Animation


class AnimatonicSystem(pygame.sprite.Sprite):
    Animatonics = []

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls.Animatonics.append(instance)
        return instance

    def __init__(self, aggro_rate, seconds, target) -> None:
        self.target = target
        self.aggro_rate = aggro_rate

        self.__aggro = 0
        self.__currentlyAttack = False
        self.__state, self.__max_state = 0, 1

    @classmethod
    def attack_avaiable(cls):
        for animatonic in cls.Animatonics:
            if animatonic.__currentlyAttack:
                return False
        return True

    def try_to_move(self):
        if randint(0, 10) < 7 - self.__aggro:
            self.__aggro += self.aggro_rate
            return

        if self.__state + 1 < self.__max_state:
            self.__state += 1
            return

        # if not AnimatonicSystem.attack_avaiable():
        #     return


class BirdMan(AnimatonicSystem):
    def __init__(self, aggro_rate, seconds, target, x, y) -> None:
        super().__init__(aggro_rate, seconds, target)
        pygame.sprite.Sprite.__init__(self)

        path = Path.cwd() / "Assets" / "BirdMan" / "Appear.png"
        self.animation = (
            Animation(path).set_input(90, 64).set_output(64, 64).set_scale(5)
        )
        self.animation.load_sprite(3, 4, 2)

    def __prepare_attack(self, screen):
        self.animation.draw_sprite(screen, 650, 150)
