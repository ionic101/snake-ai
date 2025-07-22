import pygame
from models.direction import Direction
from collections import deque
from models.settings import CELL_SIZE, SNAKE_COLOR

from pygame.math import Vector2
from utils import Utils


class Snake:
    def __init__(self, start: Vector2) -> None:
        self.body: deque[Vector2] = deque((start,))
        self.occupied_cells: set[tuple[int, int]] = set([Utils.vector2_to_tuple(start)])
        self.move_direction: Direction = Direction.UP
    
    @property
    def size(self) -> int:
        '''
        Получение размера змейки
        '''
        return len(self.body)

    @property
    def head(self) -> Vector2:
        '''
        Получение координат головы змейки
        '''
        assert self.size > 0, 'attribute "body" can`t be empty'
        return self.body[0]

    def move(self) -> None:
        '''
        Движение змейки по направлению
        '''
        assert self.size > 0, 'attribute "body" can`t be empty'
        # Добавление
        head = self.body[0] + self.move_direction.value
        self.body.appendleft(head)
        self.occupied_cells.add(Utils.vector2_to_tuple(head))
        # Удаление
        tail = self.body.pop()
        tail_tuple = Utils.vector2_to_tuple(tail)
        if tail_tuple in self.occupied_cells:
            self.occupied_cells.remove(tail_tuple)
    
    def display(self, screen: pygame.Surface) -> None:
        '''
        Отображение змейки
        '''
        for coord in self.body:
            pygame.draw.rect(
                screen,
                SNAKE_COLOR,
                pygame.Rect(
                    coord.x * CELL_SIZE,
                    coord.y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
            )
    
    def eat(self) -> None:
        '''
        Увеличение длины змейки на 1
        '''
        assert self.size > 0, 'attribute "body" can`t be empty'
        tail = self.body[-1]
        self.body.append(tail)
        self.occupied_cells.add(Utils.vector2_to_tuple(tail))
