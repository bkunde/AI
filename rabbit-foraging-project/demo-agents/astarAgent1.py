#!/usr/bin/env python3

import gymnasium as gym
import rabbit_foraging
import astar
import random
from time import sleep
import time

def agent_function(observation):
    state = observation
    s0 = astar.Node(0, state, None, None, 0, 0)
    G = astar.astar_search(s0)
    foodState = G
    food_actions = []
    if G == False:
        print("Failed at G")
        return None
    else:
        while (G.getDepth() > 0):
            food_actions.append(G.getAction())
            G = G.getPnode()
        food_actions.reverse()

    home_actions = []
    #return food_actions 
    A = astar.astar_search_home(foodState)
    if A == False:
        print("Failed at A")
        return None
    else:
        while (A.getDepth() > foodState.getDepth()):
            home_actions.append(A.getAction())
            A = A.getPnode()
        home_actions.reverse()
    
    actions = food_actions+home_actions
    return actions

def main():

    map_size = 100

    #render_mode = "ansi"
    #render_mode = "human"
    render_mode = None


    env = gym.make('rabbit_foraging/RabbitForaging-v0', render_mode=render_mode, map_size=map_size)

    total_reward = 0
    episodes = 50
    total_time = 0

    for episode in range(episodes):
        observation, info = env.reset()
        state = rabbit_foraging.RabbitForagingState()
        state.observation = observation
        e_reward =  0
        terminated = truncated = False
        if render_mode == "ansi":
            print("Current state:", env.render())

        start = time.time()
        actions = agent_function(observation)
        end = time.time()
        total_time += (end - start)
        if (actions == None):
            terminated = True
            reward = -100

        while not (terminated or truncated):
            for action in actions:
                if render_mode == "ansi":
                    print()
                    print(f"Action: {action}.")
                observation, reward, terminated, truncated, info = env.step(action)
                e_reward += reward
                #state.observation = observation
                if render_mode == "ansi":
                    print("Current state:", env.render())
        total_reward += e_reward 

    #sleep(2)
    print("Time: ", total_time/episodes)
    print("Reward: ", total_reward/episodes)
    env.close()
    return

if __name__ == "__main__":
    main()
