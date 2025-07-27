import torch
from models.step_info import StepInfo
from collections import deque
from models.state import State
import random
from ai.model import *
from utils import Utils
import torch.optim as optim

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self) -> None:
        self.epoch: int = 1
        self.epsilon: float = 1.0
        self.epsilon_min: float = 0.01
        self.epsilon_decay: float = 0.995
        self.gamma: float = 0.9
        self.memory: deque[StepInfo] = deque(maxlen=MAX_MEMORY)
        self.model: QNet = QNet()
        self.optimizer = optim.Adam(self.model.parameters(), lr=LR)
        self.criterion = torch.nn.MSELoss()
    
    @property
    def last_state(self) -> State:
        assert len(self.memory) > 0, 'memory is empty'
        return self.memory[-1].state

    def remember(self, new_state: StepInfo):
        self.memory.append(new_state)

    def train_short_memory(self, step: StepInfo):
        self._train_step(step)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            batch = random.sample(self.memory, BATCH_SIZE)
        else:
            batch = list(self.memory)
        if not batch:
            return
        for step in batch:
            self._train_step(step)

    def _train_step(self, step: StepInfo):
        state = Utils.state_to_tensor(step.state)
        next_state = Utils.state_to_tensor(step.next_state)
        with torch.no_grad():
            next_values = self.model(next_state)
            next_pred = torch.max(next_values).item()
            target = step.reward + self.gamma * next_pred * (1 - int(step.done))
        pred = self.model(state)[step.action]
        target_tensor = torch.tensor(target, dtype=torch.float32)
        loss = self.criterion(pred, target_tensor)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def get_action(self, state: State) -> int:
        if random.random() <= self.epsilon:
            return random.randint(0, 2)
        else:
            state_tensor = Utils.state_to_tensor(state)
            with torch.no_grad():
                q_values = self.model(state_tensor)
            action = torch.argmax(q_values).item()
            return int(action)
