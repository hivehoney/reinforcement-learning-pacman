from Sprites import Player, Ghost, Block
import pygame
from Const import Config

"""
게임 초기화 로직
팩맨, 유령, 블록의 초기화는 별도 모듈
"""
def initialize_blocks(all_sprites_list, wall_list):
    block_list = pygame.sprite.RenderPlain()
    for row in range(19):
        for column in range(19):
            if (row, column) in [(7, 8), (7, 9), (7, 10), (8, 8), (8, 9), (8, 10)]:
                continue
            block = Block(Config.YELLOW, 4, 4)
            block.rect.x = (30 * column + 6) + 26
            block.rect.y = (30 * row + 6) + 26

            if not pygame.sprite.spritecollide(block, wall_list, False):
                block_list.add(block)
                all_sprites_list.add(block)
    return block_list