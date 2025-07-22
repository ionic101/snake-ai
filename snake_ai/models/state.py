from dataclasses import dataclass


@dataclass
class State:
    cell_up: float
    cell_right: float
    cell_down: float
    cell_left: float

    wall_up: float
    wall_right: float
    wall_down: float
    wall_left: float

    direction_up: float
    direction_right: float
    direction_down: float
    direction_left: float

    food_up: float
    food_right: float
    food_down: float
    food_left: float