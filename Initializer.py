from Sprites import Player, Ghost, Block
import pygame
from Const import Config

"""
게임 초기화 로직
- 팩맨, 유령, 블록의 초기화는 별도 모듈에서 관리
"""

def initialize_blocks(all_sprites_list, wall_list):
    """
    블록(코인)을 초기화하는 함수
    - 게임 맵에 블록(코인)을 배치하며, 벽과 겹치지 않도록 설정
    - 중앙 영역(팩맨과 유령의 시작 지점)은 블록을 생성하지 않음

    Args:
        all_sprites_list (pygame.sprite.RenderPlain): 모든 스프라이트를 포함하는 그룹
        wall_list (pygame.sprite.RenderPlain): 벽 스프라이트 그룹

    Returns:
        pygame.sprite.RenderPlain: 생성된 블록(코인) 스프라이트 그룹
    """
    # 블록(코인)을 저장할 그룹 생성
    block_list = pygame.sprite.RenderPlain()

    for row in range(19):
        for column in range(19):
            # 중앙 영역은 블록 생성 제외 (팩맨 및 유령 초기 위치)
            if (row, column) in [(7, 8), (7, 9), (7, 10), (8, 8), (8, 9), (8, 10)]:
                continue

            # 새로운 블록 생성
            block = Block(Config.YELLOW, 4, 4)

            # 블록의 화면 위치 계산
            block.rect.x = (30 * column + 6) + 26
            block.rect.y = (30 * row + 6) + 26

            # 벽과 충돌하지 않을 경우 블록 추가
            if not pygame.sprite.spritecollide(block, wall_list, False):
                block_list.add(block)          # 블록 그룹에 추가
                all_sprites_list.add(block)   # 전체 스프라이트에 추가

    return block_list
