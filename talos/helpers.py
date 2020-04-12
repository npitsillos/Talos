async def get_kaggle_comps(api, category=None):
    return api.competitions_list(category=category, sort_by="latestDeadline")