import gym

SUPPORTED_ENVS = {  "frozenlake":
                        {
                            "name": "FrozenLake-v0",
                            "states": {"S": "start point, safe", "F": "frozen tile, safe", "H": "hole, fall to your doom", "G": "goal"}
                        },
                    "frozenlake8":
                        {
                            "name": "FrozenLake8x8-v0",
                            "states": {}
                        },
                }

def get_supported_envs():
    envs = []
    for key in SUPPORTED_ENVS.keys():
        envs.append(SUPPORTED_ENVS[key]["name"])
    return envs

def is_env_supported(env_name):
    return env_name in SUPPORTED_ENVS

def get_gym_name(env_name):
    return SUPPORTED_ENVS[env_name]["name"]

def get_env_details(env_name):
    ''' Returns dictionary with correct env name
        containing entries for the action and obs_space
    '''
    env = gym.make(SUPPORTED_ENVS[env_name]["name"])
    obs_space = env.observation_space.n
    action_space = env.action_space.n
    del env
    return_dict = SUPPORTED_ENVS[env_name]
    if "8x8" in env_name:
        return_dict[env_name]["states"] = SUPPORTED_ENVS[env_name[:-3]]["states"]
    return_dict["action_space"] = action_space
    return_dict["obs_space"] = obs_space

    return return_dict

def get_string_respresentation_of_env(env):
    row, col = env.s // env.ncol, env.s % env.ncol
    desc = env.desc.tolist()
    desc = [[c.decode('utf-8') for c in line] for line in desc]
    desc[row][col] = '|' + desc[row][col] + '|'
    action = None
    if env.lastaction is not None:
        action = "{}".format(["Left","Down","Right","Up"][env.lastaction])
    world = "\n".join(''.join(line) for line in desc)
    return action, world