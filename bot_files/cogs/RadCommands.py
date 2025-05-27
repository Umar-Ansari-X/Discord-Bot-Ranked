import asyncio
import discord
import random
import json
import math
from discord.ext import commands
import numpy as np
import re
import time
from pymongo import MongoClient
import asyncio
import string
from PIL import Image
import requests
import io
from datetime import datetime, timedelta,timezone
import csv
import ast
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import sqlite3
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageSequence

color = 0x32006e
def date_diff_in_seconds(dt2, dt1):
  timedelta = dt1 - dt2
  return timedelta.days * 24 * 3600 + timedelta.seconds

def dhms_from_seconds(seconds):
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	return (days, hours, minutes, seconds)
async def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class RareCommon(discord.ui.View):
    def __init__(self,buttoner,embedpic, poke, name):
        super().__init__(timeout = 60)
        self.poke = poke
        self.buttoner = buttoner
        self.value = None
        self.embedpic = embedpic
        self.disable_buttons = False
        self.name = name


            
    @discord.ui.button(label = "Best Moveset", style = discord.ButtonStyle.red)
    async def confirm_button(self, button: discord.Button, interaction : discord.Interaction):
        try:
            self.disable_buttons = True
            
            common_embed = discord.Embed(
                title = f"{self.name}",
                description = '',
                colour = color
            )
            moveset = self.poke[0]['moveset']
            if moveset == None:
                await interaction.response.send_message(f"There is no data for this Pokemon, if you want to help us let us know!", ephemeral=True)
                self.disable_buttons = False
            else:
                moves11 = moveset.split(" | ")
                if "\\n" in moves11[-1]:
                    last_item_parts = moves11[-1].split("\\n", 1)
                    moves11[-1] = last_item_parts[0]
                    moves11.extend(last_item_parts[1].strip().split(" | "))
                    moves1 = f"{moves11[0].title()}\n{moves11[1].title()}\n{moves11[2].title()}\n{moves11[3].title()}\n\n{moves11[4].title()}"
                else:
                    moves1 = f"{moves11[0].title()}\n{moves11[1].title()}\n{moves11[2].title()}\n{moves11[3].title()}"
                common_embed.set_thumbnail(url=f"attachment://{self.embedpic}")
                common_embed.add_field(name='Best moveset is:', value=f'{moves1}')
                await interaction.response.edit_message(file = discord.File(self.embedpic), embed=common_embed, attachments=interaction.message.attachments)
                self.disable_buttons = False


        except discord.errors.InteractionResponded:
            return

    @discord.ui.button(label = "Stats Guide", style = discord.ButtonStyle.blurple)
    async def csonfirm_button(self, button: discord.Button, interaction : discord.Interaction):
        try:
            self.disable_buttons = True
            name = self.poke[0]['pokemon'] 

            mints = self.poke[0]['search1']
            if mints == None:
                await interaction.response.send_message(f"There is no data for this Pokemon, if you want to help us let us know!", ephemeral=True)
                self.disable_buttons = False
            else:
                mints = mints.split(' | ')
                desc = mints[0]
                if len(mints) < 2:
                    await interaction.response.send_message("Error, please call a mod.")
                    return
                foot = f"Written by {mints[1]} / See something wrong? Let us know!"
                common_embed = discord.Embed(
                    title = f"{name.title()}",
                    description = f'{desc}',
                    colour = color
                )
                common_embed.set_footer(text=foot)
                common_embed.set_thumbnail(url=f"attachment://{self.embedpic}")
                await interaction.response.edit_message(file = discord.File(self.embedpic), embed=common_embed, attachments=interaction.message.attachments)
                self.disable_buttons = False


        except discord.errors.InteractionResponded:
            return

    @discord.ui.button(label = "About Mints", style = discord.ButtonStyle.gray)
    async def coddnfirm_button(self, button: discord.Button, interaction : discord.Interaction):
        try:
            self.disable_buttons = True
            name = self.poke[0]['pokemon'] 

            mints = self.poke[0]['mints']
            if mints == None:
                await interaction.response.send_message(f"There is no data for this Pokemon, if you want to help us let us know!", ephemeral=True)
                self.disable_buttons = False
            else:
                mints = mints.split(' | ')
                desc = mints[0]
                if len(mints) < 2:
                    await interaction.response.send_message("Error, please call a mod.")
                    return
            
                foot = f"Written by {mints[1]} / See something wrong? Let us know!"
                common_embed = discord.Embed(
                    title = f"{name.title()}",
                    description = f'{desc}',
                    colour = color
                )
                common_embed.set_footer(text=foot)
                common_embed.set_thumbnail(url=f"attachment://{self.embedpic}")
                await interaction.response.edit_message(file = discord.File(self.embedpic), embed=common_embed, attachments=interaction.message.attachments)
                self.disable_buttons = False

        except discord.errors.InteractionResponded:
            return
        
    async def interaction_check(self, interaction: discord.Interaction):

        if self.disable_buttons:
            await interaction.response.send_message("Please wait...", ephemeral=True)
            
            return False

        return interaction.user == self.buttoner
                                        
    async def on_timeout(self):
        self.value = None

        for i in self.children:
            i.disabled = True
        
class RareCommon2(discord.ui.View):
    def __init__(self,buttoner):
        super().__init__(timeout = 30)
        self.buttoner = buttoner
        self.disable_buttons = False


            
    @discord.ui.button(label = "Best Moveset", style = discord.ButtonStyle.red)
    async def confirm_button(self, button: discord.Button, interaction : discord.Interaction):
        try:
            self.disable_buttons = True
            await interaction.response.send_message(f"There is no data for this Pokemon, if you want to help us let us know!", ephemeral=True)
            self.disable_buttons = False


        except discord.errors.InteractionResponded:
            return

    @discord.ui.button(label = "Stats Guide", style = discord.ButtonStyle.blurple)
    async def confdairm_button(self, button: discord.Button, interaction : discord.Interaction):
        try:
            self.disable_buttons = True
            await interaction.response.send_message(f"There is no data for this Pokemon, if you want to help us let us know!", ephemeral=True)
            self.disable_buttons = False


        except discord.errors.InteractionResponded:
            return
        
    @discord.ui.button(label = "About Mints", style = discord.ButtonStyle.gray)
    async def confsdirm_button(self, button: discord.Button, interaction : discord.Interaction):
        try:
            self.disable_buttons = True
            await interaction.response.send_message(f"There is no data for this Pokemon, if you want to help us let us know!", ephemeral=True)
            self.disable_buttons = False


        except discord.errors.InteractionResponded:
            return

    async def interaction_check(self, interaction: discord.Interaction):

        if self.disable_buttons:
            await interaction.response.send_message("Please wait...", ephemeral=True)
            
            return False

        return interaction.user == self.buttoner
                                        
    async def on_timeout(self):
        self.value = None

        for i in self.children:
            i.disabled = True

def format_time_difference(delta):
    if delta == None:
        return
    seconds = delta.total_seconds()
    
    intervals = (
        ('weeks', 604800),
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
    )

    components = []
    for name, count in intervals:
        value = int(seconds // count)
        if value:
            seconds -= value * count
            components.append(f"{value} {name}" if value > 1 else f"{value} {name[:-1]}")

    if not components:
        return "just now"
    elif len(components) == 1:
        return components[0]
    else:
        return ', '.join(components[:-1]) + f" and {components[-1]}"

async def get_ban_data():
    with open("users.json", "r") as f:
        users = json.load(f)
    
    return users

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


class ConfirmW(discord.ui.View):
    def __init__(self, member : discord.Member):
        super().__init__(timeout = 30)

        self.value = None
        self.member = member

    @discord.ui.button(label = "Change POV", style = discord.ButtonStyle.blurple, emoji = "🔎" )
    async def confirm_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = True
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


class roninPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 6
    numbre : int = 0


    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb, self.bot)


    async def create_embed(self, data,lb,bot):
        lb = self.lb
        bot = self.bot

        lb_embed = discord.Embed(
            title = 'Blades Queued',
            description = 'Click the buttons to change pages.',
            colour = color
        )


        for i in data:
            
            rank_value = lb[self.numbre]['rank_value']
            if rank_value == 0:
                rank = 'Bronze'
            elif rank_value == 1:
                rank = 'Silver'
            elif rank_value == 2:
                rank = 'Gold'
            elif rank_value == 3:
                rank = 'Platinum'
            elif rank_value == 4:
                rank = 'Dominant'

            scoreStr = f"**Rank 》 **{rank}\n**Points 》 **{lb[self.numbre]['points']}"    
            lb_embed.add_field(name = f"{lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
            self.numbre = self.numbre + 1
                 

        lb_embed.set_footer(text = f'Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')

        return lb_embed

    async def update_message(self,data, lb,bot):
        self.update_buttons()
        await self.message.edit(embed= await self.create_embed(data, lb,bot), view=self)

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.red
            self.prev_button.style = discord.ButtonStyle.blurple

        if self.current_page == math.ceil(len(self.data) / self.sep):
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.red
            self.next_button.style = discord.ButtonStyle.blurple

    def get_current_page_data(self):
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        if self.current_page == 1:
            from_item = 0
            until_item = self.sep
        if self.current_page == math.ceil(len(self.data) / self.sep):
            from_item = self.current_page * self.sep - self.sep
            until_item = len(self.data)
        return self.data[from_item:until_item]



    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red, emoji='♦️')
    async def first_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page = 1
        self.numbre = 0

        await self.update_message(self.get_current_page_data(), self.lb,self.bot )

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple,emoji='🔹')
    async def prev_button(self,  button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()

        delete =  int(len(self.data)) - self.sep * self.current_page
        delete = 12
        if int(len(self.data)) < self.sep * self.current_page:
            new = int(len(self.data)) - self.sep * (self.current_page -1)
            delete = new + 6
        self.current_page -= 1
        self.numbre -= delete
        await self.update_message(self.get_current_page_data(), self.lb,self.bot)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple,emoji='🔹')
    async def next_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data(), self.lb,self.bot)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red, emoji='♦️')
    async def last_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page = math.ceil(len(self.data) / self.sep)
        self.numbre = (self.sep * (self.current_page -1))
        await self.update_message(self.get_current_page_data(), self.lb,self.bot)


class CAPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 6
    numbre : int = 0
    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb, self.stat)

    async def create_embed(self, data,lb,stat ):
        lb = self.lb
        stat = self.stat

        scoreStr = ''        
        lb_embed = discord.Embed(
            title = 'Tournament Leaderboard',
            description = f'Click the buttons to view other pages.',
            colour = color
        )
        
        for i in data:
            scoreStr = f"**Wins **{stat[self.numbre]}"
            lb_embed.add_field(name = f"{self.numbre+1}# {i.title()} ", value = f'{scoreStr}', inline=False)
            self.numbre = self.numbre + 1

            lb_embed.set_footer(text = f"Page {self.current_page}")

        return lb_embed

    async def update_message(self,data, lb, stat):


        self.update_buttons()
        await self.message.edit(embed= await self.create_embed(data, lb, stat), view=self)

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.red
            self.prev_button.style = discord.ButtonStyle.blurple

        if self.current_page == math.ceil(len(self.data) / self.sep):
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.red
            self.next_button.style = discord.ButtonStyle.blurple

    def get_current_page_data(self):



        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        if self.current_page == 1:
            from_item = 0
            until_item = self.sep
        if self.current_page == math.ceil(len(self.data) / self.sep):
            from_item = self.current_page * self.sep - self.sep
            until_item = len(self.data)
        return self.data[from_item:until_item]


    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red,emoji="♦️")
    async def first_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page = 1
        self.numbre = 0

        
        
        await self.update_message(self.get_current_page_data(), self.lb, self.stat)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple,emoji='🔹')
    async def prev_button(self,  button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()

        delete = 12
        if int(len(self.data)) < self.sep * self.current_page:
            new = int(len(self.data)) - self.sep * (self.current_page -1)
            delete = new + 6
        self.current_page -= 1
        self.numbre -= delete
        await self.update_message(self.get_current_page_data(), self.lb, self.stat)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple,emoji='🔹')
    async def next_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()


        self.current_page += 1
        await self.update_message(self.get_current_page_data(), self.lb, self.stat)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red,emoji='♦️')
    async def last_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()



        self.current_page = math.ceil(len(self.data) / self.sep)
        self.numbre = (self.sep * (self.current_page -1))
        await self.update_message(self.get_current_page_data(), self.lb, self.stat)

class WPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 8
    numbre : int = 0
    sort_option = "blade"
    change = 'no'

    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb, self.stat, self.stats)

    async def create_embed(self, data,lb,stat, stats ):
        lb = self.lb
        stat = self.stat
        stats = self.stats


        scoreStr = ''        
        lb_embed = discord.Embed(
            title = 'War Leaderboard',
            description = f'Click the buttons to change pages.',
            colour = color
        )
        if self.change == 'no':
            pass
        else:
            self.numbre = 0
        
        if self.sort_option == 'wl':      
            lb = await stat.db.fetch(f'SELECT * FROM registered ORDER BY wl DESC')
            
            for i in data:
                score = lb[self.numbre]['wl']
                if score > 0:
                    score = f"+{lb[self.numbre]['wl']}"
                scoreStr = f"**W/L 》** **{score}**⠀({lb[self.numbre]['wwar']}/{lb[self.numbre]['lwar']})\n**Clan 》 **{lb[self.numbre]['clan_1']}"
                lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1
        elif self.sort_option == 'w':      
            lb = await stat.db.fetch(f'SELECT * FROM registered ORDER BY wwar DESC')
            for i in data:
                scoreStr = f"**Wins 》 **{lb[self.numbre]['wwar']}\n**Clan 》 **{lb[self.numbre]['clan_1']}"
                lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1               

        elif self.sort_option == 'l':      
            lb = await stat.db.fetch(f'SELECT * FROM registered ORDER BY lwar DESC')
            for i in data:
                scoreStr = f"**Losses 》 **{lb[self.numbre]['lwar']}\n**Clan 》 **{lb[self.numbre]['clan_1']}"
                lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1   

        elif self.sort_option == 'mvp':      
            lb = await stat.db.fetch(f'SELECT * FROM registered ORDER BY mvps DESC')
            for i in data:
                scoreStr = f"**MVPs 》 **{lb[self.numbre]['mvps']}\n**Clan 》 **{lb[self.numbre]['clan_1']}"
                lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1   

        elif self.sort_option == 'blade':      
            lb = await stat.db.fetch(f'SELECT * FROM wars ORDER BY points DESC')
            for i in data:
                rank_value = lb[self.numbre]['rank_value']
                if rank_value == 0:
                    rank = 'Bronze'
                elif rank_value == 1:
                    rank = 'Silver'
                elif rank_value == 2:
                    rank = 'Gold'
                elif rank_value == 3:
                    rank = 'Platinum'
                elif rank_value == 4:
                    rank = 'Dominant'
                scoreStr = f"**Rank 》 **{rank}\n**Points 》 **{lb[self.numbre]['points']}"
                lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1  
        
        self.change = 'no'
        lb_embed.set_footer(text = f'Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')

        return lb_embed

    async def update_message(self,data, lb, stat, stats):
        self.update_buttons()
        await self.message.edit(embed= await self.create_embed(data, lb, stat, stats), view=self)

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.red
            self.prev_button.style = discord.ButtonStyle.blurple

        if self.current_page == math.ceil(len(self.data) / self.sep):
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.red
            self.next_button.style = discord.ButtonStyle.blurple

    def get_current_page_data(self):
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        if self.current_page == 1:
            from_item = 0
            until_item = self.sep
        if self.current_page == math.ceil(len(self.data) / self.sep):
            from_item = self.current_page * self.sep - self.sep
            until_item = len(self.data)
        return self.data[from_item:until_item]


    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red,emoji="♦️")
    async def first_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page = 1
        self.numbre = 0

        await self.update_message(self.get_current_page_data(), self.lb, self.stat,self.stats)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple,emoji='🔹')
    async def prev_button(self,  button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()

        delete = 16
        if int(len(self.data)) < self.sep * self.current_page:
            new = int(len(self.data)) - self.sep * (self.current_page -1)
            delete = new + 8
        self.current_page -= 1
        self.numbre -= delete
        await self.update_message(self.get_current_page_data(), self.lb, self.stat,self.stats)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple,emoji='🔹')
    async def next_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data(), self.lb, self.stat,self.stats)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red,emoji='♦️')
    async def last_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page = math.ceil(len(self.data) / self.sep)
        self.numbre = (self.sep * (self.current_page -1))
        await self.update_message(self.get_current_page_data(), self.lb, self.stat,self.stats)


    @discord.ui.select(placeholder="Sort by...", min_values=1, max_values=1,
                       options=[
                           discord.SelectOption(label="Blades Ranked", value="blade"),
                           discord.SelectOption(label="W/L Ratio", value="wl"),
                           discord.SelectOption(label="Wins", value="w"),
                           discord.SelectOption(label="Loses", value="l"),
                           discord.SelectOption(label="MVPs", value="mvp"),

                       ])

    async def sort_dropdown(self, select: discord.ui.Select, interaction: discord.Interaction):
        await interaction.response.defer()
        self.sort_option = select.values[0]
        self.change = 'yes'
        self.current_page = 1
        
        await self.update_message(self.get_current_page_data(), self.lb, self.stat,self.stats)

class VPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 6
    numbre : int = 0


    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb, self.bot)

    
    async def create_embed(self, data,lb,bot):
        lb = self.lb
        bot = self.bot

        lb_embed = discord.Embed(
            title = 'Community Votes Leaderboard',
            description = 'Click the buttons to change pages.',
            colour = color
        )

        for i in data:
            scoreStr = f"**Votes 》 **{lb[self.numbre]['votes']}"

            lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
            self.numbre = self.numbre + 1            
            

        lb_embed.set_footer(text = f'Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')

        return lb_embed

    async def update_message(self,data, lb,bot):
        self.update_buttons()
        await self.message.edit(embed= await self.create_embed(data, lb,bot), view=self)

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.red
            self.prev_button.style = discord.ButtonStyle.blurple

        if self.current_page == math.ceil(len(self.data) / self.sep):
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.red
            self.next_button.style = discord.ButtonStyle.blurple

    def get_current_page_data(self):
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        if self.current_page == 1:
            from_item = 0
            until_item = self.sep
        if self.current_page == math.ceil(len(self.data) / self.sep):
            from_item = self.current_page * self.sep - self.sep
            until_item = len(self.data)
        return self.data[from_item:until_item]



    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red, emoji='♦️')
    async def first_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page = 1
        self.numbre = 0

        await self.update_message(self.get_current_page_data(), self.lb,self.bot )

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple,emoji='🔹')
    async def prev_button(self,  button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()

        delete =  int(len(self.data)) - self.sep * self.current_page
        delete = 12
        if int(len(self.data)) < self.sep * self.current_page:
            new = int(len(self.data)) - self.sep * (self.current_page -1)
            delete = new + 6
        self.current_page -= 1
        self.numbre -= delete
        await self.update_message(self.get_current_page_data(), self.lb,self.bot)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple,emoji='🔹')
    async def next_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data(), self.lb,self.bot)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red, emoji='♦️')
    async def last_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page = math.ceil(len(self.data) / self.sep)
        self.numbre = (self.sep * (self.current_page -1))
        await self.update_message(self.get_current_page_data(), self.lb,self.bot)

        
