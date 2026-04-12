import math
import random

import pygame


class StaticOverlay:
    def __init__(self, width: int, height: int) -> None:
        self._w = width
        self._h = height
        self._noise_surf = self._make_noise(width, height)
        self._scanlines = self._make_scanlines(width, height)
        self._vignette = self._make_vignette(width, height)

    def draw(self, surface: pygame.Surface) -> None:
        self._noise_surf.set_alpha(random.randint(6, 18))
        ox = random.randint(-2, 2)
        oy = random.randint(-2, 2)
        surface.blit(self._noise_surf, (ox, oy))
        surface.blit(self._scanlines, (0, 0))
        surface.blit(self._vignette, (0, 0))

    @staticmethod
    def _make_noise(w: int, h: int) -> pygame.Surface:
        surf = pygame.Surface((w, h))
        arr = pygame.PixelArray(surf)
        for x in range(w):
            for y in range(h):
                v = random.randint(0, 255)
                arr[x, y] = surf.map_rgb(v, v, v)
        del arr
        return surf

    @staticmethod
    def _make_scanlines(w: int, h: int) -> pygame.Surface:
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        for y in range(0, h, 3):
            pygame.draw.line(surf, (0, 0, 0, 55), (0, y), (w, y))
        return surf

    @staticmethod
    def _make_vignette(w: int, h: int) -> pygame.Surface:
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        cx, cy = w // 2, h // 2
        max_r = math.hypot(cx, cy)
        for y in range(0, h, 2):
            for x in range(0, w, 2):
                d = math.hypot(x - cx, y - cy) / max_r
                a = int(min(255, d**2.2 * 255 * 1.4))
                surf.set_at((x, y), (0, 0, 0, a))
                surf.set_at((x + 1, y), (0, 0, 0, a))
                surf.set_at((x, y + 1), (0, 0, 0, a))
                surf.set_at((x + 1, y + 1), (0, 0, 0, a))
        return surf
