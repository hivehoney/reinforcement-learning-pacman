import pygame

import Setup
import Sprites
from Const import Config
from GeneticAlgorithm import GeneticAlgorithm

def start_game():
    pygame.init()
    screen = pygame.display.set_mode([606, 606])
    pygame.display.set_caption('Pacman')
    background = pygame.Surface(screen.get_size()).convert()
    background.fill(Config.BLACK)
    clock = pygame.time.Clock()
    font = pygame.font.Font("freesansbold.ttf", 24)

    all_sprites_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()
    monsta_list = pygame.sprite.RenderPlain()
    pacman_collide = pygame.sprite.RenderPlain()

    wall_list = Setup.setup_room_one(all_sprites_list)
    gate = Setup.setup_gate(all_sprites_list)

    pacman = Sprites.Player(287, 439, "images/pacman.png")
    all_sprites_list.add(pacman)
    pacman_collide.add(pacman)

    ghosts = {
        "Blinky": Sprites.Ghost(287, 199, "images/Blinky.png"),
        "Pinky": Sprites.Ghost(287, 199, "images/Pinky.png"),
        "Inky": Sprites.Ghost(287, 199, "images/Inky.png"),
        "Clyde": Sprites.Ghost(287, 199, "images/Clyde.png")
    }

    # pygame.sprite.Group으로 유령 추가
    ghost_group = pygame.sprite.Group()

    for ghost in ghosts.values():
        ghost_group.add(ghost)

    directions = {
        "Pinky": Config.Pinky_directions,
        "Blinky": Config.Blinky_directions,
        "Inky": Config.Inky_directions,
        "Clyde": Config.Clyde_directions
    }

    turns_steps = {
        ghost: [0, 0] for ghost in ghosts
    }

    for ghost in ghosts.values():
        monsta_list.add(ghost)
        all_sprites_list.add(ghost)

    for row in range(19):
        for column in range(19):
            if (row, column) in [(7, 8), (7, 9), (7, 10), (8, 8), (8, 9), (8, 10)]:
                continue
            block = Sprites.Block(Config.YELLOW, 4, 4)
            block.rect.x = (30 * column + 6) + 26
            block.rect.y = (30 * row + 6) + 26

            if not pygame.sprite.spritecollide(block, wall_list, False):
                block_list.add(block)
                all_sprites_list.add(block)

    # 유전 알고리즘 실행
    ga = GeneticAlgorithm(population_size=16, gene_length=100, mutation_rate=0.2, generations=3)
    best_genes = ga.run(
        wall_list,
        block_list,
        pacman,
        ghost_group,  # 유령 그룹 전달
        screen,
        all_sprites_list,
        gate,
        font,
        directions
    )

    print("Best Genes:", best_genes)

    score = 0
    total_blocks = len(block_list)
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if not Config.AUTO_MODE:  # 수동 모드일 때만 키보드 입력 처리
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pacman.changespeed(-30, 0)
                    if event.key == pygame.K_RIGHT:
                        pacman.changespeed(30, 0)
                    if event.key == pygame.K_UP:
                        pacman.changespeed(0, -30)
                    if event.key == pygame.K_DOWN:
                        pacman.changespeed(0, 30)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        pacman.changespeed(30, 0)
                    if event.key == pygame.K_RIGHT:
                        pacman.changespeed(-30, 0)
                    if event.key == pygame.K_UP:
                        pacman.changespeed(0, 30)
                    if event.key == pygame.K_DOWN:
                        pacman.changespeed(0, -30)

    if Config.AUTO_MODE:  # 자동 모드일 때 유전 알고리즘 결과 사용
        for move in best_genes:
            if move == 'UP':
                pacman.changespeed(0, -30)
            elif move == 'DOWN':
                pacman.changespeed(0, 30)
            elif move == 'LEFT':
                pacman.changespeed(-30, 0)
            elif move == 'RIGHT':
                pacman.changespeed(30, 0)

            pacman.update(wall_list, gate)

    else:  # 수동 모드일 때 팩맨 업데이트
        pacman.update(wall_list, gate)

    # 유령 업데이트 (공통)
    for ghost_name, ghost in ghosts.items():
        turn, steps = turns_steps[ghost_name]
        length = len(directions[ghost_name]) - 1
        turn, steps = ghost.changespeed(directions[ghost_name], ghost_name, turn, steps, length)
        ghost.update(wall_list, gate)
        turns_steps[ghost_name] = [turn, steps]

    pacman.update(wall_list, gate)
    blocks_hit_list = pygame.sprite.spritecollide(pacman, block_list, True)
    score += len(blocks_hit_list)

    screen.fill(Config.BLACK)
    wall_list.draw(screen)
    gate.draw(screen)
    all_sprites_list.draw(screen)

    text = font.render(f"Score: {score}/{total_blocks}", True, Config.RED)
    screen.blit(text, [10, 10])

    # if score == total_blocks:
    #     done = True
    #     print("Congratulations!")
    #
    # if pygame.sprite.spritecollide(pacman, monsta_list, False):
    #     done = True
    #     print("Game Over!")

    pygame.display.flip()
    clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    start_game()