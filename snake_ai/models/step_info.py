from dataclasses import dataclass
from models.state import State


@dataclass
class StepInfo:
    state: State # состояние до действия
    action: int # 0 - прямо, 1 - вправо, 2 - влево
    reward: float # полученная награда после действия
    next_state: State # состояние после действия
    done: bool # умерла ли змейка?
    done: bool # умерла ли змейка?
