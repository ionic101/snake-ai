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
        self.steps_since_apple = 0
    
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
        self.steps_since_apple = 0

    def get_state(self) -> State:
        head = self.snake.head
        direction = self.snake.move_direction

        # Определяем направления
        directions = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = directions.index(direction)
        dir_straight = directions[idx]
        dir_right = directions[(idx + 1) % 4]
        dir_left = directions[(idx - 1) % 4]

        point_straight = head + dir_straight.value
        point_right = head + dir_right.value
        point_left = head + dir_left.value

        def is_danger(point):
            return (
                point.x < 0 or point.x >= COUNT_CELLS_WIDTH or
                point.y < 0 or point.y >= COUNT_CELLS_HEIGHT or
                Utils.vector2_to_tuple(point) in self.snake.occupied_cells
            )

        # Направления
        direction_left = float(direction == Direction.LEFT)
        direction_right = float(direction == Direction.RIGHT)
        direction_up = float(direction == Direction.UP)
        direction_down = float(direction == Direction.DOWN)

        # Еда относительно направления
        apple = self.apple
        food_straight = float(
            (dir_straight == Direction.RIGHT and apple.x > head.x) or
            (dir_straight == Direction.LEFT and apple.x < head.x) or
            (dir_straight == Direction.UP and apple.y < head.y) or
            (dir_straight == Direction.DOWN and apple.y > head.y)
        )
        food_right = float(
            (dir_right == Direction.RIGHT and apple.x > head.x) or
            (dir_right == Direction.LEFT and apple.x < head.x) or
            (dir_right == Direction.UP and apple.y < head.y) or
            (dir_right == Direction.DOWN and apple.y > head.y)
        )
        food_left = float(
            (dir_left == Direction.RIGHT and apple.x > head.x) or
            (dir_left == Direction.LEFT and apple.x < head.x) or
            (dir_left == Direction.UP and apple.y < head.y) or
            (dir_left == Direction.DOWN and apple.y > head.y)
        )
        # Новый признак: еда ниже головы
        food_down = float(apple.y > head.y)

        return State(
            danger_straight=float(is_danger(point_straight)),
            danger_right=float(is_danger(point_right)),
            danger_left=float(is_danger(point_left)),
            direction_left=direction_left,
            direction_right=direction_right,
            direction_up=direction_up,
            direction_down=direction_down,
            food_straight=food_straight,
            food_right=food_right,
            food_left=food_left,
            food_down=food_down
        )

    def step(self, action: int) -> StepInfo:
        old_state = self.get_state()
        self.steps_since_apple += 1

        # Получаем новое направление
        new_direction = Utils.relative_action_to_direction(self.snake.move_direction, action)
        self.snake.move_direction = new_direction

        # Проверяем столкновение
        next_head = self.snake.head + self.snake.move_direction.value
        if (
            next_head.x < 0 or next_head.x >= COUNT_CELLS_WIDTH or
            next_head.y < 0 or next_head.y >= COUNT_CELLS_HEIGHT or
            Utils.vector2_to_tuple(next_head) in self.snake.occupied_cells
        ):
            reward = -100
            done = True
            return StepInfo(
                state=old_state,
                action=action,
                reward=reward,
                next_state=self.get_state(),
                done=done
            )

        self.snake.move()
        reward = -0.1
        done = False

        if self.snake.head == self.apple:
            self.snake.eat()
            reward = 10
            self.steps_since_apple = 0
            if self.score < MAX_SCORE:
                self.spawn_apple()

        # Early stopping: если слишком долго не ест яблоко — завершить эпизод
        if self.steps_since_apple > 100:
            reward = -100
            done = True
            return StepInfo(
                state=old_state,
                action=action,
                reward=reward,
                next_state=self.get_state(),
                done=done
            )

        self.update_screen()
        return StepInfo(
            state=old_state,
            action=action,
            reward=reward,
            next_state=self.get_state(),
            done=done
        )
