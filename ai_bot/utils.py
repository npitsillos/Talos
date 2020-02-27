import gym
import numpy as np

# Default params for all toy envs
EPISODES = 1000
MAX_EPSILON = 0.99
MIN_EPSILON = 0.01
EPSILON = 0.99
MAX_STEPS = 99
DECAY_RATE = 0.005
GAMMA = 0.95
ALPHA = 0.8

SUPPORTED_ENVS = {  "frozenlake":
                        {
                            "name": "FrozenLake-v0",
                            "states": {"S": "start point, safe", "F": "frozen tile, safe", "H": "hole, fall to your doom", "G": "goal"}
                        },
                    "frozenlake8x8":
                        {
                            "name": "FrozenLake8x8-v0",
                            "states": {}
                        },
                }

def get_env_details(env_name, **kwargs):
    ''' Returns dictionary with correct env name
        containing entries for the action and obs_space
    '''
    gym_name = SUPPORTED_ENVS[env_name]["name"]
    env = gym.make(gym_name)
    obs_space = env.observation_space.n
    action_space = env.action_space.n
    del env
    return_dict = SUPPORTED_ENVS[env_name]
    if "8x8" in env_name:
        return_dict[env_name]["states"] = SUPPORTED_ENVS[env_name[:-3]]["states"]
    return_dict["action_space"] = action_space
    return_dict["obs_space"] = obs_space

    return return_dict

def check_supported_envs(env_name):
    return env_name in SUPPORTED_ENVS

class Agent():
    ''' Represent an Agent that is trained on an environment.
        This class is created to maintain a reference to the 
        converged Q-table among other things.
    '''
    def __init__(self, env_name, **kwargs):
        self.env_name = SUPPORTED_ENVS[env_name]["name"]
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
        self.alpha = ALPHA
        self.decay_rate = DECAY_RATE
        self.gamma = GAMMA

    async def train_agent(self):
        env = gym.make(self.env_name)
        rewards = []
        episode = 0
        self.q_table = np.zeros((env.observation_space.n, env.action_space.n))
        epsilon = self.max_epsilon
        for episode in range(self.episodes):
            # Reset environment
            state = env.reset()
            step = 0
            done = False
            total_rewards = 0

            for step in range(self.max_steps):
                # Choose and take action
                if np.random.sample() > epsilon:
                    # Take action from q_table that is action that will give highest discounted reward
                    action = np.argmax(self.q_table[state, :])
                else:
                    action = env.action_space.sample()
                
                new_state, reward, done, info = env.step(action)

                # Update the Q table
                self.q_table[state, action] = self.q_table[state, action] + self.alpha * (reward + self.gamma * np.max(self.q_table[new_state, :]) - self.q_table[state, action])

                total_rewards += reward
                state = new_state

                if done:
                    break
                
            epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon)*np.exp(-self.decay_rate*episode)
            rewards.append(total_rewards)
        print ("Score over time: " +  str(sum(rewards)/EPISODES))
        print(self.q_table)