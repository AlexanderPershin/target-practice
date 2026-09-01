import random

import pygame

BULLET_HOLE_LIFETIME = 4000


class BulletHole(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: tuple[int, int], *groups):
        super().__init__(*groups)

        self.size = random.randint(10, 30)

        self.image = pygame.transform.scale(
            image, (self.size * 1.2, self.size)
        )

        angle = random.randint(0, 360)
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=pos)

        self.lifetime = BULLET_HOLE_LIFETIME
        self.alpha = 160
        self.image.set_alpha(self.alpha)

    def update(self, dt: float, *args, **kwargs) -> None:
        self.lifetime = max(0, self.lifetime - dt)
        if self.lifetime <= 0:
            self.kill()
            return

        self.alpha -= dt * 50
        self.image.set_alpha(max(0, self.alpha))
