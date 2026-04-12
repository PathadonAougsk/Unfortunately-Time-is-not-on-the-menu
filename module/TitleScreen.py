import math
import random
import sys

import pygame

from module.StaticOverlay import StaticOverlay

TITLE_TEXT = "TILL 6 AM"
SUBTITLE = "A night to survive"
MENU_ITEMS = ["New Night", "Statistic", "Quit"]

COL_BG = (0, 0, 0)
COL_TITLE = (200, 30, 30)
COL_TITLE_GLOW = (80, 0, 0)
COL_SUBTITLE = (140, 140, 140)
COL_ITEM = (180, 180, 180)
COL_ITEM_SEL = (230, 230, 50)
COL_ITEM_SHADOW = (60, 60, 20)

BLINK_SPEED = 0.9
FLICKER_PROB = 0.003


class TitleScreen:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.done = False
        self.chosen: str | None = None

        sw, sh = screen.get_size()
        self.sw, self.sh = sw, sh

        try:
            self.font_title = pygame.font.Font(None, int(sh * 0.14))
            self.font_subtitle = pygame.font.Font(None, int(sh * 0.045))
            self.font_menu = pygame.font.Font(None, int(sh * 0.06))
            self.font_hint = pygame.font.Font(None, int(sh * 0.035))
        except Exception:
            self.font_title = pygame.font.SysFont("arial", int(sh * 0.14))
            self.font_subtitle = pygame.font.SysFont("arial", int(sh * 0.045))
            self.font_menu = pygame.font.SysFont("arial", int(sh * 0.06))
            self.font_hint = pygame.font.SysFont("arial", int(sh * 0.035))

        self._phase = "attract"
        self._sel_index = 0
        self._tick = 0
        self._time = 0.0
        self._flicker = False
        self._blink_on = True
        self._menu_alpha = 0
        self._menu_rects: list[pygame.Rect] = []

        self._title_y = -int(sh * 0.25)
        self._title_target = int(sh * 0.18)
        self._title_vel = 0.0

        self._overlay = StaticOverlay(sw, sh)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self.done:
            return

        if self._phase == "attract":
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self._phase = "menu"

        elif self._phase == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self._sel_index = (self._sel_index - 1) % len(MENU_ITEMS)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self._sel_index = (self._sel_index + 1) % len(MENU_ITEMS)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self._confirm()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(self._menu_rects):
                    if rect.collidepoint(event.pos):
                        self._sel_index = i
                        self._confirm()
                        break

            elif event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(self._menu_rects):
                    if rect.collidepoint(event.pos):
                        self._sel_index = i
                        break

    def process(self) -> None:
        self._time += 1 / 60
        self._tick += 1
        self._flicker = random.random() < FLICKER_PROB
        self._blink_on = (self._time % BLINK_SPEED) < (BLINK_SPEED * 0.55)

        if self._title_y < self._title_target:
            self._title_vel += (self._title_target - self._title_y) * 0.18
            self._title_vel *= 0.72
            self._title_y = min(self._title_y + self._title_vel, self._title_target)

        if self._phase == "menu" and self._menu_alpha < 255:
            self._menu_alpha = min(255, self._menu_alpha + 6)

    def render(self) -> None:
        screen = self.screen
        screen.fill(COL_BG)

        self._draw_title()
        self._draw_subtitle()

        if self._phase == "attract":
            self._draw_attract_prompt()
        else:
            self._draw_menu()

        self._overlay.draw(screen)

    def _confirm(self) -> None:
        label = MENU_ITEMS[self._sel_index]
        self.chosen = label
        if label == "Quit":
            pygame.quit()
            sys.exit()
        elif label == "Statistic":
            pass
        else:
            self.done = True

    def _draw_title(self) -> None:
        sw = self.sw
        alpha = 0 if self._flicker else 255
        col = COL_TITLE if not self._flicker else (50, 0, 0)

        for offset, a in ((6, 80), (4, 120), (2, 160)):
            glow = self.font_title.render(TITLE_TEXT, True, COL_TITLE_GLOW)
            glow.set_alpha(a)
            gx = sw // 2 - glow.get_width() // 2 + offset
            self.screen.blit(glow, (gx, self._title_y + offset))

        surf = self.font_title.render(TITLE_TEXT, True, col)
        surf.set_alpha(alpha)
        x = sw // 2 - surf.get_width() // 2
        self.screen.blit(surf, (x, self._title_y))

    def _draw_subtitle(self) -> None:
        sw, sh = self.sw, self.sh
        surf = self.font_subtitle.render(SUBTITLE, True, COL_SUBTITLE)
        surf.set_alpha(180)
        x = sw // 2 - surf.get_width() // 2
        y = self._title_y + self.font_title.get_height() + int(sh * 0.01)
        self.screen.blit(surf, (x, y))

    def _draw_attract_prompt(self) -> None:
        if not self._blink_on:
            return
        sw, sh = self.sw, self.sh
        surf = self.font_hint.render("- PRESS ANY KEY -", True, COL_ITEM)
        surf.set_alpha(200)
        x = sw // 2 - surf.get_width() // 2
        y = sh - int(sh * 0.12)
        self.screen.blit(surf, (x, y))

    def _draw_menu(self) -> None:
        sw, sh = self.sw, self.sh
        spacing = int(sh * 0.09)
        start_y = int(sh * 0.50)
        self._menu_rects = []

        for i, label in enumerate(MENU_ITEMS):
            selected = i == self._sel_index
            col = COL_ITEM_SEL if selected else COL_ITEM

            scale = 1.0 + (0.04 * math.sin(self._time * 5.0) if selected else 0.0)

            surf = self.font_menu.render(label, True, col)
            w, h = int(surf.get_width() * scale), int(surf.get_height() * scale)
            surf = pygame.transform.smoothscale(surf, (w, h))
            surf.set_alpha(self._menu_alpha)

            shadow = self.font_menu.render(label, True, COL_ITEM_SHADOW)
            shadow = pygame.transform.smoothscale(shadow, (w, h))
            shadow.set_alpha(self._menu_alpha)

            x = sw // 2 - w // 2
            y = start_y + i * spacing

            self.screen.blit(shadow, (x + 3, y + 3))
            self.screen.blit(surf, (x, y))
            self._menu_rects.append(pygame.Rect(x, y, w, h))

        if self._menu_rects and self._blink_on:
            r = self._menu_rects[self._sel_index]
            cx = r.left - 22
            cy = r.centery
            pts = [(cx, cy - 8), (cx, cy + 8), (cx + 14, cy)]
            pygame.draw.polygon(self.screen, COL_ITEM_SEL, pts)
