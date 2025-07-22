from dataclasses import dataclass
from models.state import State
from models.direction import Direction


@dataclass
class StepInfo:
    state: State # состояние до действия
    action: Direction # выбранное действие
    reward: float # полученная награда после действия
    next_state: State # состояние после действия
    done: bool # умерла ли змейка?
