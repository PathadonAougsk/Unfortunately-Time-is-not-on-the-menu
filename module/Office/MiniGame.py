import random

import pygame


class MiniGameLogic:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.center = self.screen.get_rect().center

        self.container = pygame.Rect(0, 0, 50, 50)
        self.container.center = self.center

        self.green = (154, 177, 122)
        self.red = (139, 0, 0)

        self.current_color = self.green
        self.previous_tick = pygame.time.get_ticks()
        self.container_last_tick = pygame.time.get_ticks()
        self.direction = "Left"
        self.score = 0
        self.combo = 0

        self._feedback = None
        self._feedback_tick = 0

        self._font = pygame.font.SysFont(None, 28)
        self._font_small = pygame.font.SysFont(None, 22)

    def _cycle_ms(self):
        return max(300, 1000 - (self.score // 5) * 60)

    def Update(self):
        now = pygame.time.get_ticks()
        cycle_ms = self._cycle_ms()

        if (
            self.container.width < self.screen_rect.width // 2
            and self.container.height < self.screen_rect.height // 2
        ):
            if now - self.container_last_tick > 50:
                self.container_last_tick = now
                self.container.scale_by_ip(1.1, 1.1)
                self.container.center = self.center

        if now - self.previous_tick >= cycle_ms:
            self.Swipe_left()
            now = pygame.time.get_ticks()

        pygame.draw.rect(self.screen, self.current_color, self.container)
        if self.direction == "Right":
            label = "SUMBIT"
        else:
            label = "REJECT"
        label_surf = self._font_small.render(label, True, (255, 255, 255))
        self.screen.blit(label_surf, label_surf.get_rect(center=self.container.center))

        elapsed = now - self.previous_tick
        ratio = max(0.0, 1.0 - elapsed / cycle_ms)
        bar_max_w = int(self.screen_rect.width * 0.8)
        bar_bg = pygame.Rect(0, 0, bar_max_w, 7)
        bar_bg.centerx = self.screen_rect.centerx
        bar_bg.bottom = self.screen_rect.height - 8
        bar_fill = pygame.Rect(bar_bg.left, bar_bg.top, int(bar_max_w * ratio), 7)
        bar_color = (
            (100, 200, 100)
            if ratio > 0.5
            else (220, 150, 50)
            if ratio > 0.25
            else (200, 60, 60)
        )
        pygame.draw.rect(self.screen, (50, 50, 50), bar_bg)
        if bar_fill.width > 0:
            pygame.draw.rect(self.screen, bar_color, bar_fill)

        if self.combo >= 2:
            combo_surf = self._font.render(f"x{self.combo}", True, (255, 220, 50))
            self.screen.blit(combo_surf, (5, 5))

        if self._feedback and now - self._feedback_tick < 400:
            colors = {
                "HIT": (100, 220, 100),
                "MISS": (200, 180, 50),
                "WRONG": (220, 60, 60),
            }
            fb_surf = self._font.render(self._feedback, True, colors[self._feedback])
            self.screen.blit(
                fb_surf, fb_surf.get_rect(centerx=self.screen_rect.centerx, top=5)
            )

    def Swipe_left(self):
        if self.direction == "Right":
            self.combo = 0
            self._show_feedback("MISS")
        self.__reset__()

    def Swipe_right(self):
        if self.direction == "Right":
            self.score += 1
            self.combo += 1
            self._show_feedback("HIT")
        else:
            self.score = max(0, self.score - 1)
            self.combo = 0
            self._show_feedback("WRONG")
        self.__reset__()

    def _show_feedback(self, text):
        self._feedback = text
        self._feedback_tick = pygame.time.get_ticks()

    def __reset__(self):
        self.previous_tick = pygame.time.get_ticks()
        self.container = pygame.Rect(0, 0, 50, 50)
        self.container.center = self.center

        self.direction = random.choice(["Left", "Right"])
        self.current_color = self.green if self.direction == "Right" else self.red


class MiniGame:
    def __init__(self) -> None:
        self.surface = pygame.Surface((215, 170))
        self.surface_rect = self.surface.get_rect(topleft=(290, 100))
        self.logic = MiniGameLogic(self.surface)

    def behavior(self, condition: bool):
        if condition:
            self.logic.Update()

    def render(self, screen):
        screen.blit(self.surface, self.surface_rect)
        self.surface.fill((0, 0, 0))
