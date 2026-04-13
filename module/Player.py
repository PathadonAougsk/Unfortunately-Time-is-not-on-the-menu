from pathlib import Path

import pygame

from module.Animation import Animation


class Player:
    def __init__(self, screen) -> None:
        self.previous_tick = pygame.time.get_ticks()

        self.screen = screen
        self.centerx = screen.get_rect().centerx
        self.centery = screen.get_rect().centery

        mask_path = Path.cwd() / "Assets" / "Player" / "MaskOn.png"
        self.is_mask_on = False
        self.mask_animation = Animation(mask_path)
        self.mask_animation.set_sprites_frame(256, 256).set_output(
            1300, 1300
        ).load_sprite(2, 8, gap_px=2, exceed_number=6)
        self.mask_tick = 0

    def toggle_mask(self, result):
        self.is_mask_on = result

    def render(self):
        self._run_animation(not self.is_mask_on)
        if self.mask_animation.frame > 0:
            self.mask_animation.draw_sprite(self.screen, 0, 0, True)

    def _run_animation(self, reverse=False):
        current_tick = pygame.time.get_ticks()

        if current_tick - self.mask_tick > 100:
            self.mask_tick = current_tick
            self.mask_animation.animate(reverse)
