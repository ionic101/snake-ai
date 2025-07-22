from ai.agent import Agent
from game.game import SnakeGame
import time
import pygame
from stats import update_stats  # добавить импорт


if __name__ == '__main__':
    agent = Agent()
    game = SnakeGame()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        state = agent.last_state if len(agent.memory) > 0 else game.get_state()
        action = agent.get_action(state)
        step_info = game.step(action)
        agent.train(step_info)
        agent.remember(step_info)
        agent.train_batch()  # обучение на батче
        if step_info.done:
            print(f'Epoch: {agent.epoch} Score: {game.score} Epsilon: {agent.epsilon:.3f}')
            update_stats(agent.epoch, game.score)  # обновление графика
            game.restart()
            agent.epoch += 1
            agent.update_epsilon()  # уменьшение epsilon

