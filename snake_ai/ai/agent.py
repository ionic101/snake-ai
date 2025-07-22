import torch
from models.step_info import StepInfo
from collections import deque
from models.state import State
from models.direction import Direction
import random
from ai.model import *
from utils import Utils
import torch.optim as optim




MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001 # learning rate


class Agent:
    def __init__(self) -> None:
        self.epoch: int = 1
        self.epsilon: float = 1.0  # Начать с большего значения
        self.epsilon_min: float = 0.05
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

    def train(self, step: StepInfo):
        # Один шаг обучения (оставить для совместимости)
        state = Utils.state_to_tensor(step.state)
        next_state = Utils.state_to_tensor(step.next_state)
        with torch.no_grad():
            next_values = self.model(next_state)
            next_pred = torch.max(next_values).item()
            target = step.reward + self.gamma * next_pred * (1 - int(step.done))
        pred = self.model(state)[Utils.direction_to_int(step.action)]
        target_tensor = torch.tensor(target, dtype=torch.float32)
        loss = self.criterion(pred, target_tensor)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def train_batch(self):
        if len(self.memory) < BATCH_SIZE:
            return
        batch = random.sample(self.memory, BATCH_SIZE)
        states = torch.stack([Utils.state_to_tensor(s.state) for s in batch])
        actions = torch.tensor([Utils.direction_to_int(s.action) for s in batch], dtype=torch.long)
        rewards = torch.tensor([s.reward for s in batch], dtype=torch.float32)
        next_states = torch.stack([Utils.state_to_tensor(s.next_state) for s in batch])
        dones = torch.tensor([s.done for s in batch], dtype=torch.float32)

        q_values = self.model(states)
        q_values = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)

        with torch.no_grad():
            next_q_values = self.model(next_states)
            max_next_q_values = torch.max(next_q_values, dim=1)[0]
            targets = rewards + self.gamma * max_next_q_values * (1 - dones)

        loss = self.criterion(q_values, targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def get_action(self, state: State) -> Direction:
        if random.random() <= self.epsilon:
            return Utils.INT_TO_DIRECTION[random.randint(0, 3)]
        else:
            state_tensor = Utils.state_to_tensor(state)
            with torch.no_grad():
                q_values = self.model(state_tensor)
            action = torch.argmax(q_values).item()
            return Utils.INT_TO_DIRECTION[int(action)]
