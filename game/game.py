import pygame
from pygame.math import Vector2

from game.settings import *
from game.models.snake import Snake
import random


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.snake = Snake(
            start=Vector2(COUNT_CELLS_WIDTH // 2, COUNT_CELLS_WIDTH // 2)
        )
        self.is_run: bool = True
        self.font: pygame.font.Font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.last_dt: int = pygame.time.get_ticks()
        self.spawn_apple()
        self.update_screen()
    
    @property
    def score(self) -> int:
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
    
    def listen_events(self) -> None:
        '''
        Прослушивание событий pygame
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_run = False
    
    def spawn_apple(self) -> None:
        '''
        Генерация яблока на карте
        '''
        occupied_cells: set[tuple[int, int]] = set(map(lambda cell: (int(cell.x), int(cell.y)), self.snake.body))
        empty_cells: list[Vector2] = [
            Vector2(x, y)
            for x in range(COUNT_CELLS_WIDTH)
            for y in range(COUNT_CELLS_HEIGHT)
            if (x, y) not in occupied_cells
        ]
        self.apple = random.choice(empty_cells)
    
    def stop(self) -> None:
        self.is_run = False
    
    def check_collision(self) -> None:
        new_cell = self.snake.move_direction.value + self.snake.head
        for cell in self.snake.body:
            if new_cell == cell:
                self.stop()
                return
        if new_cell.x < 0 or new_cell.x >= COUNT_CELLS_WIDTH or new_cell.y < 0 or new_cell.y >= COUNT_CELLS_HEIGHT:
            self.stop()
            return

    def is_collide(self, cell: Vector2) -> bool:
        if cell.x < 0 or cell.x >= COUNT_CELLS_WIDTH or cell.y < 0 or cell.y >= COUNT_CELLS_HEIGHT:
            return True
        for snake_cell in self.snake.body:
            if cell == snake_cell:
                return True
        return False
    
    def run(self) -> None:
        '''
        Запуск игры
        '''
        while self.is_run:
            self.listen_events()
            self.snake.control()
            dt = pygame.time.get_ticks()
            if dt - self.last_dt >= TICK_DELAY:
                self.last_dt = dt

                if self.is_collide(self.snake.move_direction.value + self.snake.head):
                    self.stop()
                else:
                    self.snake.move()
                
                if self.snake.head == self.apple:
                    self.snake.eat()
                    if self.score < MAX_SCORE:
                        self.spawn_apple()
    
                self.update_screen()
