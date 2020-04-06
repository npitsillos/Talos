# Talos

### Github Actions
<p align="center">
    ![](https://github.com/npitsillos/Talos/.github/workflows/Greetings/badge.svg)
    ![](https://github.com/npitsillos/Talos/.github/workflows/Talos%20Package/badge.svg)
    ![](https://github.com/npitsillos/Talos/.github/workflows/PR%20Labeler/badge.svg)
</p>

> A discord.py bot to help learn and play with the basics of AI with a focus on DL and RL.  It uses the Open AI [gym](https://github.com/openai/gym) library to implement several toy examples of RL and hopefully DL & DRL.

## Usage
The bot runs when a command is issued that is prefixed with an exclamation mark (!).

### General Commands
```!help``` Displays all the supported commands.

```!contribute``` Returns the link to Talos's Github repository.

### Env Command Group
```!env ls``` Returns a list with the supported gym environments.

```!env describe <env-name>``` Describes the environment providing details about the action and observation space.

```!env train <env-name> [params]``` Trains a basic agent with default or provided params on the specified environment.

```!env test``` Tests the trained agent for several episodes in its environment.

```!env delete``` Deletes trained agent corresponding to channel.

### Vision Command Group
```!vision ls``` Returns a list of supported object detection models.

```!vision create <model-name>``` Creates an instance of the specified vision model.

```!vision run``` Carries out prediction on attached image.

```!vision delete``` Deletes instance of vision model corresponding to channel.

## Contributors
* [npitsillos](https://github.com/npitsillos)

### Please feel free to contribute
<p>
  <a href="http://makeapullrequest.com">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg">
  </a>
</p>