import pygame
import os
import random
from random import randint

from pygame.constants import K_a, K_d, K_s, K_w


class Settings(object):
    window_width = 1280
    window_height = 720
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    hedgehog_size = (100, 100)
    hedgehog_speed = 25
    chestnut_size = (50, 50)
    heart_size = (50, 50)
    border_size = 70
    title = "Hedgehog"


class Background(object):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(
            Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass


class Hedgehog(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(
            Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.hedgehog_size)
        self.hedgehog_speed = Settings.hedgehog_speed
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.teleport()
        self.speed_x = 0
        self.speed_y = 0

    def teleport(self):
        self.rect.left = (Settings.window_width / 2)
        self.rect.top = Settings.window_height - Settings.border_size

    def update(self):
        self.move_ip()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def change_left(self):
        self.speed_x -= Settings.hedgehog_speed

    def change_right(self):
        self.speed_x += Settings.hedgehog_speed

    def change_top(self):
        self.speed_y -= Settings.hedgehog_speed

    def change_down(self):
        self.speed_y += Settings.hedgehog_speed

    def stop(self):
        self.speed_x = 0
        self.speed_y = 0
    
    def move_ip(self):
        pygame.Rect.move_ip(self.rect, self.speed_x, self.speed_y)

class Chestnut(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(
            Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.chestnut_size)
        self.rect = self.image.get_rect()
        self.rect.left = (random.randint(
            0, Settings.window_width - Settings.chestnut_size[1]))
        self.rect.top = 0 - Settings.chestnut_size[0]
        self.speed = random.randint(1, 8)

    def update(self):
        self.rect.top += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Game(object):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode(
            (Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(Settings.title)
        self.background = Background("Forest.jpg")
        self.hedgehog = Hedgehog("hedgehog.png")
        self.chestnut = pygame.sprite.Group()
        self.counter = 0
        self.lives = 3
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()

    def reset(self):
        self.chestnut.empty()
        self.hedgehog.teleport()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_a:
                    self.hedgehog.change_left()
                if event.key == pygame.K_w:
                    self.hedgehog.change_top()
                if event.key == pygame.K_s:
                    self.hedgehog.change_down()
                if event.key == pygame.K_d:
                    self.hedgehog.change_right()
            if event.type == pygame.KEYUP:
                if event.key == K_a or event.key == K_w or event.key == K_d or event.key == K_s:
                    self.hedgehog.stop()
            elif event.type == pygame.QUIT:
                self.running = False

    def update(self):
        if pygame.sprite.spritecollide(self.hedgehog, self.chestnut, True, False):
            self.reset()
            self.lives -= 1
        self.counter += 1
        if self.counter >= 50:
            self.chestnut.add(Chestnut("chestnut.png"))
            self.counter = 0
        self.chestnut.update()
        self.hedgehog.update()

    def draw(self):
        self.background.draw(self.screen)
        self.hedgehog.draw(self.screen)
        self.chestnut.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "170, 50"

    game = Game()
    game.run()