"""방과 게이트 생성 로직
setup_room_one와 setup_gate 함수 별도 모듈"""

import pygame
from Sprites import Wall
from Const import Config

def setup_room_one(all_sprites_list):
    MAP_list = pygame.sprite.RenderPlain()

    for wall in Config.MAPS:
        wall_sprite = Wall(*wall, Config.BLUE)
        MAP_list.add(wall_sprite)
        all_sprites_list.add(wall_sprite)

    return MAP_list

def setup_gate(all_sprites_list):
    gate = pygame.sprite.Group()
    gate.add(Wall(282, 242, 42, 2, Config.WHITE))
    all_sprites_list.add(gate)

    return gate
