from pathlib import Path

import pygame
from numpy.random.mtrand import randint

from module.Animation import Animation
from module.Corountine import Corountine


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
        self._system_corountine = Corountine(self.__will_move, seconds)
        self._attack_corountine = Corountine(self._prepare_attack, seconds)

    @classmethod
    def attack_avaiable(cls):
        for animatonic in cls.Animatonics:
            if animatonic.__currentlyAttack:
                return False
        return True

    def start(self):
        self._system_corountine.start()

    def stop(self):
        self._system_corountine.stop()

    def get_sprite_for_state(self):
        pass

    def __will_move(self):
        chosen_number = randint(1, 10)
        if chosen_number >= (7 - self.__aggro):
            self.__changing_state()
            self.__aggro = 0
            return

        self.__aggro += 1 * self.aggro_rate

    @property
    def aggro(self):
        return self.__aggro

    def __changing_state(self):
        if self.__state == self.__max_state and AnimatonicSystem.attack_avaiable():
            self.__currentlyAttack = True
            self.__state = 0

            self.change_sprite()
            self._attack_corountine.start()
            self._system_corountine.stop()
            return

        self.__state += 1

    def change_sprite(self):
        pass

    def _prepare_attack(self):
        pass


# class BirdMan(AnimatonicSystem):
#     def __init__(self, aggro_rate, seconds, target, x, y) -> None:
#         super().__init__(aggro_rate, seconds, target)
#         pygame.sprite.Sprite.__init__(self)

#         path = Path.cwd() / "Assets" / "BirdMan" / "Appear.png"

#         self.frame = 0
#         self.sprite = pygame.image.load(path).convert()
#         self.sprites = []

#         self.sprites_to_list(3, 4, False)
#         self.sprites[::-3]

#     def sprites_to_list(self, row: int, column: int, reverse):
#         for y in range(row):
#             for x in range(column):
#                 self.sprites.append(
#                     SpriteSheet.extract_sprite(self.sprite, x, y, 90, 64, 4, reverse)
#                 )

#     def draw_sprite(self, screen):
#         if len(self.sprites) <= 0:
#             raise IndexError("There is no sprite in list")

#         screen.blit(self.sprites[self.frame], (650, 150))

#     def animate(self):
#         if self.isattacking:
#             if self.frame + 1 < len(self.sprites) - 1:
#                 self.frame += 1
#                 return
#             self.isattacking = not self.isattacking
#         else:
#             if self.frame - 1 > 0:
#                 self.frame -= 1
#                 return
#             self.isattacking = not self.isattacking

#     def _prepare_attack(self):
#         self.isattacking = True
#         self.animate()
#         if not self.target.is_mask_on:
#             self.target.dead()
#             self._attack_corountine.stop()
#             self.__currentlyAttack = False
#             return

#         print("Pheew I survive")
#         self._system_corountine.start()
#         self._attack_corountine.stop()
#         self.image = pygame.Surface((500, 500))


# class PP(AnimatonicSystem):
#     def __init__(self, aggro_rate, seconds, target, x, y) -> None:
#         super().__init__(aggro_rate, seconds, target)

#         pygame.sprite.Sprite.__init__(self)

#         self.images = PP.find_sprite_related(__class__.__name__)

#         self.image = pygame.Surface((500, 500))
#         self.rect = self.image.get_rect()
#         self.rect.center = (x, y)

#     def change_sprite(self):
#         self.image = pygame.image.load(self.images[0]).convert()

#     def _prepare_attack(self):
#         if not self.target.is_mask_on:
#             self.target.dead()
#             self._attack_corountine.stop()
#             self.__currentlyAttack = False
#             return

#         print("Pheew I survive")
#         self._system_corountine.start()
#         self._attack_corountine.stop()
#         self.image = pygame.Surface((500, 500))
