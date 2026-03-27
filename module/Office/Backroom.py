from pathlib import Path

import pygame

from module.Animation import Animation


class Backroom:
    def __init__(self):
        backroom = Path.cwd() / "Assets" / "Office" / "back_side.png"

        self.backroom = (
            Animation(backroom).set_sprites_frame(256, 256).set_output(256 * 3, 256 * 3)
        )
        self.backroom.load_sprite(1, 6, gap_px=2)
        self.backroom.frame = 5

    def render(self, screen):
        self.backroom.draw_sprite(screen, 0, 0, True)
