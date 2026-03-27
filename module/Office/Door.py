from pathlib import Path

import pygame

from module.Animation import Animation


class Door:
    def __init__(self):
        door_animation = Path.cwd() / "Assets" / "Office" / "door_animation.png"
        self.door = (
            Animation(door_animation)
            .set_sprites_frame(256, 256)
            .set_output(256 * 3, 256 * 3)
        )
        self.door.load_sprite(1, 10, gap_px=2)
        self.door_tick = 0

    def render(self, screen):
        self.door.draw_sprite(screen, 0, 0, True)

    def _run_animation(self, reverse=False):
        current_tick = pygame.time.get_ticks()

        if current_tick - self.door_tick > 100:
            self.door_tick = current_tick
            self.door.animate(reverse)
