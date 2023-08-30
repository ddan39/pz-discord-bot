# pz-discord-bot
discord.py bot for Project Zomboid linux server

i'm using this with linuxgsm at the moment (not a big fan of it though to be honest, so don't take this as a recomendation lol), but i think this will all work fine with anything else, as long as you have a script you run to kick off a timed restart.

the rcon program used in my 15minrestart.sh script is from https://github.com/gorcon/rcon-cli . i just downloaded a compiled release (e.g. https://github.com/gorcon/rcon-cli/releases/download/v0.10.3/rcon-0.10.3-amd64_linux.tar.gz ) and used that. edit rcon.yaml file to set your rcon password and probably delete the log setting like i did

## INSTALL/USE:
* setup discord bot - see https://discordpy.readthedocs.io/en/stable/discord.html
* clone repo
* create/activate a python virtual environment. i used pyvenv
* pip install discord.py rcon
* copy files into venv
* edit pzbot.py to add in your bot code at the bottom. also change the RconPassword which is a few lines up from the bottom. probably want to also edit the allowed_roles variable near top of file for the roles in your discord server that you want to allow to run restart commands
* probably need to edit paths to restart scripts in pzbot.py that i hardcoded since this is just my own use DIY bot. cron15minrestart.sh is a duplicate of 15minrestart.sh that i made so i can kill the specific one run by cron, using pkill.
* run the bot: ./pzbot.py

### TODO
* probably better bot-wide rate limiting. currently only the !players command is rate limited. all the other commands can only be run by specific roles, but i guess the error message could be abused by people since it is not rate limited. i'm not sure if discord has some rate limiting built in already. i bet it does.
* i wanted to implement a vote-for-restart feature where regular users can do a vote to kick off a restart, like if 5 people of the lowest role vote to restart all within 15 minutes it will be done, or 2 people of a specific role do. everyone else thought this would be abused, so i didn't do it.
