from dataclasses import dataclass


@dataclass
class State:
    danger_straight: float
    danger_right: float
    danger_left: float

    direction_left: float
    direction_right: float
    direction_up: float
    direction_down: float

    food_straight: float
    food_right: float
    food_left: float
    food_down: float
