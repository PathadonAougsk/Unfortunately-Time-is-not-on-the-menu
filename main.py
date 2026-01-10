import pygame

from module.Animatonic import AnimatonicSystem


class App:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True

        self.Awake()
        self.Update()

    def Awake(self):
        self.dummy = AnimatonicSystem(0.3, 2)
        self.dummy.start()

    def Update(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.Quit()

            pygame.display.flip()
            self.clock.tick(60)

    def Quit(self):
        self.dummy.stop()


main = App()
