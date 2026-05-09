import random

import pygame

from module.EventHandler import EventHandler


class AnimatonicController:
    def __init__(self, animatonics: dict, event_handler: EventHandler, session=None) -> None:
        self.animatonics = animatonics
        self.event_handler = event_handler
        self.session = session

        self.states = {name: 0 for name in animatonics}
        self._cooldown_until: int = 0

    def _cooldown_ms(self) -> int:
        upper = max(3.0, 10.0 - self.event_handler.score * 0.14)
        return int(random.uniform(3.0, upper) * 1000)

    def process(self):
        self.process_movement()
        self.process_behaviour()

    def process_movement(self):
        ball_active = (
            "MrBall" in self.animatonics and self.animatonics["MrBall"].mode == "prep"
        )
        temp_active = (
            "MrTemp" in self.animatonics and self.animatonics["MrTemp"].mode == "prep"
        )
        happy_active = (
            "MrHappy" in self.animatonics and self.animatonics["MrHappy"].mode == "prep"
        )

        now = pygame.time.get_ticks()
        in_cooldown = now < self._cooldown_until

        for name, animatonic in self.animatonics.items():
            if animatonic.mode == "idle":
                if not self.is_valid_to_move(name):
                    continue
                if in_cooldown:
                    continue

            if name == "MrTemp" and (ball_active or happy_active):
                continue
            if name == "MrBall" and temp_active:
                continue
            if name == "MrHappy" and (ball_active or temp_active):
                continue

            if animatonic.try_to_move(self.event_handler.score):
                self.states[name] += 1

    def process_behaviour(self):
        for name, animatonic in self.animatonics.items():
            if not self.is_valid_to_move(name) and animatonic.mode == "idle":
                continue
            prev_mode = animatonic.mode
            event = animatonic.behavior(self.states[name])
            if self.session and prev_mode != "prep" and animatonic.mode == "prep":
                self.session.on_threat_prep(name)
            if event:
                self.internal_process(event)

    def render_below_office(self):
        if "MrBall" in self.animatonics:
            animatonic = self.animatonics["MrBall"]
            if animatonic.mode in ["prep", "reset"]:
                animatonic.draw()

    def render(self):
        for name, animatonic in self.animatonics.items():
            if name == "MrBall":
                if animatonic.mode == "jumpscare":
                    animatonic.draw()
                continue
            if not self.is_valid_to_behaviour(name) and animatonic.mode in [
                "prep",
                "reset",
            ]:
                continue
            animatonic.draw()

    def force_character_state(self, name, state):
        self.states[name] = state

    def internal_process(self, event):
        event_type, character_name = event

        if event_type not in ["Attack", "Reset"]:
            return

        if event_type == "Attack":
            for name, animatonic in self.animatonics.items():
                animatonic.freeze()

            killed = self.event_handler.try_kill_player(character_name)
            if self.session:
                self.session.on_attack(character_name, survived=not killed, score=self.event_handler.score, aggro_rate=self.animatonics[character_name].aggro_rate)

            if killed:
                self.animatonics[character_name].jumpscare()
                return "Attack!"

            self.force_character_state(character_name, -1)

        elif event_type == "Reset":
            animatonic = self.animatonics[character_name]
            for name, animatonic in self.animatonics.items():
                animatonic.unfreeze()

            self.force_character_state(character_name, 0)
            self._cooldown_until = pygame.time.get_ticks() + self._cooldown_ms()

    def is_valid_to_move(self, name):
        if name == "MrHappy":
            if not self.event_handler.is_pc_on or self.event_handler._is_facing_office:
                return False
        return True

    def is_valid_to_behaviour(self, name):
        if name == "MrHappy":
            if self.event_handler._is_facing_office:
                return False
            if not self.event_handler.is_pc_on:
                if self.states[name] == 3:
                    self.force_character_state(name, 0)
                    self.animatonics[name].interrupt()
                return False
        else:
            if not self.event_handler._is_facing_office:
                return False

        return True

    def reset_animatonic(self):
        for name, animatonic in self.animatonics.items():
            animatonic.reset_game_over()

        self._cooldown_until = 0
        self.internal_process(["Reset", "MrTemp"])
        self.internal_process(["Reset", "MrHappy"])
        self.internal_process(["Reset", "MrBall"])
