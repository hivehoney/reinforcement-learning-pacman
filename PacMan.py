import pygame
from sys import exit
from pygame.locals import *
from Const import Config
from SpriteSheet import SpriteSheet


class PacMan:
    def __init__(self):
        try:
            pygame.init()  # 초기화
            # 게임창 설정 w:640 h:200
            self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
            pygame.display.set_caption("PACMAN Game")
        except pygame.error as e:
            print(f"pygame 초기화 실패: {e}")
            exit()

        # 스프라이트 시트 로드
        sprite_sheet = SpriteSheet(Config.SPRITE_SHEET_PATH)

        # 스프라이트 추출
        self.wall_sprite = sprite_sheet.get_sprite(0, 64, 32, 32)  # 벽
        self.coin_sprite = sprite_sheet.get_sprite(43, 3, 13, 13)  # 코인
        self.blinky_sprite = sprite_sheet.get_sprite(123, 83, 14, 14)  # 유령 (블링키)
        self.pacman_sprite = sprite_sheet.get_sprite(3, 23, 12, 13)  # 팩맨 단일 이미지

        # 타일 크기 계산
        self.tile_size = Config.TILE_SIZE

        # 배경 이미지 로드 및 비율 유지하여 화면 크기에 맞춤
        self.bg_img = pygame.image.load("img/bg_img.png").convert_alpha()
        self.bg_img, self.bg_offset_x, self.bg_offset_y = self.adjust_background_image(
            self.bg_img, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT
        )

        # 초기화 시 배경에서 맵 데이터 추출
        self.map_data = self.extract_map_from_background()

        # 팩맨 초기 위치 설정
        self.pacman_pos = self.find_pacman_start_position()

        # 게임 상태
        self.running = True
        self.game_active = False  # 대기 상태
        self.clock = pygame.time.Clock()
        # 점수 초기화
        self.score = 0

    def adjust_background_image(self, image, screen_width, screen_height):
        """이미지 비율 유지하며 화면 크기에 맞게 조정"""
        image_width, image_height = image.get_width(), image.get_height()
        scale_width = screen_width / image_width
        scale_height = screen_height / image_height

        # 최소 스케일을 기준으로 크기 조정
        scale = min(scale_width, scale_height)
        new_width = int(image_width * scale)
        new_height = int(image_height * scale)

        # 중앙에 정렬하기 위한 오프셋 계산
        offset_x = (screen_width - new_width) // 2
        offset_y = (screen_height - new_height) // 2

        scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))
        return scaled_image, offset_x, offset_y

    def draw_text(self, text, size, color, pos):
        """텍스트를 화면에 그리기"""
        font = pygame.font.SysFont("Arial", size)
        render_text = font.render(text, True, color)
        self.screen.blit(render_text, pos)

    def start_screen(self):
        """게임 시작 화면"""
        while not self.game_active:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.start_button.collidepoint(mouse_pos):
                        self.game_active = True

            # 배경
            self.screen.blit(self.bg_img, (0, 0))  # 배경 이미지

            # start
            self.start_button = pygame.Rect(Config.SCREEN_WIDTH // 2 - 100, 100, 200, 50)
            pygame.draw.rect(self.screen, (0, 0, 0), self.start_button)
            self.draw_text("START", 40, (255, 255, 255), (Config.SCREEN_WIDTH // 2 - 50, 100))

            pygame.display.flip()
            self.clock.tick(Config.FPS)

    # 배경 이미지의 픽셀 데이터 분석
    def extract_map_from_background(self):
        """배경 이미지에서 벽 데이터를 추출 (RGB 기반)"""
        map_data = []
        for y in range(0, self.bg_img.get_height(), self.tile_size):
            row = []
            for x in range(0, self.bg_img.get_width(), self.tile_size):
                color = self.bg_img.get_at((x, y))[:3]  # RGB 값만 가져오기
                if color != (0, 0, 0):  # 파란색 (RGB)
                    row.append(0)  # 빈 공간
                else:
                    row.append(1)  # 벽
            map_data.append(row)
        return map_data

    def find_pacman_start_position(self):
        """벽이 아닌 위치에서 팩맨 초기 위치를 찾음"""
        for row_idx, row in enumerate(self.map_data):
            for col_idx, tile in enumerate(row):
                if tile == 0:  # 빈 공간
                    return [col_idx * self.tile_size, row_idx * self.tile_size]
        return [0, 0]  # 기본 위치 (예외 처리)

    def render_map(self):
        """맵 데이터 기반으로 벽과 기타 요소 렌더링"""
        for row_idx, row in enumerate(self.map_data):
            for col_idx, tile in enumerate(row):
                x = col_idx * Config.TILE_SIZE
                y = row_idx * Config.TILE_SIZE

                if tile == 1:  # 벽
                    pygame.draw.rect(self.screen, (0, 0, 255), (x, y, Config.TILE_SIZE, Config.TILE_SIZE))  # 벽 표시
                elif tile == 2:  # 코인
                    self.screen.blit(self.coin_sprite, (x + self.tile_size // 4, y + self.tile_size // 4))
                # elif tile == 3:  # 파워 펠릿
                #     self.screen.blit(self.power_pellet_sprite, (x + self.tile_size // 4, y + self.tile_size // 4))
                elif tile == 4:  # 몬스터
                    self.screen.blit(self.blinky_sprite, (x, y))
                elif tile == 5:  # 팩맨 초기 위치
                    self.pacman_pos = [x, y]  # 팩맨 위치 설정

    def render(self):
        """전체 화면 렌더링"""
        self.screen.fill((0, 0, 0))  # 검은색 배경
        self.screen.blit(self.bg_img, (self.bg_offset_x, self.bg_offset_y))
        self.render_map()  # 맵 데이터 렌더링
        self.screen.blit(self.pacman_sprite, (self.pacman_pos[0] + self.bg_offset_x, self.pacman_pos[1] + self.bg_offset_y))  # 팩맨 렌더링
        self.display_score()  # 점수 표시
        pygame.display.flip()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        new_pos = list(self.pacman_pos)

        if keys[K_UP]:
            self.pacman_pos[1] -= Config.CHAR_SPEED
        if keys[K_DOWN]:
            self.pacman_pos[1] += Config.CHAR_SPEED
        if keys[K_LEFT]:
            self.pacman_pos[0] -= Config.CHAR_SPEED
        if keys[K_RIGHT]:
            self.pacman_pos[0] += Config.CHAR_SPEED

        # 벽 충돌 검사
        tile_x = new_pos[0] // Config.TILE_SIZE
        tile_y = new_pos[1] // Config.TILE_SIZE

        if self.map_data[tile_y][tile_x] != 1:  # 다음 위치가 벽이 아니면 이동
            self.pacman_pos = new_pos

    def display_score(self):
        """점수 표시"""
        font = pygame.font.SysFont("Arial", 15)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def game_loop(self):
        self.start_screen()  # 시작 화면 표시

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:  # 창 종료
                    self.running = False
                    pygame.quit()
                    exit()

            # 키 입력 처리
            self.handle_input()
            # 화면 렌더링
            self.render()  # 캐릭터 렌더링
            # 프레임 제한
            self.clock.tick(Config.FPS)
