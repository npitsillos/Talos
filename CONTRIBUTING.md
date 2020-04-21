# How to Contribute

1. Fork repository and clone

2. Create a Discord account and create your own server on Discord

3. Create a bot and invite it to your server by following this [tutorial](https://discordpy.readthedocs.io/en/latest/discord.html)

4. Create a ```.env``` file in the root directory of the repo and add the following line:
    * ```TALOS_TOKEN=YOUR_API_KEY_HERE```

5. Download your Kaggle credentials to enable Kaggle API interaction and add the following lines in the ```.env``` file:
    * ```KAGGLE_USERNAME=YOUR_KAGGLE_USERNAME_HERE```
    * ```KAGGLE_KEY=YOUR_KAGGLE_KEY_HERE```
    
5. Finally if you have Docker installed run ```docker-compose up -f docker-compose.yml -f docker-compose.dev.yml up```

