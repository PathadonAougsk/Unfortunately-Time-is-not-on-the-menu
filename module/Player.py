import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        self.is_occupied = False
        self.is_mask_on = False
        self.is_light_off = False
        self.is_door_close = False

    def toggle_light(self):
        self.is_light_off = not self.is_light_off

    def toggle_door(self):
        self.is_door_close = not self.is_door_close

    def toggle_mask(self):
        self.is_mask_on = not self.is_mask_on

    def dead(self):
        pass
