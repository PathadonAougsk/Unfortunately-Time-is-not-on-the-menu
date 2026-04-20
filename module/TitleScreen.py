import math
import random
import sys
from pathlib import Path

import pygame

from module.StaticOverlay import StaticOverlay

TITLE_TEXT = "Unfortunately"
SUBTITLE = "Time is not on the menu"
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

SLIDER_CHARS = ["MrTemp", "MrBall"]
SLIDER_W = 220
SLIDER_H = 8
SLIDER_HANDLE_R = 9
COL_SLIDER_BG = (60, 60, 60)
COL_SLIDER_FILL = (200, 30, 30)
COL_SLIDER_HANDLE = (230, 230, 230)
COL_SLIDER_LABEL = (180, 180, 180)


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

        self.volumes = {name: 1.0 for name in SLIDER_CHARS}
        self._slider_bars: dict[str, pygame.Rect] = {}
        self._dragging: str | None = None
        self._preview_sounds: dict[str, pygame.mixer.Sound] = (
            self._load_preview_sounds()
        )

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
                hit_slider = self._try_grab_slider(event.pos)
                if not hit_slider:
                    for i, rect in enumerate(self._menu_rects):
                        if rect.collidepoint(event.pos):
                            self._sel_index = i
                            self._confirm()
                            break

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._dragging = None

            elif event.type == pygame.MOUSEMOTION:
                if self._dragging:
                    self._update_slider(self._dragging, event.pos[0])
                else:
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
            self._draw_sliders()

        self._overlay.draw(screen)

    def _confirm(self) -> None:
        label = MENU_ITEMS[self._sel_index]
        self.chosen = label
        if label == "Quit":
            pygame.quit()
            sys.exit()
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

    def _draw_sliders(self) -> None:
        sw, sh = self.sw, self.sh
        label_surf = self.font_hint.render("VOLUME", True, COL_SLIDER_LABEL)
        label_surf.set_alpha(self._menu_alpha)
        self.screen.blit(
            label_surf, (sw // 2 - label_surf.get_width() // 2, int(sh * 0.80))
        )

        self._slider_bars = {}
        for i, name in enumerate(SLIDER_CHARS):
            cx = sw // 2
            y = int(sh * 0.855) + i * int(sh * 0.07)

            bar = pygame.Rect(cx - SLIDER_W // 2, y - SLIDER_H // 2, SLIDER_W, SLIDER_H)
            self._slider_bars[name] = bar

            # Track
            bg = pygame.Surface((bar.w, bar.h), pygame.SRCALPHA)
            bg.fill((*COL_SLIDER_BG, self._menu_alpha))
            self.screen.blit(bg, bar.topleft)

            # Fill
            fill_w = int(bar.w * self.volumes[name])
            if fill_w > 0:
                fill = pygame.Surface((fill_w, bar.h), pygame.SRCALPHA)
                fill.fill((*COL_SLIDER_FILL, self._menu_alpha))
                self.screen.blit(fill, bar.topleft)

            # Handle
            hx = bar.left + int(bar.w * self.volumes[name])
            handle_col = (*COL_SLIDER_HANDLE, self._menu_alpha)
            handle_surf = pygame.Surface(
                (SLIDER_HANDLE_R * 2, SLIDER_HANDLE_R * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                handle_surf,
                handle_col,
                (SLIDER_HANDLE_R, SLIDER_HANDLE_R),
                SLIDER_HANDLE_R,
            )
            self.screen.blit(handle_surf, (hx - SLIDER_HANDLE_R, y - SLIDER_HANDLE_R))

            # Label
            lbl = self.font_hint.render(name, True, COL_SLIDER_LABEL)
            lbl.set_alpha(self._menu_alpha)
            self.screen.blit(
                lbl, (bar.left - lbl.get_width() - 10, y - lbl.get_height() // 2)
            )

            # Value
            val_text = self.font_hint.render(
                f"{int(self.volumes[name] * 100)}%", True, COL_SLIDER_LABEL
            )
            val_text.set_alpha(self._menu_alpha)
            self.screen.blit(val_text, (bar.right + 8, y - val_text.get_height() // 2))

    def _try_grab_slider(self, pos: tuple[int, int]) -> bool:
        for name, bar in self._slider_bars.items():
            hx = bar.left + int(bar.w * self.volumes[name])
            hy = bar.centery
            if math.hypot(pos[0] - hx, pos[1] - hy) <= SLIDER_HANDLE_R + 6:
                self._dragging = name
                return True
            if bar.inflate(0, 16).collidepoint(pos):
                self._dragging = name
                self._update_slider(name, pos[0])
                return True
        return False

    def _update_slider(self, name: str, mouse_x: int) -> None:
        bar = self._slider_bars.get(name)
        if not bar:
            return
        ratio = max(0.0, min(1.0, (mouse_x - bar.left) / bar.w))
        old = self.volumes[name]
        self.volumes[name] = ratio
        if abs(ratio - old) >= 0.01:
            sound = self._preview_sounds.get(name)
            if sound:
                sound.set_volume(ratio)
                sound.stop()
                sound.play()

    def _load_preview_sounds(self) -> dict[str, pygame.mixer.Sound]:
        sounds = {}
        asset_dirs = {"MrTemp": "MrTemp", "MrBall": "MrBall"}
        for name, folder in asset_dirs.items():
            path = Path.cwd() / "Assets" / folder / "Appear.mp3"
            if path.exists():
                sounds[name] = pygame.mixer.Sound(path)
        return sounds
