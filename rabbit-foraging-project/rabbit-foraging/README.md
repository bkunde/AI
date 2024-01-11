Rabbit Foraging Environment
---------------------------

# Description
This environment is a simple simulation of a rabbit population. The rabbits starts in a burrow. They must go out and search for food and make it back to the burrow. Obstacles such as a river, trees and rocks will be present. The map is randomized each time.

# Action Space
There are five discrete actions available:
0: Move down
1: Move up
2: Move right
3: Move left
4: Eat Food

# Observation Space
An observation is a 2d array of 'int8', and shape = (map_size, map_size). The entries can be a int '0-6', representing the following:
0: An empty space
1: Tree obstacle
2: Rock obstacle
3: Water
4: Food bush
5: Burrow
6: Rabbit (Agent)

# Rewards
-1 per step unless other reward is triggered.
+10 eat food
+10 make it back to burrow
-10 executing "eat food" action illegally
-10 dying (Truncation of episode)

# Starting State
The rabbit burrow starts in a random location each run.

# Episode Termination
The episode ends if the rabbit doesn't make it to the food in 100 steps(truncation)

The episode will truncate after 100 steps. This limit can be overridden with the 'max_episode_steps' parameter to 'gymnasium.make()'.
