from pygame.math import Vector2
from models.state import State
from models.direction import Direction
import torch


class Utils:
    DIRECTION_TO_INT = {
        Direction.UP: 0,
        Direction.DOWN: 1,
        Direction.LEFT: 2,
        Direction.RIGHT: 3
    }
    INT_TO_DIRECTION = {
        0: Direction.UP,
        1: Direction.DOWN,
        2: Direction.LEFT,
        3: Direction.RIGHT
    }

    @staticmethod
    def vector2_to_tuple(value: Vector2) -> tuple[int, int]:
        '''
        Конвертация pygame.math.Vector2 в tuple[int, int]
        (использовать, когда необходимо pygame.math.Vector2 захешировать)
        '''
        return (int(value.x), int(value.y))
    
    @staticmethod
    def state_to_tensor(state: State) -> torch.Tensor:
        features = [
            state.cell_up,
            state.cell_right,
            state.cell_down,
            state.cell_left,
            state.wall_up,
            state.wall_right,
            state.wall_down,
            state.wall_left,
            state.direction_up,
            state.direction_right,
            state.direction_down,
            state.direction_left,
            state.food_up,
            state.food_right,
            state.food_down,
            state.food_left
        ]
        return torch.tensor(features, dtype=torch.float32)
    
    @staticmethod
    def direction_to_int(value: Direction) -> int:
        return Utils.DIRECTION_TO_INT[value]
    
    @staticmethod
    def int_to_direction(value: int) -> Direction:
        return Utils.INT_TO_DIRECTION[value]
