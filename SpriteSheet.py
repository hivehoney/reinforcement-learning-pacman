import pygame

class SpriteSheet:
    def __init__(self, image_path):
        self.sheet = pygame.image.load(image_path).convert_alpha()

    def get_sprite(self, x, y, width, height):
        """스프라이트 시트에서 개별 이미지를 추출"""
        sprite = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        return sprite
