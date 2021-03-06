from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PIL import Image
import gym
import zero_ad

class StateBuilder():
    def __init__(self, space):
        self.space = space

    def from_json(self, state):
        pass

    def to_image(self, state):
        arry = self.from_json(state)
        return Image.fromarray(arry)

class ActionBuilder():
    def __init__(self, space):
        self.space = space

    def to_json(self, action, state):
        pass

    def to_image(self, action):
        pass

def get_player_state(state, index):
    return state.data['players'][index]['state']

class RewardBuilder():
    def __call__(self, prev_state, state):
        pass

    def reset(self, initial_state):
        pass

class WinLoseReward(RewardBuilder):
    def __call__(self, prev_state, state):
        if get_player_state(state, 1) == 'defeated':
            return -1
        elif get_player_state(state, 2) == 'defeated':
            return 1
        else:
            return 0

#TODO: tune rewards
class HealthDeathReward(RewardBuilder):
    def __call__(self, prev_state, state):
        if get_player_state(state, 1) == 'defeated':
            return -30
        elif get_player_state(state, 2) == 'defeated':
            return 30
        else:
            # Each dead enemy is a positive reward of x
            x = 1
            reward = x * (len(prev_state.units(2)) - len(state.units(2)))
            # Each dead ally is a negative reward of y
            y = 1
            reward -= y * (len(prev_state.units(1)) - len(state.units(1)))

            # Each percentage of missing enemy health increases the reward by c1 * percentage
            c1 = 1
            prev_enemy_health = 0
            for enemy in prev_state.units(2):
                prev_enemy_health += enemy.health()

            cur_enemy_health = 0
            for enemy in state.units(2):
                cur_enemy_health += enemy.health()

            reward += c1 * ((prev_enemy_health-cur_enemy_health)/prev_enemy_health)
            
            # Each percentage of missing ally health decreases the reward by c2 * percentage
            c2 = .3
            prev_ally_health = 0
            for ally in prev_state.units(1):
                prev_ally_health += ally.health()

            cur_ally_health = 0
            for ally in state.units(1):
                cur_ally_health += ally.health()

            reward -= c2 * ((prev_ally_health-cur_ally_health)/prev_ally_health)

            return reward

# No direct reward for dealing damage
class DefensiveReward(RewardBuilder):
    def __call__(self, prev_state, state):
        if get_player_state(state, 1) == 'defeated':
            return -30
        elif get_player_state(state, 2) == 'defeated':
            return 30
        else:
            # Each dead enemy is a positive reward of x
            x = 1
            reward = x * (len(prev_state.units(2)) - len(state.units(2)))
            # Each dead ally is a negative reward of y
            y = 1
            reward -= y * (len(prev_state.units(1)) - len(state.units(1)))

            # Each percentage of missing ally health decreases the reward by c2 * percentage
            c2 = .1
            prev_ally_health = 0
            for ally in prev_state.units(1):
                prev_ally_health += ally.health()

            cur_ally_health = 0
            for ally in state.units(1):
                cur_ally_health += ally.health()

            reward -= c2 * ((prev_ally_health-cur_ally_health)/prev_ally_health)

            return reward

# No direct reward for dealing damage and killing enemies
class AvoidantReward(RewardBuilder):
    def __call__(self, prev_state, state):
        if get_player_state(state, 1) == 'defeated':
            return -30
        elif get_player_state(state, 2) == 'defeated':
            return 30
        else:
            reward = 0
            # Each dead ally is a negative reward of y
            y = 1
            reward -= y * (len(prev_state.units(1)) - len(state.units(1)))
            
            # Each percentage of missing ally health decreases the reward by c2 * percentage
            c2 = .1
            prev_ally_health = 0
            for ally in prev_state.units(1):
                prev_ally_health += ally.health()

            cur_ally_health = 0
            for ally in state.units(1):
                cur_ally_health += ally.health()

            reward -= c2 * ((prev_ally_health-cur_ally_health)/prev_ally_health)

            return reward

class ZeroADEnv(gym.Env):
    def __init__(self, action_builder, state_builder, reward_builder=HealthDeathReward(), step_count=8):
        self.actions = action_builder
        self.states = state_builder
        self.reward = reward_builder
        self.action_space = self.actions.space
        self.observation_space = self.states.space
        self.step_count = step_count
        self.game = zero_ad.ZeroAD(self.address)
        self.prev_state = None
        self.state = None
        self.cum_reward = 0

    @property
    def address(self):
        return 'http://127.0.0.1:6000'

    @property
    def scenario_config(self):
        pass

    def reset(self):
        self.prev_state = self.game.reset(self.scenario_config)
        
        self.reward.reset(self.prev_state)
        self.state = self.game.step([zero_ad.actions.reveal_map()])
        return self.observation(self.state)

    def step(self, action_index):
        action = self.actions.to_json(action_index, self.state)
        self.prev_state = self.state
        if isinstance(action,list):
            self.state = self.game.step(action)
        else:
            self.state = self.game.step([action])
        for _ in range(self.step_count - 1):
            self.state = self.game.step()

        player_states = [player['state'] for player in self.state.data['players']]
        players_finished = [state != 'active' for state in player_states]
        done = any(players_finished)
        reward = self.reward(self.prev_state, self.state)
        self.cum_reward += reward
        if done:
            stats = self.episode_complete_stats(self.state)
            stats_str = ' '
            for (k, v) in stats.items():
                stats_str += k + ': ' + str(v) + '; '

            print(f'episode complete.{stats_str}')
            self.cum_reward = 0

        return self.observation(self.state), reward, done, {}

    def episode_complete_stats(self, state):
        stats = {}
        stats['reward'] = self.cum_reward
        stats['win'] = get_player_state(state, 2) == 'defeated'
        return stats

    def observation(self, state):
        return self.states.from_json(state)


BaseZeroADEnv = ZeroADEnv
