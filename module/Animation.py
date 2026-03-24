import pygame


class Animation:
    def __init__(self, path) -> None:
        self.frame = 0
        self.path = path
        self.__sprites = []
        self.__sprite_width, self.__sprite_height = 64, 64
        self.__output_width, self.__output_height = 64, 64

    def set_sprites_frame(self, x, y):
        self.__sprite_width = x
        self.__sprite_height = y

        return self

    def set_output(self, x, y):
        self.__output_width = x
        self.__output_height = y
        return self

    def draw_sprite(self, screen, x, y, center=False):
        sprite = self.__sprites[self.frame]
        rect = sprite.get_rect()

        if center:
            rect.center = screen.get_rect().center
            rect.centerx += x
            rect.centery += y
        else:
            rect.left = x
            rect.top = y

        screen.blit(sprite, rect)

    def animate(self, reverse=False):
        if reverse:
            if self.frame - 1 >= 0:
                self.frame -= 1
            else:
                return True
        else:
            if self.frame + 1 < len(self.__sprites):
                self.frame += 1
            else:
                return True

        return False

    def load_sprite(self, row: int, column: int, gap_px=1, exceed_number=0):
        sprite = pygame.image.load(self.path)
        for y in range(row):
            for x in range(column):
                self.__sprites.append(self.__extract_sprite(sprite, x, y, gap_px))

        if exceed_number > 0:
            self.__sprites = self.__sprites[:-exceed_number]

        if len(self.__sprites) <= 0:
            raise ValueError("Slicing sprite failed")

    def __extract_sprite(self, sprite, src_x, src_y, gap_px, flip=False):
        image = pygame.Surface(
            (self.__sprite_width, self.__sprite_height), pygame.SRCALPHA
        )
        x = src_x * (self.__sprite_width + gap_px)
        y = src_y * (self.__sprite_height + gap_px)

        image.blit(sprite, (0, 0), (x, y, self.__sprite_width, self.__sprite_height))

        if flip:
            image = pygame.transform.flip(image, True, False)

        if image.get_size() != (self.__output_width, self.__output_height):
            image = pygame.transform.scale(
                image,
                (self.__output_width, self.__output_height),
            )
        return image

    def __len__(self):
        return len(self.__sprites)
