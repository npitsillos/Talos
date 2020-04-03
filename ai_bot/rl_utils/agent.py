import gym
from rl_utils.helpers import get_string_respresentation_of_env
import numpy as np

##################################
# RL Agent Details
##################################
# Default params for all toy envs
EPISODES = 1000
MAX_EPSILON = 0.99
MIN_EPSILON = 0.01
EPSILON = 0.99
MAX_STEPS = 99
DECAY_RATE = 0.005
GAMMA = 0.95
ALPHA = 0.8

# Agent class
class Agent():
    ''' Represent an Agent that is trained on an environment.
        This class is created to maintain a reference to the 
        converged Q-table among other things.
    '''
    def __init__(self, env_name, **kwargs):
        self.env_name = env_name
        if len(kwargs) == 0:
            self.init_default_agent()
        else:
            for key in kwargs.keys():
                self.__setattr__(self, key, kwargs[key])

    def init_default_agent(self):
        self.episodes = EPISODES
        self.max_epsilon = MAX_EPSILON
        self.min_epsilon = MIN_EPSILON
        self.max_steps = MAX_STEPS
        self.max_test_steps = 20
        self.alpha = ALPHA
        self.decay_rate = DECAY_RATE
        self.gamma = GAMMA

    async def train(self):
        env = gym.make(self.env_name)
        self.env = env
        rewards = []
        episode = 0
        self.q_table = np.zeros((env.observation_space.n, env.action_space.n))
        epsilon = self.max_epsilon
        for episode in range(self.episodes):
            # Reset environment
            state = env.reset()
            done = False
            total_rewards = 0
            step = 0
            while step < self.max_steps:
                # Choose and take action
                if np.random.sample() > epsilon:
                    # Take action from q_table that is action that will give highest discounted reward
                    action = np.argmax(self.q_table[state, :])
                else:
                    action = env.action_space.sample()
                
                new_state, reward, done, _ = env.step(action)

                # Update the Q table
                self.q_table[state, action] = self.q_table[state, action] + self.alpha * (reward + self.gamma * np.max(self.q_table[new_state, :]) - self.q_table[state, action])

                total_rewards += reward
                state = new_state

                if done:
                    break
                step += 1
            epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon)*np.exp(-self.decay_rate*episode)
            rewards.append(total_rewards)
        return {"num_eps": self.episodes, "q_table": self.q_table, "avg_score": sum(rewards) / self.episodes}
        
    async def test(self):
        episodes = {}
        for i in range(1):
            state = self.env.reset()
            done = False
            episode_steps = []
            step = 0
            while step < self.max_test_steps:
                
                action = np.argmax(self.q_table[state, :])
                new_state, reward, done, info = self.env.step(action)
                movement, world =  get_string_respresentation_of_env(self.env, actions)
                episode_steps.append({"action": movement, "world": world})
                if done:
                    break

                state = new_state
                step += 1
            episodes["ep_{}".format(i)] = episode_steps
        self.env.close()
        return episodes
