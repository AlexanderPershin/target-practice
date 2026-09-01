import random

import pygame

from bullethole import BulletHole
from config import Config
from crosshair import Crosshair
from targets import HorizontalBouncingTarget, TargetDirections, VerticalTarget

SCREEN_SPAWN_OFFSET = 300
GRID_LINE_COLOR = "#aaaaaa"

MAX_BULLET_HOLES = 50

SPAWN_INTERVAL = 900


class Game:
    def __init__(self, config: Config):
        self.running = False
        self.config = config

    def __enter__(self):
        pygame.mixer.pre_init(
            frequency=44100,
            size=-16,
            channels=2,
            buffer=512,
            allowedchanges=pygame.AUDIO_ALLOW_ANY_CHANGE,
        )

        pygame.init()

        pygame.mixer.set_num_channels(16)

        self.screen = pygame.display.set_mode((0, 0), flags=pygame.FULLSCREEN)

        self.screen_width, self.screen_height = self.screen.get_size()
        self.screen_rect = self.screen.get_rect().inflate(
            SCREEN_SPAWN_OFFSET, SCREEN_SPAWN_OFFSET
        )

        pygame.display.set_caption("Target practice")
        pygame.mouse.set_visible(False)

        self.clock = pygame.time.Clock()

        self._load_font()
        self._load_images()
        self._load_sounds()

        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.targets = pygame.sprite.Group()
        self.bullet_holes = pygame.sprite.Group()

        self.crosshair = Crosshair(self.crosshair_image)
        self.all_sprites.add(self.crosshair, layer=3)

        self.score = 0
        self.hits = 0
        self.misses = 0
        self.streak = 0
        self.best_streak = 0

        self.last_spawn_time = SPAWN_INTERVAL
        self.spawn_interval = SPAWN_INTERVAL

        self.running = True

        return self

    def __exit__(self, *args):
        pygame.quit()

    def _load_font(self) -> None:
        self.font = pygame.font.Font(
            self.config.font_path, self.config.gui_font_size
        )

    def _load_images(self) -> None:
        self.crosshair_image = pygame.image.load(
            "images/crosshair.svg"
        ).convert_alpha()
        self.bot_image = pygame.image.load(
            "images/bot_head.svg"
        ).convert_alpha()
        self.bullethole_image = pygame.image.load(
            "images/bullethole.svg"
        ).convert_alpha()

    def _load_sounds(self) -> None:
        self.shot_sound = pygame.mixer.Sound("sounds/shot.wav")
        self.shot_sound.set_volume(0.5)
        self.hit_sound = pygame.mixer.Sound("sounds/hit.wav")

        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.load("sounds/theme.wav")
        pygame.mixer.music.play(-1)

    def run(self):
        while self.running:
            self.dt = self.clock.tick(self.config.fps) / 1000
            self.watch_for_events()
            self.update()
            self.draw()

    def watch_for_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                case pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.shoot(event.pos)

    def spawn_target(self):
        direction = random.choice(list(TargetDirections))
        if direction in (
            TargetDirections.LEFT_TO_RIGHT,
            TargetDirections.RIGHT_TO_LEFT,
        ):
            target = HorizontalBouncingTarget(
                self.bot_image,
                direction,
                self.config.min_speed,
                self.config.max_speed,
                self.screen_width,
                self.screen_height,
            )
        else:
            target = VerticalTarget(
                self.bot_image,
                direction,
                self.config.min_speed,
                self.config.max_speed,
                self.screen_width,
                self.screen_height,
            )

        self.targets.add(target)
        self.all_sprites.add(target, layer=2)

    def check_bounds(self):
        for target in self.targets.sprites():
            if not self.screen_rect.colliderect(target.rect):
                target.kill()

    def add_bullet_hole(self, pos):
        hole = BulletHole(self.bullethole_image, pos)
        self.bullet_holes.add(hole)
        self.all_sprites.add(hole, layer=1)

        if len(self.bullet_holes) > MAX_BULLET_HOLES:
            oldest = min(self.bullet_holes, key=lambda h: h.lifetime)
            oldest.kill()

    def shoot(self, pos):
        self.shot_sound.play()

        self.add_bullet_hole(pos)

        hit_targets = [t for t in self.targets if t.rect.collidepoint(pos)]
        if hit_targets:
            self.hit_sound.play()
            hit_targets[0].kill()
            self.score += 10
            self.hits += 1
            self.streak += 1
            self.best_streak = max(self.streak, self.best_streak)
        else:
            self.misses += 1
            self.streak = 0

    def update(self):
        self.last_spawn_time = max(0, self.last_spawn_time - self.dt * 1000)

        if self.last_spawn_time == 0:
            self.last_spawn_time = self.spawn_interval
            self.spawn_target()

        self.all_sprites.update(self.dt)
        self.check_bounds()

    def draw(self):
        self.screen.fill(self.config.bg_color)

        for x in range(0, self.screen_width, 80):
            pygame.draw.line(
                self.screen, GRID_LINE_COLOR, (x, 0), (x, self.screen_height)
            )
        for y in range(0, self.screen_height, 80):
            pygame.draw.line(
                self.screen, GRID_LINE_COLOR, (0, y), (self.screen_width, y)
            )

        self.all_sprites.draw(self.screen)

        total_shots = self.hits + self.misses
        accuracy = (self.hits / total_shots * 100) if total_shots > 0 else 0.0

        gui_texts = (
            f"Score: {self.score}",
            f"Hits: {self.hits}   Misses: {self.misses}",
            f"Accuracy: {accuracy:.1f}%",
            f"Streak: {self.streak}   Best: {self.best_streak}",
            "ESC — exit",
        )

        y_offset = 10
        for line in gui_texts:
            surf = self.font.render(line, True, (220, 220, 220))
            self.screen.blit(surf, (15, y_offset))
            y_offset += 30

        pygame.display.flip()
