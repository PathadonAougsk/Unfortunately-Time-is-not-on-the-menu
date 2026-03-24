from pathlib import Path

import pygame

from module.Animation import Animation


class Player:
    def __init__(self, screen) -> None:
        self.previous_tick = pygame.time.get_ticks()
        self.state = "idle"

        self.screen = screen
        self.centerx = screen.get_rect().centerx
        self.centery = screen.get_rect().centery

        mask_path = Path.cwd() / "Assets" / "Player" / "Mask.png"
        self.mask_animation = Animation(mask_path)
        self.mask_animation.set_sprites_frame(256, 256).set_output(
            1300, 1300
        ).load_sprite(1, 1)

    def _receive_event(self, event):
        if event:
            self.state = "mask on"
            return

        self.state = "idle"

    def draw(self):
        if self.state == "mask on":
            self.mask_animation.draw_sprite(self.screen, 0, 0, True)
