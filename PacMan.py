import pygame
import numpy as np

import Setup
import Sprites
from Const import Config
from GeneticAlgorithm import GeneticAlgorithm
from NeuralNetwork import NeuralNetwork

def start_game():
    """
    팩맨 게임 시작 함수
    - 게임 초기화, 스프라이트 생성 및 유전 알고리즘 학습 실행
    - 수동 또는 자동 모드로 팩맨을 조작
    """
    # pygame 초기화 및 화면 설정
    pygame.init()
    screen = pygame.display.set_mode([606, 606])  # 게임 화면 크기 설정
    pygame.display.set_caption('Pacman')
    background = pygame.Surface(screen.get_size()).convert()
    background.fill(Config.BLACK)
    clock = pygame.time.Clock()  # 게임 루프를 제어하는 시계 객체
    font = pygame.font.Font("freesansbold.ttf", 24)  # 점수 표시를 위한 폰트 설정

    # 스프라이트 그룹 생성
    all_sprites_list = pygame.sprite.RenderPlain()  # 모든 스프라이트 관리 그룹
    block_list = pygame.sprite.RenderPlain()  # 블록(코인) 스프라이트 그룹
    monsta_list = pygame.sprite.RenderPlain()  # 유령 스프라이트 그룹
    pacman_collide = pygame.sprite.RenderPlain()  # 팩맨 충돌 검사용 그룹

    # 방(벽) 및 게이트 생성
    wall_list = Setup.setup_room_one(all_sprites_list)  # 첫 번째 방 생성
    gate = Setup.setup_gate(all_sprites_list)  # 게이트 생성

    # 팩맨 생성 및 초기 위치 설정
    pacman = Sprites.Player(287, 439, "images/pacman.png")  # 팩맨 객체 생성
    all_sprites_list.add(pacman)  # 팩맨을 모든 스프라이트 리스트에 추가
    pacman_collide.add(pacman)  # 충돌 그룹에 팩맨 추가

    # 유령 생성 및 초기 위치 설정
    ghosts = {
        "Blinky": Sprites.Ghost(287, 199, "images/Blinky.png"),
        "Pinky": Sprites.Ghost(287, 199, "images/Pinky.png"),
        "Inky": Sprites.Ghost(287, 199, "images/Inky.png"),
        "Clyde": Sprites.Ghost(287, 199, "images/Clyde.png")
    }
    ghost_group = pygame.sprite.Group()  # 유령 스프라이트 그룹 생성
    for ghost in ghosts.values():
        ghost_group.add(ghost)  # 유령 그룹에 추가

    directions = {  # 유령 이동 경로 설정
        "Pinky": Config.Pinky_directions,
        "Blinky": Config.Blinky_directions,
        "Inky": Config.Inky_directions,
        "Clyde": Config.Clyde_directions
    }
    turns_steps = {ghost: [0, 0] for ghost in ghosts}  # 유령 이동 상태 초기화

    for ghost in ghosts.values():
        monsta_list.add(ghost)  # 유령 그룹에 유령 추가
        all_sprites_list.add(ghost)  # 모든 스프라이트 리스트에 유령 추가

    # 블록(코인) 생성 및 초기화
    for row in range(19):
        for column in range(19):
            if (row, column) in [(7, 8), (7, 9), (7, 10), (8, 8), (8, 9), (8, 10)]:
                continue  # 중앙 영역은 블록 생성 제외
            block = Sprites.Block(Config.YELLOW, 4, 4)
            block.rect.x = (30 * column + 6) + 26  # 블록의 x 좌표 설정
            block.rect.y = (30 * row + 6) + 26  # 블록의 y 좌표 설정
            if not pygame.sprite.spritecollide(block, wall_list, False):  # 벽과 겹치지 않으면 추가
                block_list.add(block)
                all_sprites_list.add(block)

    # 신경망 및 유전 알고리즘 생성
    input_size = 4  # 입력: 팩맨 좌표, 가장 가까운 유령 좌표
    output_size = 4  # 출력: UP, DOWN, LEFT, RIGHT
    network = NeuralNetwork(input_size, output_size)  # 신경망 생성
    ga = GeneticAlgorithm(  # 유전 알고리즘 생성
        population_size=16,
        mutation_rate=0.2,
        generations=10,
        network=network
    )

    # 유전 알고리즘 실행
    best_genes = ga.run(
        wall_list, block_list, pacman, ghost_group, screen, all_sprites_list, gate, font, directions
    )
    print("Best Genes:", best_genes)  # 학습된 최적 유전자 출력

    # 학습된 유전자 저장
    np.save('GA1.npy', np.array(best_genes))
    print("학습된 모델이 'GA.npy' 파일로 저장")

    # 게임 루프 실행
    score = 0
    total_blocks = len(block_list)  # 블록의 총 개수
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 창 종료 이벤트 처리
                done = True

            # 수동 모드일 때 키보드 입력 처리
            if not Config.AUTO_MODE:
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

        # 자동 모드 실행
        if Config.AUTO_MODE:
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

        else:  # 수동 모드에서 팩맨 업데이트
            pacman.update(wall_list, gate)

        # 유령 업데이트
        for ghost_name, ghost in ghosts.items():
            turn, steps = turns_steps[ghost_name]
            length = len(directions[ghost_name]) - 1
            turn, steps = ghost.changespeed(directions[ghost_name], ghost_name, turn, steps, length)
            ghost.update(wall_list, gate)
            turns_steps[ghost_name] = [turn, steps]

        # 팩맨과 블록(코인) 충돌 처리
        blocks_hit_list = pygame.sprite.spritecollide(pacman, block_list, True)
        score += len(blocks_hit_list)  # 점수 갱신

        # 화면 업데이트
        screen.fill(Config.BLACK)
        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        text = font.render(f"Score: {score}/{total_blocks}", True, Config.RED)
        screen.blit(text, [10, 10])
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()  # 게임 종료