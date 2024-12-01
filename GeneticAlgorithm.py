import random
import pygame

import Sprites
from Const import Config

class GeneticAlgorithm:
    def __init__(self, population_size, gene_length, mutation_rate, generations):
        self.population_size = population_size
        self.gene_length = gene_length
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = []

    def initialize_population(self):
        """초기 유전자 생성"""
        self.population = [
            [random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT']) for _ in range(self.gene_length)]
            for _ in range(self.population_size)
        ]

    def reset_game_state(self, pacman, ghost_names, ghost_group, block_list, initial_positions, all_sprites_list):
        """팩맨, 유령, 블록(코인)의 상태를 초기화"""
        # 팩맨 위치 초기화
        pacman.rect.left, pacman.rect.top = initial_positions['pacman']

        # 유령 위치 초기화
        for ghost_name, ghost in zip(ghost_names, ghost_group):
            ghost.rect.left, ghost.rect.top = initial_positions['ghosts'][ghost_name]

        # 블록 초기화
        # 기존 블록 제거
        for block in block_list:
            all_sprites_list.remove(block)  # 렌더링 리스트에서도 제거
        block_list.empty()

        # 초기 블록 위치에서 새 블록 생성
        for block_position in initial_positions['blocks']:
            new_block = Sprites.Block(Config.YELLOW, 4, 4)
            new_block.rect.x, new_block.rect.y = block_position
            block_list.add(new_block)               # 블록 리스트에 추가
            all_sprites_list.add(new_block)         # 렌더링 리스트에 추가

        print(f"Blocks reset: {len(block_list)}")  # 디버깅 로그

    def move_pacman(self, pacman, move):
        """팩맨의 이동을 처리"""
        if move == 'UP':
            pacman.rect.top -= 30
        elif move == 'DOWN':
            pacman.rect.top += 30
        elif move == 'LEFT':
            pacman.rect.left -= 30
        elif move == 'RIGHT':
            pacman.rect.left += 30

    def fitness(self, genes, wall_list, block_list, pacman, ghost_group, directions, turns_steps, screen, all_sprites_list, gate, font):
        initial_positions = {
            'pacman': (287, 439),
            'ghosts': {
                "Blinky": (287, 199),
                "Pinky": (287, 199),
                "Inky": (287, 199),
                "Clyde": (287, 199)
            },
            'blocks': [(block.rect.x, block.rect.y) for block in block_list]
        }

        pacman.rect.left, pacman.rect.top = initial_positions['pacman']
        score, survival_time = 0, 0
        ghost_names = ["Blinky", "Pinky", "Inky", "Clyde"]
        start_time = pygame.time.get_ticks()

        for move in genes:
            old_x, old_y = pacman.rect.left, pacman.rect.top
            self.move_pacman(pacman, move)

            # 벽 충돌 처리
            if pygame.sprite.spritecollide(pacman, wall_list, False):
                pacman.rect.left, pacman.rect.top = old_x, old_y
                score -= 5

            # 유령 충돌 처리
            if pygame.sprite.spritecollide(pacman, ghost_group, False):
                score -= 100
                break

            # 블록(코인) 충돌 처리
            blocks_hit = pygame.sprite.spritecollide(pacman, block_list, True)
            score += len(blocks_hit) * 50

            # 유령 업데이트
            for ghost, ghost_name in zip(ghost_group, ghost_names):
                turn, steps = turns_steps[ghost_name]
                length = len(directions[ghost_name]) - 1
                turn, steps = ghost.changespeed(directions[ghost_name], ghost_name, turn, steps, length)
                ghost.update(wall_list, gate)
                turns_steps[ghost_name] = [turn, steps]

            # 화면 업데이트
            screen.fill(Config.BLACK)
            wall_list.draw(screen)
            gate.draw(screen)
            all_sprites_list.draw(screen)

            survival_time = (pygame.time.get_ticks() - start_time) / 1000
            text = font.render(f"Score: {score} | Time: {survival_time:.2f}", True, Config.RED)
            screen.blit(text, [10, 10])

            pygame.display.flip()
            pygame.time.delay(100)

            if len(block_list) == 0:
                break

        self.reset_game_state(
            pacman, ghost_names, ghost_group, block_list,
            initial_positions, all_sprites_list
        )

        print(f"Survival Time: {survival_time:.2f} seconds, Score: {score}")
        return score + survival_time

    def select_parents(self, fitness_scores):
        """적합도가 높은 부모를 선택"""
        sorted_population = [x for _, x in sorted(zip(fitness_scores, self.population), reverse=True)]
        return sorted_population[:2]

    def crossover(self, parent1, parent2):
        """교배를 통해 자식 유전자를 생성"""
        point = random.randint(1, self.gene_length - 1)
        return (
            parent1[:point] + parent2[point:],
            parent2[:point] + parent1[point:]
        )

    def mutate(self, genes):
        """돌연변이 적용"""
        return [
            random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT']) if random.random() < self.mutation_rate else gene
            for gene in genes
        ]

    def evolve(self, fitness_scores):
        """한 세대 진화"""
        new_population = []
        for _ in range(self.population_size // 2):
            parent1, parent2 = self.select_parents(fitness_scores)
            child1, child2 = self.crossover(parent1, parent2)
            new_population.extend([self.mutate(child1), self.mutate(child2)])
        self.population = new_population

    def run(self, wall_list, block_list, pacman, ghost_group, screen, all_sprites_list, gate, font, directions):
        self.initialize_population()
        ghost_names = ["Blinky", "Pinky", "Inky", "Clyde"]
        turns_steps = {name: [0, 0] for name in ghost_names}

        for generation in range(self.generations):
            print(f"Generation {generation + 1}")

            fitness_scores = [
                self.fitness(genes, wall_list, block_list, pacman, ghost_group, directions,
                             turns_steps, screen, all_sprites_list, gate, font)
                for genes in self.population
            ]

            avg_survival = sum(fitness_scores) / len(fitness_scores)
            print(f"Generation {generation + 1}: Avg Fitness = {avg_survival:.2f}")
            self.evolve(fitness_scores)

        best_genes = max(self.population, key=lambda genes: self.fitness(
            genes, wall_list, block_list, pacman, ghost_group, directions, turns_steps, screen, all_sprites_list, gate, font
        ))
        return best_genes