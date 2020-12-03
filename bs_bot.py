#!usr/bin/env python3


import discord
import google_api_custom_search as gcs
import db
import os

gcs = gcs.GoogleCustomSearch()
data = db.Database()
data.createTables()

class MyClient(discord.Client):
        
    async def on_ready(self):
        print('Logged in as', self.user)

    async def on_message(self, message):

        global gcs, data
        # don't respond to ourselves
        if message.author == self.user:
            return
        
        # to respond to the 'hi' from the user
        if str(message.content).lower() == 'hi':
            await message.channel.send('hey')

        # to handle !google search command
        if message.content.startswith('!google'):
            msg = (str(message.content)[8:].strip()).lower()
            data.insertUser(message.author.id, message.author.name)
            data.insertSearchQuery(msg, message.author.id)
            top5 = gcs.parsedTop5(query=msg)
            await message.channel.send(top5)

        # to handle !recent search commmand 
        if message.content.startswith('!recent'):
            msg = (str(message.content)[8:].strip()).lower()
            lst = data.getSearchHistory(message.author.id, msg)
            string = ''
            for item in lst:
                string += item[0] + '\n'
            history = string.strip()
            await message.channel.send(history) 


client = MyClient()
client.run(os.environ['TOKEN'])