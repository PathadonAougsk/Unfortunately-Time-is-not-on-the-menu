import pygame


class Animation:
    def __init__(self, path) -> None:
        self.frame = 0
        self.path = path
        self.__sprites = []
        self.__input_width, self.__input_height = 64, 64
        self.__output_width, self.__output_height = 200, 200
        self.__scale = 1

    def set_input(self, x, y):
        self.__input_width = x
        self.__input_height = y

        return self

    def set_output(self, x, y):
        self.__output_width = x
        self.__output_height = y

        return self

    def set_scale(self, x):
        self.__scale = x
        return self

    def draw_sprite(self, screen, x, y):
        screen.blit(self.__sprites[self.frame], (x, y))

    def animate(self, reverse=False):
        if reverse:
            if self.frame - 1 > 0:
                self.frame -= 1
            else:
                return True
        else:
            if self.frame + 1 < len(self.__sprites):
                self.frame += 1
            else:
                return True

        return False

    def load_sprite(self, row: int, column: int, exceed_number=0):
        sprite = pygame.image.load(self.path)
        for y in range(row):
            for x in range(column):
                self.__sprites.append(self.__extract_sprite(sprite, x, y))

    def __extract_sprite(self, sprite, src_x, src_y, flip=False):
        image = pygame.Surface(
            (self.__output_width, self.__output_height), pygame.SRCALPHA
        )
        x = src_x * (self.__output_width + 1)
        y = src_y * (self.__output_height + 1)

        image.blit(sprite, (0, 0), (x, y, self.__output_width, self.__output_height))
        if flip:
            image = pygame.transform.flip(image, True, False)
        if self.__scale != 1:
            image = pygame.transform.scale(
                image,
                (
                    self.__output_width * self.__scale,
                    self.__output_height * self.__scale,
                ),
            )
        return image
