import gym

SUPPORTED_ENVS = ["frozenlake", "frozenlake8x8", "taxi"]
INDEX_TO_NAME = {0: "FrozenLake-v0", 1: "FrozenLake8x8-v0", 2: "Taxi-v3"}

def get_env_details(env_name):
    ''' Returns dictionary with correct env name
        containing entries for the action and obs_space
    '''
    gym_name = INDEX_TO_NAME[SUPPORTED_ENVS.index(env_name)]
    env = gym.make(gym_name)
    obs_space = env.observation_space.n
    action_space = env.action_space.n
    del env
    return {gym_name: {"action_space": action_space, "obs_space": obs_space}}