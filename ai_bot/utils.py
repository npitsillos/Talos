import gym
import numpy as np

# Default params for all toy envs
EPISODES = 1000
MAX_EPSILON = 0.99
MIN_EPSILON = 0.01
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

async def train_on_env(ctx, callback, params):
    ''' Trains a simple agent on the specified environment
        given the specified parameters in *params
    '''
    rewards = []
    episode = 0
    env_name = list(params)[0].lower()
    env = gym.make(SUPPORTED_ENVS[env_name]["name"])
    actions = env.action_space.n
    states = env.observation_space.n

    q_table = np.zeros((states, actions))
    epsilon = MAX_EPSILON
    for episode in range(EPISODES):
        print(episode)
        # Reset environment
        state = env.reset()
        step = 0
        done = False
        total_rewards = 0

        for step in range(MAX_STEPS):
            # Choose and take action
            if np.random.sample() > epsilon:
                # Take action from q_table that is action that will give highest discounted reward
                action = np.argmax(q_table[state, :])
            else:
                action = env.action_space.sample()
            
            new_state, reward, done, info = env.step(action)

            # Update the Q table
            q_table[state, action] = q_table[state, action] + ALPHA * (reward + GAMMA * np.max(q_table[new_state, :]) - q_table[state, action])

            total_rewards += reward
            state = new_state

            if done:
                break
            
        epsilon = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON)*np.exp(-DECAY_RATE*episode)
        rewards.append(total_rewards)
    print ("Score over time: " +  str(sum(rewards)/EPISODES))
    print(q_table)