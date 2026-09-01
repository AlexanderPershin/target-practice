import pygame


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(
            image,
            (150, 150),
        )
        self.image.set_alpha(196)
        self.rect = self.image.get_rect()

    def update(self, *args, **kwargs) -> None:
        self.rect.center = pygame.mouse.get_pos()
