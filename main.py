import sys

import pygame

from module.Animatonics.Controller import AnimatonicController
from module.Animatonics.MrBall import MrBall
from module.Animatonics.MrHappy import MrHappy
from module.Animatonics.MrTemp import MrTemp
from module.DebugOverlay import DebugOverlay
from module.EventHandler import EventHandler
from module.GameOverScreen import GameOverScreen
from module.Office.Controller import Office_controller
from module.Player import Player
from module.Recording import Session
from module.StaticOverlay import StaticOverlay
from module.StatisticScreen import StatisticScreen
from module.TitleScreen import TitleScreen
from module.WinScreen import WinScreen

ERROR_PINK = (255, 0, 220)


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((790, 790))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.running = True
        self.Awake()
        self.Update()

    def Awake(self):
        self.event_handler = EventHandler()
        self.session = Session(self.event_handler)
        self.player = Player(self.screen)
        tempcharacter = MrTemp(self.screen, 0.2, self.player, self.event_handler, 0, 0)
        mrhappy = MrHappy(self.screen, 0.2, self.player, self.event_handler, 0, 0)
        mrball = MrBall(self.screen, 0.2, self.player, self.event_handler, 0, 0)
        animatonics = {"MrTemp": tempcharacter, "MrHappy": mrhappy, "MrBall": mrball}
        self.animatonic_controller = AnimatonicController(
            animatonics, self.event_handler, session=self.session
        )
        self.office_controller = Office_controller(self.screen, self.event_handler)
        self.title_screen = TitleScreen(self.screen)
        self.gameover_screen = GameOverScreen(self.screen)
        self.win_screen = WinScreen(self.screen)
        self.statistic_page = StatisticScreen(self.screen)
        self.state = "title"
        self.score_font = pygame.font.SysFont(None, 36)
        self.pc_button = pygame.Rect(250, 355, 50, 50)
        self.door_button = pygame.Rect(230, 400, 40, 40)
        self.turn_right = pygame.Rect(720, 25, 50, 740)
        self.turn_left = pygame.Rect(20, 25, 50, 740)
        self.center_button = pygame.Rect(345, 470, 100, 100)

        sw, sh = self.screen.get_size()
        self.static_overlay = StaticOverlay(sw, sh)
        self.debug_overlay = DebugOverlay(
            self.screen, self.event_handler, self.animatonic_controller
        )

    def Update(self):
        while self.running:
            pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Quit()

                if self.state == "title":
                    self.title_screen.handle_event(event)

                elif self.state == "statistic":
                    self.statistic_page.handle_event(event)

                elif self.state == "game":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.door_button.collidepoint(pos):
                            self.event_handler.toggle_door()
                            self.session.on_action("Door")
                        elif self.pc_button.collidepoint(pos):
                            self.event_handler.toggle_pc()
                            self.session.on_action("PC")
                        elif self.center_button.collidepoint(pos):
                            self.event_handler.sumbit_order()
                            self.session.on_action("Submit")

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.event_handler.toggle_mask()
                            self.session.on_action("Mask")
                        elif event.key == pygame.K_F3:
                            self.debug_overlay.toggle()

                elif self.state == "gameover":
                    self.gameover_screen.handle_event(event)

                elif self.state == "win":
                    self.win_screen.handle_event(event)

            self.screen.fill((0, 0, 0))

            if self.state == "game":
                if self.event_handler.is_game_over:
                    self.session.on_session_end(
                        survived=False, score=self.event_handler.score
                    )
                    self.state = "gameover"
                    self.animatonic_controller.reset_animatonic()
                    self.office_controller.reset_office()
                    self.gameover_screen.reset()
                elif self.event_handler.score >= 100:
                    self.session.on_session_end(
                        survived=True, score=self.event_handler.score
                    )
                    self.state = "win"
                    self.animatonic_controller.reset_animatonic()
                    self.office_controller.reset_office()
                    self.win_screen.reset()

            if self.state == "win":
                self.win_screen.process()
                self.win_screen.render()
                if self.win_screen.done:
                    self.event_handler.go_to_menu()
                    if self.win_screen.chosen == "Play Again":
                        self.session.reset()
                        self.state = "game"
                    else:
                        self.state = "title"
                        self.title_screen.done = False
                        self.title_screen._phase = "attract"

            elif self.state == "gameover":
                self.gameover_screen.process()
                self.gameover_screen.render()
                if self.gameover_screen.done:
                    self.event_handler.go_to_menu()
                    if self.gameover_screen.chosen == "Try Again":
                        self.session.reset()
                        self.state = "game"
                    else:
                        self.state = "title"
                        self.title_screen.done = False
                        self.title_screen._phase = "attract"

            elif self.state == "statistic":
                self.statistic_page.process()
                self.statistic_page.render()
                if self.statistic_page.done:
                    self.statistic_page.reset()
                    self.screen = pygame.display.set_mode((790, 790))
                    self.screen_rect = self.screen.get_rect()
                    self.title_screen.screen = self.screen
                    self.state = "title"
                    self.title_screen.done = False
                    self.title_screen._phase = "menu"

            elif self.state == "title":
                self.title_screen.process()
                self.title_screen.render()
                if self.title_screen.done:
                    if self.title_screen.chosen == "Statistic":
                        self.title_screen.done = False
                        self.screen = pygame.display.set_mode((1100, 790))
                        self.screen_rect = self.screen.get_rect()
                        self.statistic_page.screen = self.screen
                        self.statistic_page.sw = 1100
                        self.state = "statistic"
                    else:
                        self.state = "game"
                        volumes = self.title_screen.volumes
                        for (
                            name,
                            animatonic,
                        ) in self.animatonic_controller.animatonics.items():
                            if name in volumes and hasattr(animatonic, "_appear_sound"):
                                animatonic._appear_sound.set_volume(volumes[name])

            elif self.state == "game":
                _prev_facing = self.event_handler._is_facing_office
                if self.turn_right.collidepoint(pos):
                    self.event_handler.turn_to_backroom()
                if self.turn_left.collidepoint(pos):
                    self.event_handler.turn_to_office()
                if _prev_facing != self.event_handler._is_facing_office:
                    self.session.on_action(
                        "TurnLeft"
                        if self.event_handler._is_facing_office
                        else "TurnRight"
                    )

                self.office_controller.process()
                self.animatonic_controller.process()
                self.animatonic_controller.render_below_office()
                self.office_controller.render()
                self.animatonic_controller.render()

                self.player.toggle_mask(self.event_handler.is_mask_on)
                self.player.render()
                self.static_overlay.draw(self.screen)
                self.debug_overlay.draw()
                score_text = self.score_font.render(
                    f"{self.event_handler.score}/100", True, (255, 255, 255)
                )
                self.screen.blit(
                    score_text,
                    (self.screen_rect.centerx - score_text.get_width() // 2, 30),
                )

            pygame.display.flip()
            self.clock.tick(60)

    def Quit(self):
        pygame.quit()
        sys.exit()


main = App()
