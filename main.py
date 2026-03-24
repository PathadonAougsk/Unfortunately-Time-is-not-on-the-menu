import sys

import pygame

from module.Animatonic import BirdMan, MrHappy, TempCharacter

# from module.Animatonic import BirdMan
from module.EventHandler import EventHandler
from module.Office import Office
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
        self.player = Player(self.screen)
        self.office = Office(self.screen)

        self.event_handler = EventHandler(self.player, self.office)
        self.birdman = BirdMan(self.screen, 0.5, self.player, self.event_handler, 0, 0)

        self.tempcharacter = TempCharacter(
            self.screen, 1, self.player, self.event_handler, 0, 0
        )

        self.mrhappy = MrHappy(self.screen, 0.5, self.player, self.event_handler, 0, 0)

        animatonics = [self.birdman, self.tempcharacter, self.mrhappy]
        self.event_handler.add_animatonics(animatonics)

        self.pc_button = pygame.Rect(250, 355, 50, 50)
        self.door_button = pygame.Rect(230, 400, 40, 40)
        self.turn_right = pygame.Rect(720, 25, 50, 740)
        self.turn_left = pygame.Rect(20, 25, 50, 740)

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.event_handler.toggle_mask()

                    if event.key == pygame.K_w:
                        self.event_handler.toggle_light()

                if self.turn_right.collidepoint(pos):
                    self.event_handler.turn_right()

                if self.turn_left.collidepoint(pos):
                    self.event_handler.turn_left()

            self.current_tick = pygame.time.get_ticks()

            self.screen.fill((0, 0, 0))

            self.office.update_behavior()
            # pygame.draw.rect(self.screen, ERROR_PINK, self.pc_button)

            # self.birdman.try_to_move()
            # self.birdman.update_behavior()

            # Known Bug when Character Appear and Player move quickly to computer, temp
            # will still appear

            self.tempcharacter.try_to_move()
            self.tempcharacter.update_behavior(self.event_handler.is_facing_front)

            if not self.event_handler.is_facing_front and self.event_handler.is_pc_on:
                self.mrhappy.try_to_move()
                self.mrhappy.update_behavior(True)
            else:
                self.mrhappy.interrupt()

            self.player.draw()

            pygame.display.flip()
            self.clock.tick(60)

    def Quit(self):
        sys.exit()


main = App()
