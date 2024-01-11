#!/usr/bin/env python3

import gymnasium as gym
import rabbit_foraging
import random
from time import sleep

def agent_function(observation):
    action = random.choice(rabbit_foraging.RabbitForagingModel.ACTIONS(observation))
    #print("current rabbit:", observation.rabbit)
    return action

def main():
    map_size = 10

    #render_mode = "ansi"
    render_mode = "human"

    env = gym.make('rabbit_foraging/RabbitForaging-v0', render_mode=render_mode, map_size=map_size)
    observation, info = env.reset()
    state = rabbit_foraging.RabbitForagingState()
    state.observation = observation

    total_reward = 0
    terminated = truncated = False
    if render_mode == "ansi":
        print("Current state:", env.render())
    while not (terminated or truncated):
        action = agent_function(observation)
        if render_mode == "ansi":
            print()
            print(f"Action: {action}.")
        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        #state.observation = observation
        if render_mode == "ansi":
            print("Current state:", env.render())

    sleep(5)
    print("Reward:", total_reward)
    env.close()
    return

if __name__ == "__main__":
    main()
