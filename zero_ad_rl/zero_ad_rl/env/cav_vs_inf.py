from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PIL import Image
import gym
import math
from gym.spaces import Discrete, Box
from .base import AvoidantReward, DefensiveReward, StateBuilder, ActionBuilder, ZeroADEnv
import numpy as np
import zero_ad
from os import path
import shapely.geometry as sg

DISTANCE = 30

def center(units):
    positions = np.array([unit.position() for unit in units])
    return np.mean(positions, axis=0)

def enemy_offset(state):
    player_units = state.units(owner=1)
    enemy_units = state.units(owner=2)
    print("center(enemy_units):", center(enemy_units))
    print("center(player_units):", center(player_units))
    return center(enemy_units) - center(player_units)

def individual_offset(state):
    player_units = state.units(owner=1)
    enemy_units = state.units(owner=2)

    offsets = np.zeros(shape=(5,7))
    for i, player in enumerate(player_units):
        ind_offsets = np.zeros(shape=7)
        for j, enemy in enumerate(enemy_units):
            dist = np.linalg.norm(np.asarray(enemy.position()) - np.asarray(player.position()))
            max_dist = 80
            normalized_dist = dist/max_dist if not np.isnan(dist/max_dist) else 1.
            ind_offsets[j] = min(normalized_dist, 1.)
        offsets[i] = ind_offsets
    return offsets

class EnemyDistance(StateBuilder):
    def __init__(self):
        space = Box(0.0, 1.0, shape=(1, ), dtype=np.float32)
        super().__init__(space)

    def from_json(self, state):
        dist = np.linalg.norm(enemy_offset(state))
        max_dist = 80
        normalized_dist = dist/max_dist if not np.isnan(dist/max_dist) else 1.
        return np.array([min(normalized_dist, 1.)])

class IndividualDistance(StateBuilder):
    def __init__(self):
        space = Box(0.0, 1.0, shape=(5, 7), dtype=np.float32)
        super().__init__(space)

    def from_json(self, state):
        return individual_offset(state)

