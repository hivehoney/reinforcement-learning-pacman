import pygame
from sys import exit
from pygame.locals import *

class PacMan:
    def __init__(self):
        pygame.init()  # 초기화

        # 게임창 설정 w:1000 h:600
        width, height = 1000, 600
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("PACMAN Game")

        # 이미지 파일 경로 설정
        imgs = ['blinky.png', 'clyde.png', 'cobra.png', 'inky.png', 'pinky.png']
        imgs = ['img/' + file for file in imgs]

        # 이미지 서피스 객체 생성
        self.chars = [pygame.image.load(img).convert_alpha() for img in imgs]

        self.bg = pygame.Surface(self.screen.get_size()).convert()
        self.bg_img = pygame.image.load('img/pacman_intro.png').convert()

        self.clock = pygame.time.Clock()

    def render(self, pos):
        # 배경 및 배경 이미지 설정
        self.screen.blit(self.bg, (0, 0))
        self.bg.blit(self.bg_img, (0, 0))

        # 캐릭터 렌더링
        for name in self.chars:
            x, y = pos
            pos = ((x + 80) % 600, y)
            self.screen.blit(name, pos)

        pygame.display.flip()

    def game_loop(self):
        running = True  # 게임 진행 중
        pos = (x, y) = (0, 200)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 창 종료
                    running = False
                    pygame.quit()
                    exit()

            # 캐릭터 위치 업데이트
            x, y = pos
            pos = (x + 10, y)

            # 화면 렌더링
            self.render(pos)
            self.clock.tick(60)  # 프레임 제한
