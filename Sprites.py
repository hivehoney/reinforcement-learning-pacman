"""
Block, Wall, Player, Ghost와 같이 스프라이트를 정의하는 클래스
"""
import pygame
from Const import Config

class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(Config.WHITE)
        self.image.set_colorkey(Config.WHITE)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        super().__init__()
        self.image = pygame.image.load(filename).convert()
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.change_x = 0
        self.change_y = 0

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def update(self, walls, gate):
        old_x, old_y = self.rect.left, self.rect.top
        self.rect.left += self.change_x

        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.left = old_x

        self.rect.top += self.change_y
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.top = old_y

        # 팩맨은 게이트를 통과하지 못함
        if gate and pygame.sprite.spritecollide(self, gate, False):
            self.rect.left, self.rect.top = old_x, old_y

class Ghost(Player):
    def changespeed(self, directions, ghost, turn, steps, length):
        if steps < directions[turn][2]:
            self.change_x, self.change_y = directions[turn][:2]
            steps += 1
        else:
            turn = (turn + 1) if turn < length else (2 if ghost == "clyde" else 0)
            self.change_x, self.change_y = directions[turn][:2]
            steps = 0
        return turn, steps
