help_dict = {}

help_dict["general"] = '''
!help [comand-list]
Display the help message for every command

!contribute
Return Github link for Talos
'''

help_dict["env"] = '''
!env ls
Returns a list of supported  gym environments

!env describe <env-name>
Returns a description of the specified environment

!env train <env-name> [params]
Trains the specified environment on default or specified params

!env test
From within agent environment channel, runs the trained agent for several episodes

!env delete
From within agent environment channel, deletes the trained agent (if no other environments then delete category)
'''

help_dict["vision"] = '''
!vision ls
Returns a list of supported vision models

!vision create <model-name>
Creates an instance of the specified vision model

!vision run
From within model created channel attach an image and add the above command as a comment
'''