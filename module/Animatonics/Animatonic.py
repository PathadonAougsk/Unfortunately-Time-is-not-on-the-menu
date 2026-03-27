from pathlib import Path

import pygame
from numpy.random.mtrand import randint

from module.Animation import Animation
from module.Player import Player


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
        event_type, data = self.__event_handler.try_kill_player(self.__class__.__name__)
        if not data:
            self._state = -1
            return

        self._state = -2

    def _receive_event(self, type_of_event, data):
        pass

    def _jumpscare(self):
        pass

    def _reset(self):
        self.unfreeze()
        self._state = 0
