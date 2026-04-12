from pathlib import Path

from module.Animation import Animation
from module.Animatonics.AnimatonicSystem import AnimatonicSystem
from module.Player import Player


class MrHappy(AnimatonicSystem):
    def __init__(self, screen, aggro_rate, target: Player, eventhandler, x, y) -> None:
        super().__init__(screen, target, eventhandler, aggro_rate)

        self.name = "MrHappy"
        self.mode = "idle"

        Appear_path = Path.cwd() / "Assets" / "MrHappy" / "Prepare.png"
        Jump_scare_path = Path.cwd() / "Assets" / "MrHappy" / "Jump_scare.png"

        self.prep_animation = (
            Animation(Appear_path)
            .set_sprites_frame(256, 256)
            .set_output(256 * 3, 256 * 3)
        )
        self.prep_animation.load_sprite(1, 8, gap_px=2)

        self.jump_animation = (
            Animation(Jump_scare_path)
            .set_sprites_frame(256, 256)
            .set_output(256 * 3, 256 * 3)
        )
        self.jump_animation.load_sprite(1, 5, gap_px=2)

        self.current_animation = self.prep_animation
        self._max_state = 3

        self._prep_tick = 0
        self._jump_tick = 0
        self._reset_tick = 0

    def interrupt(self):
        self.current_animation = self.prep_animation
        self.current_animation.frame = 0

    def behavior(self, state):
        self.current_animation = self.prep_animation

        if self.mode == "jumpscare":
            self.current_animation = self.jump_animation
            return self._run_animation(
                self.jump_animation, self._gameover, "_jump_tick", delay=100
            )

        if state == self._max_state:
            self.mode = "prep"
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
        if self.mode == "idle":
            return
        self.current_animation.draw_sprite(self.screen, 0, 0, center=True)
