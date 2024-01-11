from gymnasium.envs.registration import register

from rabbit_foraging.envs.rabbit_foraging_env import RabbitForagingEnv
from rabbit_foraging.envs.rabbit_foraging_model import RabbitForagingModel
from rabbit_foraging.envs.rabbit_foraging_model import RabbitForagingState

register(
    id="rabbit_foraging/RabbitForaging-v0",

    entry_point="rabbit_foraging.envs:RabbitForagingEnv",

    max_episode_steps=100,
)
