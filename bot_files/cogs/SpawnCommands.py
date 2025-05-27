import asyncio
import discord
import random
import json
import math
from discord.ext import commands
import numpy as np
import re
import datetime
from io import BytesIO
import time
from pymongo import MongoClient
import os
import asyncio
import string
from PIL import Image
from datetime import timezone
import requests
import io
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageSequence
from datetime import datetime, timedelta


color = 0xff2159

class ConfirmCancel(discord.ui.View):
    def __init__(self, member : discord.Member):
        super().__init__(timeout = 15)

        self.value = None
        self.member = member

    @discord.ui.button(label = "Accept", style = discord.ButtonStyle.green, emoji = "✅" )
    async def confirm_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = True
        self.stop()
                
        for i in self.children:
            i.disabled = True

        await interaction.response.edit_message(view = self)
            
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red, emoji = "❌" )
    async def cancel_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = False
        self.stop()
                
        for i in self.children:
            i.disabled = True
                
        await interaction.response.edit_message(view = self)
        
    async def interaction_check(self, interaction : discord.Interaction):
        return interaction.user == self.member
                                        
    async def on_timeout(self):
        self.value = None

        for i in self.children:
            i.disabled = True

class SpawnCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(name ='world', aliases = ['wld'])
    async def world(self, ctx,number : int = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:

            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

    
            if user_ban_list:
                await ctx.send('You are banned from the bot.')

            else:
                if number == None:
                    title = 'World Map'
                    mapname = 'world.png'

                    mapbase = Image.open(mapname)
                    mapbase = mapbase.resize((2048,2048))


                    spawn_check = await self.bot.db.fetch(f'SELECT * FROM tiles WHERE player_id IS NOT NULL')
                    if spawn_check == []:
                        pass
                    else:
                        for i in spawn_check:
                            pfpid = i['player_id']
                            x = i['x']
                            y = i['y']

                            pfp = Image.open(f'/home/ubuntu/bot_files/database/pfps/{pfpid}.png')

                            pfp = pfp.resize((18,18))

                            mapbase.paste(pfp, (((x-1)*32)+14,((y-1)*32)+14), pfp)



                    banner_embed = discord.Embed(
                        title = title,
                        description = f'',
                        colour = color
                    )

                    bytes = BytesIO()
                    mapbase.save(bytes, format="PNG")
                    bytes.seek(0)

                    banner_embed.set_image(url=f"attachment://mapbase.png")
                    await ctx.send(file = discord.File(bytes,"mapbase.png"),embed = banner_embed)

                elif number > 16:
                    await ctx.send("There are only 16 Chunks.")
                else:

                    title = f'Chunk {number}'
                    mapname = f'{number}.png'
                    gridname = f'grid{number}.png'

                    x_range = 16  # Range for x (width)
                    y_range = 16  # Range for y (height)

                    number -= 1  # Adjusting for zero-based indexing


                    ytruenumber = number // 4
                    ynumber = math.ceil(ytruenumber) +1

                    xtruenumber = number % 4
                    xnumber = math.ceil(xtruenumber) +1



                    numbermaxx = xnumber * x_range + 1
                    numberminx = xnumber * x_range - x_range

                    numbermaxy = ynumber * y_range + 1
                    numberminy = ynumber * y_range - y_range

                    mapbase = Image.open(mapname)
                    grid = Image.open(gridname)


                    spawn_check = await self.bot.db.fetch(f'SELECT * FROM tiles WHERE player_id IS NOT NULL AND x BETWEEN {numberminx} AND {numbermaxx} AND y BETWEEN {numberminy} AND {numbermaxy}')
                    if spawn_check == []:
                        mapbase.paste(grid, (0,0), grid.convert('RGBA'))  
                    else:
                        for i in spawn_check:
                            pfpid = i['player_id']
                            x = i['x']
                            y = i['y']

                            x = (x - 1) % 16 + 1 
                            y = (y - 1) % 16 + 1

                            pfp = Image.open(f'C:\\Users\\Hi\\Documents\\codes\\dominant_bot\\bot_files\\database\\pfps\\{pfpid}.png')

                            mapbase.paste(pfp, (((x-1)*64)+11,((y-1)*64)+11), pfp)
                        
                        mapbase.paste(grid, (0,0), grid.convert('RGBA'))  
                        

                        
                    banner_embed = discord.Embed(
                        title = title,
                        description = f'',
                        colour = color
                    )
        
                    bytes = BytesIO()
                    mapbase.save(bytes, format="PNG")
                    bytes.seek(0)

                    banner_embed.set_image(url=f"attachment://mapbase.png")
                    await ctx.send(file = discord.File(bytes,"mapbase.png"),embed = banner_embed)


    @commands.command(name ='attack', aliases = ['atk'])
    async def attack(self, ctx,tile : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:

            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

    
            if user_ban_list:
                await ctx.send('You are banned from the bot.')

            else:
                if tile == None:

                    em = discord.Embed(
                        title = 'Attack a tile',
                        description = '**Attack a tile**\n\nd!attack [tile]',
                        colour = color
                    ) 

                    await ctx.send(embed = em)
                
                else:
                    tile_check = await self.bot.db.fetch(f'SELECT * FROM tiles WHERE tileid = $1', tile)
                    if tile_check == []:
                        await ctx.send("This tile doesn't exist!")
                        return
                    else:
                        view = ConfirmCancel(ctx.author)                                                     
                        await ctx.send(f"Are you sure you want to attack the tile **{tile}**?", view = view)
                        await view.wait()

                        if view.value is True:
                            if tile_check[0]['effect'] == 'neutral':
                                pass
                            else:
                                print('working')
                        elif view.value is False:
                            await ctx.send("Cancelled.")
                        else:
                            await ctx.send("Timed out.")



def setup(bot):
    bot.add_cog(SpawnCommands(bot))