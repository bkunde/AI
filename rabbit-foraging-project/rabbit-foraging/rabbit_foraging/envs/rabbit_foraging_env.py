#Rabbit Foraging Env v0
#Brevin Kunde
#CS4300
#Utah Tech University

"""Img credit: Bunny created by tebruno99 and hosted on OpenGameArt.org, all other images created by CDmir hosted on OpenGameArt.org"""


import gymnasium
import numpy as np
from os import path
from gymnasium import spaces
from rabbit_foraging.envs.rabbit_foraging_model import RabbitForagingModel
from rabbit_foraging.envs.rabbit_foraging_model import RabbitForagingState

try:
    import pygame
except ImportError as error:
    raise DependencyNotInstalled(
            "pygame is not installed, 'pip install' must have failed."
    ) from error


class RabbitForagingEnv(gymnasium.Env):

    metadata = {
            "render_modes": ["human", "ansi"],
            "render_fps": 3,
    }

    def __init__(self, render_mode=None, map_size=5):
        num_states = map_size*map_size
        num_actions = 5

        self.render_mode = render_mode  
        self.map_size = map_size
        self.action_space = spaces.Discrete(num_actions)
        #self.observation_space = spaces.Box(0, 7, shape=(map_size, map_size,), dtype=int)
        self.observation_space = spaces.Dict(
                {"map": spaces.Box(0, 7, shape=(map_size, map_size,), dtype=np.int8),
                 "rabbit": spaces.Box(low=0, high=map_size-1, shape=(3,), dtype=np.int8),
                 "size": spaces.Discrete(map_size+1)
                })

        WINDOW_SIZE = (550, 350)
        c = 1
        if map_size >= 25:
            c = 2
        # display support
        self.cell_size = (
            (WINDOW_SIZE[0] / map_size)*c,
            (WINDOW_SIZE[1] / map_size)*c,
                
        )
        self.window_size = (
            self.map_size * self.cell_size[0],
            self.map_size * self.cell_size[1],
        )
        self.window_surface = None
        self.clock = None
        self.background_img = None
        self.rabbit_imgs = None
        self.rabbit_orientation = 0
        self.tree_imgs = None
        self.rock_imgs = None
        self.water_img = None
        self.bush_imgs = None
        self.burrow_img = None
        self.eatenbush_imgs = None
        return

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        state = RabbitForagingState(self.map_size)
        state.randomize(seed)
        self.state = state.observation
        self.lastacation = None
        self.taxi_orientation = 0

        observation = self.state
        info = {}
        return observation, info

    def step(self, action):
        state = self.state
        state1 = RabbitForagingModel.RESULT(state, action)
        self.pstate = state
        self.state = state1
        self.lastaction = action

        reward = 0
        reward -= RabbitForagingModel.STEP_COST(state, action, state1)
        success = RabbitForagingModel.GOAL_TEST(state1)

        observation = self.state

        terminated = False
        truncated = False
        if success:
            reward += 100
            terminated = True
        info = {}

        # display support
        if self.render_mode == "human":
            self.render()
        return observation, reward, terminated, truncated, info

    def render(self):
        if self.render_mode is None:
            assert self.spec is not None
            gym.logger.warn(
                    "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
            )
            return

        if self.render_mode == "ansi":
            return self._render_text()
        else:
            return self._render_gui(self.render_mode)

    def _render_text(self):
        return str(self.state)

    def _render_gui(self, mode):
        if self.window_surface is None:
            pygame.init()

            if mode == "human":
                pygame.display.init()
                pygame.display.set_caption("Rabbit Foraging")
                self.window_surface = pygame.display.set_mode(self.window_size)
            else:
                self.window_surface = pygame.Surface(self.window_size)
        if self.clock is None:
            self.clock = pygame.time.Clock()
        
        rect = pygame.Rect((0,0), self.window_size)
        #background
        if self.background_img is None:
            file_name = path.join(path.dirname(__file__), "imgs/grass.png")
            self.background_img = pygame.transform.scale(
                    pygame.image.load(file_name), self.cell_size
            )

        for y in range(self.state["size"]):
            for x in range(self.state["size"]):
                cell = (x * self.cell_size[0], y * self.cell_size[1])
                self.window_surface.blit(self.background_img, cell)

        trees = []
        rocks = []
        river = []
        bushes = []
        burrows = []
        eatenbushes = []
        r = c = 0
        #print()
        #print(self.state.map)
        #print()
        for row in self.state["map"]:
            c = 0
            for col in row:
                if col == 1:
                    trees.append((r,c))
                elif col == 2:
                    rocks.append((r,c))
                elif col == 3:
                    river.append((r,c))
                elif col == 4:
                    bushes.append((r,c))
                elif col == 5:
                    burrows.append((r,c))
                elif col == 7:
                    eatenbushes.append((r,c))
                c += 1
            r += 1

        #trees
        if self.tree_imgs is None:
            file_names = [path.join(path.dirname(__file__), "imgs/tree1.png"),
            ]
            self.tree_imgs = [
                    pygame.transform.scale(pygame.image.load(file_name), self.cell_size) for file_name in file_names
            ]
        for tree in trees:
            x = tree[0]*self.cell_size[0]
            y = tree[1]*self.cell_size[1]
            self.window_surface.blit(self.tree_imgs[0], (x,y))

        #rocks
        if self.rock_imgs is None:
            file_names = [path.join(path.dirname(__file__), "imgs/rock.png"),
            ]
            self.rock_imgs = [
                    pygame.transform.scale(pygame.image.load(file_name), self.cell_size) for file_name in file_names
            ]
        for rock in rocks:
            x = rock[0]*self.cell_size[0]
            y = rock[1]*self.cell_size[1]
            self.window_surface.blit(self.rock_imgs[0], (x,y))
        #water
        if self.water_img is None:
            file_name = path.join(path.dirname(__file__), "imgs/water.png")
            self.water_img = pygame.transform.scale(pygame.image.load(file_name), self.cell_size)
        for water in river:
            x = water[0]*self.cell_size[0]
            y = water[1]*self.cell_size[1]
            self.window_surface.blit(self.water_img, (x,y))
        #food bush
        if self.bush_imgs is None:
            file_names = [path.join(path.dirname(__file__), "imgs/berrybush.png"),
            ]
            self.bush_imgs = [
                    pygame.transform.scale(pygame.image.load(file_name), self.cell_size) for file_name in file_names
            ]
        for bush in bushes:
            x = bush[0]*self.cell_size[0]
            y = bush[1]*self.cell_size[1]
            self.window_surface.blit(self.bush_imgs[0], (x,y))
        #burrow
        if self.burrow_img is None:
            file_name = path.join(path.dirname(__file__), "imgs/burrow.png")
            self.burrow_img = pygame.transform.scale(pygame.image.load(file_name), self.cell_size)
        for burrow in burrows:
            x = burrow[0]*self.cell_size[0]
            y = burrow[1]*self.cell_size[1]
            self.window_surface.blit(self.burrow_img, (x,y))

        #eaten bush
        if self.eatenbush_imgs is None:
            file_names = [path.join(path.dirname(__file__), "imgs/eatenbush.png"),
            ]
            self.eatenbush_imgs = [
                    pygame.transform.scale(pygame.image.load(file_name), self.cell_size) for file_name in file_names
            ]
        for eatenbush in eatenbushes:
            x = eatenbush[0]*self.cell_size[0]
            y = eatenbush[1]*self.cell_size[1]
            self.window_surface.blit(self.eatenbush_imgs[0], (x,y))
        #rabbit
        if self.rabbit_imgs is None:
            file_names = [
                    path.join(path.dirname(__file__), "imgs/bunny1.png"),
                    path.join(path.dirname(__file__), "imgs/bunny2.png"),
                    path.join(path.dirname(__file__), "imgs/bunny3.png"),
                    path.join(path.dirname(__file__), "imgs/bunny4.png"),
            ]
            self.rabbit_imgs = [
                    pygame.transform.scale(pygame.image.load(file_name), self.cell_size) for file_name in file_names
            ]

        x = (self.state["rabbit"][0])*self.cell_size[0]
        y = (self.state["rabbit"][1])*self.cell_size[1]
        if self.lastaction in [0,1,2,3]:
            i = self.whichway()
        else:
            i = 1
        self.window_surface.blit(self.rabbit_imgs[i], (x,y))
        if mode == "human":
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else: 
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.window_surface)), axes(1,0, 2)
            )

    def whichway(self):
        direction = 1
        if (self.lastaction == 0):
            self.state["rabbit"][0] == self.pstate["rabbit"][0]+1
            direction = 3
        if (self.lastaction == 1):
            self.state["rabbit"][0] == self.pstate["rabbit"][0]-1
            direction = 2
        if (self.lastaction == 2):
            self.state["rabbit"][1] == self.pstate["rabbit"][1]+1
            direction = 1
        if (self.lastaction == 3):
            self.state["rabbit"][1] == self.pstate["rabbit"][1]-1
            direction = 0
        return direction


    def close(self):
        if self.window_surface is not None:
            pygame.display.quit()
            pygame.quit()
        return

