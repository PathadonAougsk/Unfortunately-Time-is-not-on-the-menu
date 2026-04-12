from pathlib import Path

import pygame

from module.Animation import Animation
from module.Animatonics.AnimatonicSystem import AnimatonicSystem
from module.Player import Player


class MrBall(AnimatonicSystem):
    def __init__(self, screen, aggro_rate, target: Player, eventhandler, x, y) -> None:
        super().__init__(screen, target, eventhandler, aggro_rate)

        self.name = "MrBall"
        self.mode = "idle"

        Appear_path = Path.cwd() / "Assets" / "MrBall" / "Appear.png"
        Jump_scare_path = Path.cwd() / "Assets" / "MrBall" / "Jump_scare.png"

        self.prep_animation = (
            Animation(Appear_path)
            .set_sprites_frame(256, 256)
            .set_output(256 * 3, 256 * 3)
        )

        self.prep_animation.load_sprite(2, 8, gap_px=2, exceed_number=4)

        self.jump_animation = (
            Animation(Jump_scare_path)
            .set_sprites_frame(256, 256)
            .set_output(2000, 2000)
        )
        self.jump_animation.load_sprite(1, 7)

        self.current_animation = self.prep_animation
        self._max_state = 3

        self._prep_tick = 0
        self._jump_tick = 0
        self._reset_tick = 0

        appear_sound_path = Path.cwd() / "Assets" / "MrBall" / "Appear.mp3"
        self._appear_sound = pygame.mixer.Sound(appear_sound_path)

    def behavior(self, state, should_appear=True):
        self.current_animation = self.prep_animation

        if self.mode == "jumpscare":
            self.current_animation = self.jump_animation
            self.draw()
            return self._run_animation(
                self.jump_animation, self._gameover, "_jump_tick", delay=100
            )

        if state == self._max_state:
            if self.mode != "prep":
                self._appear_sound.play()
            self.mode = "prep"
            self.freeze()
            return self._run_animation(self.prep_animation, self._attack, "_prep_tick")

        elif state == -1:
            self.mode = "reset"
            return self._run_animation(
                self.prep_animation, self._reset, "_reset_tick", reverse=True
            )

        self.mode = "idle"
        return ("Idle", self.name)

    def reset_game_over(self):
        super().reset_game_over()
        self.prep_animation.frame = 0
        self.jump_animation.frame = 0

    def jumpscare(self):
        self.mode = "jumpscare"

    def draw(self):
        self.current_animation.draw_sprite(self.screen, -5, 0, True)
