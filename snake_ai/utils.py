from pygame.math import Vector2
from models.state import State
from models.direction import Direction
import torch


class Utils:
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
            state.danger_straight,
            state.danger_right,
            state.danger_left,
            state.direction_left,
            state.direction_right,
            state.direction_up,
            state.direction_down,
            state.food_straight,
            state.food_right,
            state.food_left
        ]
        return torch.tensor(features, dtype=torch.float32)
    
    @staticmethod
    def relative_action_to_direction(current_direction: Direction, action: int) -> Direction:
        # action: 0 - straight, 1 - right, 2 - left
        directions = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = directions.index(current_direction)
        if action == 0:
            new_idx = idx
        elif action == 1:
            new_idx = (idx + 1) % 4
        else:
            new_idx = (idx - 1) % 4
        return directions[new_idx]
    
    @staticmethod
    def direction_to_int(value: Direction) -> int:
        return Utils.DIRECTION_TO_INT[value]
    
    @staticmethod
    def int_to_direction(value: int) -> Direction:
        return Utils.INT_TO_DIRECTION[value]
        return Utils.INT_TO_DIRECTION[value]
