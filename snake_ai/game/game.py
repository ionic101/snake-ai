import pygame
import random
from pygame.math import Vector2

from models.settings import *
from utils import Utils
from models.snake import Snake
from models.direction import Direction
from models.step_info import StepInfo
from models.state import State


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.is_run: bool = True
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.snake: Snake = Snake(
            start=SNAKE_SPAWN_COORD
        )
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.last_dt: int = pygame.time.get_ticks()
        self.spawn_apple()
        self.update_screen()
    
    @property
    def score(self) -> int:
        '''
        Получение количества текущих очков
        '''
        return self.snake.size
    
    def display_apple(self) -> None:
        '''
        Отображание яблока на экране
        '''
        pygame.draw.rect(self.screen, APPLE_COLOR, pygame.Rect(self.apple.x * CELL_SIZE, self.apple.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    def update_screen(self) -> None:
        '''
        Обновление экрана
        '''
        self.screen.fill(BG_COLOR)
        self.display_apple()
        self.snake.display(self.screen)
        # Отображение очков
        score = self.font.render(f'Score: {self.score}', True, FONT_COLOR)
        self.screen.blit(score, (0, 0))
        pygame.display.flip()
    
    
    def spawn_apple(self) -> None:
        '''
        Генерация яблока на карте
        '''
        empty_cells: list[Vector2] = [
            Vector2(x, y)
            for x in range(COUNT_CELLS_WIDTH)
            for y in range(COUNT_CELLS_HEIGHT)
            if (x, y) not in self.snake.occupied_cells
        ]
        self.apple = random.choice(empty_cells)

    def is_collide(self, cell: Vector2) -> bool:
        '''
        Занята ли клетка чем-то

        True - занята
        False - свободна
        '''
        if cell.x < 0 or cell.x >= COUNT_CELLS_WIDTH or cell.y < 0 or cell.y >= COUNT_CELLS_HEIGHT:
            return True
        for snake_cell in self.snake.body:
            if cell == snake_cell:
                return True
        return False
    
    def restart(self) -> None:
        '''
        Перезапуск игры
        '''
        self.snake = Snake(
            start=SNAKE_SPAWN_COORD
        )
        self.spawn_apple()
        self.update_screen()
    

    def get_state(self) -> State:
        '''
        Получение текущего состояния игры
        '''
        head = self.snake.head
        apple = self.apple
        def cell_occupied(vec):
            return float(Utils.vector2_to_tuple(vec) in self.snake.occupied_cells)
        def wall(vec):
            return float(
                vec.x < 0 or vec.x >= COUNT_CELLS_WIDTH or
                vec.y < 0 or vec.y >= COUNT_CELLS_HEIGHT
            )
        return State(
            cell_up=cell_occupied(head + Direction.UP.value),
            cell_right=cell_occupied(head + Direction.RIGHT.value),
            cell_down=cell_occupied(head + Direction.DOWN.value),
            cell_left=cell_occupied(head + Direction.LEFT.value),

            wall_up=wall(head + Direction.UP.value),
            wall_right=wall(head + Direction.RIGHT.value),
            wall_down=wall(head + Direction.DOWN.value),
            wall_left=wall(head + Direction.LEFT.value),

            direction_up=float(self.snake.move_direction == Direction.UP),
            direction_right=float(self.snake.move_direction == Direction.RIGHT),
            direction_down=float(self.snake.move_direction == Direction.DOWN),
            direction_left=float(self.snake.move_direction == Direction.LEFT),

            food_up=float(apple.y < head.y),
            food_right=float(apple.x > head.x),
            food_down=float(apple.y > head.y),
            food_left=float(apple.x < head.x)
        )
    
    def step(self, action: Direction) -> StepInfo:
        '''
        Сделать шаг игры (вызывать через агента)
        '''
        reward = 0
        old_state = self.get_state()

        opposite_direction = Vector2(-self.snake.move_direction.value.x, -self.snake.move_direction.value.y)
        if action.value != opposite_direction:
            self.snake.move_direction = action

        if self.is_collide(self.snake.move_direction.value + self.snake.head):
            reward -= 100
            return StepInfo(
                state=old_state,
                action=action,
                reward=reward,
                next_state=self.get_state(),
                done=True
            )
        else:
            self.snake.move()

        reward -= 1

        if self.snake.head == self.apple:
            self.snake.eat()
            reward += 100
            if self.score < MAX_SCORE:
                self.spawn_apple()

        self.update_screen()
        return StepInfo(
                state=old_state,
                action=action,
                reward=reward,
                next_state=self.get_state(),
                done=False
            )
