import sys

import pygame

# from module.Animatonic import BirdMan
from module.Office import Office
from module.Player import Player


class App:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 600))
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.running = True

        self.Awake()
        self.Update()

    def Awake(self):
        self.player = Player()
        self.office = Office()
        # self.birdman = BirdMan(
        #     0.3, 2, self.player, self.screen_rect.centerx, self.screen_rect.centery
        # )
        # self.birdman.start()

        # self.pp = PP(
        #     0.5, 2, self.player, self.screen_rect.centerx, self.screen_rect.centery
        # )
        # # self.pp.start()

        # self.all_sprites = pygame.sprite.Group()
        # self.all_sprites.add(self.birdman)
        # self.all_sprites.add(self.pp)

    def Update(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.Quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.office.door.closing_door_button.collidepoint(pos):
                        self.office.toggle_door()

            keys = pygame.key.get_pressed()
            self.Event(keys)

            self.screen.fill((0, 0, 0))
            self.office.draw_office(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

    def Event(self, keys):
        if keys[pygame.K_a]:
            self.office.toggle_door()
        if keys[pygame.K_SPACE]:
            self.player.is_mask_on = True
        else:
            self.player.is_mask_on = False

    def Quit(self):
        # self.birdman.stop()
        # self.pp.stop()
        sys.exit()


main = App()
