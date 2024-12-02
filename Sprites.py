import pygame
from Const import Config

class Block(pygame.sprite.Sprite):
    """
    게임 내 블록(코인)을 나타내는 클래스
    - 팩맨이 수집해야 하는 대상
    """
    def __init__(self, color, width, height):
        """
        Block 클래스 초기화 메서드
        Args:
            color (tuple): 블록의 색상 (RGB 값)
            width (int): 블록의 가로 크기
            height (int): 블록의 세로 크기
        """
        super().__init__()
        self.image = pygame.Surface([width, height])  # 블록의 이미지 생성
        self.image.fill(Config.WHITE)
        self.image.set_colorkey(Config.WHITE)  # 흰색을 투명 처리
        # 타원형 블록을 지정된 색상으로 그림
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()  # 블록의 위치와 크기를 정의

class Wall(pygame.sprite.Sprite):
    """
    게임 내 벽을 나타내는 클래스
    - 팩맨과 유령의 이동을 제한하는 요소
    """
    def __init__(self, x, y, width, height, color):
        """
        Wall 클래스 초기화 메서드
        Args:
            x (int): 벽의 왼쪽 상단 x 좌표
            y (int): 벽의 왼쪽 상단 y 좌표
            width (int): 벽의 가로 크기
            height (int): 벽의 세로 크기
            color (tuple): 벽의 색상 (RGB 값)
        """
        super().__init__()
        self.image = pygame.Surface([width, height])  # 벽의 이미지 생성
        self.image.fill(color)  # 벽의 색상 채우기
        self.rect = self.image.get_rect()  # 벽의 위치와 크기를 정의
        self.rect.top = y  # 벽의 y 좌표 설정
        self.rect.left = x  # 벽의 x 좌표 설정

class Player(pygame.sprite.Sprite):
    """
    팩맨을 나타내는 클래스
    - 플레이어 캐릭터로, 사용자의 입력에 따라 움직임
    """
    def __init__(self, x, y, filename):
        """
        Player 클래스 초기화 메서드
        Args:
            x (int): 팩맨의 초기 x 좌표
            y (int): 팩맨의 초기 y 좌표
            filename (str): 팩맨 이미지 파일 경로
        """
        super().__init__()
        self.image = pygame.image.load(filename).convert()  # 팩맨 이미지를 로드
        self.rect = self.image.get_rect()  # 팩맨의 위치와 크기를 정의
        self.rect.top = y  # 팩맨의 초기 y 좌표 설정
        self.rect.left = x  # 팩맨의 초기 x 좌표 설정
        self.change_x = 0  # x 방향 이동 속도
        self.change_y = 0  # y 방향 이동 속도

    def changespeed(self, x, y):
        """
        팩맨의 이동 속도를 변경
        Args:
            x (int): x 방향 속도 변경 값
            y (int): y 방향 속도 변경 값
        """
        self.change_x += x
        self.change_y += y

    def update(self, walls, gate):
        """
        팩맨의 위치를 업데이트
        - 벽이나 게이트와 충돌할 경우 이동 취소
        Args:
            walls (pygame.sprite.Group): 벽 스프라이트 그룹
            gate (pygame.sprite.Group): 게이트 스프라이트 그룹
        """
        # 이동 전 위치 저장
        old_x, old_y = self.rect.left, self.rect.top

        # x 방향으로 이동
        self.rect.left += self.change_x
        if pygame.sprite.spritecollide(self, walls, False):  # 벽과 충돌하면 이동 취소
            self.rect.left = old_x

        # y 방향으로 이동
        self.rect.top += self.change_y
        if pygame.sprite.spritecollide(self, walls, False):  # 벽과 충돌하면 이동 취소
            self.rect.top = old_y

        # 게이트와 충돌할 경우 이동 취소
        if gate and pygame.sprite.spritecollide(self, gate, False):
            self.rect.left, self.rect.top = old_x, old_y

class Ghost(Player):
    """
    유령을 나타내는 클래스
    - Player 클래스를 상속하여 이동 로직 추가
    """
    def changespeed(self, directions, ghost, turn, steps, length):
        """
        유령의 이동 방향과 속도를 변경
        - 지정된 경로에 따라 이동하며, 랜덤 방향 전환
        Args:
            directions (list): 유령의 경로 지시 목록 [(x속도, y속도, 단계 수), ...]
            ghost (str): 유령의 이름
            turn (int): 현재 경로 인덱스
            steps (int): 현재 단계 수
            length (int): 경로 지시 목록의 길이
            
        Returns:
            tuple: (다음 경로 인덱스, 단계 수)
        """
        if steps < directions[turn][2]:  # 현재 경로의 단계 수가 완료되지 않은 경우
            self.change_x, self.change_y = directions[turn][:2]  # 현재 경로의 속도 설정
            steps += 1  # 단계 수 증가
        else:  # 현재 경로 완료 시 다음 경로로 전환
            turn = (turn + 1) if turn < length else (2 if ghost == "clyde" else 0)
            self.change_x, self.change_y = directions[turn][:2]  # 다음 경로의 속도 설정
            steps = 0  # 단계 수 초기화
        return turn, steps
