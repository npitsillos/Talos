import gym

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

def get_env_details(env_name):
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