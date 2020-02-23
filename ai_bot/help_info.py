help_dict = {}

help_dict["general"] = '''
!help [comand-list]
Display the help message for every command

!envs
Returns a list of supported openai gym environments

!contribute
Return Github link for Talos
'''

help_dict["env"] = '''
!env describe <env-name>
Returns a description of the specified environment.

!env train <env-name> [params]
Trains the specified environment on default or specified params.
'''