import pygame
from Sprites import Wall
from Const import Config

def setup_room_one(all_sprites_list):
    """
    첫 번째 벽 생성 함수
    - 벽의 위치와 크기 정보는 Config.MAPS에 정의되어 있음
    - 벽 스프라이트를 생성하여 스프라이트 그룹에 추가

    Args:
        all_sprites_list (pygame.sprite.RenderPlain): 모든 스프라이트를 포함하는 그룹

    Returns:
        pygame.sprite.RenderPlain: 방(벽) 스프라이트 그룹
    """
    # 벽 스프라이트를 저장할 그룹 생성
    MAP_list = pygame.sprite.RenderPlain()

    for wall in Config.MAPS:
        # Wall 스프라이트 생성 (x, y, width, height, color)
        wall_sprite = Wall(*wall, Config.BLUE)
        MAP_list.add(wall_sprite)  # 그룹에 추가
        all_sprites_list.add(wall_sprite)  # 전체 스프라이트 그룹에 추가

    return MAP_list  # 벽 그룹 반환

def setup_gate(all_sprites_list):
    """
    게이트를 생성하는 함수 - 제외
    - 게이트는 팩맨이 통과하지 못하도록 설정된 특수한 벽
    all_sprites_list (pygame.sprite.RenderPlain): 모든 스프라이트를 포함하는 그룹

    Returns:
        pygame.sprite.Group: 게이트 스프라이트 그룹
    """
    # 게이트 스프라이트 그룹 생성
    gate = pygame.sprite.Group()

    # Wall 클래스를 사용하여 게이트 생성
    gate.add(Wall(282, 242, 42, 2, Config.WHITE))
    all_sprites_list.add(gate)

    return gate