class AttackRetreat(ActionBuilder):
    def __init__(self, space=Discrete(5)):
        super().__init__(space)

    def to_json(self, action_index, state):
        print("ACTION INDEX:", action_index)
        if action_index == 0:
            return self.retreat(state)
        elif action_index == 1:
            return self.attack(state)
        elif action_index == 2:
            return self.moveClockwise(state)
        elif action_index == 3:
            return self.moveAntiClockwise(state)
        elif action_index == 4:
            return self.attack_lowest(state)
        #else:
        #    return self.move(state, 2 * math.pi * action_index/8)

    def move(self, state, angle, distance=15):
        units = state.units(owner=1)
        center_pt = center(units)

        offset = distance * np.array([math.cos(angle), math.sin(angle)])
        position = list(center_pt + offset)

        return zero_ad.actions.walk(units, *position)

    def moveClockwise(self, state):
        actions = []
        units = state.units(owner=1)
        for unit in units:
            center_pt = center([unit])
            center_pt_enemy = center(state.units(owner=2))
            enemy_to_unit_line = sg.LineString([center_pt_enemy, center_pt])
            right = enemy_to_unit_line.parallel_offset(DISTANCE, 'right')
            new_pos = right.boundary[0]
            actions.append(zero_ad.actions.walk([unit], *np.array(new_pos)))
        return actions
        '''
        units1 = units[:len(units)//2]
        units2 = units[len(units)//2:]

        center_pt = center(units1)
        center_pt_enemy = center(state.units1(owner=2))
        enemy_to_unit_line = sg.LineString([center_pt_enemy, center_pt])
        right = enemy_to_unit_line.parallel_offset(DISTANCE, 'right')
        new_pos = right.boundary[0]

        actions.append(zero_ad.actions.walk(units1, *new_pos))

        center_pt = center(units2)
        center_pt_enemy = center(state.units2(owner=2))
        enemy_to_unit_line = sg.LineString([center_pt_enemy, center_pt])
        right = enemy_to_unit_line.parallel_offset(DISTANCE, 'right')
        new_pos = right.boundary[0]
        
        actions.append(zero_ad.actions.walk(units2, *new_pos))
        return actions
        '''

    def moveAntiClockwise(self, state):
        actions = []
        units = state.units(owner=1)
        for unit in units:
            center_pt = center([unit])
            center_pt_enemy = center(state.units(owner=2))
            enemy_to_unit_line = sg.LineString([center_pt_enemy, center_pt])
            right = enemy_to_unit_line.parallel_offset(DISTANCE, 'left')
            new_pos = right.boundary[1]
            actions.append(zero_ad.actions.walk([unit], *np.array(new_pos)))
        return actions
        '''
        units1 = units[:len(units)//2]
        units2 = units[len(units)//2:]

        center_pt = center(units1)
        center_pt_enemy = center(state.units1(owner=2))
        enemy_to_unit_line = sg.LineString([center_pt_enemy, center_pt])
        right = enemy_to_unit_line.parallel_offset(DISTANCE, 'left')
        new_pos = right.boundary[1]
        actions.append(zero_ad.actions.walk(units1, *new_pos))

        center_pt = center(units2)
        center_pt_enemy = center(state.units2(owner=2))
        enemy_to_unit_line = sg.LineString([center_pt_enemy, center_pt])
        right = enemy_to_unit_line.parallel_offset(DISTANCE, 'left')
        new_pos = right.boundary[1]
        actions.append(zero_ad.actions.walk(units2, *new_pos))

        return actions
        '''
    def retreat(self, state):
        actions = []
        units = state.units(owner=1)
        for unit in units:
            center_pt = center([unit])
            offset = enemy_offset(state)
            rel_position = 20 * (offset / np.linalg.norm(offset, ord=2))
            position = list(center_pt - rel_position)
            actions.append(zero_ad.actions.walk([unit], *position))
        return actions
        '''
        units1 = units[:len(units)//2]
        units2 = units[len(units)//2:]

        center_pt = center(units1)
        offset = enemy_offset(state)
        rel_position = 20 * (offset / np.linalg.norm(offset, ord=2))
        position = list(center_pt - rel_position)
        actions.append(zero_ad.actions.walk(units1, *position))

        center_pt = center(units2)
        offset = enemy_offset(state)
        rel_position = 20 * (offset / np.linalg.norm(offset, ord=2))
        position = list(center_pt - rel_position)
        actions.append(zero_ad.actions.walk(units2, *position))

        return actions
        '''

    def attack(self, state):
        units = state.units(owner=1)
        center_pt = center(units)

        enemy_units = state.units(owner=2)
        enemy_positions = np.array([unit.position() for unit in enemy_units])
        dists = np.linalg.norm(enemy_positions - center_pt, ord=2, axis=1)
        closest_index = np.argmin(dists)
        closest_enemy = enemy_units[closest_index]

        return zero_ad.actions.attack(units, closest_enemy)

    def attack_lowest(self, state):
        units = state.units(owner=1)

        enemy_units = state.units(owner=2)
        enemy_health = np.array([unit.health() for unit in enemy_units])
        closest_index = np.argmin(enemy_health)
        closest_enemy = enemy_units[closest_index]

        return zero_ad.actions.attack(units, closest_enemy)

class CavalryVsInfantryEnv(ZeroADEnv):
    def __init__(self, config):
        #super().__init__(AttackRetreat(), EnemyDistance())
        #super().__init__(AttackRetreat(), IndividualDistance())
        super().__init__(AttackRetreat(), IndividualDistance())
    def scenario_config_file(self):
        return 'CavalryVsInfantry.json'

    @property
    def scenario_config(self):
        configs_dir = path.join(path.dirname(path.realpath(__file__)), 'scenarios')
        filename = self.scenario_config_file()
        config_path = path.join(configs_dir, filename)
        with open(config_path) as f:
            config = f.read()
        return config

class CavalryVsSpearmenEnv(CavalryVsInfantryEnv):
    def scenario_config_file(self):
        return 'CavalryVsSpearmen.json'

class CavalryVsInfantryMazeEnv(CavalryVsInfantryEnv):
    def scenario_config_file(self):
        return 'CavalryVsInfantryMaze.json'

