import enum
import math
import random

import pygame

TARGET_MIN_SIZE = 30
TARGET_MAX_SIZE = 128


class TargetDirections(enum.Enum):
    RIGHT_TO_LEFT = enum.auto()
    LEFT_TO_RIGHT = enum.auto()
    TOP_TO_BOTTOM = enum.auto()
    BOTTOM_TO_TOP = enum.auto()


class Target(pygame.sprite.Sprite):
    def __init__(
        self,
        image: pygame.Surface,
        direction: TargetDirections,
        min_speed: int,
        max_speed: int,
        screen_width: int,
        screen_height: int,
        *groups,
    ):
        super().__init__(*groups)

        self.direction = direction
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.size = random.randint(
            TARGET_MIN_SIZE,
            TARGET_MAX_SIZE,
        )

        self.image = pygame.transform.scale(image, (self.size, self.size))

        self.rect = self.image.get_rect()

    def update(self, dt: float, *args, **kwargs):
        pass


class HorizontalBouncingTarget(Target):
    MIN_JUMP_HEIGHT = 70
    MAX_JUMP_HEIGHT = 180

    def __init__(
        self,
        image: pygame.Surface,
        direction: TargetDirections,
        min_speed: int,
        max_speed: int,
        screen_width: int,
        screen_height: int,
        *groups,
    ):
        super().__init__(
            image,
            direction,
            min_speed,
            max_speed,
            screen_width,
            screen_height,
            *groups,
        )
        self.vx = random.randint(min_speed, max_speed)

        if direction == TargetDirections.RIGHT_TO_LEFT:
            self.vx = -self.vx
            start_x = self.screen_width + self.size + 10
        else:
            start_x = -self.size - 10

        self.base_y = random.randint(120, self.screen_height - 120)
        self.jump_height = random.randint(
            self.MIN_JUMP_HEIGHT, self.MAX_JUMP_HEIGHT
        )
        self.jump_freq = random.uniform(0.006, 0.018)
        self.phase_offset = random.uniform(0, math.pi * 2)

        self.rect.center = (start_x, self.base_y)

    def update(self, dt: float, *args, **kwargs):
        self.rect.x += self.vx * dt * 100
        jump = abs(
            math.sin((self.rect.x + self.phase_offset) * self.jump_freq)
        )
        self.rect.y = self.base_y - jump * self.jump_height


class VerticalTarget(Target):
    def __init__(
        self,
        image: pygame.Surface,
        direction: TargetDirections,
        min_speed: int,
        max_speed: int,
        screen_width: int,
        screen_height: int,
        *groups,
    ):
        super().__init__(
            image,
            direction,
            min_speed,
            max_speed,
            screen_width,
            screen_height,
            *groups,
        )

        self.vy = random.randint(self.min_speed, self.max_speed)
        self.direction = direction

        if direction == TargetDirections.BOTTOM_TO_TOP:
            self.vy = -self.vy
            start_y = self.screen_height + self.size + 10
        else:
            start_y = -self.size - 10

        self.rect.center = (
            random.randint(100, self.screen_width - 100),
            start_y,
        )

    def update(self, dt: float, *args, **kwargs):
        self.rect.y += self.vy * dt * 100
