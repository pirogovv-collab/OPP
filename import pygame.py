import pygame
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def find_gif():
    path = os.path.join(SCRIPT_DIR, "frog.gif")
    if os.path.exists(path):
        return path
    gifs = [f for f in os.listdir(SCRIPT_DIR) if f.lower().endswith(".gif")]
    if gifs:
        return os.path.join(SCRIPT_DIR, gifs[0])
    print("В папке", SCRIPT_DIR, "нет ни одной .gif. Там лежит:")
    for f in os.listdir(SCRIPT_DIR):
        print("   ", repr(f))
    sys.exit(1)


GIF_PATH = find_gif()


def load_background(size):
    for ext in ("jpg", "jpeg", "png", "webp"):
        path = os.path.join(SCRIPT_DIR, f"background.{ext}")
        if os.path.exists(path):
            img = pygame.image.load(path).convert()
            scale = max(size[0] / img.get_width(), size[1] / img.get_height())
            new_size = (round(img.get_width() * scale), round(img.get_height() * scale))
            img = pygame.transform.smoothscale(img, new_size)
            crop = pygame.Rect(0, 0, *size)
            crop.center = img.get_rect().center
            return img.subsurface(crop).copy()
    print("Фон не найден: положи background.jpg в", SCRIPT_DIR)
    return None
PLAYER_HEIGHT = 150 


def load_gif(path, height=None):
    frames, durations = [], []
    for surf, delay in pygame.image.load_animation(path):
        durations.append(delay or 100)
        surf = surf.convert_alpha()
        if height:
            w, h = surf.get_size()
            surf = pygame.transform.smoothscale(surf, (int(w * height / h), height))
        frames.append(surf)
    return frames, durations


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.frames, self.durations = load_gif(GIF_PATH, PLAYER_HEIGHT)
        self.frame_index = 0
        self.last_switch = pygame.time.get_ticks()

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 5

    def _animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_switch >= self.durations[self.frame_index]:
            self.last_switch = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

        self._animate()


class Game:
    def __init__(self):
        pygame.init()

        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Брегданс лягушка")

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.is_running = True

        self.background = load_background((self.screen_width, self.screen_height))

        self.player = Player(self.screen_width // 2, self.screen_height // 2)
        self.all_sprites = pygame.sprite.Group(self.player)

    def run(self):
        while self.is_running:
            self._check_events()
            self._update()
            self._draw()
            self.clock.tick(self.fps)
        pygame.quit()
        sys.exit()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.is_running = False

    def _update(self):
        self.all_sprites.update()

    def _draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((40, 44, 52))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    Game().run()