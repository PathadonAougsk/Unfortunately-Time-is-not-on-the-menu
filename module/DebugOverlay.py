import pygame

_GREEN = (80, 220, 80)
_RED = (220, 60, 60)
_YELLOW = (220, 200, 60)
_WHITE = (220, 220, 220)
_DIM = (160, 160, 160)
_BG = (0, 0, 0, 180)

_PANEL_X = 8
_PANEL_Y = 8
_PAD = 8
_LINE_H = 18
_FONT_SIZE = 15


def _bool_color(value):
    return _GREEN if value else _RED


class DebugOverlay:
    def __init__(self, screen, event_handler, animatonic_controller=None):
        self.screen = screen
        self.event_handler = event_handler
        self.animatonic_controller = animatonic_controller
        self.enabled = False

        self._font = pygame.font.SysFont("monospace", _FONT_SIZE)
        self._surface = None

    def toggle(self):
        self.enabled = not self.enabled

    def draw(self):
        if not self.enabled:
            return

        eh = self.event_handler
        now = pygame.time.get_ticks()

        lines = []

        lines.append(("── EventHandler ──", "", _YELLOW))

        lines.append(
            (
                "facing_office",
                str(eh._is_facing_office),
                _bool_color(eh._is_facing_office),
            )
        )
        lines.append(("mask_on", str(eh.is_mask_on), _bool_color(eh.is_mask_on)))
        lines.append(("pc_on", str(eh.is_pc_on), _bool_color(eh.is_pc_on)))
        lines.append(
            ("door_close", str(eh.is_door_close), _bool_color(eh.is_door_close))
        )

        if eh.is_door_close and eh._door_close_start:
            elapsed = now - eh._door_close_start
            remaining = max(0, eh._door_max_close - elapsed)
            door_timer_str = f"{remaining / 1000:.1f}s / {eh._door_max_close // 1000}s"
            door_timer_col = _GREEN if remaining > 2000 else _RED
        else:
            door_timer_str = "—"
            door_timer_col = _DIM
        lines.append(("door_timer", door_timer_str, door_timer_col))

        locked = eh.is_door_locked
        if locked:
            unlock_in = (eh._door_locked_until - now) / 1000
            lock_str = f"LOCKED ({unlock_in:.1f}s)"
        else:
            lock_str = "open"
        lines.append(("door_locked", lock_str, _RED if locked else _DIM))

        lines.append(("submit", str(eh.is_sumbit), _bool_color(eh.is_sumbit)))
        lines.append(
            ("game_over", str(eh.is_game_over), _RED if eh.is_game_over else _DIM)
        )
        lines.append(("reset", str(eh.is_reset), _RED if eh.is_reset else _DIM))
        lines.append(("score", str(eh.score), _WHITE))

        ac = self.animatonic_controller
        if ac is not None:
            lines.append(("", "", _WHITE))
            lines.append(("── Animatronics ──", "", _YELLOW))
            for name, animatonic in ac.animatonics.items():
                state_val = ac.states.get(name, "?")
                aggro = getattr(animatonic, "_aggro", None)
                mode = getattr(animatonic, "mode", "?")
                frozen = getattr(animatonic, "_frozen", False)

                val_parts = [f"st={state_val}", f"mode={mode}"]
                if aggro is not None:
                    val_parts.append(f"aggro={aggro:.1f}")
                if frozen:
                    val_parts.append("FROZEN")

                color = (
                    _RED
                    if mode == "jumpscare"
                    else (_YELLOW if mode == "prep" else _WHITE)
                )
                lines.append((name, "  ".join(val_parts), color))

        col_label = 110
        col_value = 220
        panel_w = col_label + col_value + _PAD * 2
        panel_h = len(lines) * _LINE_H + _PAD * 2

        surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        surf.fill(_BG)

        y = _PAD
        for label, value, color in lines:
            if label.startswith("──"):
                text = self._font.render(label, True, color)
                surf.blit(text, (_PAD, y))
            else:
                label_surf = self._font.render(label, True, _DIM)
                value_surf = self._font.render(value, True, color)
                surf.blit(label_surf, (_PAD, y))
                surf.blit(value_surf, (_PAD + col_label, y))
            y += _LINE_H

        self.screen.blit(surf, (_PANEL_X, _PANEL_Y))