type_chart = {"fighting": {
"normal": 2, "fighting": 1, "flying": 0.5, "poison": 0.5,
"ground": 1, "rock": 2, "bug": 0.5, "ghost": 0, "steel": 2,
"fire": 1, "water": 1, "grass": 1, "electric": 1, "psychic": 0.5,
"ice": 2, "dragon": 1, "dark": 2, "fairy": 0.5
},

"flying": {
"normal": 1, "fighting": 2, "flying": 1, "poison": 1,
"ground": 1, "rock": 0.5, "bug": 2, "ghost": 1, "steel": 0.5,
"fire": 1, "water": 1, "grass": 2, "electric": 0.5, "psychic": 1,
"ice": 1, "dragon": 1, "dark": 1, "fairy": 1
},

"poison": {
"normal": 1, "fighting": 1, "flying": 1, "poison": 0.5,
"ground": 0.5, "rock": 0.5, "bug": 1, "ghost": 0.5, "steel": 0,
"fire": 1, "water": 1, "grass": 2, "electric": 1, "psychic": 1,
"ice": 1, "dragon": 1, "dark": 1, "fairy": 2
},

"ground": {
"normal": 1, "fighting": 1, "flying": 0, "poison": 2,
"ground": 1, "rock": 2, "bug": 0.5, "ghost": 1, "steel": 2,
"fire": 2, "water": 1, "grass": 0.5, "electric": 2, "psychic": 1,
"ice": 1, "dragon": 1, "dark": 1, "fairy": 1
},

"rock": {
"normal": 1, "fighting": 0.5, "flying": 2, "poison": 1,
"ground": 0.5, "rock": 1, "bug": 2, "ghost": 1, "steel": 0.5,
"fire": 2, "water": 1, "grass": 1, "electric": 1, "psychic": 1,
"ice": 2, "dragon": 1, "dark": 1, "fairy": 1
},

"bug": {
"normal": 1, "fighting": 0.5, "flying": 0.5, "poison": 0.5,
"ground": 1, "rock": 1, "bug": 1, "ghost": 0.5, "steel": 0.5,
"fire": 0.5, "water": 1, "grass": 2, "electric": 1, "psychic": 2,
"ice": 1, "dragon": 1, "dark": 2, "fairy": 0.5
},

"ghost": {
"normal": 0, "fighting": 1, "flying": 1, "poison": 1,
"ground": 1, "rock": 1, "bug": 1, "ghost": 2, "steel": 1,
"fire": 1, "water": 1, "grass": 1, "electric": 1, "psychic": 2,
"ice": 1, "dragon": 1, "dark": 0.5, "fairy": 1
},

"steel": {
"normal": 1, "fighting": 1, "flying": 1, "poison": 1,
"ground": 1, "rock": 2, "bug": 1, "ghost": 1, "steel": 0.5,
"fire": 0.5, "water": 0.5, "grass": 1, "electric": 0.5, "psychic": 1,
"ice": 2, "dragon": 1, "dark": 1, "fairy": 2
},

"fire": {
"normal": 1, "fighting": 1, "flying": 1, "poison": 1,
"ground": 1, "rock": 0.5, "bug": 2, "ghost": 1, "steel": 2,
"fire": 0.5, "water": 0.5, "grass": 2, "electric": 1, "psychic": 1,
"ice": 2, "dragon": 0.5, "dark": 1, "fairy": 1
},

"water": {
"normal": 1, "fighting": 1, "flying": 1, "poison": 1,
"ground": 2, "rock": 2, "bug": 1, "ghost": 1, "steel": 1,
"fire": 2, "water": 0.5, "grass": 0.5, "electric": 1, "psychic": 1,
"ice": 1, "dragon": 0.5, "dark": 1, "fairy": 1
},

"grass": {
"normal": 1, "fighting": 1, "flying": 0.5, "poison": 0.5,
"ground": 2, "rock": 2, "bug": 0.5, "ghost": 1, "steel": 0.5,
"fire": 0.5, "water": 2, "grass": 0.5, "electric": 1, "psychic": 1,
"ice": 1, "dragon": 0.5, "dark": 1, "fairy": 1
},

"electric": {
"normal": 1, "fighting": 1, "flying": 2, "poison": 1,
"ground": 0, "rock": 1, "bug": 1, "ghost": 1, "steel": 1,
"fire": 1, "water": 2, "grass": 0.5, "electric": 0.5, "psychic": 1,
"ice": 1, "dragon": 0.5, "dark": 1, "fairy": 1
},

"psychic": {
"normal": 1, "fighting": 2, "flying": 1, "poison": 2,
"ground": 1, "rock": 1, "bug": 1, "ghost": 1, "steel": 0.5,
"fire": 1, "water": 1, "grass": 1, "electric": 1, "psychic": 0.5,
"ice": 1, "dragon": 1, "dark": 0, "fairy": 1
},

"ice": {
"normal": 1, "fighting": 1, "flying": 2, "poison": 1,
"ground": 2, "rock": 1, "bug": 1, "ghost": 1, "steel": 0.5,
"fire": 0.5, "water": 0.5, "grass": 2, "electric": 1, "psychic": 1,
"ice": 0.5, "dragon": 2, "dark": 1, "fairy": 1
},

"dragon": {
"normal": 1, "fighting": 1, "flying": 1, "poison": 1,
"ground": 1, "rock": 1, "bug": 1, "ghost": 1, "steel": 0.5,
"fire": 1, "water": 1, "grass": 1, "electric": 1, "psychic": 1,
"ice": 1, "dragon": 2, "dark": 1, "fairy": 0
},

"dark": {
"normal": 1, "fighting": 0.5, "flying": 1, "poison": 1,
"ground": 1, "rock": 1, "bug": 1, "ghost": 2, "steel": 1,
"fire": 1, "water": 1, "grass": 1, "electric": 1, "psychic": 2,
"ice": 1, "dragon": 1, "dark": 0.5, "fairy": 0.5
},

"fairy": {
"normal": 1, "fighting": 2, "flying": 1, "poison": 0.5,
"ground": 1, "rock": 1, "bug": 1, "ghost": 1, "steel": 0.5,
"fire": 0.5, "water": 1, "grass": 1, "electric": 1, "psychic": 1,
"ice": 1, "dragon": 2, "dark": 2, "fairy": 1
},

"normal": {
"normal": 1, "fighting": 1, "flying": 1, "poison": 1,
"ground": 1, "rock": 0.5, "bug": 1, "ghost": 0, "steel": 0.5,
"fire": 1, "water": 1, "grass": 1, "electric": 1, "psychic": 1,
"ice": 1, "dragon": 1, "dark": 1, "fairy": 1
}
}


class RadCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = MongoClient("####")
        database = self.cluster['discord']
        self.collection = database["miniboard"]

    def get_move_type(self, move):
        with open('moves.json', 'r') as file:
            moves_data = json.load(file)
        
        move_data = moves_data[move]
        return move_data['type']

    def check_effectiveness(self, defending_types, attacking_type):
        effectiveness = 1
        for defense_type in defending_types:

            effectiveness *= type_chart[attacking_type.lower()][defense_type.lower()]

        if effectiveness > 1:
            return "super effective"
        elif effectiveness == 1:
            return "effective"
        elif effectiveness < 1 and effectiveness > 0:
            return "not very effective"
        else:
            return "does no damage"    



    def listing(self, str1 : str):
        if str1 is not None:
            list_str = str1.split()

            if list_str[0] == '':
                list_str.remove(list_str[0])

            list_num = []

            for e in list_str:
                list_num.append((e.strip()))

            return list_num
        
        elif str1 is None:
            list1 = []

            return list1
    def llisting(self, str1 : str):
        if str1 is not None:
            list_str = str1.split()

            if list_str[0] == '':
                list_str.remove(list_str[0])

            list_num = []

            for e in list_str:
                list_num.append(int(e.strip()))

            return list_num
        
        elif str1 is None:
            list1 = []

            return list1     

    def find_matching_pokemon(self, pokemon1, allnames):

        starting_with_input = [pokemon for pokemon in allnames if pokemon.lower().startswith(pokemon1.lower())]

        if not starting_with_input:
            matches = [(pokemon, fuzz.partial_ratio(pokemon1.lower(), pokemon.lower())) for pokemon in allnames]

            sorted_matches = sorted(matches, key=lambda x: x[1], reverse=True)
        
        else:

            matches = [(pokemon, fuzz.partial_ratio(pokemon1.lower(), pokemon.lower())) for pokemon in starting_with_input]

            sorted_matches = sorted(matches, key=lambda x: x[1], reverse=True)



        best_match, similarity_score = sorted_matches[0]

        threshold = 80 


        if similarity_score >= threshold:
            return f"{best_match}"
        else:
            return None


    @commands.command(name = 'wleaderboard', aliases = ['wlb'])
    async def wwwleaderboard_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
   
        if registered_check:
            lb = await self.bot.db.fetch(f'SELECT * FROM wars')
            data = []
            for faction in lb:
                data.append(faction['player_id'])

            stat = self.bot
            stats = None
            pagination_view = WPaginationView()
            pagination_view.data = data
            pagination_view.lb = lb
            pagination_view.stat = stat
            pagination_view.stats = stats
            await pagination_view.send(ctx)

                

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'voteleaderboard', aliases = ['vlb'])
    async def votes_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

  
        if user_ban_list:
            await ctx.send('You are banned from the bot.')
            return

        if registered_check:

            lb = await self.bot.db.fetch('SELECT * FROM casual WHERE votes >= 1 ORDER BY votes DESC')

            data = []
            for faction in lb:
                data.append(faction['player_name'])
   
    
            pagination_view = VPaginationView()
            pagination_view.data = data
            pagination_view.lb = lb
            pagination_view.bot = self.bot
   
            await pagination_view.send(ctx)

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')


    @commands.command(name ='winner')
    async def winnergw(self, ctx, formats : str = None):
        if ctx.author.id == 0:
            pass
        else:
            await ctx.send("You can't use this command!")
            return
        
        ticket = await self.bot.db.fetch('SELECT * FROM gamble WHERE ticket > 0')
        raffle = []
        totaltickets = 0
        for i in ticket:

            name = i['player_id']
            tickets = i['ticket']
            ticket_id = (name,tickets)
            for t in range(tickets):
                raffle.append(ticket_id)
                totaltickets += 1
    
        winner = random.choice(raffle)

        winner_message = await ctx.send('**The winner is... **:drum: ')
        await asyncio.sleep(2)
        await winner_message.edit('**The winner is...** :drum: :drum:')
        await asyncio.sleep(2)
        await winner_message.edit('**The winner is...** :drum: :drum: :drum:')
        await asyncio.sleep(3)
        await winner_message.edit(f'**The winner is...** <@{winner[0]}> :tada: :tada: :tada:\n\nThere were a total of **{totaltickets}** tickets and they had **{winner[1]}** of the tickets..')
        

    @commands.command(name ='enter')
    async def strejoijn(self, ctx, player : discord.Member = None, player2 : discord.Member = None,player3 : discord.Member = None,*, team : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check: 

            

        
            if player == None:
                await ctx.send("Please enter a player, d!enter <mention> <mention> <mention> <teamname>")
                return
            if player2 == None:
                await ctx.send("Please enter a player, d!enter <mention> <mention> <mention> <teamname>")
                return
            
            if player3 == None:
                await ctx.send("Please enter a player, d!enter <mention> <mention> <mention> <teamname>")
                return
            if team == None:
                await ctx.send("Please enter a team name, d!enter <mention> <mention> <mention> <teamname>")
                return


            team = team.lower()

            tourney_check = await self.bot.db.fetch('SELECT * FROM tournament WHERE player_id = $1', player.id)
            if tourney_check:
                await ctx.send("They are already in the tournament!")
                return
            else:
                pass

            author_name = player.name
            author_name2 = player2.name
            author_name3 = player3.name
            alive = 'yes'

            await self.bot.db.execute('INSERT INTO tournament (player_id, player_name, matches_played, wins, teamscore, teams, alive) VALUES ($1, $2, 0, 0, 0, $3, $4)', player.id, author_name, team, alive)
            await self.bot.db.execute('INSERT INTO tournament (player_id, player_name, matches_played, wins, teamscore, teams, alive) VALUES ($1, $2, 0, 0, 0, $3, $4)', player2.id, author_name2, team, alive)
            await self.bot.db.execute('INSERT INTO tournament (player_id, player_name, matches_played, wins, teamscore, teams, alive) VALUES ($1, $2, 0, 0, 0, $3, $4)', player3.id, author_name3, team, alive)

            await ctx.send(f"Entered! {team} \n {player} {player2} {player3}")
                
    
        else:
            await ctx.send("You haven't registered yet! Please do `d!start` do register.")

    @commands.command(aliases=['tournament', 'tourney', 'trm'])
    async def tournbozo(self,ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:         


            alive = 'yes'
            lb = await self.bot.db.fetch(f'SELECT * FROM tournament WHERE alive = $1 ORDER BY teamscore DESC', alive)


            data = []
            stat = []
            for faction in lb:
                if faction['teams'] in data:
                    pass
                else:
                    stat.append(faction['teamscore'])
                    data.append(faction['teams'])
                        

            pagination_view = CAPaginationView()
            pagination_view.data = data
            pagination_view.lb = lb
            pagination_view.stat = stat
            await pagination_view.send(ctx)
            
    
        else:
            await ctx.send("You haven't registered yet! Please do `d!start` do register.")

    @commands.command(aliases=['team'])
    async def toutefffanozo(self,ctx,*, teamname : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:         

            
            if teamname == None:
                name = await self.bot.db.fetch(f'SELECT * FROM tournament WHERE player_id = $1', ctx.author.id)
                if name == None:
                    await ctx.send("Please enter a team name.. d!team <name>")
                    return
                
                teamname = name[0]['teams']
            else:
                teamname = teamname.lower()
            lb = await self.bot.db.fetch(f'SELECT * FROM tournament WHERE teams = $1', teamname)

            if lb == []:
                await ctx.send("This team doesn't exist")
                return
            

            if len(lb) != 3:
                await ctx.send("This team does not have enough members..")
                return

            war = discord.Embed(
            title = f"Team {lb[0]['teams']}",
            description = f'',
            colour = color
            )
            war.add_field(name = f"{lb[0]['player_name']}", value = f"{lb[0]['wins']} / {lb[0]['matches_played'] - lb[0]['wins']}", inline=False)
            war.add_field(name = f"{lb[1]['player_name']}", value = f"{lb[1]['wins']} / {lb[1]['matches_played'] - lb[1]['wins']}", inline=False)
            war.add_field(name = f"{lb[2]['player_name']}", value = f"{lb[2]['wins']} / {lb[2]['matches_played'] - lb[2]['wins']}", inline=False)
            war.add_field(name = f"Total Wins {lb[0]['teamscore']}", value = f"", inline=False)
            await ctx.send(embed = war)
           
            
    
        else:
            await ctx.send("You haven't registered yet! Please do `d!start` do register.")


    @commands.command(name = 'tstart')
    async def tourneyd(self,ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if registered_check:
            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(786448967172882442)
            role2 = guild.get_role(1090438349455622204)
            role3 = guild.get_role(781452019578961921)
            if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles):

                mode = 'br'


                await ctx.message.delete()
                one = await ctx.send(f"{ctx.author.mention} Please specify the **1st** Team name.")
                try:
                    winne = await self.bot.wait_for(
                        'message',
                        timeout = 60,
                        check = lambda message: message.author == ctx.author and message.channel == ctx.channel
                    )

                except asyncio.TimeoutError:
                    await ctx.send('Timed-out.')

                else:
                    clan_1 = winne.content
                    
                    await one.delete()
                    await winne.delete() 

                    teams = await self.bot.db.fetch('SELECT * FROM tournament WHERE teams = $1', clan_1)
                    if teams == []:
                        await ctx.send("This team name hasn't been registered..")
                        return

                    three =await ctx.send(f"{ctx.author.mention} Please mention the ally members of **{clan_1}**")
                    try:
                        allies = await self.bot.wait_for(
                            'message',
                            timeout = 60,
                            check = lambda message: message.author == ctx.author and message.channel == ctx.channel
                        )

                    except asyncio.TimeoutError:
                        await ctx.send('Timed-out.')

                    else:

                        alliesList = [x.id for x in allies.mentions]

                        if len(alliesList) != 3:
                            await ctx.send("3 Members only")
                            return
                        else:
                            await three.delete()
                            await allies.delete()


                        two = await ctx.send(f"{ctx.author.mention} Please specify the **2nd** Clan name.")
                        try:
                            lose = await self.bot.wait_for(
                                'message',
                                timeout = 60,
                                check = lambda message: message.author == ctx.author and message.channel == ctx.channel
                            )

                        except asyncio.TimeoutError:
                            await ctx.send('Timed-out.')

                        else:
                            clan_2 = lose.content   

                            await two.delete()
                            await lose.delete()                      


                            teams = await self.bot.db.fetch('SELECT * FROM tournament WHERE teams = $1', clan_2)
                            if teams == []:
                                await ctx.send("This team name hasn't been registered..")
                                return

                            four = await ctx.send(f"{ctx.author.mention} Please mention the ally members of **{clan_2}**. *Make sure you ask them before adding them here*")
                            try:
                                enemies = await self.bot.wait_for(
                                    'message',
                                    timeout = 60,
                                    check = lambda message: message.author == ctx.author and message.channel == ctx.channel
                                )

                            except asyncio.TimeoutError:
                                await ctx.send('Timed-out.')

                            else:
                                enemiesList = [x.id for x in enemies.mentions]
                                if len(enemiesList) != 3 :
                                    await ctx.send("3 Members only")
                                    return

                                else:

                                    await four.delete()
                                    await enemies.delete() 

                                    faction_name = str(clan_1.title())

                                    efaction_name = str(clan_2.title())

                                    enemyitems = len(enemiesList)
                                    enemyscore = [0] * enemyitems
                                    enemyscored = [0] * enemyitems
                                    
                                    allyitems = len(alliesList)
                                    allyscore = [0] * allyitems
                                    allyscored = [0] * allyitems

                                    winscore = 10
                                    duration = 7

                                    view = ConfirmCancel(ctx.author)
                                    message = await ctx.send(f'{ctx.author.mention} Are you sure? This will be a **BR** first to reach **{winscore}** wins between **{clan_1}** and **{clan_2}**', view = view)
                                    
                                    await view.wait()

                                    if view.value is True: 

                                        await message.delete()   

                                        powerups = 'no'                                                                          

                                        time_change = timedelta(days=duration)
                                        t = datetime.now(timezone.utc) + time_change
                                        timenew = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
                                        enemiesListname = ''
                                        alliesListname = ''
                                        for i in alliesList:
                                                nun  = await self.bot.fetch_user(i)
                                                alliesListname += f"`{nun.name}` "
                                        oppmemberStr = ""
                                        for i in enemiesList:
                                                nun  = await self.bot.fetch_user(i)
                                                enemiesListname += f"`{nun.name}` "
                                        warid = await id_generator()
                                        history = []
                                        power = '97551132211'
                                        self.collection.insert_one({"_id": warid, "allyscore": 0, "enemyscore" : 0, "allymembers": alliesList, "enemymembers": enemiesList,"allymembersname": alliesListname, "enemymembersname": enemiesListname, "allyplayerscored": allyscored, "enemyplayerscored": enemyscored,"allyplayerscore": allyscore, "enemyplayerscore": enemyscore, "winscore" : winscore, "time" : timenew,"teamone": faction_name, "teamtwo":efaction_name,  "faction": True, "wartype": 'br',"history": history,"powerups": powerups, "1powerup": power, "2powerup" : power })
                                        allymemberStr = ""
                                        for i in alliesList:
                                                allymemberStr += f"<@{i}> "
                                        oppmemberStr = ""
                                        for i in enemiesList:
                                                oppmemberStr += f"<@{i}> "
                                        war = discord.Embed(
                                        title = f"⚔️ {faction_name} VS {efaction_name} First to get {winscore} wins",
                                        description = f'To log wins do d!log war [Opponent]\nd!viewwar **{warid}** to view this war.',
                                        colour = color
                                        )
                                        war.add_field(name = f'{faction_name} Score: 0', value = allymemberStr, inline=False)
                                        war.add_field(name = f'{efaction_name} Score: 0', value = oppmemberStr, inline=False)
                                        war.add_field(name = 'Scoreboard: ', value = "Log your wins and they'll show up here.", inline=False)
                                        war.set_footer(text = f'Ends in {duration} Day(s).')
                                        await ctx.send(embed = war)

                                    elif view.value is False:
                                        await ctx.send("Cancelled.")
                                    else:
                                        await ctx.send("Timed out.")

            else:
                await ctx.send('You do not have permission to use that command.')               
        else:
            await ctx.send("You haven't registered yet! do `d!start` to register.")


    @commands.command(name='twars')
    async def warddsss(self,ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

            if user_ban_list:
                await ctx.send('You are banned from the bot.')
                return
            
            faction_score = list(self.collection.aggregate([{"$sort" : {"time" : -1}}]))
            id = []
            for faction in faction_score:
                id.append(faction["_id"])
            teamone = []
            for faction in faction_score:
                teamone.append(faction["teamone"])
            teamtwo = []
            for faction in faction_score:
                teamtwo.append(faction["teamtwo"])
            teamonescore = []
            for faction in faction_score:
                teamonescore.append(faction["allyscore"])
            teamtwoscore  = []
            for faction in faction_score:
                teamtwoscore.append(faction["enemyscore"])
            times = []
            for faction in faction_score:
                times.append(faction["time"])
            byscore = list(zip(id,teamone,teamtwo,teamonescore,teamtwoscore,times))
            serial = 1
            wars = discord.Embed(
            title = f"Current ongoing tournament wars",
            description = f'',
            colour = color
            )

            for i in byscore:
                scorelist = list(i)
                crudescore1 = str(scorelist[0])
                crudescore2 = str(scorelist[1])
                crudescore3 = str(scorelist[2])
                crudescore4 = int(scorelist[3])
                crudescore5 = int(scorelist[4])
            
                
                wars.add_field(name = f'`{serial}#` {crudescore1} {crudescore2} {crudescore4} :crossed_swords:  {crudescore3} {crudescore5}', value = f'', inline=False)
                serial += 1
            await ctx.send(embed = wars)
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name='tlog')
    async def log_fafdadcdfation_command(self,ctx, warid =None, opponent : discord.Member = None, user : discord.Member = None ):
        if (opponent == None) or (warid == None):
            em = discord.Embed(
                title = "War",
                description = 'Log a war duel.\n\n**d!tlog warid [Opponent]**',
                colour = color
            )
            await ctx.send(embed = em)

        else:
            g = 'no'
            player = ctx.author
            if user == None:
                pass
            else:
                guild = self.bot.get_guild(774883579472904222)
                role = guild.get_role(786448967172882442)
                role2 = guild.get_role(1090438349455622204)
                if (role in ctx.author.roles) or (role2 in ctx.author.roles):  
                    g = 'yes'    
                    player = user
                else:
                    await ctx.send("You don't have perms for this command!")
                    return
            registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', player.id)
            if registered_check:
                winner = player.id
                loser = opponent.id

                if self.collection.count_documents({"_id": warid}, limit = 1):
                    if self.collection.count_documents({"_id": warid, "allymembers": opponent.id, "enemymembers": player.id}, limit = 1):
                        winner = opponent.id
                        loser = player.id
                    
                    if self.collection.count_documents({"_id": warid, "allymembers": winner,}, limit = 1):
                        if self.collection.count_documents({"_id": warid, "enemymembers": loser}, limit = 1):
                            if g == 'yes':
                                view = ConfirmCancel(ctx.author)
                                await ctx.send(f"Are you sure? **{player.name}** will be the **WINNER** and {opponent.name} will be the **LOSER**.", view=view)
                                await view.wait()
                            else:
                                view = ConfirmCancel(opponent)
                                await ctx.send (f'{opponent.mention} Do you accept the log request? **{player}** Will be the winner.', view = view)
                                await view.wait()
                            if view.value == True:



                                war_data = self.collection.find_one({"_id": warid})
                                formats = war_data["wartype"]

                                allyffscore = war_data["allyscore"]
                                enemyffscore = war_data["enemyscore"]

                                if (allyffscore == 10) or (enemyffscore == 10):
                                    await ctx.send("A team has already reached 10 wins.")
                                    return


                                if formats == 'br':
                                    if winner == player.id:
                                        faction_name = war_data['teamone']
                                        efaction_name = war_data['teamtwo']                                       
                                        allymembers = war_data["allymembers"]
                                        actualally = []
                                        for i in allymembers:
                                            actualally.append(i)
                                        indexally = actualally.index(winner)

                                        enemymembers = war_data["enemymembers"]
                                        actualenemy = []
                                        for i in enemymembers:
                                            actualenemy.append(i)
                                        indexallyd = actualenemy.index(loser)
                                        enemyscored = war_data["enemyplayerscored"]
                                        enemyscored[indexallyd] += 1
                                        self.collection.update_one({"_id":warid}, {"$set": {"enemyplayerscored": enemyscored}})         
                                                                       
                                        allyscore = war_data["allyplayerscore"]
                                        allyscore[indexally] += 1
                                        allyscored = war_data["allyplayerscored"]
                                        allyscored[indexally] += 1
                                        self.collection.update_one({"_id":warid}, {"$set": {"allyplayerscored": allyscored}})
                                        self.collection.update_one({"_id":warid}, {"$set": {"allyplayerscore": allyscore}})
                                        enemyffscore = war_data["enemyscore"]

                                        history = None


                                        allyffscore = war_data["allyscore"] + 1
                                        self.collection.update_one({"_id":warid}, {"$inc": {"allyscore": 1}})

                                        await ctx.send(f"{player.mention} Won. Updated war scores")

                                        ranked_battle_embed = discord.Embed(
                                            title = f'{faction_name} {allyffscore} VS {efaction_name} {enemyffscore} {warid}',
                                            description = f'{ctx.message.author.mention} beat {opponent.mention} in {ctx.message.channel.mention}\n**Message Link** {ctx.message.jump_url}',
                                            colour = color
                                        )

                                        await self.bot.db.execute('UPDATE tournament SET teamscore = teamscore + 1 WHERE teams = $1', faction_name.lower())
                                        await self.bot.db.execute('UPDATE tournament SET wins = wins + 1, matches_played = matches_played + 1 WHERE player_id = $1', player.id)
                                        await self.bot.db.execute('UPDATE tournament SET matches_played = matches_played + 1 WHERE player_id = $1', opponent.id)


                                        ranking_channel = self.bot.get_channel(1091745597301723156)

                                        await ranking_channel.send(embed = ranked_battle_embed)

                                        flists = str(registered_check[0]['achievements'])
                                        new_admins = ''
                                        admins_list = self.listing(flists)
                                        for p,admin in enumerate(admins_list):
                                            if p == 0:
                                                new_admins += str(admin)
                                            elif p == 26:
                                                if int(admin) == 99:
                                                    admins_list[27] = 1
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   player.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  player.id)
                                                    await ctx.send("**Bronze Achievement Completed! ✦ Win 100 Clan Duels ✦**\n*10dc rewarded*")
                                                elif int(admin) == 249:
                                                    admins_list[27] = 2
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   player.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  player.id)
                                                    await ctx.send("**Silver Achievement Completed! ✦✦ Win 250 Clan Duels ✦✦**\n*25dc rewarded*")
                                                elif int(admin) == 499:
                                                    admins_list[27] = 3
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   player.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  player.id)
                                                    await ctx.send("**Gold Achievement Completed! ✦✦✦ Win 500 Clan Duels ✦✦✦**\n*50dc rewarded*")

                                                admin = int(admin) + 1
                                                new_admins += f' {admin}'                                                       
                                            else:
                                                new_admins += f' {admin}'  
                                        await self.bot.db.execute(f'UPDATE registered SET wwar = wwar + 1, wl = wl + 1 WHERE player_id = $1', player.id)       
                                        await self.bot.db.execute(f'UPDATE registered SET lwar = lwar + 1, wl = wl - 1 WHERE player_id = $1', opponent.id)

                                        await self.bot.db.execute(f"UPDATE wars SET wins = wins + 1 WHERE player_id = $1", player.id)    
                                        
                                        await self.bot.db.execute(f'UPDATE wars SET loses = loses + 1 WHERE player_id = $1', opponent.id) 


                                        await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, player.id)                                              
                                        if winner == player.id:
                                            self.collection.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                            self.collection.update_one({"_id": warid}, {"$push": {"history": f'🟢 **Won** `{player.name}` ⚔️ 🔴 **Lost** `{opponent.name}`'}})
                                            if history != None:
                                                self.collection.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.collection.update_one({"_id": warid}, {"$push": {"history": history}})                                                
                                            
                                        elif loser == player.id:
                                            self.collection.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                            self.collection.update_one({"_id": warid}, {"$push": {"history": f'🔴 **Lost** `{opponent.name}` ⚔️ 🟢 **Won** `{player.name}`'}})
                                            if history != None:
                                                self.collection.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.collection.update_one({"_id": warid}, {"$push": {"history": history}})                                            
                                    else:
                                        faction_name = war_data['teamone']
                                        efaction_name = war_data['teamtwo']  
                                        enemymembers = war_data["enemymembers"]
                                        actualenemy = []
                                        for i in enemymembers:
                                            actualenemy.append(i)
                                        indexenemy = actualenemy.index(loser)
                                        enemyscore = war_data["enemyplayerscore"]
                                        enemyscore[indexenemy] += 1
                                        enemyscored = war_data["enemyplayerscored"]
                                        enemyscored[indexenemy] += 1
                                        self.collection.update_one({"_id":warid}, {"$set": {"enemyplayerscored": enemyscored}})
                                        self.collection.update_one({"_id":warid}, {"$set": {"enemyplayerscore": enemyscore}})

                                        allymembers = war_data["allymembers"]
                                        actualally = []
                                        for i in allymembers:
                                            actualally.append(i)
                                        indexallyd = actualally.index(winner)
                                        allyscored = war_data["allyplayerscored"]
                                        allyscored[indexallyd] += 1
                                        self.collection.update_one({"_id":warid}, {"$set": {"allyplayerscored": allyscored}})    
                                        allyffscore = war_data["allyscore"]

                                        history = None

                                        enemyffscore = war_data["enemyscore"] + 1
                                        self.collection.update_one({"_id":warid}, {"$inc": {"enemyscore": 1}})


                                        await ctx.send(f"{player.mention} Won. Updated war scores")

                                        faction_name = war_data['teamone']
                                        efaction_name = war_data['teamtwo']

                                        ranked_battle_embed = discord.Embed(
                                            title = f'{faction_name} {allyffscore} VS {efaction_name} {enemyffscore} {warid}',
                                            description = f'{player.mention} beat {opponent.mention} in {ctx.message.channel.mention}\n**Message Link** {ctx.message.jump_url}',
                                            colour = color
                                        )

                                        await self.bot.db.execute('UPDATE tournament SET teamscore = teamscore + 1 WHERE teams = $1', efaction_name.lower())
                                        await self.bot.db.execute('UPDATE tournament SET wins = wins + 1, matches_played = matches_played + 1 WHERE player_id = $1', player.id)
                                        await self.bot.db.execute('UPDATE tournament SET matches_played = matches_played + 1 WHERE player_id = $1', opponent.id)

                                        ranking_channel = self.bot.get_channel(1091745597301723156)

                                        await ranking_channel.send(embed = ranked_battle_embed)      

                                        flists = str(registered_check[0]['achievements'])
                                        new_admins = ''
                                        admins_list = self.listing(flists)
                                        for p,admin in enumerate(admins_list):
                                            if p == 0:
                                                new_admins += str(admin)
                                            elif p == 26:
                                                if int(admin) == 99:
                                                    admins_list[27] = 1
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   player.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  player.id)
                                                    await ctx.send("**Bronze Achievement Completed! ✦ Win 100 Clan Duels ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                elif int(admin) == 249:
                                                    admins_list[27] = 2
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   player.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  player.id)
                                                    await ctx.send("**Silver Achievement Completed! ✦✦ Win 250 Clan Duels ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                elif int(admin) == 499:
                                                    admins_list[27] = 3
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   player.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  player.id)
                                                    await ctx.send("**Gold Achievement Completed! ✦✦✦ Win 500 Clan Duels ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                admin = int(admin) + 1
                                                new_admins += f' {admin}'                                                       
                                            else:
                                                new_admins += f' {admin}'  
                                                
                                        await self.bot.db.execute(f'UPDATE registered SET wwar = wwar + 1, wl = wl + 1 WHERE player_id = $1', player.id)       
                                        await self.bot.db.execute(f'UPDATE registered SET lwar = lwar + 1, wl = wl - 1 WHERE player_id = $1', opponent.id)

                                        war_check = await self.bot.db.fetch('SELECT * FROM wars WHERE player_id  = $1', player.id)
                                        await self.bot.db.execute(f"UPDATE wars SET wins = wins + 1 WHERE player_id = $1", player.id)    
                                        
                                        await self.bot.db.execute(f'UPDATE wars SET loses = loses + 1 WHERE player_id = $1', opponent.id) 


                                        await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, player.id)                                              
                                        if winner == player.id:
                                            self.collection.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                            self.collection.update_one({"_id": warid}, {"$push": {"history": f'🟢 **Won** `{player.name}` ⚔️ 🔴 **Lost** `{opponent.name}`'}})
                                            if history != None:
                                                self.collection.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.collection.update_one({"_id": warid}, {"$push": {"history": history}})                                               
                                        elif loser == player.id:
                                            self.collection.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                            self.collection.update_one({"_id": warid}, {"$push": {"history": f'🔴 **Lost** `{opponent.name}` ⚔️ 🟢 **Won** `{player.name}`'}})
                                            if history != None:
                                                self.collection.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.collection.update_one({"_id": warid}, {"$push": {"history": history}})            


                
                            elif view.value == False:
                                await ctx.send("Cancelled.")
                            else:
                                await ctx.send("Timed Out.")
                        else:
                            await ctx.send(f"Either **{opponent}** or **{player}** is not in the war.")
                    else:
                        await ctx.send(f"Either **{opponent}** or **{player}** is not in the war.")
                else:
                    await ctx.send(f"Incorrect War ID.")
            else:
                await ctx.send("You haven't registered yet! do `d!start` to register.")


    @commands.command(name ="tviewwar", aliases = ['tvv'], )
    async def vddsdiefdw_dfadfwar_command(self, ctx,*, warid = None):
        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

  
        if user_ban_list:
            await ctx.send('You are banned from the bot.')

        else:
            if warid == None:
                em = discord.Embed(
                    title = "Wars",
                    description = 'View a tournament war.\n\n**d!tviewwar [war ID] **',
                    colour = color
                )
                await ctx.send(embed = em)
            else:
                registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                if registered_check:            
                    if self.collection.count_documents({"_id": warid }, limit = 1):
                        load = await ctx.send("**Generating embed.**")
                        war_data = self.collection.find_one({"_id": warid}, {
                            "_id": 0,
                            "teamone": 1,
                            "teamtwo": 1,
                            "winscore": 1,
                            "allyscore": 1,
                            "enemyscore": 1,
                            "allymembersname": 1,
                            "enemymembersname": 1,
                            "allymembers": 1,
                            "allyplayerscore": 1,
                            "enemymembers": 1,
                            "enemyplayerscore": 1,
                            'allyplayerscored': 1,
                            'enemyplayerscored' : 1,
                            'wartype': 1,
                            'history':1,
                            'powerups':1
                        })

                        faction_name = war_data['teamone']
                        efaction_name = war_data['teamtwo']
                        winscore = war_data['winscore']
                        allyffscore = war_data['allyscore']
                        enemyffscore = war_data['enemyscore']
                        allymembers = war_data['allymembers']
                        allyscore = war_data['allyplayerscore']
                        allyscored = war_data['allyplayerscored']
                        enemymembers = war_data['enemymembers']
                        enemyscore = war_data['enemyplayerscore']
                        enemyscored = war_data['enemyplayerscored']
                        powerups = war_data['powerups']
                        formats = war_data['wartype']
                        logstrs = war_data['history']
                        logstrs.reverse()

                        profile = Image.open("vs.png")


                        pfp = Image.open("clandefault.png")
                        pfp.convert('RGBA')

                        pfp = pfp.resize((300,300))
                        profile.paste(pfp, (210,50),pfp.convert('RGBA'))

                        pfp = Image.open("clandefault.png")
                        pfp.convert('RGBA')
                       
                        pfp = pfp.resize((300,300))
                        profile.paste(pfp, (930,50),pfp.convert('RGBA'))

                        font = ImageFont.truetype("Pacifico-Regular.ttf", 60)

                        blurred = Image.new('RGBA', profile.size)
                        draw = ImageDraw.Draw(blurred)
                        draw.text((360, 450), text=faction_name, fill='black', font=font,anchor="mm")
                        blurred = blurred.filter(ImageFilter.BoxBlur(7))
                        profile.paste(blurred,blurred)
                        draw3 = ImageDraw.Draw(profile)
                        draw3.text((360, 450), faction_name, (255,255,255), font = font,anchor="mm")
                        
                        blurred = Image.new('RGBA', profile.size)
                        draw = ImageDraw.Draw(blurred)
                        draw.text((1080, 450), text=efaction_name, fill='black', font=font,anchor="mm")
                        blurred = blurred.filter(ImageFilter.BoxBlur(7))
                        profile.paste(blurred,blurred)
                        draw3 = ImageDraw.Draw(profile)
                        draw3.text((1080, 450), efaction_name, (255,255,255), font = font,anchor="mm")
                        

                        bytes = BytesIO()
                        rgb_img = profile.convert("RGB")
                        aspect_ratio = profile.width / profile.height
                        target_width = 1440
                        target_height = int(target_width / aspect_ratio)
                        rgb_img = profile.resize((target_width, target_height), resample=Image.BICUBIC)

                        rgb_img.save(bytes, format="PNG", quality=25)
                        bytes.seek(0)


                        if formats == 'br':
                            ally_score = list(zip(allymembers,allyscore,allyscored))
                            allyStr = ""
                            ok = 0
                            for i in ally_score:
                                
                                scorelist = list(i)
                                crudescore1 = int(scorelist[0])
                                crudescore2 = str(scorelist[1])
                                crudescore3 = str(scorelist[2])
                                if ok == 0:
                                    check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', int(crudescore1))

                                    if check[0]['blade'] == warid:
                                        allyStr += f'<@{crudescore1}> `{crudescore2}` / `{int(crudescore3)-int(crudescore2)}` :drop_of_blood:\n'
                                    else:
                                        allyStr += f'<@{crudescore1}> `{crudescore2}` / `{int(crudescore3)-int(crudescore2)}`\n'
                                    ok += 1
                                else:
                                    allyStr += f'<@{crudescore1}> `{crudescore2}` / `{int(crudescore3)-int(crudescore2)}`\n'
                            enemy_score = list(zip(enemymembers,enemyscore,enemyscored))
                            await load.edit("**Generating embed..**")
                            enemyStr = ""
                            no = 0
                            for i in enemy_score:
                                scorelist = list(i)
                                crudescore1 = int(scorelist[0])
                                crudescore2 = str(scorelist[1])
                                crudescore3 = str(scorelist[2])

                                if no == 0:
                                    check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', int(crudescore1))

                                    if check[0]['blade'] == warid:
                                        enemyStr += f'<@{crudescore1}> `{crudescore2}` / `{int(crudescore3)-int(crudescore2)}` :drop_of_blood:\n'
                                    else:
                                        enemyStr += f'<@{crudescore1}> `{crudescore2}` / `{int(crudescore3)-int(crudescore2)}`\n'
                                    
                                    no += 1
                                else:
                                    enemyStr += f'<@{crudescore1}> `{crudescore2}` / `{int(crudescore3)-int(crudescore2)}`\n'

                            await load.edit("**Generating embed...**")
                            logstr = ''
                            for i in logstrs:
                                logstr += f'{i}\n'
             
                            embedScore = discord.Embed(
                            title = f"{faction_name} VS {efaction_name} (First to {winscore})",
                            description = f'To log wins do d!tlog [Opponent]\n\u200b',
                            colour = color
                            )
                            embedScore.add_field(name = 'ＳＣＯＲＥＢＯＡＲＤ', value = f"", inline=False)
                            embedScore.add_field(name = f'{faction_name} {allyffscore}', value = allyStr)
                            embedScore.add_field(name = f'{efaction_name} {enemyffscore}', value = enemyStr)
                            embedScore.add_field(name = f'History', value= logstr, inline=False)

                            embedScore.set_image(url=f"attachment://rgb_img.png")
                            await load.edit("",file = discord.File(bytes,"rgb_img.png"),embed = embedScore)

                    else:
                        await ctx.send("Incorrect War ID.")
                else:
                    await ctx.send("You haven't registered yet! do `d!start` to register.")























    @commands.command(aliases=['tlkkkog'])
    async def tourloggnbozo(self,ctx,types : str = None, loser : discord.Member = None, ):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:  

            if (loser == None) or (types == None):
                await ctx.send("The command is `d!tlog rare/common @loser`")
                return
            else:
                if types == 'com':
                    types = 'common'
                elif types == 'coms':
                    types = 'common'                     
                if types == 'rares':
                    types = 'rare'

            channelist = [867504450498723850,1089940839960170567, 1089940862500352031, 1150446880719900764]
            if ctx.channel.id not in channelist:
                await ctx.send("This command can only be used in the Ranked Battling channels which are <#867504450498723850> <#1089940839960170567> <#1089940862500352031>")
                return   

            tourney_check = await self.bot.db.fetch('SELECT * FROM tournament WHERE player_id = $1 AND format = $2', ctx.author.id, types)
            if tourney_check:
                pass
            else:
                await ctx.send("You're not in the tournament or this format.")
                return
            loser_check = await self.bot.db.fetch('SELECT * FROM tournament WHERE player_id = $1 AND format = $2', loser.id, types)
            if loser_check:
                pass
            else:
                await ctx.send(f"{loser.mention} is not in the tournament or this format.")
                return
            
            if tourney_check[0]['alive'] == 'no':
                await ctx.send("You've been removed from the tournament.. either due to inactivity or by losing. DM a mod if inacivity is the reason and you would like to join back.")
                return
            else:
                pass

            if loser_check[0]['alive'] == 'no':
                await ctx.send("You've been removed from the tournament.. either due to inactivity or by losing. DM a mod if inacivity is the reason and you would like to join back.")
                return
            else:
                pass


            if loser_check[0]['groups'] == tourney_check[0]['groups']:
                pass
            else:
                await ctx.send("You both are not in the same group.. please check your group using the command. `d!tournament rare/common`")     
                return


            if tourney_check[0]['matches_played'] == 10:
                await ctx.send("You've already played the max amount of matches in this stage which is 10. ")
                return
            else:
                pass

            if loser_check[0]['matches_played'] == 10:
                await ctx.send("They have already played the max amount of matches in this stage which is 10. ")
                return
            else:
                pass            
            
 
            
      
            view = ConfirmCancel(loser)

            await ctx.send (f'{loser.mention} Do you accept the log request? **{ctx.author}** Will be the winner.', view = view)
            await view.wait()
            if view.value == True:
                winnerwins = tourney_check[0]['wins']
                wcareercheck = tourney_check[0]["career"]
                if wcareercheck == None:
                    wcareercheck = ''
                else:
                    pass
                wcareer = f'{wcareercheck}' + f'🟢 **Won** `{ctx.author.name}` ⚔️ 🔴 **Lost** `{loser.name}`\n'
                if winnerwins == 8:
                    pass
                else:
                    await self.bot.db.execute(f'UPDATE tournament SET wins = wins + 1 WHERE player_id = $1 AND format = $2',   ctx.author.id, types)
                if tourney_check[0]['matches_played'] >7 :
                    await self.bot.db.execute(f'UPDATE tournament SET buffer  = buffer + 1 WHERE player_id = $1 AND format = $2',   ctx.author.id, types)
                await self.bot.db.execute(f'UPDATE tournament SET matches_played = matches_played + 1, career = $1 WHERE player_id = $2 AND format = $3', wcareer,  ctx.author.id, types)
                

                careercheck = loser_check[0]["career"]
                if careercheck == None:
                    careercheck = ''
                else:
                    pass

                lcareer = f'{careercheck}' + f'🔴 **Lost** `{loser.name}` ⚔️ 🟢 **Won** `{ctx.author.name}`\n'

                if loser_check[0]['matches_played'] > 7:
                    await self.bot.db.execute(f'UPDATE tournament SET wins = wins - 1 WHERE player_id = $1 AND format = $2',  loser.id, types)
                    await self.bot.db.execute(f'UPDATE tournament SET buffer  = buffer - 1 WHERE player_id = $1 AND format = $2',   loser.id, types)
                else:
                    pass
                await self.bot.db.execute(f'UPDATE tournament SET matches_played = matches_played + 1, career = $1 WHERE player_id = $2 AND format = $3', lcareer,    loser.id, types)
                
                await ctx.send(f"{ctx.author.mention} was the winner! Updated Group Leaderboard..")

            elif view.value == False:
                await ctx.send("Cancelled.")
            else:
                await ctx.send("Timed out.")
    
        else:
            await ctx.send("You haven't registered yet! Please do `d!start` do register.")

    @commands.command(aliases=['career'])
    async def tourgaddfnbozo(self,ctx,types : str = None, loser : discord.Member = None, ):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:   

            if loser == None:
                loser = ctx.author

            if (types == None):
                await ctx.send("The command is `d!career rare/common @someonelse`")
                return
            else:
                if types == 'com':
                    types = 'common'
                elif types == 'coms':
                    types = 'common'                     
                if types == 'rares':
                    types = 'rare'

            loser_check = await self.bot.db.fetch('SELECT * FROM tournament WHERE player_id = $1 AND format = $2', loser.id, types)
            if loser_check:
                pass
            else:
                await ctx.send(f"{loser.mention} is not in the tournament or this format.")
                return 
            
            careerStr = loser_check[0]['career']

            em = discord.Embed(
            title = f"{loser.name.title()} Career",
            description = f"Past matches will be shown here.\n\n{careerStr}",
            colour = color
            )

            em.set_footer(text=f"Played {loser_check[0]['matches_played']} matches")            

            await ctx.send(embed = em)

        else:
            await ctx.send("You haven't registered yet! Please do `d!start` do register.")


    @commands.command(aliases=['forcheck'])
    async def groupsnbozo(self,ctx, types : str):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if ctx.author.id == 0:    
                
            if types == 'common':  
                cmfor = 'common'
                lb = await self.bot.db.fetch(f'SELECT * FROM tournament WHERE format = $1 AND matches_played > 0', cmfor)
            else:
                    
                rrfor = 'rare'
                lb = await self.bot.db.fetch(f'SELECT * FROM tournament WHERE format = $1 AND matches_played > 0' , rrfor)

            num = 0
            numbre = 0
            stringto = ''
            for i in lb:
                
                stringto += f"<@{i['player_id']}> "

            em = discord.Embed(
            title = f"all",
            description = f"everymember\n\n {stringto}",
            colour = color
            )            
            
            await ctx.send(embed = em)

    
        else:
            await ctx.send("You haven't registered yet! Please do `d!start` do register.")

    @commands.command(aliases=['send'])
    async def groupsfadfadsnbozo(self,ctx, types : str):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if ctx.author.id == 0:    
            message = f"**Things changed...**\n•__Buffer matches__, are 2 matches in the end that add on to your win score. If you have 8 wins you wont get more than 8 wins.\n\n• The amount of wins you have is the most important stat in this tournament and will determine if you pass onto the next stage or not. The winrate will always be by 8 matches, the special properties of buffer matches make it so they're not counted.\n\n• You have the next 48 hours and for this stage you must do the following: **BE THE PLAYER WITH THE HIGHEST AMOUNT OF WINS**\n\n• You can check your groups by doing `d!tournament rare/common`\n\nGoodluck! Go to the DOMINANT in the battling channels https://discord.com/channels/774883579472904222/867504450498723850 https://discord.com/channels/774883579472904222/1089940839960170567 https://discord.com/channels/774883579472904222/1089940862500352031"
            

            em = discord.Embed(
            title = f"**The Tournament Stage Has Begun! STAGE 3**",
            description = f"{message}",
            colour = color
            )           
            await ctx.send(embed = em)
            alive = 'yes'
            if types == 'common':  
                cmfor = 'common'
                lb = await self.bot.db.fetch(f'SELECT * FROM tournament WHERE format = $1 AND alive = $2', cmfor, alive)
            else:
                    
                rrfor = 'rare'
                lb = await self.bot.db.fetch(f'SELECT * FROM tournament WHERE format = $1 AND alive = $2', rrfor, alive)
            for i in lb:

                member  = await self.bot.fetch_user(i['player_id'])
                
                try:
                    await member.send(embed = em)
                    print(f"sent to {i['player_name']}")
                except Exception as e:
                    pass 

    
        else:
            await ctx.send("You haven't registered yet! Please do `d!start` do register.")


    @commands.command(aliases=['shuffled'])
    async def shufdadffle(self,ctx, types : str):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if ctx.author.id == 0:        
            message = f"**Things changed...**\n• Introducing __Buffer matches__, now a player can play 10 matches but 10 are mandatory to pass. The last 2 matches are called buffer matches and can add onto your score. For example if you have 8 wins, if you win a buffer match you will now have 9 wins but if you choose to play a buffer match but lose you will now have 7 wins. If you have 10 wins you wont get more than 10 wins.\n\n• Your win rate is the most important stat in this tournament and will determine if you pass onto the next stage or not. The winrate will always be by 10 matches, the special properties of buffer matches make it so they're not counted.\n\n**New Commands added...**\n- `d!tlog rare/common @loser`\n- `d!tcareer rare/common`\n\n**Important information**\n• You have the next 24 hours and for this stage you must do the following: **COMPLETE AT LEAST 10 MATCHES TO MOVE ON**\n• You can check your groups by doing `d!tournament rare/common`\n• There will be a 2hour break between each stage and that's all.\n\nGoodluck! Go to the DOMINANT in the battling channels https://discord.com/channels/774883579472904222/867504450498723850 https://discord.com/channels/774883579472904222/1089940839960170567 https://discord.com/channels/774883579472904222/1089940862500352031"
            
            alive = 'yes'
            if types == 'common':  
                types = 'common'
                lb = await self.bot.db.fetch(f'SELECT * FROM tournament WHERE format = $1 AND alive = $2', types, alive)
            else:
                    
                types = 'rare'
                lb = await self.bot.db.fetch(f'SELECT * FROM tournament WHERE format = $1 AND alive = $2', types , alive)

            random.shuffle(lb)
            num = 0
            checknum =0
            for i in lb:
                if checknum % 6 == 0:
                    num += 1
                checknum += 1
                print(num)
                await self.bot.db.execute(f'UPDATE tournament SET groups = $1 WHERE player_id = $2 AND format = $3',num, i["player_id"], types)
                   
        else:
            await ctx.send("You haven't registered yet! Please do `d!start` do register.")


    @commands.command(aliases=['tttlb', 'leaderdsadsaboard'])
    async def notbozo(self,ctx):
        if self.collection.count_documents({ "_id": ctx.author.id }, limit = 1):
            sortd = list(self.collection.aggregate([{"$sort" : {"score" : -1}}, {"$limit" : 10}]))
            load = await ctx.send("**Creating leaderboard.**")
            bid = []
            for faction in sortd:
                
                bid.append(faction["_id"])
            await load.edit("**Creating leaderboard..**")
            id = []
            for i in bid:
                member  = f'<@{i}>'
                id.append(member)
            await load.edit("**Creating leaderboard...**")
            score = []
            for faction in sortd:
                score.append(faction["score"])

            byscore = list(zip(id,score))
            scoreStr = ""
            serial = 0
            await load.edit("**Creating leaderboard.**")
            for i in byscore:
                scorelist = list(i)
                crudescore1 = str(scorelist[0])
                crudescore2 = scorelist[1]
                crudescore22 = round(crudescore2, 1)
                serial += 1

                if serial == 1:
                    apple = '》'
                    badge = ':first_place:'
                if serial == 2:
                    apple = '》'
                    badge = ':second_place:'
                if serial == 3:
                    apple = '》'
                    badge = ':third_place:'
                if serial > 3:
                    apple = '》'
                    badge = ' '
                scoreStr += f'**{serial}# {crudescore1}** {apple} `{crudescore22}` {badge}\n'
            await load.edit("**Creating leaderboard..**")
            yourscore = list(self.collection.find( {"_id": ctx.author.id}))
            name = yourscore[0]['_id']
            scorett = yourscore[0]["score"]
            scoret = round(scorett, 1)
            memberd  = await self.bot.fetch_user(name)
            sortdd = list(self.collection.aggregate([{"$sort" : {"score" : -1}}]))
            bidnew = []
            for faction in sortdd:
                
                bidnew.append(faction["_id"])
            scoredd = []
            for faction in sortdd:
                scoredd.append(faction["score"])
            await load.edit("**Creating leaderboard...**")
            byscord = list(zip(bidnew,scoredd))
            res = sorted(byscord, key = lambda x: x[1], reverse=True)
            carl = 0
            for i in res:
                carl += 1
                scorelist = list(i)
                crudescore1 = str(scorelist[0])
                if crudescore1 == str(ctx.author.id):
                    pindex = carl
            if pindex == 1:
                papple = ':first_place:'
            if pindex == 2:
                papple = ':second_place:'
            if pindex == 3:
                papple = ':third_place:'
            if pindex > 3:
                papple = '》'
            if pindex > 20:
                playerStr = f'**{pindex}# {memberd.name}** {papple} `{scoret}`  (You will get 3 points for your next win)'
            elif pindex > 10:
                playerStr = f'**{pindex}# {memberd.name}** {papple} `{scoret}`  (You will get 2 points for your next win)'
            else:
                playerStr = f'**{pindex}# {memberd.name}** {papple} `{scoret}`'
            await load.edit("**Done!**")
            embed = discord.Embed(
                title = f"Leaderboard",
                description = f"Keep dueling!!\n\n{scoreStr}**...**\n{playerStr}",
                colour = color
            )
            embed.set_footer(text = f"Not on the leaderboard? Don't worry! You get 2 points if you're below 10th and 3 points if you're below 20th.")
            await load.edit("	",embed = embed)
        else:
            await ctx.send("You've not entered the tournament yet! Do d!enter to join.")

    @commands.command(name = 'tttrewtlog')
    async def siuu_log(self,ctx, opponent : discord.Member = None):
        if opponent == None:
            em = discord.Embed(
                title = "Help 🛠️",
                description = '**d!tlog [Mention Opponent]**',
                colour = color
            )
            await ctx.send(embed = em)
            
        else:
            if opponent.id == ctx.author.id:
                    await ctx.send("You can't duel yourself!")
            else:
                
                user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

                player_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', opponent.id)
                if (not user_ban_list) and (not player_ban_list):
                    if self.collection.count_documents({ "_id": ctx.author.id }, limit = 1) != 1:
                        await ctx.send(f"**{ctx.author}** has not registered yet!")
                    elif self.collection.count_documents({ "_id": opponent.id }, limit = 1) != 1:
                        await ctx.send(f"**{opponent}** has not registered yet!")
                    else:
      
                        view = ConfirmCancel(opponent)

                        await ctx.send (f'{opponent.mention} Do you accept the log request? **{ctx.author}** Will be the winner.', view = view)
                        await view.wait()
                        if view.value == True:
                            player = list(self.collection.find( {"_id": ctx.author.id}))
                            puishin = player[0]['placement']
                            if puishin == 0:
                                self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"score": 1}, })
                                self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"placement": 1}, })
                                self.collection.update_one({"_id": opponent.id}, {"$inc": {"placement": 1}, })
                            else:

                                sortdd = list(self.collection.aggregate([{"$sort" : {"score" : -1}}]))
                                bidnew = []
                                for faction in sortdd:
                                    
                                    bidnew.append(faction["_id"])
                                scoredd = []
                                for faction in sortdd:
                                    scoredd.append(faction["score"])

                                byscord = list(zip(bidnew,scoredd))
                                res = sorted(byscord, key = lambda x: x[1], reverse=True)
                                carl = 0
                                for i in res:
                                    carl += 1
                                    scorelist = list(i)
                                    crudescore1 = str(scorelist[0])
                                    if crudescore1 == str(ctx.author.id):
                                        pindex = carl
                                if pindex > 20:
                                    self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"score": 3}, })
                                    self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"placement": 3}, })
                                    self.collection.update_one({"_id": opponent.id}, {"$inc": {"placement": 1}, })
                                elif pindex > 10:
                                    self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"score": 2}, })
                                    self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"placement": 2}, })
                                    self.collection.update_one({"_id": opponent.id}, {"$inc": {"placement": 1}, })
                                else:
                                    self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"score": 1}, })
                                    self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"placement": 1}, })
                                    self.collection.update_one({"_id": opponent.id}, {"$inc": {"placement": 1}, })

                            await ctx.send(f"{ctx.author.mention} was the winner!")

                                
                        elif view.value == False:
                            await ctx.send("Cancelled.")
                        else:
                            await ctx.send("Timed Out.")

                elif not user_ban_list and player_ban_list:
                    await ctx.send('That person is banned.')

                elif user_ban_list and not player_ban_list:
                    await ctx.send('You are banned.')

                elif user_ban_list and player_ban_list:
                    await ctx.send('Both of you are banned.')
    @commands.group(name = 'abydsass', invoke_without_command = True)
    async def abyss_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            emo = '<:abyss:1096728826702213231>'
            pokeball = '<:pokeball:919647297808240680>'
            masterball = '<:MasterBall:1097952840045039677>'  
            em = discord.Embed(
                title = f'{emo} The Abyss ',
                description = 'Challenge a player from the abyss to take their spot.. `d!abyss log`\nChallenging the Elites costs **50dc** and Lowers costs **35dc**\nElites are rewarded **30dc** whereas Lowers are rewarded **20dc**',
                colour = 0x000000                   
            )
            rare_check1 = await self.bot.db.fetch('SELECT * FROM rank_system WHERE floor = 1')
            rare_check2 = await self.bot.db.fetch('SELECT * FROM rank_system WHERE floor = 2')
            rare_check3 = await self.bot.db.fetch('SELECT * FROM rank_system WHERE floor = 3')
            rare_check4 = await self.bot.db.fetch('SELECT * FROM rank_system WHERE floor = 4')
            rare_check5 = await self.bot.db.fetch('SELECT * FROM rank_system WHERE floor = 5')
            rare1 = str(rare_check1[0]['player_id'])
            rare2 = str(rare_check2[0]['player_id'])
            rare3 = str(rare_check3[0]['player_id'])
            rare4 = str(rare_check4[0]['player_id'])
            rare5 = str(rare_check5[0]['player_id'])
            rare_check1 = await self.bot.db.fetch('SELECT * FROM common_system WHERE floor = 1')
            rare_check2 = await self.bot.db.fetch('SELECT * FROM common_system WHERE floor = 2')
            rare_check3 = await self.bot.db.fetch('SELECT * FROM common_system WHERE floor = 3')
            rare_check4 = await self.bot.db.fetch('SELECT * FROM common_system WHERE floor = 4')
            rare_check5 = await self.bot.db.fetch('SELECT * FROM common_system WHERE floor = 5')
            com1 = str(rare_check1[0]['player_id'])
            com2 = str(rare_check2[0]['player_id'])
            com3 = str(rare_check3[0]['player_id'])
            com4 = str(rare_check4[0]['player_id'])
            com5 = str(rare_check5[0]['player_id'])
            em.add_field(name = f'Rares Elite {masterball}', value = f'**1#** <@{rare1}>\n\n**Rare Lower** {masterball}\n**2#** <@{rare2}>\n**3#** <@{rare3}>\n**4#** <@{rare4}>\n**5#** <@{rare5}>')
            em.add_field(name = f'Common Elite {pokeball}', value = f'**1#** <@{com1}>\n\n**Common Lower** {pokeball}\n**2#** <@{com2}>\n**3#** <@{com3}>\n**4#** <@{com4}>\n**5#** <@{com5}>')
            em.add_field(name = f'Rules', value = f'● Abyss Elites/Members ALWAYS get match sending priority\n\n● Rares Elite:\nThe Abyss Lower can see all the pokemons you will use before the duel. Not the order! \n\n● Common Elite:\nThe Abyss Elite can ban 5 pokemon, but may use anything that they want to.\n\n● Rares Lower:\nThe Abyss Lower can see 2 out of the 3 pokemon you will use before the duel. Not the order!\n\n● Commons Lower:\nThe Abyss Lower can ban 3 pokemon, but may use anything that they want to.',inline=False)
            em.set_image(url=f"attachment://xtheabyss.png")
            em.set_footer(text= f"Organization leader Rad")
            await ctx.send(file = discord.File("xtheabyss.png"),embed = em)
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')
    @abyss_command.command(name='lsdog')
    async def abyss_rank_log(self,ctx,member : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        member_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)
        if registered_check:
            if member_check:
                if member == None:
                    em = discord.Embed(
                        title = "Help 🛠️",
                        description = '**d!abyss log [Mention Opponent]**',
                        colour = 0x5404b0
                    )
                    await ctx.send(embed = em)
                    
                else:
                    view = ConfirmCancel(member)
                    await ctx.send(f"Do you accept this log? {member.mention}, **{ctx.author.name}** will be the **WINNER** of this challenge. *abyss duels are bo3*", view = view)
                    await view.wait()
                    if view.value == True:
                        guild = self.bot.get_guild(774883579472904222)
                        role = guild.get_role(949659557200822283)
                        role2 = guild.get_role(1104134096252305490)
                        author_check_rare = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', ctx.author.id)
                        author_check_com = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', ctx.author.id)
                        author_check_raree = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', member.id)
                        author_check_comm = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', member.id)
                        if (author_check_rare[0]['floor'] != 0) or (author_check_com[0]['floor'] != 0):
                            if (author_check_comm[0]['floor'] != 0) or (author_check_raree[0]['floor'] != 0):
                                await ctx.send("Abyss members can't duel each other.")
                                return
                            else:
                                pass
                        else:
                            if (author_check_comm[0]['floor'] != 0) or (author_check_raree[0]['floor'] != 0):
                                pass
                            else:
                                await ctx.send("None of you are from **The Abyss**")
                                return                                
                        if author_check_rare[0]['floor'] != 0:
                            if author_check_rare[0]['floor'] == 1:
                                if member_check[0]['banner_pieces'] < 50:
                                    await ctx.send("Opponent doesn't have enough dc! You need **75dc** to challenge an Elite.")
                                    return
                                else:
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - 50 WHERE player_id = $1', member.id)
                                    await ctx.send(f"**The Abyss** took **50dc** from {member.mention}")
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 30 WHERE player_id = $1', ctx.author.id)
                                    await ctx.send(f"**The Abyss** awarded **30dc** to {ctx.author.mention}")
                            else:
                                if member_check[0]['banner_pieces'] < 35:
                                    await ctx.send("Opponent doesn't have enough dc! You need **75dc** to challenge an Elite.")
                                    return
                                else:
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - 35 WHERE player_id = $1', member.id)
                                    await ctx.send(f"**The Abyss** took **35dc** from {member.mention}")
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 20 WHERE player_id = $1', ctx.author.id)
                                    await ctx.send(f"**The Abyss** awarded **20dc** to {ctx.author.mention}")
                            if registered_check[0]['special'] is None:
                                await self.bot.db.execute(f'UPDATE registered SET special = 2 WHERE player_id = $1', ctx.author.id)    
                            else:                        
                                await self.bot.db.execute(f'UPDATE registered SET special = special + 2 WHERE player_id = $1', ctx.author.id)



                        elif author_check_com[0]['floor'] != 0:

                            if author_check_com[0]['floor'] == 1:
                                if member_check[0]['banner_pieces'] < 50:
                                    await ctx.send("Opponent doesn't have enough dc! You need **75dc** to challenge an Elite.")
                                    return
                                else:
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - 50 WHERE player_id = $1', member.id)
                                    await ctx.send(f"**The Abyss** took **50dc** from {member.mention}")
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 30 WHERE player_id = $1', ctx.author.id)
                                    await ctx.send(f"**The Abyss** awarded **30dc** to {ctx.author.mention}")
                            else:
                                if member_check[0]['banner_pieces'] < 35:
                                    await ctx.send("Opponent doesn't have enough dc! You need **75dc** to challenge an Elite.")
                                    return
                                else:
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - 35 WHERE player_id = $1', member.id)
                                    await ctx.send(f"**The Abyss** took **35dc** from {member.mention}")
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 20 WHERE player_id = $1', ctx.author.id)
                                    await ctx.send(f"**The Abyss** awarded **20dc** to {ctx.author.mention}")
                            if registered_check[0]['special'] is None:
                                await self.bot.db.execute(f'UPDATE registered SET special = 2 WHERE player_id = $1', ctx.author.id)    
                            else:                        
                                await self.bot.db.execute(f'UPDATE registered SET special = special + 2 WHERE player_id = $1', ctx.author.id)


                                
                        else:

                            await self.bot.db.execute(f'UPDATE registered SET special = NULL WHERE player_id = $1', member.id)
                            await self.bot.db.execute(f'UPDATE registered SET special = 0 WHERE player_id = $1', ctx.author.id)
                            
                            await ctx.send(f"Welcome to **The Abyss** {ctx.author.mention}")
                            if author_check_comm[0]['floor'] != 0:
                                floor = author_check_comm[0]['floor']
                                await self.bot.db.execute(f'UPDATE common_system SET floor = $1 WHERE player_id = $2', floor,ctx.author.id)
                                await self.bot.db.execute(f'UPDATE common_system SET floor = 0 WHERE player_id = $1', member.id)
                                if author_check_comm[0]['floor'] == 1:
                                    await ctx.author.add_roles(role2)
                                    await member.remove_roles(role2)
                                else:
                                    await ctx.author.add_roles(role)
                                    await member.remove_roles(role)
                                await ctx.send(f"You have been kicked from **The Abyss** {member.mention}")


                            elif author_check_raree[0]['floor'] != 0:
                                floor = author_check_raree[0]['floor']
                                await self.bot.db.execute(f'UPDATE rank_system SET floor = $1 WHERE player_id = $2', floor, ctx.author.id)
                                await self.bot.db.execute(f'UPDATE rank_system SET floor = 0 WHERE player_id = $1', member.id)
                                if author_check_raree[0]['floor'] == 1:
                                    await ctx.author.add_roles(role2)
                                    await member.remove_roles(role2)
                                else:
                                    await ctx.author.add_roles(role)
                                    await member.remove_roles(role)
                                
                                await ctx.send(f"You have been kicked from **The Abyss** {member.mention}")
                            else:
                                await ctx.send("Unkown Error")

                    elif view.value == False:
                        await ctx.send("Denied.")
                    else:
                        await ctx.send("Timed out.")                     
            else:
                await ctx.send('Member has not registered yet! Use `d!start` to register.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @abyss_command.command(name='chnjeck')
    async def abyss_check_log(self,ctx,member : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        member_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)
        if registered_check:
            if member_check:
                if member == None:
                    em = discord.Embed(
                        title = "Help 🛠️",
                        description = '**d!abyss check [Mention]**',
                        colour = 0x5404b0
                    )
                    await ctx.send(embed = em)
                    
                else:               
                    author_check_rare = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', ctx.author.id)
                    author_check_com = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', ctx.author.id)
                    if (author_check_rare[0]['floor'] != 0) or (author_check_com[0]['floor'] != 0):
                        if member_check[0]['banner_pieces'] < 75:
                            if member_check[0]['banner_pieces'] < 50:
                                await ctx.send("Opponent doesn't have enough dc to challenge an **Elite** or a **Lower**.")
                            else:
                                await ctx.send(f"Opponent doesn't have enough dc to challenge an **Elite**.")
                        else:
                            await ctx.send(f"Opponent has enough dc to challenge both **Elites** and **Lowers**.")
                    else:
                        await ctx.send("You're not in **The Abyss**")
            else:
                await ctx.send("Member has not registered yet! Use `d!start` to register.")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'achievements', aliases=['achieve'] )
    async def achievement_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if registered_check:
            
            em1 = discord.Embed(
                title = 'Achievements',
                description = 'Complete achievements to get rewarded!',
                colour = color
            )

            achieve = str(registered_check[0]['achievements'])
            no1 = '<:no1:1100516249085161553>'
            no2 =   '<:no2:1100516250507018250>'
            no3=    '<:no3:1100516253275279532>'
            s4=    '<:s4:1100520820998148156>' 
            s2=    '<:s2:1100520817827262515>'
            s3=    '<:s3:1100520813138026606>' 
            s1=    '<:s1:1100520815734308945>'
            g4=    '<:g4:1100520811212841054>'
            g3=    '<:g3:1100520804539703366>'
            g2=    '<:g2:1100520807282778193>'
            g1=    '<:g1:1100520808922751036>'
            b1 = '<:b1:1100515527245439007>'
            b2=    '<:b2:1100515528893796382>'
            b3=    '<:b3:1100515524502372422>'
            b4=    '<:b4:1100515532039528498>'

            achieve_list = self.llisting(achieve)
            strs = ['Play 250 matches','Play 500 matches', 'Play 1000 matches',  'Win 100 matches','Win 300 matches','Win 700 matches', 'Get 1000 points', 'Get 2500 points', 'Get 5000 points', 'Get a streak of 10', 'Get a streak of 15','Get a streak of 25','Buy 7 Keys','Buy 15 Keys','Buy 30 Keys','Buy 10 items','Buy 25 items','Buy 50 items','Open 10 Lootboxes','Open 20 Boxes','Open 30 Boxes']
            tots = [250,500,1000,100,300,700,1000,2500,5000,10,15,25,7,15,30,10,25,50,10,20,30]
            rew = [10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50]

            for p,admin in enumerate(achieve_list):
                a = 0
                if (p % 2 == 0) and (p < 14): 
                    forstr = int((p*3)/2)
                    realdex = p    
      
                    if achieve_list[realdex+1] == 0:
                        
                        badge1 = '<:bronze1:1112807329512038400>'
                        
                        str1 = strs[forstr]
                        total = tots[forstr]
                        reward = f'x1 LootBox + {rew[forstr]}' 
                        if achieve_list[realdex]/total < 1/10:
                            stat1 = f'{no1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 1/10) and (achieve_list[realdex]/total < 2/10):
                            stat1 = f'{b1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 2/10) and (achieve_list[realdex]/total < 3/10):
                            stat1 = f'{b1}{b2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 3/10) and (achieve_list[realdex]/total < 4/10):
                            stat1 = f'{b1}{b2}{b2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 4/10) and (achieve_list[realdex]/total < 5/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 5/10) and (achieve_list[realdex]/total < 6/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 6/10) and (achieve_list[realdex]/total < 7/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{no2}{no2}{no2}{no3}'                        
                        elif (achieve_list[realdex]/total >= 7/10) and (achieve_list[realdex]/total < 8/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 8/10) and (achieve_list[realdex]/total < 9/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 9/10) and (achieve_list[realdex]/total < 9.5/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{no3}'
                        elif (achieve_list[realdex]/total >= 9.5/10) and (achieve_list[realdex]/total < 10/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b3}'
                        else: 
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b4}'

                    elif achieve_list[realdex+1] == 1:
                        badge1 = '<:bronze2:1112807988969873418>'
                        str1 = strs[forstr+1]  
                        total = tots[forstr+1]   
                        reward = f'x1 LootBox + {rew[forstr+1]}'
                        if achieve_list[realdex]/total < 1/10:
                            stat1 = f'{no1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 1/10) and (achieve_list[realdex]/total < 2/10):
                            stat1 = f'{s1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 2/10) and (achieve_list[realdex]/total < 3/10):
                            stat1 = f'{s1}{s2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 3/10) and (achieve_list[realdex]/total < 4/10):
                            stat1 = f'{s1}{s2}{s2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 4/10) and (achieve_list[realdex]/total < 5/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 5/10) and (achieve_list[realdex]/total < 6/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 6/10) and (achieve_list[realdex]/total < 7/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{no2}{no2}{no2}{no3}'                        
                        elif (achieve_list[realdex]/total >= 7/10) and (achieve_list[realdex]/total < 8/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 8/10) and (achieve_list[realdex]/total < 9/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 9/10) and (achieve_list[realdex]/total < 9.5/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{no3}'
                        elif (achieve_list[realdex]/total >= 9.5/10) and (achieve_list[realdex]/total < 10/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s3}'
                        else: 
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s4}'

                    elif achieve_list[realdex+1] == 2:
                        badge1 = '<:bronze3:1112807867741909094>'
                        str1 = strs[forstr+2]
                        total = tots[forstr+2]
                        reward = f'x1 LootBox + {rew[forstr+2]}'
                        if achieve_list[realdex]/total < 1/10:
                            stat1 = f'{no1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 1/10) and (achieve_list[realdex]/total < 2/10):
                            stat1 = f'{g1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 2/10) and (achieve_list[realdex]/total < 3/10):
                            stat1 = f'{g1}{g2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 3/10) and (achieve_list[realdex]/total < 4/10):
                            stat1 = f'{g1}{g2}{g2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 4/10) and (achieve_list[realdex]/total < 5/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 5/10) and (achieve_list[realdex]/total < 6/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 6/10) and (achieve_list[realdex]/total < 7/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{no2}{no2}{no2}{no3}'                        
                        elif (achieve_list[realdex]/total >= 7/10) and (achieve_list[realdex]/total < 8/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 8/10) and (achieve_list[realdex]/total < 9/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 9/10) and (achieve_list[realdex]/total < 9.5/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{no3}'
                        elif (achieve_list[realdex]/total >= 9.5/10) and (achieve_list[realdex]/total < 10/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g3}'
                        else: 
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g4}'        
                    else: 
                        badge1 = '<:bronze3:1112807867741909094>'
                        str1 = strs[forstr+2]
                        total = tots[forstr+2]
                        reward = 'Completed!' 
                        stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g4}'
                        a = 1  
                    if a == 1:
                        em1.add_field(name = f'{str1}', value = f'{badge1} {stat1} `{achieve_list[realdex]}/{total}`\n**Completed! ✅**',inline=False)
                        a = 0
                    else:
                        em1.add_field(name = f'{str1}', value = f'{badge1} {stat1} `{achieve_list[realdex]}/{total}`\n**Reward: **{reward} Dom Coins',inline=False)

                else:
                    pass

            strs = ['Play 100 Casual matches','Play 250 Casual matches','Play 500 Casual matches','End top 8 in a weekly leaderboard','End top 8 in a weekly leaderboard 3 times','End top 8 in a weekly leaderboard 5 times', 'Complete 20 daily quests','Complete 50 daily quests','Complete 100 daily quests','Win 100 Gambles','Win 250 Gambles','Win 500 Gambles','Play 250 Gambles','Play 500 Gambles','Play 1000 Gambles', 'Win 10 Gambles in a row', 'Win 15 Gambles in a row', 'Win 25 Gambles in a row', 'Win 100 Clan duels', 'Win 250 Clan duels', 'Win 500 Clan duels']
            tots = [100,250,500,1,3,5,20,50,100,100,250,500,250,500,1000,10,20,30,100,250,500]
            rew = [10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50]
            em2 = discord.Embed(
                title = 'Achievements',
                description = 'Achievements: *(Page 2/3)*',
                colour = color
            )
            
            for p,admin in enumerate(achieve_list):
                a = 0
                if (p % 2 == 0) and (p < 14): 
                    forstr = int((p*3)/2)
                    realdex = p+14

                    if achieve_list[realdex+1] == 0:
                        
                        badge1 = '<:bronze1:1112807329512038400>'
                        
                        str1 = strs[forstr]
                        total = tots[forstr]
                        reward = f'x1 LootBox + {rew[forstr]}' 
                        if achieve_list[realdex]/total < 1/10:
                            stat1 = f'{no1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 1/10) and (achieve_list[realdex]/total < 2/10):
                            stat1 = f'{b1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 2/10) and (achieve_list[realdex]/total < 3/10):
                            stat1 = f'{b1}{b2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 3/10) and (achieve_list[realdex]/total < 4/10):
                            stat1 = f'{b1}{b2}{b2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 4/10) and (achieve_list[realdex]/total < 5/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 5/10) and (achieve_list[realdex]/total < 6/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 6/10) and (achieve_list[realdex]/total < 7/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{no2}{no2}{no2}{no3}'                        
                        elif (achieve_list[realdex]/total >= 7/10) and (achieve_list[realdex]/total < 8/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 8/10) and (achieve_list[realdex]/total < 9/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 9/10) and (achieve_list[realdex]/total < 9.5/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{no3}'
                        elif (achieve_list[realdex]/total >= 9.5/10) and (achieve_list[realdex]/total < 10/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b3}'
                        else: 
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b4}'

                    elif achieve_list[realdex+1] == 1:
                        badge1 = '<:bronze2:1112807988969873418>'
                        str1 = strs[forstr+1]  
                        total = tots[forstr+1]   
                        reward = f'x1 LootBox + {rew[forstr+1]}'
                        
                        if achieve_list[realdex]/total < 1/10:
                            stat1 = f'{no1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 1/10) and (achieve_list[realdex]/total < 2/10):
                            stat1 = f'{s1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 2/10) and (achieve_list[realdex]/total < 3/10):
                            stat1 = f'{s1}{s2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 3/10) and (achieve_list[realdex]/total < 4/10):
                            stat1 = f'{s1}{s2}{s2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 4/10) and (achieve_list[realdex]/total < 5/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 5/10) and (achieve_list[realdex]/total < 6/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 6/10) and (achieve_list[realdex]/total < 7/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{no2}{no2}{no2}{no3}'                        
                        elif (achieve_list[realdex]/total >= 7/10) and (achieve_list[realdex]/total < 8/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 8/10) and (achieve_list[realdex]/total < 9/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 9/10) and (achieve_list[realdex]/total < 9.5/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{no3}'
                        elif (achieve_list[realdex]/total >= 9.5/10) and (achieve_list[realdex]/total < 10/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s3}'
                        else: 
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s4}'

                    elif achieve_list[realdex+1] == 2:
                        badge1 = '<:bronze3:1112807867741909094>'
                        str1 = strs[forstr+2]
                        total = tots[forstr+2]
                        reward = f'x1 LootBox + {rew[forstr+2]}'
                        if achieve_list[realdex]/total < 1/10:
                            stat1 = f'{no1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 1/10) and (achieve_list[realdex]/total < 2/10):
                            stat1 = f'{g1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 2/10) and (achieve_list[realdex]/total < 3/10):
                            stat1 = f'{g1}{g2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 3/10) and (achieve_list[realdex]/total < 4/10):
                            stat1 = f'{g1}{g2}{g2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 4/10) and (achieve_list[realdex]/total < 5/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 5/10) and (achieve_list[realdex]/total < 6/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 6/10) and (achieve_list[realdex]/total < 7/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{no2}{no2}{no2}{no3}'                        
                        elif (achieve_list[realdex]/total >= 7/10) and (achieve_list[realdex]/total < 8/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 8/10) and (achieve_list[realdex]/total < 9/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 9/10) and (achieve_list[realdex]/total < 9.5/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{no3}'
                        elif (achieve_list[realdex]/total >= 9.5/10) and (achieve_list[realdex]/total < 10/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g3}'
                        else: 
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g4}'    
                    else: 
                        badge1 = '<:bronze3:1112807867741909094>'
                        str1 = strs[forstr+2]
                        total = tots[forstr+2]
                        reward = 'Completed!' 
                        stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g4}'  
                        a = 1  
                    if a == 1:
                        em2.add_field(name = f'{str1}', value = f'{badge1} {stat1} `{achieve_list[realdex]}/{total}`\n**Completed! ✅**',inline=False)
                        a = 0
                    else:
                        em2.add_field(name = f'{str1}', value = f'{badge1} {stat1} `{achieve_list[realdex]}/{total}`\n**Reward: **{reward} Dom Coins',inline=False)


                else:
                    pass
            
            strs = [ 'Buy an oddity', 'Buy 2 oddities', 'Buy 3 oddities', '*Coming soon*', 'Participate in 10 Wars', 'Participate in 30 Wars', '*Coming Soon*', 'Register into a tournament', 'Register into a tournament', 'Get MVP in a war', 'Get MVP 3 times', 'Get MVP 10 times']
            tots = [1,2,3,3,10,30,1,1,1,1,3,10]
            rew = [10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50,10,25,50]
            em3 = discord.Embed(
                title = 'Achievements',
                description = 'Achievements: *(Page 3/3)*',
                colour = color
            )

            for p,admin in enumerate(achieve_list):
                a = 0
                if (p % 2 == 0) and (p < 8): 
                    forstr = int((p*3)/2)
                    realdex = p+28
                    if achieve_list[realdex+1] == 0:
                        
                        badge1 = '<:bronze1:1112807329512038400>'
                        
                        str1 = strs[forstr]
                        total = tots[forstr]
                        reward = f'x1 LootBox + {rew[forstr]}'
                        if achieve_list[realdex]/total < 1/10:
                            stat1 = f'{no1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 1/10) and (achieve_list[realdex]/total < 2/10):
                            stat1 = f'{b1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 2/10) and (achieve_list[realdex]/total < 3/10):
                            stat1 = f'{b1}{b2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 3/10) and (achieve_list[realdex]/total < 4/10):
                            stat1 = f'{b1}{b2}{b2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 4/10) and (achieve_list[realdex]/total < 5/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 5/10) and (achieve_list[realdex]/total < 6/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 6/10) and (achieve_list[realdex]/total < 7/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{no2}{no2}{no2}{no3}'                        
                        elif (achieve_list[realdex]/total >= 7/10) and (achieve_list[realdex]/total < 8/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 8/10) and (achieve_list[realdex]/total < 9/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 9/10) and (achieve_list[realdex]/total < 9.5/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{no3}'
                        elif (achieve_list[realdex]/total >= 9.5/10) and (achieve_list[realdex]/total < 10/10):
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b3}'
                        else: 
                            stat1 = f'{b1}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b2}{b4}'

                    elif achieve_list[realdex+1] == 1:
                        badge1 = '<:bronze2:1112807988969873418>'
                        str1 = strs[forstr+1]  
                        total = tots[forstr+1]   
                        reward = f'x1 LootBox + {rew[forstr+1]}'
                        if achieve_list[realdex]/total < 1/10:
                            stat1 = f'{no1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 1/10) and (achieve_list[realdex]/total < 2/10):
                            stat1 = f'{s1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 2/10) and (achieve_list[realdex]/total < 3/10):
                            stat1 = f'{s1}{s2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 3/10) and (achieve_list[realdex]/total < 4/10):
                            stat1 = f'{s1}{s2}{s2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 4/10) and (achieve_list[realdex]/total < 5/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 5/10) and (achieve_list[realdex]/total < 6/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 6/10) and (achieve_list[realdex]/total < 7/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{no2}{no2}{no2}{no3}'                        
                        elif (achieve_list[realdex]/total >= 7/10) and (achieve_list[realdex]/total < 8/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 8/10) and (achieve_list[realdex]/total < 9/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 9/10) and (achieve_list[realdex]/total < 9.5/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{no3}'
                        elif (achieve_list[realdex]/total >= 9.5/10) and (achieve_list[realdex]/total < 10/10):
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s3}'
                        else: 
                            stat1 = f'{s1}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s2}{s4}'

                    elif achieve_list[realdex+1] == 2:
                        badge1 = '<:bronze3:1112807867741909094>'
                        str1 = strs[forstr+2]
                        total = tots[forstr+2]
                        reward = f'x1 LootBox + {rew[forstr+2]}'
                        if achieve_list[realdex]/total < 1/10:
                            stat1 = f'{no1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 1/10) and (achieve_list[realdex]/total < 2/10):
                            stat1 = f'{g1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 2/10) and (achieve_list[realdex]/total < 3/10):
                            stat1 = f'{g1}{g2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 3/10) and (achieve_list[realdex]/total < 4/10):
                            stat1 = f'{g1}{g2}{g2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 4/10) and (achieve_list[realdex]/total < 5/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{no2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 5/10) and (achieve_list[realdex]/total < 6/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{no2}{no2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 6/10) and (achieve_list[realdex]/total < 7/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{no2}{no2}{no2}{no3}'                        
                        elif (achieve_list[realdex]/total >= 7/10) and (achieve_list[realdex]/total < 8/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{no2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 8/10) and (achieve_list[realdex]/total < 9/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{no2}{no3}'
                        elif (achieve_list[realdex]/total >= 9/10) and (achieve_list[realdex]/total < 9.5/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{no3}'
                        elif (achieve_list[realdex]/total >= 9.5/10) and (achieve_list[realdex]/total < 10/10):
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g3}'
                        else: 
                            stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g4}' 
                    else: 
                        badge1 = '<:bronze3:1112807867741909094>'
                        str1 = strs[forstr+2]
                        total = tots[forstr+2]
                        reward = 'Completed!' 
                        stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g4}'  
                        a = 1  
                    if a == 1:
                        em3.add_field(name = f'{str1}', value = f'{badge1} {stat1} `{achieve_list[realdex]}/{total}`\n**Completed! ✅**',inline=False)
                        a = 0
                    else:
                        em3.add_field(name = f'{str1}', value = f'{badge1} {stat1} `{achieve_list[realdex]}/{total}`\n**Reward: **{reward} Dom Coins',inline=False)

                
                else:
                    pass          

            embeds = [em1, em2, em3]

            current_page = 0

            ranked_msg = await ctx.send(embed = em1)

            await ranked_msg.add_reaction('◀️')
            await ranked_msg.add_reaction('▶️')


            def check(reaction : discord.Reaction, user : discord.User):
                return user.id == ctx.author.id and reaction.message.channel.id == ctx.channel.id and str(reaction.emoji) in ['◀️', '▶️']

            while True:
                try:
                    reaction_add, user = await self.bot.wait_for(
                        'reaction_add',
                        timeout = 60,
                        check = check
                    )

                except asyncio.TimeoutError:
                    break

                else:
                    if str(reaction_add) in ['▶️']:
                        if (current_page > -1) and (current_page < 2):
                            current_page += 1

                            await ranked_msg.edit(embed = embeds[current_page])

                        elif current_page >= 2:
                            current_page = 0

                            await ranked_msg.edit(embed = embeds[current_page]) 


                    elif str(reaction_add) in ['◀️']:
                        if current_page < 1:
                            current_page = 2

                            await ranked_msg.edit(embed = embeds[current_page])

                        elif current_page < 3:
                            current_page -= 1

                            await ranked_msg.edit(embed = embeds[current_page])    


        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')





    @commands.command(name = 'quests', aliases = ['quest'])
    async def que_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:

            g4=    '<:g4:1100520811212841054>'
            g2=    '<:g2:1100520807282778193>'
            g1=    '<:g1:1100520808922751036>'
            no1 = '<:no1:1100516249085161553>'
            no2 =   '<:no2:1100516250507018250>'
            no3=    '<:no3:1100516253275279532>'
            g3=    '<:g3:1100520804539703366>'

            strs = [ 'Complete 5 casual duel', 'Win 3 casual duel','Complete 5 ranked duels', 'Win 3 ranked duel','Complete 5 ranked with commons' , 'Complete 5 ranked with rares','Trade 3 times with another user in Dom Bot']
            total = [5,3,5,3,5,5,3]



            check = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', ctx.author.id)
            current_time = datetime.now()
            if (check[0]['quests'] is None) or (check[0]['daily'] is None) or (check[0]['daily'] <= current_time):
                flists = str(check[0]['quests'])
                new_admins = ''
                admins_list = self.listing(flists)
                randomRol = random.randint(2,6)
                new_admins = f'{randomRol} 0 {total[randomRol]}' 

                now = datetime.now()
                midnight = datetime(now.year, now.month, now.day) + timedelta(days=1)
                time_until_midnight = midnight - now            
                delete_time = datetime.now() + time_until_midnight 
                                                      
                await self.bot.db.execute(f'UPDATE casual SET quests = $1, daily = $2 WHERE player_id = $3', new_admins,delete_time, ctx.author.id)

            check = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', ctx.author.id)
            flists = str(check[0]['quests'])
            new_admins = ''
            admins_list = self.listing(flists)
            idc = int(admins_list[0])


            em1 = discord.Embed(
                title = 'Daily Quests',
                description = 'Complete Daily Quests to get rewarded **50dc**!',
                colour = color
            )

            start_time = datetime.now()
            duration = check[0]['daily'] - start_time
            days, seconds = divmod(duration.total_seconds(), 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            checkd = int(admins_list[1])/total[idc]
            if checkd < 1/10:
                stat1 = f'{no1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
            elif (checkd >= 1/10) and (checkd < 2/10):
                stat1 = f'{g1}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
            elif (checkd >= 2/10) and (checkd < 3/10):
                stat1 = f'{g1}{g2}{no2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
            elif (checkd >= 3/10) and (checkd< 4/10):
                stat1 = f'{g1}{g2}{g2}{no2}{no2}{no2}{no2}{no2}{no2}{no3}'
            elif (checkd >= 4/10) and (checkd < 5/10):
                stat1 = f'{g1}{g2}{g2}{g2}{no2}{no2}{no2}{no2}{no2}{no3}'
            elif (checkd >= 5/10) and (checkd < 6/10):
                stat1 = f'{g1}{g2}{g2}{g2}{g2}{no2}{no2}{no2}{no2}{no3}'
            elif (checkd >= 6/10) and (checkd< 7/10):
                stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{no2}{no2}{no2}{no3}'                        
            elif (checkd >= 7/10) and (checkd < 8/10):
                stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{no2}{no2}{no3}'
            elif (checkd >= 8/10) and (checkd < 9/10):
                stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{no2}{no3}'
            elif (checkd >= 9/10) and (checkd < 9.5/10):
                stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{no3}'
            elif (checkd >= 9.5/10) and (checkd < 10/10):
                stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g3}'
            else: 
                stat1 = f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g4}' 
            
            if stat1 == f'{g1}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g2}{g4}':
                em1.add_field(name = f'{strs[idc]}', value = f'{stat1} `{admins_list[1]}/{total[idc]}`\n**Completed! ✅**',inline=False)
            else:
                em1.add_field(name = f'{strs[idc]}', value = f'{stat1} `{admins_list[1]}/{total[idc]}`\n**In Progress.. 🔃**',inline=False)

            em1.set_footer(text = f'⏰ {int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s')
            await ctx.send(embed = em1)

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'claim')
    async def claimy_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(798548690860113982)
            modrole = guild.get_role(786448967172882442)
            
            if (role in ctx.author.roles) or (ctx.author.id == 0) or (modrole in ctx.author.roles):
                check = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', ctx.author.id)
                current_time = datetime.now()
                
                if (check[0]['dc'] == None) or (check[0]['dc'] <= current_time):
                    now = datetime.now()
                    midnight = datetime(now.year, now.month, now.day) + timedelta(days=1)
                    time_until_midnight = midnight - now
                    if modrole in ctx.author.roles:
                        if (role in ctx.author.roles):

                            if (check[0]['double'] == None) or (check[0]['double'] == 0):
                                if modrole in ctx.author.roles:
                                    delete_time = datetime.now() + time_until_midnight
                                    await self.bot.db.execute(f'UPDATE casual SET dc = $1  WHERE player_id = $2', delete_time, ctx.author.id)  
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 120 WHERE player_id = $1',  ctx.author.id)
                                    await ctx.send("**You were rewarded 120 Dc.**\n\nThank you for Supporting & Moderating <:dominant_tier:1149652514350825552>** Dominant **<:dominant_tier:1149652514350825552>")

                            else:

                                if (check[0]['double'] == 7):                          
                                    delete_time = datetime.now() + time_until_midnight
                                    delete_time2 = datetime.now() + timedelta(days=7)
                                    await self.bot.db.execute(f'UPDATE casual SET dc = $1, lootbox = $2, double = double - 1 WHERE player_id = $3', delete_time, delete_time2, ctx.author.id)
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 140, wishes = wishes + 1, scraps = scraps + 1  WHERE player_id = $1',  ctx.author.id)
                                    await ctx.send("**You were rewarded 140 Dc, Lootbox and a Key.**\n\nThank you for Supporting & Moderating <:dominant_tier:1149652514350825552>** Dominant**<:dominant_tier:1149652514350825552>")
                                else:
                                    delete_time = datetime.now() + time_until_midnight
                                    await self.bot.db.execute(f'UPDATE casual SET dc = $1, double = double - 1  WHERE player_id = $2', delete_time, ctx.author.id)      
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 140 WHERE player_id = $1',  ctx.author.id) 
                                    await ctx.send("**You were rewarded 140 Dc.**\n\nThank you for Supporting & Moderating <:dominant_tier:1149652514350825552>** Dominant **<:dominant_tier:1149652514350825552>")
                               
                        else:
                            delete_time = datetime.now() + time_until_midnight
                            await self.bot.db.execute(f'UPDATE casual SET dc = $1  WHERE player_id = $2', delete_time, ctx.author.id)  
                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 70 WHERE player_id = $1',  ctx.author.id)
                            await ctx.send("**You were rewarded 70 Dc.**\n\nThank you for Moderating <:dominant_tier:1149652514350825552>** Dominant **<:dominant_tier:1149652514350825552>")
                        return


                    if (check[0]['double'] == None) or (check[0]['double'] == 0):
  
                        delete_time = datetime.now() + time_until_midnight
                        await self.bot.db.execute(f'UPDATE casual SET dc = $1  WHERE player_id = $2', delete_time, ctx.author.id)  
                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 60 WHERE player_id = $1',  ctx.author.id)
                        await ctx.send("**You were rewarded 60 Dc.**\n\nThank you for supporting <:dominant_tier:1149652514350825552>** Dominant **<:dominant_tier:1149652514350825552>")
                    else:

                        if (check[0]['double'] == 7):                          
                            delete_time = datetime.now() + time_until_midnight
                            delete_time2 = datetime.now() + timedelta(days=7)
                            await self.bot.db.execute(f'UPDATE casual SET dc = $1, lootbox = $2, double = double - 1 WHERE player_id = $3', delete_time, delete_time2, ctx.author.id)
                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 80, wishes = wishes + 1, scraps = scraps + 1  WHERE player_id = $1',  ctx.author.id)
                            await ctx.send("**You were rewarded 80 Dc, Lootbox and a Key.**\n\nThank you for supporting <:dominant_tier:1149652514350825552>** Dominant**<:dominant_tier:1149652514350825552>")
                        else:
                            delete_time = datetime.now() + time_until_midnight
                            await self.bot.db.execute(f'UPDATE casual SET dc = $1, double = double - 1  WHERE player_id = $2', delete_time, ctx.author.id)      
                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 80 WHERE player_id = $1',  ctx.author.id) 
                            await ctx.send("**You were rewarded 80 Dc.**\n\nThank you for supporting <:dominant_tier:1149652514350825552>** Dominant **<:dominant_tier:1149652514350825552>")

                else:
                    time_difference = check[0]['dc'] - datetime.now()
                    formatted_time = format_time_difference(time_difference)
                    await ctx.send(f"You still have time remaining before you can claim again.. **{formatted_time} Left**")

            else:
                await ctx.send("**<:boost:1094167198118989884> Boost the Server to Earn Free Rewards!**\n\n**》** **SINGLE BOOST**\nFree **350 Dc** Per Week (50 Dc per day)\nFree **Custom Role**\n**Coloured Text** for their Dominant profile\n\n**》** **DOUBLE BOOST**\nFree **490 Dc**, **Lootbox** and a **Key** Every Week (70Dc per day)\nFree **Icon Custom Role**\n**Coloured Text** for their Dominant profile\n\nIf you miss a day, you will not be refunded...")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'boost')
    async def vip_command(self, ctx, action : str = None ,member : discord.Member = None ):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(798548690860113982)

            role1 = guild.get_role(786448967172882442)
            role3 = guild.get_role(781452019578961921)
            if (role1 in ctx.author.roles) or (role3 in ctx.author.roles) or (ctx.author.id == 0):
                if action == 'dbl':
                    if (role in member.roles) or (ctx.author.id == 0):
                        pass
                    else:
                        await ctx.send("This user is not a Booster. ⚠️")
                        return

                    tcheck = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', member.id)
                    current_time = datetime.now()
                    check = False
                    if  (tcheck[0]['lootbox'] == None):
                        pass
                    else:
                        if (tcheck[0]['lootbox'] <= current_time):
                            check = True
                        else:
                            pass
                    if check:
                        view = ConfirmCancel(ctx.author)
                        await ctx.send("This user still hasn't claimed thier rewards, do you still want to renew the status?", view = view)
                        await view.wait()

                        if view.value == True:
                            pass
                        else:
                            await ctx.send("Cancelled.")
                            return
                    stat = 7
                    await self.bot.db.execute(f'UPDATE casual SET double = $1, lootbox = NULL  WHERE player_id = $2', stat, member.id)  
                    await ctx.send(f"{member.mention} now has the **Double Booster** status for the next 7 Days.")
                elif action == 'dbllist':
                    listofdbl = await self.bot.db.fetch('SELECT * FROM casual WHERE double IS NOT NULL')
                    strofdbl = ''
                    for i in listofdbl:
                        times = format_time_difference(i['lootbox'])
                        if times == None:
                            times = 'None'
                        strofdbl += f"<@{i['player_id']}> : {i['double']} | Time Remaining: {times}\n"
                    if strofdbl == '':
                        await ctx.send("None")
                    else:    
                        await ctx.send(f"{strofdbl}")
                elif action == 'list':
                    mentioned_users = [member.mention for member in ctx.guild.members if role in member.roles]
                    rolld = await self.bot.db.fetch('SELECT * FROM casual WHERE custom IS NOT NULL')
                    strofdbl = ''

                    for i in rolld:
                        strofdbl += f"<@{i['player_id']}> "

                    if mentioned_users:
                        await ctx.send(f"Certified Boosters {' '.join(mentioned_users)}\nAll Users that have a custom role {strofdbl}")
                    else:
                        await ctx.send(f"No users found with the Role.")
                
                elif action == 'snga':
  
                    await self.bot.db.execute(f'UPDATE casual SET custom = 1  WHERE player_id = $1',  member.id)  
                    await ctx.send(f"{member.mention} now has the **Custom Role**")

                elif action == 'sngr':
  
                    await self.bot.db.execute(f'UPDATE casual SET custom = NULL  WHERE player_id = $1',  member.id)  
                    await ctx.send(f"{member.mention} does not have the **Custom Role** now")

                else:
                    await ctx.send("dbllist, dbl, snga, sngr, list")
            
            
            else:
                await ctx.send("You can't use this command.")


    @commands.command(name = 'queue', aliases =['q'])
    async def qup(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
 
            rankvaluer = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', ctx.author.id)
            rankvaluec = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', ctx.author.id)

            war_check = await self.bot.db.fetch('SELECT * FROM wars WHERE player_id = $1', ctx.author.id)
            inq = war_check[0]['inq']
            if inq == None:
                pass
            else:

                view = ConfirmCancel(ctx.author)
                await ctx.send("Are you sure you want to dequeue? ", view = view)
                await view.wait()
                if view.value is True:
                    pass
                else:
                    await ctx.send("Cancelled.")
                    return
                await self.bot.db.execute(f'UPDATE wars SET inq = NULL, added = NULL  WHERE player_id = $1', ctx.author.id)
                await ctx.send("Dequeued...")   
                return                 
            

            compositions = await self.bot.db.fetch('SELECT player_id FROM common_system ORDER BY points DESC')
            common_positions = []
            index_number = 0
            for i in range(len(compositions)):
                common_positions.append(compositions[index_number]['player_id'])
                index_number += 1
            user_placement = common_positions.index(ctx.author.id)
            position = user_placement + 1

            compositions1 = await self.bot.db.fetch('SELECT player_id FROM rank_system ORDER BY points DESC')

            rare_positions = []
            index_number = 0
            for i in range(len(compositions1)):
                rare_positions.append(compositions1[index_number]['player_id'])
                index_number += 1
            user1_placement = rare_positions.index(ctx.author.id)
            position1 = user1_placement + 1

            
            if (position <= 20) or (position1  <= 20):
                pass
            else:
                await ctx.send("You must be in the **Top 20** in **Rares or Common** to be able to queue as a **Blade**.")
                return
            
            if registered_check[0]['clan_1'] is not None:
                clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', registered_check[0]['clan_1'])
                if clan[0]['opted'] == 'False':
                    await ctx.send("Your clan has opted out of allowing blades to enter a war, ask them to opt in.")
                    return
                else:
                    pass
            
            if (registered_check[0]['blade'] == None):
                pass
            else:
                await ctx.send("You're already in a war as a Blade!")
                return


            view = ConfirmCancel(ctx.author)
            await ctx.send("Are you sure you want to queue? You can't back out if you get into a war and will punished for being AFK.", view = view)
            await view.wait()
            if view.value == True:
                

                inq = 'True'
                added = datetime.now()
                await self.bot.db.execute(f'UPDATE wars SET inq = $1, added = $2  WHERE player_id = $3', inq, added, ctx.author.id)
                await ctx.send("Queued Up!")

            elif view.value == False:
                await ctx.send("canceled")
            else:
                await ctx.send("Timed out!")



        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'qdddd', aliases =['queddued'])
    async def quroninsp(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

    
            if user_ban_list:
                await ctx.send('You are banned from the bot.')
                return

            if registered_check:

                lb = await self.bot.db.fetch('SELECT * FROM wars WHERE inq IS NOT NULL ORDER BY added ASC')

                data = []
                for faction in lb:
                    data.append(faction['player_name'])
    
        
                pagination_view = roninPaginationView()
                pagination_view.data = data
                pagination_view.lb = lb
                pagination_view.bot = self.bot
    
                await pagination_view.send(ctx)

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')



    @commands.command(name = 'addpoke')
    async def qurofdainsp(self, ctx, types : str = None,*, pokename : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

    
            if user_ban_list:
                await ctx.send('You are banned from the bot.')
                return
            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(1182354616034275479)


            if (role in ctx.author.roles) or (ctx.author.id == 0):
                if pokename == None:                    
                    await ctx.send("Please enter a name.")
                    return
                
                if types == None:
                    await ctx.send("please enter a type for the pokemon, Rare or Common")
                    return
                
                pokename = pokename.lower()

                poke = await self.bot.db.fetch('SELECT * FROM pokes WHERE pokemon = $1', pokename)

                if poke:
                    await ctx.send("This pokemon has already been added.")
                    return
                
                types = types.lower()
                if (types == 'rare') or (types == 'common'):
                    pass
                else:
                    await ctx.send("incorrect format")
                    return

                await self.bot.db.execute('INSERT INTO pokes (pokemon, type) VALUES ($1, $2)', pokename, types)
                await ctx.send(f"added {pokename}")
            else:
                await ctx.send("no")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'addmove')
    async def qurofddadainsp(self, ctx, pokedes : str = None, *, move : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

    
            if user_ban_list:
                await ctx.send('You are banned from the bot.')
                return

            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(1182354616034275479)


            if (role in ctx.author.roles) or (ctx.author.id == 0):
                if pokedes == None:                    
                    await ctx.send("Please enter a name.")
                    return
                
                if move == None:
                    await ctx.send("please enter a move for the pokemon")
                    return
                


                with open(f'pokedex.csv', mode='r', encoding='ISO-8859-1') as file:
                    reader = csv.reader(file)
                    data = list(reader)

                allnames = []
                for pokemon in data:
                    pokenamed = pokemon[1].title().split('-')
                    if pokenamed[-1] == 'Mega':
                        pokenamed.pop(-1)
                        pokenamed = ['Mega'] + pokenamed
                        nameis = ('').join(pokenamed)
                    
                    else:
                        nameis = ('').join(pokenamed)

                    if nameis in allnames:
                        pass
                    else:
                        allnames.append(nameis)

                pokemon1 = pokedes.title()
                test = pokemon1.replace(" ","")  
                test = test.replace("-","")  
                if test in allnames:
                    pokemon1 = test.title()
                else:
                    pokemon1 = self.find_matching_pokemon(pokemon1.title(), allnames)

                if pokemon1 == None:
                    await ctx.send(f"Could not find **{pokedes}**. If you want to help us add this Pokemon, Make a ticket in <#1091112838581461153> !")
                    return
                
                for pokemon in data:
                    pokenamed = pokemon[1].title().split('-')
                    doc = pokemon[1].title()
                    if pokenamed[-1] == 'Mega':
                        pokenamed.pop(-1)
                        pokenamed = ['Mega'] + pokenamed
                        elephant1 = (' ').join(pokenamed)
                        if elephant1 == 'Mega Rayquaza':
                            elephant1 = 'Rayquaza'
                        nameis = ('').join(pokenamed)
                    
                    else:
                        elephant1 = (' ').join(pokenamed)
                        if elephant1 == 'Mega Rayquaza':
                            elephant1 = 'Rayquaza'

                        nameis = ('').join(pokenamed)

                    if nameis == pokemon1:
                        pokemon1 = doc
                        break
                    else:
                        pass

                poke = await self.bot.db.fetch('SELECT * FROM pokes WHERE pokemon = $1', elephant1.lower())

                if poke:
                    pass
                else:
                    await ctx.send(f"{elephant1.lower()} pokemon has not been added.")
                    return
                
                move = move.lower()


                await self.bot.db.execute('UPDATE pokes SET moveset = $1 WHERE pokemon = $2', move, elephant1.lower())
                
                await ctx.send(f"added {move} for {pokemon1}")
            else:
                await ctx.send("no")

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'addmint')
    async def qucdsadainsp(self, ctx, pokename : str = None, *, mint : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

    
            if user_ban_list:
                await ctx.send('You are banned from the bot.')
                return
            
            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(1182354616034275479)


            if (role in ctx.author.roles) or (ctx.author.id == 0):
                if pokename == None:                    
                    await ctx.send("Please enter a name.")
                    return
                

                if mint == None:                    
                    await ctx.send("Please enter a mintvalue. **Mint type** \\n mintstuff \\n\\n repeat")
                    return

                pokedes = pokename.lower()

                with open(f'pokedex.csv', mode='r', encoding='ISO-8859-1') as file:
                    reader = csv.reader(file)
                    data = list(reader)

                allnames = []
                for pokemon in data:
                    pokenamed = pokemon[1].title().split('-')
                    if pokenamed[-1] == 'Mega':
                        pokenamed.pop(-1)
                        pokenamed = ['Mega'] + pokenamed
                        nameis = ('').join(pokenamed)
                    
                    else:
                        nameis = ('').join(pokenamed)

                    if nameis in allnames:
                        pass
                    else:
                        allnames.append(nameis)

                pokemon1 = pokedes.title()
                test = pokemon1.replace(" ","")  
                test = test.replace("-","")  
                if test in allnames:
                    pokemon1 = test.title()
                else:
                    pokemon1 = self.find_matching_pokemon(pokemon1.title(), allnames)

                if pokemon1 == None:
                    await ctx.send(f"Could not find **{pokedes}**. If you want to help us add this Pokemon, Make a ticket in <#1091112838581461153> !")
                    return
                
                for pokemon in data:
                    pokenamed = pokemon[1].title().split('-')
                    doc = pokemon[1].title()
                    if pokenamed[-1] == 'Mega':
                        pokenamed.pop(-1)
                        pokenamed = ['Mega'] + pokenamed
                        elephant1 = (' ').join(pokenamed)
                        if elephant1 == 'Mega Rayquaza':
                            elephant1 = 'Rayquaza'
                        nameis = ('').join(pokenamed)
                    
                    else:
                        elephant1 = (' ').join(pokenamed)
                        if elephant1 == 'Mega Rayquaza':
                            elephant1 = 'Rayquaza'

                        nameis = ('').join(pokenamed)

                    if nameis == pokemon1:
                        pokemon1 = doc
                        break
                    else:
                        pass

                poke = await self.bot.db.fetch('SELECT * FROM pokes WHERE pokemon = $1', elephant1.lower())

                if poke:
                    pass
                else:
                    await ctx.send("This pokemon has not been added.")
                    return
                mint = mint.replace('\\\\n', '\n')
                await self.bot.db.execute('UPDATE pokes SET mints = $1 WHERE pokemon = $2', mint, pokename.lower())
                
                await ctx.send(f"added {mint} for {pokename}")
            else:
                await ctx.send('no')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'addsearch')
    async def qurofdfnsp(self, ctx, pokename : str = None, *, search : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

    
            if user_ban_list:
                await ctx.send('You are banned from the bot.')
                return

            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(1182354616034275479)


            if (role in ctx.author.roles) or (ctx.author.id == 0):
                if pokename == None:                    
                    await ctx.send("Please enter a name.")
                    return
              

                if search == None:                    
                    await ctx.send("Please enter a search. **command** \\n explainstuff \\n\\n repeat")
                    return


                pokedes = pokename.lower()

                with open(f'pokedex.csv', mode='r', encoding='ISO-8859-1') as file:
                    reader = csv.reader(file)
                    data = list(reader)

                allnames = []
                for pokemon in data:
                    pokenamed = pokemon[1].title().split('-')
                    if pokenamed[-1] == 'Mega':
                        pokenamed.pop(-1)
                        pokenamed = ['Mega'] + pokenamed
                        nameis = ('').join(pokenamed)
                    
                    else:
                        nameis = ('').join(pokenamed)

                    if nameis in allnames:
                        pass
                    else:
                        allnames.append(nameis)

                pokemon1 = pokedes.title()
                test = pokemon1.replace(" ","")  
                test = test.replace("-","")  
                if test in allnames:
                    pokemon1 = test.title()
                else:
                    pokemon1 = self.find_matching_pokemon(pokemon1.title(), allnames)

                if pokemon1 == None:
                    await ctx.send(f"Could not find **{pokedes}**. If you want to help us add this Pokemon, Make a ticket in <#1091112838581461153> !")
                    return
                
                for pokemon in data:
                    pokenamed = pokemon[1].title().split('-')
                    doc = pokemon[1].title()
                    if pokenamed[-1] == 'Mega':
                        pokenamed.pop(-1)
                        pokenamed = ['Mega'] + pokenamed
                        elephant1 = (' ').join(pokenamed)
                        if elephant1 == 'Mega Rayquaza':
                            elephant1 = 'Rayquaza'
                        nameis = ('').join(pokenamed)
                    
                    else:
                        elephant1 = (' ').join(pokenamed)
                        if elephant1 == 'Mega Rayquaza':
                            elephant1 = 'Rayquaza'

                        nameis = ('').join(pokenamed)

                    if nameis == pokemon1:
                        pokemon1 = doc
                        break
                    else:
                        pass

                poke = await self.bot.db.fetch('SELECT * FROM pokes WHERE pokemon = $1', elephant1.lower())

                if poke:
                    pass
                else:
                    await ctx.send("This pokemon has not been added.")
                    return
                
                search = search.replace('\\\\n', '\n')
                await self.bot.db.execute('UPDATE pokes SET search1 = $1 WHERE pokemon = $2', search, pokename.lower())
               
                await ctx.send(f"added {search} for {pokename}")
            else:
                await ctx.send("no")

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'info')
    async def infosp(self, ctx,  typed : str = None, *, pokename : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

    
            if user_ban_list:
                await ctx.send('You are banned from the bot.')
                return

            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(1182354616034275479)


            if (role in ctx.author.roles) or (ctx.author.id == 0):
                if pokename == None:                    
                    await ctx.send("Please enter a name.")
                    return
              

                if typed == None:                    
                    await ctx.send("Please enter a type.")
                    return


                pokedes = pokename.lower()

                with open(f'pokedex.csv', mode='r', encoding='ISO-8859-1') as file:
                    reader = csv.reader(file)
                    data = list(reader)

                allnames = []
                for pokemon in data:
                    pokenamed = pokemon[1].title().split('-')
                    if pokenamed[-1] == 'Mega':
                        pokenamed.pop(-1)
                        pokenamed = ['Mega'] + pokenamed
                        nameis = ('').join(pokenamed)
                    
                    else:
                        nameis = ('').join(pokenamed)

                    if nameis in allnames:
                        pass
                    else:
                        allnames.append(nameis)

                pokemon1 = pokedes.title()
                test = pokemon1.replace(" ","")  
                test = test.replace("-","")  
                if test in allnames:
                    pokemon1 = test.title()
                else:
                    pokemon1 = self.find_matching_pokemon(pokemon1.title(), allnames)

                if pokemon1 == None:
                    await ctx.send(f"Could not find **{pokedes}**. If you want to help us add this Pokemon, Make a ticket in <#1091112838581461153> !")
                    return
                
                for pokemon in data:
                    pokenamed = pokemon[1].title().split('-')
                    doc = pokemon[1].title()
                    if pokenamed[-1] == 'Mega':
                        pokenamed.pop(-1)
                        pokenamed = ['Mega'] + pokenamed
                        elephant1 = (' ').join(pokenamed)
                        if elephant1 == 'Mega Rayquaza':
                            elephant1 = 'Rayquaza'
                        nameis = ('').join(pokenamed)
                    
                    else:
                        elephant1 = (' ').join(pokenamed)
                        if elephant1 == 'Mega Rayquaza':
                            elephant1 = 'Rayquaza'

                        nameis = ('').join(pokenamed)

                    if nameis == pokemon1:
                        pokemon1 = doc
                        break
                    else:
                        pass

                poke = await self.bot.db.fetch('SELECT * FROM pokes WHERE pokemon = $1', elephant1.lower())

                if poke:
                    pass
                else:
                    await ctx.send("This pokemon has not been added.")
                    return
                
                if typed == 'mint':
                    text = poke[0]['mints']
                elif typed == 'stat':
                    text = poke[0]['search1']
               
                await ctx.send(f"```{text}```")
            else:
                await ctx.send("no")

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'addcomb')
    async def quddddddddrofdfnsp(self, ctx, pokename1 : str = None, pokename2 : str = None, *, search : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

    
            if user_ban_list:
                await ctx.send('You are banned from the bot.')
                return

            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(1182354616034275479)


            if (role in ctx.author.roles) or (ctx.author.id == 0):
                if pokename1 == None:                    
                    await ctx.send("Please enter a name.")
                    return
              
                if pokename2 == None:                    
                    await ctx.send("Please enter a name.")
                    return

                if search == None:                    
                    await ctx.send("Please enter a search. **command** \\n explainstuff \\n\\n repeat")
                    return


                pokedes1 = pokename1.lower()

                pokedes2 = pokename2.lower()

                with open(r'/home/ubuntu/bot_files/database/pokemon_combinations.csv', mode='r', encoding='ISO-8859-1') as file:
                    reader = csv.reader(file)
                    data = list(reader)

                pokename1 = pokedes1.title()

                pokename2 = pokedes2.title()


                allnames = []
                for pokemon in data:
                    if pokemon[0] in allnames:
                        pass
                    else:
                        allnames.append(pokemon[0])

                test = pokemon1.replace(" ","")  
                test = test.replace("-","")  
                if test in allnames:
                    pokemon1 = test.title()
                else:
                    pokemon1 = self.find_matching_pokemon(pokemon1.title(), allnames)

                test = pokemon2.replace(" ","")  
                test = test.replace("-","")  
                if test in allnames:
                    pokemon2 = test.title()
                else:
                    pokemon2 = self.find_matching_pokemon(pokemon2.title(), allnames)
                
                if pokename1 == None:
                    await ctx.send(f"Could not find **{pokedes1}**. If you want to help us add this Pokemon, Make a ticket in <#1091112838581461153> !")
                    return

                if pokename2 == None:
                    await ctx.send(f"Could not find **{pokedes2}**. If you want to help us add this Pokemon, Make a ticket in <#1091112838581461153> !")
                    return
                
                flag = False
                num = 0
                for pokemon in data:
                    if (pokemon[0].title() == pokename1.title()):
                        if (pokemon[1].title() == pokename1.title()):
                            index = num


                            flag = True
                        
                        else:
                            num += 1
                    else:
                        num += 1
                
                if flag == True:
                    pass
                else:
                    await ctx.send("Error.")
                    return

                data[index][2] = search
                
                view = ConfirmCancel(ctx.author)
               
                await ctx.send(f"Do you want to add {search} for {pokename1} & {pokename2}", view = view)
                await view.wait()

                with open(r'/home/ubuntu/bot_files/database/pokemon_combinations.csv', mode='w', encoding='ISO-8859-1', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)

                await ctx.send("done")
            else:
                await ctx.send("no")

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'addhelp')
    async def addhelp(self, ctx, pokename1 : str = None, pokename2 : str = None, *, help : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

    
            if user_ban_list:
                await ctx.send('You are banned from the bot.')
                return

            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(1182354616034275479)


            if (role in ctx.author.roles) or (ctx.author.id == 0):
                if pokename1 == None:                    
                    await ctx.send("Please enter a name.")
                    return
              
                if pokename2 == None:                    
                    await ctx.send("Please enter a name.")
                    return

                if help == None:                    
                    await ctx.send("Please enter a search. **command** \\n explainstuff \\n\\n repeat")
                    return


                pokedes1 = pokename1.lower()

                pokedes2 = pokename2.lower()

                with open('pokemon_combinations.csv', mode='r', encoding='ISO-8859-1') as file:
                    reader = csv.reader(file)
                    data = list(reader)

                pokename1 = pokedes1.title()

                pokename2 = pokedes2.title()


                allnames = []
                for pokemon in data:
                    if pokemon[0] in allnames:
                        pass
                    else:
                        allnames.append(pokemon[0])

                test = pokemon1.replace(" ","")  
                test = test.replace("-","")  
                if test in allnames:
                    pokemon1 = test.title()
                else:
                    pokemon1 = self.find_matching_pokemon(pokemon1.title(), allnames)

                test = pokemon2.replace(" ","")  
                test = test.replace("-","")  
                if test in allnames:
                    pokemon2 = test.title()
                else:
                    pokemon2 = self.find_matching_pokemon(pokemon2.title(), allnames)
                
                if pokename1 == None:
                    await ctx.send(f"Could not find **{pokedes1}**. If you want to help us add this Pokemon, Make a ticket in <#1091112838581461153> !")
                    return

                if pokename2 == None:
                    await ctx.send(f"Could not find **{pokedes2}**. If you want to help us add this Pokemon, Make a ticket in <#1091112838581461153> !")
                    return
                
                flag = False
                num = 0
                for pokemon in data:
                    if (pokemon[0].title() == pokename1.title()):
                        if (pokemon[1].title() == pokename1.title()):
                            index = num


                            flag = True
                        
                        else:
                            num += 1
                    else:
                        num += 1
                
                if flag == True:
                    pass
                else:
                    await ctx.send("Error.")
                    return

                data[index][3] = help
                
                view = ConfirmCancel(ctx.author)
               
                await ctx.send(f"Do you want to add HELP {help} for {pokename1} & {pokename2}", view = view)
                await view.wait()

                with open('pokemon_combinations.csv', mode='w', encoding='ISO-8859-1', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)

                await ctx.send("done")
            else:
                await ctx.send("no")

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')


    @commands.group(name = 'guide', aliases = ['g'], invoke_without_command = True)
    async def guide_command(self, ctx, pokemonog1 : str = None,*, pokemonog2 : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if registered_check:

            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

    
            if user_ban_list:
                await ctx.send('You are banned from the bot.')
                return
            
            if ctx.message.reference:
                replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                
                embed = replied_message.embeds[0]   
                embedfield = embed.fields
                
                #this is for the move embed
                firstfiled = embedfield[0]
                pokefiled1 = firstfiled.name
                index_of_used1 = pokefiled1.find("used")

                if index_of_used1 != -1:
                    result_string1 = pokefiled1[:index_of_used1].strip()

                    pokemonog1 = result_string1.replace(" ","") 
                    pokemonog1 = pokemonog1.replace("-","").lower()

                    secondfiled = embedfield[1]
                    pokefiled2 = secondfiled.name
                    index_of_used2 = pokefiled2.find("used")

                    result_string2 = pokefiled2[:index_of_used2].strip()
                    pokemonog2 = result_string2.replace(" ","") 
                    pokemonog2 = pokemonog2.replace("-","").lower()

                
                else:
                    value1 = firstfiled.value
                    matches1 = re.findall(r'\*\*(.*?)\*\*', value1)

                    pokemonog1 = matches1[0].replace(" ","") 
                    pokemonog1 = pokemonog1.replace("-","").lower()

                    secondfiled = embedfield[1]

                    value2 = secondfiled.value
                    matches2 = re.findall(r'\*\*(.*?)\*\*', value2)

                    pokemonog2 = matches2[0].replace(" ","") 
                    pokemonog2 = pokemonog2.replace("-","").lower()

            if (pokemonog1 == None) and (pokemonog2 == None):
                em1 = discord.Embed(
                    title = 'Guide [Aliases: g]',
                    description = 'Commands related to Pokemon Guides:',
                    colour = color
                )

                em1.add_field(name = 'd!guide [pokemon1]', value = 'View all the info on a certain pokemon',inline=False)

                em1.add_field(name = 'd!guide [pokemon1] [pokemon2]', value = 'View the best move in duel would be.',inline=False)

                em1.set_footer(text='Please write the pokemon name in 1 word, the bot can identify it')

                await ctx.send(embed = em1)
            elif (pokemonog2 == None):


                with open(f'pokedex.csv', mode='r', encoding='ISO-8859-1') as file:
                    reader = csv.reader(file)
                    data = list(reader)

                allnames = []
                for pokemon in data:
                    pokenamed = pokemon[1].title().split('-')
                    if pokenamed[-1] == 'Mega':
                        pokenamed.pop(-1)
                        pokenamed = ['Mega'] + pokenamed
                        nameis = ('').join(pokenamed)
                    
                    else:
                        nameis = ('').join(pokenamed)

                    if nameis in allnames:
                        pass
                    else:
                        allnames.append(nameis)

                pokemon1 = pokemonog1.title()
                test = pokemon1.replace(" ","")  
                test = test.replace("-","")  
                if test in allnames:
                    pokemon1 = test.title()
                else:
                    pokemon1 = self.find_matching_pokemon(pokemon1.title(), allnames)

                if pokemon1 == None:
                    await ctx.send(f"Could not find **{pokemonog1}**. If you want to help us add this Pokemon, Make a ticket in <#1091112838581461153> !")
                    return
                
                for pokemon in data:
                    pokenamed = pokemon[1].title().split('-')
                    doc = pokemon[1].title()
                    if pokenamed[-1] == 'Mega':
                        pokenamed.pop(-1)
                        pokenamed = ['Mega'] + pokenamed
                        elephant1 = (' ').join(pokenamed)
                        if elephant1 == 'Mega Rayquaza':
                            elephant1 = 'Rayquaza'
                        nameis = ('').join(pokenamed)
                    
                    else:
                        elephant1 = (' ').join(pokenamed)
                        if elephant1 == 'Mega Rayquaza':
                            elephant1 = 'Rayquaza'

                        nameis = ('').join(pokenamed)

                    if nameis == pokemon1:
                        pokemon1 = doc
                        break
                    else:
                        pass



                for random_pokemon in data:
                    if random_pokemon[1].lower() == pokemon1.lower():
                        name = random_pokemon[1]

                        types = random_pokemon[4]
                        try:
                            types = ast.literal_eval(types)
                        except ValueError:
                            types = [types.strip("[]'")]

                        type_str_formatted = ' / '.join(types)
                        description = random_pokemon[5]
                        image_url = random_pokemon[6]
                        hp = random_pokemon[7]
                        attack = random_pokemon[8]
                        defense = random_pokemon[9]
                        sp_atk = random_pokemon[10]
                        sp_def = random_pokemon[11]
                        speed = random_pokemon[12]
                        total = int(hp) + int(attack) + int(defense) + int(sp_atk) + int(sp_def) + int(speed)
                        embed = discord.Embed(title=f'{name.title()} #{random_pokemon[0]}', description=description, color=0xff5988)
                        embed.set_image(url=f"attachment://{image_url}")
                        embed.add_field(name='Base Stats', value=f'**HP:** {hp}\n**Attack:** {attack}\n**Defense:** {defense}\n**Sp. Atk:** {sp_atk}\n**Sp. Def:** {sp_def}\n**Speed:** {speed}\n**Total:** {total}', inline=True)
                        embed.add_field(name='Type', value=type_str_formatted, inline=True)

                        poke = await self.bot.db.fetch('SELECT * FROM pokes WHERE pokemon = $1', elephant1.lower())

                        if poke:
                            embed.add_field(name='Format Type', value=f'{poke[0]["type"].title()}', inline=True)
                            name = f'{name.capitalize()} #{random_pokemon[0]}'
                            embedpic = image_url
                            view = RareCommon(ctx.author,embedpic, poke, name)

                        else:
                            embed.add_field(name='Format Type', value=f'No Data', inline=True)
                            view = RareCommon2(ctx.author)                            
                            

                    
                        await ctx.send(file = discord.File(image_url) ,embed = embed, view = view)
                        return
                               
                await ctx.send(f"Pokemon not found: {name}")
  


            else:
                with open(f'pokedex.csv', mode='r', encoding='ISO-8859-1') as file:
                    reader = csv.reader(file)
                    data = list(reader)

                allnames = []
                for pokemon in data:
                    pokenamed = pokemon[1].title().split('-')
                    if pokenamed[-1] == 'Mega':
                        pokenamed.pop(-1)
                        pokenamed = ['Mega'] + pokenamed
                        nameis = ('').join(pokenamed)
                    
                    else:
                        nameis = ('').join(pokenamed)

                    if nameis in allnames:
                        pass
                    else:
                        allnames.append(nameis)

                pokemon1 = pokemonog1.title()
                test = pokemon1.replace(" ","")  
                test = test.replace("-","")  
                if test in allnames:
                    pokemon1 = test.title()
                else:
                    pokemon1 = self.find_matching_pokemon(pokemon1.title(), allnames)


                pokemon2 = pokemonog2.title()
                test = pokemon2.replace(" ","")  
                test = test.replace("-","")  
                if test in allnames:
                    pokemon2 = test.title()
                else:
                    pokemon2 = self.find_matching_pokemon(pokemon2.title(), allnames)

                if pokemon2 == None:
                    await ctx.send(f"Could not find **{pokemonog2}**. \nTIPS: If the Pokemon name has 2+ words, do not use a space for example **fluttermane**. If the Pokemon has a Mega version type mega in the word for example **megametagross**")
                    return

                if pokemon1 == None:
                    await ctx.send(f"Could not find **{pokemonog1}**. \nTIPS: If the Pokemon name has 2+ words, do not use a space for example **fluttermane**. If the Pokemon has a Mega version type mega in the word for example **megametagross**!")
                    return
                
                for pokemon in data:
                    pokenamed = pokemon[1].title().split('-')
                    
                    doc = pokemon[1].title()
                    if pokenamed[-1] == 'Mega':
                        pokenamed.pop(-1)
                        pokenamed = ['Mega'] + pokenamed
                        nameis = ('').join(pokenamed)
                    


                    else:
                        nameis = ('').join(pokenamed)
                        
                    if nameis == pokemon2:
                        pokemon2 = doc
                        elephant2 = (' ').join(pokenamed)
                        if elephant2 == 'Mega Rayquaza':
                            elephant2 = 'Rayquaza'
                        whole2 = pokemon
                        break
                        
                    else:
                        pass
                
                for pokemon in data:
                    pokenamed = pokemon[1].title().split('-')
                    
                    doc = pokemon[1].title()
                    if pokenamed[-1] == 'Mega':
                        pokenamed.pop(-1)
                        pokenamed = ['Mega'] + pokenamed
                        nameis = ('').join(pokenamed)
                    


                    else:
                        nameis = ('').join(pokenamed)
                        
                    if nameis == pokemon1:
                        pokemon1 = doc
                        elephant1 = (' ').join(pokenamed)
                        if elephant1 == 'Mega Rayquaza':
                            elephant1 = 'Rayquaza'
                        whole1 = pokemon
                        break
                        
                    else:
                        pass

                mon1 = await self.bot.db.fetch('SELECT * FROM pokes WHERE pokemon = $1', elephant1.lower())

                if mon1:
                    pass
                else:
                    await ctx.send(f"**{elephant1.title()}** hasn't been added, if you'd like to help us add it make a ticket in <#1091112838581461153> .")
                    return

                mon2 = await self.bot.db.fetch('SELECT * FROM pokes WHERE pokemon = $1', elephant2.lower())

                if mon2:
                    pass
                else:
                    await ctx.send(f"**{elephant2.title()}** hasn't been added, if you'd like to help us add it make a ticket in <#1091112838581461153> .")
                    return

                with open(f'pokemon_combinations.csv', mode='r', encoding='ISO-8859-1') as file:
                    reader = csv.reader(file)
                    data = list(reader)
                
                flag = False
                for pokemon in data:

                    if (pokemon[0].lower() == elephant1.lower()) and (pokemon[1].lower() == elephant2.lower()) and (pokemon[2] != ''):

                        move = pokemon[2]

                        helper = pokemon[3]
                        

                        embed = discord.Embed(title=f'{elephant1.title()} VS {elephant2.title()}', description=f'{move}', color=color)
                        embed.set_footer(text=f'Written by {helper} \ See something wrong? Let us know!')

                        type_str_formatted = 'No Data'
                        type_str_formatted2 = 'No Data'


                        pokemon12 = elephant1  

                        pokemon22 = elephant2

                        if pokemon12 == None:
                            pass
                        if pokemon22 == None:
                            pass
                        

                        types = whole1[4]
                        try:
                            types = ast.literal_eval(types)
                        except ValueError:
                            types = [types.strip("[]'")]

                        type_str_formatted = ' / '.join(types)
  

                                
                                

                        types = whole2[4]
                        try:
                            types = ast.literal_eval(types)
                        except ValueError:
                            types = [types.strip("[]'")]

                        type_str_formatted2 = ' / '.join(types)
  
                                

                        moves1 = mon1[0]['moveset']
                        if moves1 == None:
                           moves1 = 'No Data'
                        else:                        
                            moves11 = moves1.split(" | ")
                            if "\\n" in moves11[-1]:
                                last_item_parts = moves11[-1].split("\\n", 1)
                                moves11[-1] = last_item_parts[0]
                                
                            while "anything" in moves11:
                                moves11.remove("anything")
                            
                            positions = {}
                            ommon_words = ['the', 'to', 'and', 'for', 'of', 'you', 'have', 'is', 'in', 'if', 'be', 'or', 'a', 'it', 'can', 'up', 'use', 'rest', 'one', 'like', 'into', 'and', 'save']
                            for movet in moves11:
                                move = move.lower()
                                movec = movet.split()[0]
                                matches = process.extract(movec, move.split(), limit=1)

                    
                                threshold = 80

                                filtered_matches = [match[0] for match in matches if match[1] >= threshold  and match[0].lower() not in ommon_words]

                                if filtered_matches:
                                   
                                    positions[movet] = move.find(filtered_matches[0])

                            sorted_moves = sorted(positions.keys(), key=lambda move: positions[move])

                            num = 0
                            moves11.append('Switch')
                            if sorted_moves == []:
                                moves11[4] = (f"**Switch 《 Best move**")
                            else:
                                for movess in sorted_moves:
                                    index = moves11.index(movess)
                                    moves11[index] = (f"**{movess.title()} 《 Best move**")
                                    break


                            moves1  = ('\n⠀⠀⠀⠀⠀').join(moves11)
                        
                        mon2 = await self.bot.db.fetch('SELECT * FROM pokes WHERE pokemon = $1', elephant2.lower())
                        moves2 = mon2[0]['moveset']
                        if moves2 == None:
                           moves2 = 'No Data'
                        else:
                            moves22 = moves2.split(" | ")
                            if "\\n" in moves22[-1]:
                                last_item_parts = moves22[-1].split("\\n", 1)
                                moves22[-1] = last_item_parts[0]
                                
                            while "anything" in moves22:
                                moves22.remove("anything")

                            moves22 = [word.title() for word in moves22]

                            moves2  = ('\n⠀⠀⠀⠀⠀').join(moves22)
                        
                        embed.add_field(name=f'Your Pokemon | {pokemon1.title()}', value=f'**Type:** {type_str_formatted}\n**Moves:** {moves1}')
                        embed.add_field(name=f'Enemy Pokemon | {pokemon2.title()}', value=f'**Type:** {type_str_formatted2}\n**Moves:** {moves2}')

                        view = ConfirmW(ctx.author)

                        message = await ctx.send(embed = embed, view = view)
                        await view.wait()
                        if view.value == True:
                            flag = True
                        else:
                            return
                
                if flag == True:
                    pass
                else:
                    
                    types = whole1[4]
                    try:
                        types = ast.literal_eval(types)
                    except ValueError:
                        types = [types.strip("[]'")]

                    type_str_formatted = ' / '.join(types)

                            

                    types = whole2[4]
                    try:
                        types = ast.literal_eval(types)
                    except ValueError:
                        types = [types.strip("[]'")]

                    type_str_formatted2 = ' / '.join(types)


                    moves1 = mon1[0]['moveset']

                    moves1 = moves1.split(" | ")
                    if "\\n" in moves1[-1]:
                        last_item_parts = moves1[-1].split("\\n", 1)
                        moves1[-1] = last_item_parts[0]
                    newmoves111 = moves1[3].split(" or ")
                    moves111 = moves1[:3]
                    moves111.extend(newmoves111)

                    moves2 = mon2[0]['moveset']

                    moves2 = moves2.split(" | ")
                    if "\\n" in moves2[-1]:
                        last_item_parts = moves2[-1].split("\\n", 1)
                        moves2[-1] = last_item_parts[0]
                    newmoves222 = moves2[3].split(" or ")
                    moves222 = moves2[:3]
                    moves222.extend(newmoves222)


                    finalmoves1 = []

                    typesnemey = whole2[4]
                    try:
                        typesnemey = ast.literal_eval(typesnemey)
                    except ValueError:
                        typesnemey = [typesnemey.strip("[]'")]

                    for move in moves111:
                        ogmove = move
                        move = move.replace('-', '')
                        move = move.replace(' ', '')

                        our_move_type = self.get_move_type(move)
                        if our_move_type == None:
                            finalmoves1.append(f'{ogmove.title()} » Error')
                        else:
                            effective  = self.check_effectiveness(typesnemey, our_move_type)
                            finalmoves1.append(f'{ogmove.title()} » **{effective.title()}**')
                    
                    moves1 = f"• {finalmoves1[0].title()}\n• {finalmoves1[1].title()}\n• {finalmoves1[2].title()}\n• {finalmoves1[3].title()}"


                    finalmoves2 = []

                    typesnemey = whole1[4]
                    try:
                        typesnemey = ast.literal_eval(typesnemey)
                    except ValueError:
                        typesnemey = [typesnemey.strip("[]'")]

                    for move in moves222:
                        if move.lower() == 'anything':
                            pass
                        else:
                            ogmove = move
                            move = move.replace('-', '')
                            move = move.replace(' ', '')

                            our_move_type = self.get_move_type(move)

                            if our_move_type == None:
                                finalmoves2.append(f'{ogmove.title()} » Error')
                            else:
                                effective  = self.check_effectiveness(typesnemey, our_move_type)
                                finalmoves2.append(f'{ogmove.title()} » **{effective.title()}**')
                    
                    moves2 = f"• {finalmoves2[0].title()}\n• {finalmoves2[1].title()}\n• {finalmoves2[2].title()}\n• {finalmoves2[3].title()}"

                    desc = "No Data / This interaction has no user inputed data so a temporary move suggestion has been made."
                    embed = discord.Embed(title=f'{pokemon1.title()} VS {pokemon2.title()}', description=f'{desc}', color=color)
                    embed.set_footer(text=f'Written by Dom Bot ')     

                    embed.add_field(name=f'Your Pokemon | {pokemon1.title()}', value=f'**Type:** {type_str_formatted}\n**Moves:** \n{moves1}')
                    embed.add_field(name=f'Enemy Pokemon | {pokemon2.title()}', value=f'**Type:** {type_str_formatted2}\n**Moves:** \n{moves2}')

                    view = ConfirmW(ctx.author)

                    message = await ctx.send(embed = embed, view = view)
                    await view.wait()
                if view.value == True:

                    check1 = elephant1
                    elephant1 = elephant2
                    elephant2 = check1

                    check2 = pokemon1
                    pokemon1 = pokemon2
                    pokemon2 = check2

                    check3 = mon1
                    mon1 = mon2
                    mon2 = check3

                    check4 = whole1
                    whole1 = whole2
                    whole2 = check4

                    with open(f'pokemon_combinations.csv', mode='r', encoding='ISO-8859-1') as file:
                        reader = csv.reader(file)
                        data = list(reader)
                    

                    for pokemon in data:

                        if (pokemon[0].lower() == elephant1.lower()) and (pokemon[1].lower() == elephant2.lower()) and (pokemon[2] != ''):

                            move = pokemon[2]

                            helper = pokemon[3]
                            

                            newembed = discord.Embed(title=f'{elephant1.title()} VS {elephant2.title()}', description=f'{move}', color=color)
                            newembed.set_footer(text=f'Written by {helper} \ See something wrong? Let us know!')

                            type_str_formatted = 'No Data'
                            type_str_formatted2 = 'No Data'


                            pokemon12 = elephant1  

                            pokemon22 = elephant2

                            if pokemon12 == None:
                                pass
                            if pokemon22 == None:
                                pass
                            

                            types = whole1[4]
                            try:
                                types = ast.literal_eval(types)
                            except ValueError:
                                types = [types.strip("[]'")]

                            type_str_formatted = ' / '.join(types)
    

                                    
                                    

                            types = whole2[4]
                            try:
                                types = ast.literal_eval(types)
                            except ValueError:
                                types = [types.strip("[]'")]

                            type_str_formatted2 = ' / '.join(types)
    
                                    

                            moves1 = mon1[0]['moveset']
                            if moves1 == None:
                                moves1 = 'No Data'
                            else:                        
                                moves11 = moves1.split(" | ")

                                if "\\n" in moves11[-1]:
                                    last_item_parts = moves11[-1].split("\\n", 1)
                                    moves11[-1] = last_item_parts[0]
                                    
                                while "anything" in moves11:
                                    moves11.remove("anything")

                                
                                positions = {}
                                ommon_words = ['the', 'to', 'and', 'for', 'of', 'you', 'have', 'is', 'in', 'if', 'be', 'or', 'a', 'it', 'can', 'up', 'use', 'rest', 'one', 'like', 'into', 'and', 'save']
                                for movet in moves11:
                                    move = move.lower()
                                    movec = movet.split()[0]
                                    matches = process.extract(movec, move.split(), limit=1)

                        
                                    threshold = 80

                                    filtered_matches = [match[0] for match in matches if match[1] >= threshold  and match[0].lower() not in ommon_words]

                                    if filtered_matches:
                                    
                                        positions[movet] = move.find(filtered_matches[0])

                                sorted_moves = sorted(positions.keys(), key=lambda move: positions[move])

                                num = 0
                                moves11.append('Switch')
                                if sorted_moves == []:
                                    moves11[4] = (f"**Switch 《 Best move**")
                                else:
                                    for movess in sorted_moves:
                                        index = moves11.index(movess)
                                        moves11[index] = (f"**{movess.title()} 《 Best move**")
                                        break


                                moves1  = ('\n⠀⠀⠀⠀⠀').join(moves11)
                            
                            mon2 = await self.bot.db.fetch('SELECT * FROM pokes WHERE pokemon = $1', elephant2.lower())
                            moves2 = mon2[0]['moveset']
                            if moves2 == None:
                                moves2 = 'No Data'
                            else:
                                moves22 = moves2.split(" | ")
                                if "\\n" in moves22[-1]:
                                    last_item_parts = moves22[-1].split("\\n", 1)
                                    moves22[-1] = last_item_parts[0]
                                    
                                while "anything" in moves22:
                                    moves22.remove("anything")
                                moves22 = [word.title() for word in moves22]
                                moves2  = ('\n⠀⠀⠀⠀⠀').join(moves22)
                            
                            newembed.add_field(name=f'Your Pokemon | {pokemon1.title()}', value=f'**Type:** {type_str_formatted}\n**Moves:** {moves1}')
                            newembed.add_field(name=f'Enemy Pokemon | {pokemon2.title()}', value=f'**Type:** {type_str_formatted2}\n**Moves:** {moves2}')

                            await message.edit(embed = newembed)
                            return
                    
                    types = whole1[4]
                    try:
                        types = ast.literal_eval(types)
                    except ValueError:
                        types = [types.strip("[]'")]

                    type_str_formatted = ' / '.join(types)

                            

                    types = whole2[4]
                    try:
                        types = ast.literal_eval(types)
                    except ValueError:
                        types = [types.strip("[]'")]

                    type_str_formatted2 = ' / '.join(types)


                    moves1 = mon1[0]['moveset']

                    moves1 = moves1.split(" | ")
                    if "\\n" in moves1[-1]:
                        last_item_parts = moves1[-1].split("\\n", 1)
                        moves1[-1] = last_item_parts[0]
                    newmoves111 = moves1[3].split(" or ")
                    moves111 = moves1[:3]
                    moves111.extend(newmoves111)

                    moves2 = mon2[0]['moveset']

                    moves2 = moves2.split(" | ")
                    if "\\n" in moves2[-1]:
                        last_item_parts = moves2[-1].split("\\n", 1)
                        moves2[-1] = last_item_parts[0]
                    newmoves222 = moves2[3].split(" or ")
                    moves222 = moves2[:3]
                    moves222.extend(newmoves222)


                    finalmoves1 = []

                    typesnemey = whole2[4]
                    try:
                        typesnemey = ast.literal_eval(typesnemey)
                    except ValueError:
                        typesnemey = [typesnemey.strip("[]'")]

                    for move in moves111:
                        ogmove = move
                        move = move.replace('-', '')
                        move = move.replace(' ', '')

                        our_move_type = self.get_move_type(move)
                        if our_move_type == None:
                            finalmoves1.append(f'{ogmove.title()} » Error')
                        else:
                            effective  = self.check_effectiveness(typesnemey, our_move_type)
                            finalmoves1.append(f'{ogmove.title()} » **{effective.title()}**')
                    
                    moves1 = f"• {finalmoves1[0].title()}\n• {finalmoves1[1].title()}\n• {finalmoves1[2].title()}\n• {finalmoves1[3].title()}"


                    finalmoves2 = []

                    typesnemey = whole1[4]
                    try:
                        typesnemey = ast.literal_eval(typesnemey)
                    except ValueError:
                        typesnemey = [typesnemey.strip("[]'")]

                    for move in moves222:
                        if move.lower() == 'anything':
                            pass
                        else:
                            ogmove = move
                            move = move.replace('-', '')
                            move = move.replace(' ', '')

                            our_move_type = self.get_move_type(move)

                            if our_move_type == None:
                                finalmoves2.append(f'{ogmove.title()} » Error')
                            else:
                                effective  = self.check_effectiveness(typesnemey, our_move_type)
                                finalmoves2.append(f'{ogmove.title()} » **{effective.title()}**')
                    
                    moves2 = f"• {finalmoves2[0].title()}\n• {finalmoves2[1].title()}\n• {finalmoves2[2].title()}\n• {finalmoves2[3].title()}"

                    desc = "No Data / This interaction has no user inputed data so a temporary move suggestion has been made."
                    newembed = discord.Embed(title=f'{pokemon1.title()} VS {pokemon2.title()}', description=f'{desc}', color=color)
                    newembed.set_footer(text=f'Written by Dom Bot ')     

                    newembed.add_field(name=f'Your Pokemon | {pokemon1.title()}', value=f'**Type:** {type_str_formatted}\n**Moves:** \n{moves1}')
                    newembed.add_field(name=f'Enemy Pokemon | {pokemon2.title()}', value=f'**Type:** {type_str_formatted2}\n**Moves:** \n{moves2}')

                    await message.edit(embed = newembed)
                else:
                    pass
               
        
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')


    @commands.group(name = 'calculate', aliases = ['calc'], invoke_without_command = True)
    async def calculate(self, ctx, pokemonog1 : str = None,*, pokemonog2 : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if registered_check:

            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

            poke = await self.bot.db.fetch('SELECT * FROM pokes WHERE pokemon = $1', pokemonog1.lower())

            if poke:
                pass
            else:
                await ctx.send("This pokemon has not been added.")
                return
            
            
            pokedas = poke[0]['mints']
            text = pokedas.replace('\n', '\\\\n')
            await ctx.send(f"```{text}```")                

            if user_ban_list:
                await ctx.send('You are banned from the bot.')
                return
        
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')
 


    @commands.command(name='ttest')
    async def testttt_log(self,ctx):

        registered_check = await self.bot.db.fetch('SELECT * FROM registered')



    @commands.command(name = 'givedc')
    async def ranked_fadfadfgive_wish_command(self, ctx, amt : int = None, member : discord.Member = None):
        if ctx.author.id in [0, 1209502516715192332]:
            if (amt is None) or (member is None):
                em = discord.Embed(
                    title = 'Give dc',
                    description = '**Give DC to players.**\n\nd!givedc [amount] [mention]',
                    colour = color
                )

                await ctx.send(embed = em)

            else:
                player = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                if player:
                    new_wishes = player[0]["banner_pieces"] + amt

                    await self.bot.db.execute('UPDATE registered SET banner_pieces = $1 WHERE player_id = $2', new_wishes, member.id)

                    await ctx.send(f'Gave {amt} DC to {member.name}.')

                else:
                    await ctx.send('That person has not registered yet!')

        else:
            await ctx.send('You do not have permission to use that command.')

    @commands.command(name = 'takedc')
    async def ranked_takedaffafcac_wish_command(self, ctx, amt : int = None, member : discord.Member = None):
        if ctx.author.id in [0, 1209502516715192332]:
            if (amt is None) or (member is None):
                em = discord.Embed(
                    title = 'Take Dc',
                    description = '**Take DC from players.**\n\nd!takedc [amount] [mention]',
                    colour = color
                )

                await ctx.send(embed = em)

            else:
                player = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                if player:

                    if player[0]["banner_pieces"] < amt:
                        confirm_msg = await ctx.send('That person does not have that many Dom Coins!')

                    else:
                        new_wishes = player[0]["banner_pieces"] - amt

                        await self.bot.db.execute('UPDATE registered SET banner_pieces = $1 WHERE player_id = $2', new_wishes, member.id)

                        await ctx.send(f'Took {amt} DC from {member.name}.')

                else:
                    await ctx.send('That person has not registered yet!')

        else:
            await ctx.send('You do not have permission to use that command.')

    @commands.command(name = 'help2')
    async def help2(self, ctx):
        command_list = [f"`{command.name}`" for command in self.bot.commands if not command.hidden]
        await ctx.send(f"Available commands: {', '.join(command_list)}")


def setup(bot):



    bot.add_cog(RadCommands(bot))