class CavalryVsInfantryCityEnv(CavalryVsInfantryEnv):
    def scenario_config_file(self):
        return 'CavalryVsInfantryCity.json'

class Minimap(StateBuilder):
    def __init__(self):
        space = Box(0.0, 1.0, shape=(84, 84, 3), dtype=np.float32)
        super().__init__(space)

    def from_json(self, state):
        obs = np.zeros((84, 84, 3))
        my_units = state.units(owner=1)
        center_pt = center(my_units)
        if len(my_units) > 0:
            min_x = center_pt[0] - 42
            max_x = center_pt[0] + 42
            min_z = center_pt[1] - 42
            max_z = center_pt[1] + 42
            for unit in state.units():
                pos = unit.position()
                if min_x < pos[0] < max_x and min_z < pos[1] < max_z:
                    x = int(pos[0] - min_x)
                    z = int(pos[1] - min_z)
                    obs[x][z][int(unit.owner())] = 1.

        return obs

    def to_image(self, state):
        arry = 255*self.from_json(state)
        return Image.fromarray(arry.astype(np.uint8))

class SimpleMinimapCavVsInfEnv(ZeroADEnv):
    def __init__(self, config):
        super().__init__(AttackRetreat(), Minimap())

class AttackAndMove(AttackRetreat):
    def __init__(self):
        space = Discrete(9)
        super().__init__(space)

    def to_json(self, action_index, state):
        if action_index == 8:
            return self.attack(state)
        else:
            return self.move(state, 2 * math.pi * action_index/8)

    def move(self, state, angle, distance=15):
        units = state.units(owner=1)
        center_pt = center(units)

        offset = distance * np.array([math.cos(angle), math.sin(angle)])
        position = list(center_pt + offset)

        return zero_ad.actions.walk(units, *position)


class MinimapCavVsInfEnv(ZeroADEnv):
    def __init__(self, config):
        super().__init__(AttackAndMove(), Minimap())
        self.level = config.get('level', 1)
        self.caution_factor = 10

    def on_train_result(self, mean_reward):
        max_reward = self.max_reward()
        min_reward = self.min_reward()
        percent_to_advance = 0.85
        reward_to_advance = min_reward + percent_to_advance * (max_reward - min_reward)
        if mean_reward > reward_to_advance:
            self.level += 1
            print('advancing to level', self.level)
            if self.level > 5:
                self.caution_factor = 5

    def scenario_config_file(self):
        if self.level < 7:
            return 'CavalryVsInfantryL' + str(self.level)+ '.json'
        else:
            return 'CavalryVsInfantry.json'

    def player_unit_health(self, state, owner=1):
        return sum(( unit.health(True) for unit in state.units(owner=owner)))

    def reward(self, prev_state, state):
        return self.damage_diff(prev_state, state) - 0.0001

    def max_reward(self):
        enemy_units = min(self.level, 7)
        return enemy_units

    def min_reward(self):
        player_units = 5
        return -self.caution_factor * player_units

    def damage_diff(self, prev_state, state):
        prev_enemy_health = self.player_unit_health(prev_state, 2)
        enemy_health = self.player_unit_health(state, 2)
        enemy_damage = prev_enemy_health - enemy_health
        assert enemy_damage >= 0, f'Enemy damage is negative: {enemy_damage}'

        prev_player_health = self.player_unit_health(prev_state)
        player_health = self.player_unit_health(state)
        player_damage = prev_player_health - player_health
        assert player_damage >= 0, f'Player damage is negative: {player_damage}'
        return enemy_damage - self.caution_factor * player_damage

    def episode_complete_stats(self, state):
        stats = super().episode_complete_stats(state)
        stats['reward_ratio'] = (self.cum_reward - self.min_reward())/(self.max_reward() - self.min_reward())

        if stats['reward_ratio'] > 1:
            print('---------- Reward is above max expected value -----------')
            print(self.cum_reward, 'vs', self.max_reward())
            prev_enemy_health = self.player_unit_health(state, 2)
            print('enemy health:', prev_enemy_health)

        stats['level'] = self.level
        return stats
