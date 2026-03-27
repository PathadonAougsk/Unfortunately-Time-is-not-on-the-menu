from pathlib import Path

from module.Animation import Animation
from module.Animatonics.AnimatonicSystem import AnimatonicSystem
from module.Player import Player


class MrTemp(AnimatonicSystem):
    def __init__(self, screen, aggro_rate, target: Player, eventhandler, x, y) -> None:
        super().__init__(screen, target, eventhandler, aggro_rate)

        self.name = "MrTemp"
        self.mode = "idle"

        Appear_path = Path.cwd() / "Assets" / "TempCharacter" / "Appear.png"
        Jump_scare_path = Path.cwd() / "Assets" / "TempCharacter" / "Jump_scare.png"

        self.prep_animation = (
            Animation(Appear_path).set_sprites_frame(128, 128).set_output(300, 300)
        )
        self.prep_animation.load_sprite(1, 7)

        self.jump_animation = (
            Animation(Jump_scare_path)
            .set_sprites_frame(128, 128)
            .set_output(2000, 2000)
        )
        self.jump_animation.load_sprite(1, 8)

        self.current_animation = self.prep_animation
        self._max_state = 3

        self._prep_tick = 0
        self._jump_tick = 0
        self._reset_tick = 0

    def behavior(self, state):
        self.current_animation = self.prep_animation

        if self.mode == "jumpscare":
            self.current_animation = self.jump_animation
            self.draw()
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

    def jumpscare(self):
        self.mode = "jumpscare"

    def draw(self):
        self.current_animation.draw_sprite(self.screen, 120, 0, True)
