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

    def Update(self):
        if (
            self.container.width < self.screen_rect.width // 2
            and self.container.height < self.screen_rect.height // 2
        ):
            current_tick = pygame.time.get_ticks()
            if current_tick - self.container_last_tick > 50:
                self.container_last_tick = current_tick
                self.container.scale_by_ip(1.1, 1.1)
                self.container.center = self.center

        current_tick = pygame.time.get_ticks()
        if current_tick - self.previous_tick >= 1000:
            self.previous_tick = current_tick
            self.Swipe_left()

        pygame.draw.rect(self.screen, self.current_color, self.container)

    def Swipe_left(self):
        if self.direction == "Left":
            self.score += 1

        self.__reset__()

    def Swipe_right(self):
        if self.direction == "Right":
            self.score += 1

        self.__reset__()

    def __reset__(self):
        self.previous_tick = pygame.time.get_ticks()
        self.container = pygame.Rect(0, 0, 50, 50)
        self.container.center = self.center

        directions = ["Left", "Right"]
        self.direction = random.choice(directions)

        if self.direction == "Right":
            self.current_color = self.green
        else:
            self.current_color = self.red


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
