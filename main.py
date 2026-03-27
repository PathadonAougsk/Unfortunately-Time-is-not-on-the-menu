import sys

import pygame

from module.Animatonics.Controller import AnimatonicController
from module.Animatonics.MrHappy import MrHappy
from module.Animatonics.MrTemp import MrTemp
from module.EventHandler import EventHandler
from module.Office.Controller import Office_controller
from module.Player import Player

ERROR_PINK = (255, 0, 220)


class App:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((790, 790))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.running = True

        self.Awake()
        self.Update()

    def Awake(self):
        self.event_handler = EventHandler()
        self.player = Player(self.screen)

        tempcharacter = MrTemp(self.screen, 1, self.player, self.event_handler, 0, 0)
        mrhappy = MrHappy(self.screen, 0.5, self.player, self.event_handler, 0, 0)
        animatonics = {
            "MrTemp": tempcharacter,
            "MrHappy": mrhappy,
        }

        self.animatonic_controller = AnimatonicController(
            animatonics, self.event_handler
        )

        self.office_controller = Office_controller(self.screen, self.event_handler)

        self.pc_button = pygame.Rect(250, 355, 50, 50)
        self.door_button = pygame.Rect(230, 400, 40, 40)
        self.turn_right = pygame.Rect(720, 25, 50, 740)
        self.turn_left = pygame.Rect(20, 25, 50, 740)
        self.center_button = pygame.Rect(345, 470, 100, 100)

    def Update(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.Quit()

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.door_button.collidepoint(pos):
                        self.event_handler.toggle_door()
                    elif self.pc_button.collidepoint(pos):
                        self.event_handler.toggle_pc()
                    elif self.center_button.collidepoint(pos):
                        pass
                        # self.event_handler.summbit_order()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.event_handler.toggle_mask()

                    if event.key == pygame.K_w:
                        self.event_handler.toggle_light()

                if self.turn_right.collidepoint(pos):
                    self.event_handler.turn_to_backroom()

                if self.turn_left.collidepoint(pos):
                    self.event_handler.turn_to_office()

            self.screen.fill((0, 0, 0))

            self.office_controller.process()
            self.office_controller.render()

            self.animatonic_controller.process()
            self.animatonic_controller.render()

            self.player.draw()

            pygame.display.flip()
            self.clock.tick(60)

    def Quit(self):
        sys.exit()


main = App()
