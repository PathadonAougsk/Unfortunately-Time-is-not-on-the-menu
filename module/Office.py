from pathlib import Path

import pygame

from module.Animation import Animation

ERROR_PINK = (255, 0, 220)


class Office:
    def __init__(self) -> None:
        self.images = {}

        door_path = Path.cwd() / "Assets" / "Office" / "Door_closing_sprite.png"

        self.last_update = pygame.time.get_ticks()
        self.door = Door(door_path, 3, 5)

        self.last_tick = pygame.time.get_ticks()

        self.previous_tick = pygame.time.get_ticks()

    def draw_office(self, screen, key="normal"):
        self.door.draw(screen, 0, 150)

    def toggle_door(self):
        self.door.toggle_animation = True


class Door:
    def __init__(self, path: Path, row: int, column: int, reverse=False) -> None:
        self.sprite = pygame.image.load(path)
        self.sprites = []

        self.animation = Animation(path).set_output(64, 64).set_scale(5)
        self.animation.load_sprite(3, 4)

        self.toggle_animation = False
        self.closing_door_button = pygame.Rect(0, 0, 30, 40)

        self.previous_tick = pygame.time.get_ticks()
        self.reverse = False

    def draw(self, screen, x, y):
        self.animation.draw_sprite(screen, x, y)

        if self.toggle_animation:
            current_tick = pygame.time.get_ticks()

            if current_tick - self.previous_tick > 100:
                self.previous_tick = current_tick
                fininshed = self.animation.animate(self.reverse)

                if fininshed:
                    self.toggle_animation = False
                    self.reverse = not self.reverse
