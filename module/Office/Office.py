from pathlib import Path

import pygame

from module.Animation import Animation


class Office:
    def __init__(self) -> None:
        front_side = Path.cwd() / "Assets" / "Office" / "front_side.png"

        self.office = (
            Animation(front_side)
            .set_sprites_frame(256, 256)
            .set_output(256 * 3, 256 * 3)
        )
        self.office.load_sprite(1, 1)

    def render(self, screen):
        self.office.draw_sprite(screen, 0, 0, True)
