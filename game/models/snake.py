import pygame
from game.models.direction import Direction
from collections import deque
from game.settings import CELL_SIZE, SNAKE_COLOR

from pygame.math import Vector2


class Snake:
    def __init__(self, start: Vector2) -> None:
        self.body: deque[Vector2] = deque((start,))
        self.move_direction: Direction = Direction.UP

    def move(self) -> None:
        assert self.size > 0, 'attribute "body" can`t be empty'
        self.body.appendleft(self.body[0] + self.move_direction.value)
        self.body.pop()
    
    def control(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.move_direction != Direction.DOWN:
            self.move_direction = Direction.UP
        elif keys[pygame.K_s] and self.move_direction != Direction.UP:
            self.move_direction = Direction.DOWN
        elif keys[pygame.K_a] and self.move_direction != Direction.RIGHT:
            self.move_direction = Direction.LEFT
        elif keys[pygame.K_d] and self.move_direction != Direction.LEFT:
            self.move_direction = Direction.RIGHT
    
    def display(self, screen: pygame.Surface) -> None:
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
        assert self.size > 0, 'attribute "body" can`t be empty'
        self.body.append(self.body[-1])
    
    @property
    def size(self) -> int:
        return len(self.body)

    @property
    def head(self) -> Vector2:
        assert self.size > 0, 'attribute "body" can`t be empty'
        return self.body[0]
