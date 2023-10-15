#!/usr/bin/env python3

import time
import asyncio
import subprocess

import discord
from rcon.source import rcon


rate = 1.0 # unit: messages
per  = 2.0 # unit: seconds

allowed_roles = ['Moderators', 'Admin', 'Head Rat In Charge']

def checkrole(author):
    # designed to be called when receiving a message.
    # author would be the message.author, and API doc says the following about message.author:
    # "A Member that sent the message. If channel is a private channel or the user has the left the guild, then it is a User instead."
    # a discord.User object does not have roles like a discord.Member does, so we need to make sure we have a Member
    if not isinstance(author, discord.Member):
        return False

    for role in author.roles:
        if role.name in allowed_roles:
            return True
    return False

class PzBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.restartp = None
        self.restart_timers = []
        self.allowance = rate
        self.last_check = time.time()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.content.startswith('!cancelrestart'):
            if checkrole(message.author):
                print(f'cancel restart triggered by {message.author.global_name}')
            else:
                await message.channel.send('You don\'t have permission to run that command')
                return

            if self.restartp is not None and self.restartp.poll() is None:
                self.restartp.terminate()
                await message.channel.send('Sent cancel to restart script.')
            else:
                await message.channel.send('Huh, doesn\'t look like a restart is currently running')

        elif message.content.startswith('!helloworld'):
            async def sendr():
                await message.channel.send('hello world! its 3 seconds later!')

            self.restart_timers.append(client.loop.call_later(3, sendr))

        elif message.content.startswith('!cancelscheduledrestart'):
            if checkrole(message.author):
                print(f'cancel scheduled restart triggered by {message.author.global_name}')
            else:
                await message.channel.send('You don\'t have permission to run that command')
                return

            proc = await asyncio.create_subprocess_exec('pkill', '-fx', '/bin/bash /home/pzserver/cron15minrestart.sh')
            try:
                await asyncio.wait_for(proc.wait(), timeout=1)
            except TimeoutError:
                await message.channel.send('Error: Timed out trying to kill scheduled restart')
                return

            if proc.returncode == 0:
                await message.channel.send('Found and sent kill to a running restart')
            elif proc.returncode == 1:
                await message.channel.send('Didn\'t find a running restart.')
            else:
                await message.channel.send('Error: unknown return code.')

        elif message.content.startswith('!restart'):
            if checkrole(message.author):
                print(f'restart triggered by {message.author.global_name}')
            else:
                await message.channel.send('You don\'t have permission to run that command')
                return

            if self.restartp is not None and self.restartp.poll() is None:
                await message.channel.send('Restart already running')
                return
            self.restartp = subprocess.Popen(['/home/pzserver/15minrestart.sh'])
            await message.channel.send('Restart triggered')

        elif message.content.startswith('!players'):
            print('received players request')
            current = time.time()
            time_passed = current - self.last_check
            self.last_check = current
            self.allowance += time_passed * (rate / per)
            if (self.allowance > rate):
                self.allowance = rate
            if (self.allowance < 1.0):
                print('Hit rate limit, not responding')
                return
            else:
                self.allowance -= 1.0

            response = await rcon('players', host='127.0.0.1', port=27015, passwd='MyRconPassword')
            print(f'got response {response}')
            await message.channel.send(response)

intents = discord.Intents.default()
intents.message_content = True

client = PzBot(intents=intents)
client.run('discord-secret-string-thing-i-forget-what-its-called')
