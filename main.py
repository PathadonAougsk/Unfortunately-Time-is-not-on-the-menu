import sys

import pygame

from module.Animatonics.BirdMan import BirdMan
from module.Animatonics.MrHappy import MrHappy
from module.Animatonics.Temp import TempCharacter

# from module.Animatonic import BirdMan
from module.EventHandler import EventHandler
from module.Office.Office import Office
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
        self.office = Office(self.screen, self.event_handler)
        self.birdman = BirdMan(self.screen, 0.5, self.player, self.event_handler, 0, 0)

        self.tempcharacter = TempCharacter(
            self.screen, 1, self.player, self.event_handler, 0, 0
        )

        self.mrhappy = MrHappy(self.screen, 0.5, self.player, self.event_handler, 0, 0)

        self.animatonics = [self.birdman, self.tempcharacter, self.mrhappy]

        self.pc_button = pygame.Rect(250, 355, 50, 50)
        self.door_button = pygame.Rect(230, 400, 40, 40)
        self.turn_right = pygame.Rect(720, 25, 50, 740)
        self.turn_left = pygame.Rect(20, 25, 50, 740)
        self.center_button = pygame.Rect(345, 470, 100, 100)

    def Update(self):
        game_events = []
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.Quit()

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.door_button.collidepoint(pos):
                        game_events.insert(0, self.event_handler.toggle_door)
                    elif self.pc_button.collidepoint(pos):
                        game_events.insert(0, self.event_handler.toggle_pc)
                    elif self.center_button.collidepoint(pos):
                        game_events.insert(0, self.event_handler.summbit_order)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_events.insert(0, self.event_handler.toggle_mask)

                    if event.key == pygame.K_w:
                        game_events.insert(0, self.event_handler.toggle_light)

                if self.turn_right.collidepoint(pos):
                    game_events.insert(0, self.event_handler.request_right)

                if self.turn_left.collidepoint(pos):
                    game_events.insert(0, self.event_handler.request_left)

            for event in set(game_events):
                self.dequeue(event())
                game_events.pop(0)

            self.current_tick = pygame.time.get_ticks()
            self.screen.fill((0, 0, 0))

            self.office.update_behavior()
            self.tempcharacter.update_behavior()

            if not self.event_handler.is_facing_front:
                self.mrhappy.try_to_move()
                self.mrhappy.update_behavior(True)

            self.player.draw()

            pygame.display.flip()
            self.clock.tick(60)

    def dequeue(self, event):
        if not event:
            return

        event_types, data = event
        self.office._receive_event(event_types, data)

        for animatonic in self.animatonics:
            animatonic._receive_event(event_types, data)

    def Quit(self):
        sys.exit()


main = App()
