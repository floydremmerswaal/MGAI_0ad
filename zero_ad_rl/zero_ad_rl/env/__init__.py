from ray.tune.registry import register_env
from .cav_vs_inf import *

def register_envs():
    register_env('CavalryVsInfantry', lambda c: CavalryVsInfantryEnv(c))
    register_env('CavalryVsSpearmen', lambda c: CavalryVsSpearmenEnv(c))
    register_env('SimpleMinimapCavVsInf', lambda c: SimpleMinimapCavVsInfEnv(c))
    register_env('MinimapCavVsInf', lambda c: MinimapCavVsInfEnv(c))
    register_env('CavalryVsInfantryMaze', lambda c: CavalryVsInfantryMazeEnv(c))
    register_env('CavalryVsInfantryCity', lambda c: CavalryVsInfantryCityEnv(c))

