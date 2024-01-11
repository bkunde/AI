Rabbit Foraging
---------------

Description
This environment is a simple simulation of a rabbit population. The rabbits start in a burrow. They must go out and search for food and make it back to the burrow. Obstacles such as a river, trees and rocks will be present. The map is randomized each time.

Action Space
There are five discrete actions available:
0: Move down
1: Move up
2: Move right
3: Move left
4: Eat Food

Observation Space
The burrow can be located in any open space on the map. 4 food sources will be scatterd around the map. Various obstacles exist on the map and are impassable by the rabbit. A river always runs through the map. 

Rewards
-1 per step unless other reward is triggered.
+10 eat food
+10 make it back to burrow
-10 executing "eat food" action illegally
-10 dying (Truncation of episode)

Starting State
The rabbit burrow starts in a random location each run.

Episode Termination
The episode ends if the rabbit doesn't make it to the food in 100 steps(truncation)

Arguments
