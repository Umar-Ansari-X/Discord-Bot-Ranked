import asyncio
import discord
import random
import json
import math
from discord.ext import commands
import numpy as np
import re
from datetime import datetime, timedelta
import datetime

import time
from pymongo import MongoClient
import asyncio
import string
import random
import csv
import ast
import os

color = 0x32006e

async def quests(self,ctx, a, author_id,  m, member_id):

    def listing(str1 : str):
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
        

            
    if author_id == None:
        pass
    else:
        check1 = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', author_id)
        current_time = datetime.datetime.now()
        total = [5,3,5,3,5,5,3]

        if (check1[0]['quests'] is None) or (check1[0]['daily'] is None) or (check1[0]['daily'] <= current_time):
            flists = str(check1[0]['quests'])
            new_admins = ''
            admins_list = listing(flists)
            randomRol = random.randint(2,6)
            new_admins = f'{randomRol} 0 {total[randomRol]}' 

            now = datetime.datetime.now()
            midnight = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1)
            time_until_midnight = midnight - now            
            delete_time = datetime.datetime.now() + time_until_midnight 
                                                    
            await self.bot.db.execute(f'UPDATE casual SET quests = $1, daily = $2 WHERE player_id = $3', new_admins,delete_time, author_id)
        
        check1 = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', author_id) 
        if check1[0]['quests'] == None:
            pass
        else:
            flists = str(check1[0]['quests'])
            
            new_admins = ''
            admins_list = listing(flists)
            strs = [ 'Complete 5 casual duel', 'Win 3 casual duel','Complete 5 ranked duel', 'Win 3 ranked duel','Complete 5 ranked with commons' , 'complete 5 ranked with rares','Trade 3 times with another user in Dom Bot']
            for p,admin in enumerate(admins_list):
                
                if p == 0:
                    new_admins += str(admin)
                elif p == 1:

                    if int(admins_list[0]) in a:   
                        if admin == admins_list[2]:
                            pass
                        elif int(admin) == (int(admins_list[2])-1):
                            await ctx.send(f"Completed Daily Quest | {strs[int(admins_list[0])]}\n Awarded **50dc** to <@{author_id}>")
                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1', author_id) 
                            admin = int(admin) + 1

                            registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', author_id)
                            nflists = str(registered_check[0]['achievements'])
                            nnew_admins = ''
                            nadmins_list = listing(nflists)
                            for np,nadmin in enumerate(nadmins_list):
                                if np == 0:
                                    nnew_admins += str(nadmin)
                                elif np == 18:
                                    if int(nadmin) == 19:
                                        nadmins_list[19] = 1
                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  author_id)
                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  author_id)
                                        await ctx.send("**Bronze Achievement Completed! ✦ Complete 20 daily quest ✦**\n*10dc rewarded & Lootbox rewarded*")
                                    elif int(nadmin) == 49:
                                        nadmins_list[19] = 2
                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  author_id)
                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  author_id)
                                        await ctx.send("**Silver Achievement Completed! ✦✦ Complete 50 daily quest ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                    elif int(nadmin) == 99:
                                        nadmins_list[19] = 3
                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  author_id)
                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  author_id)
                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Complete 100 daily quest ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                    nadmin = int(nadmin) + 1
                                    nnew_admins += f' {nadmin}'                                                         
                                else:
                                    nnew_admins += f' {nadmin}'  
                            
                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', nnew_admins, author_id)

                        else:
                            admin = int(admin) + 1
                        new_admins += f' {admin}'   
                    else:
                        new_admins += f' {admin}'                                                  
                else:
                    new_admins += f' {admin}'  
            await self.bot.db.execute(f'UPDATE casual SET quests = $1 WHERE player_id = $2', new_admins, author_id)   
                                                            
    
    if member_id == None:
        pass
    else:
        
        check1 = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', member_id)
        current_time = datetime.datetime.now()
        total = [5,3,5,3,5,5,3]

        if (check1[0]['quests'] is None) or (check1[0]['daily'] is None) or (check1[0]['daily'] <= current_time):
            flists = str(check1[0]['quests'])
            new_admins = ''
            admins_list = listing(flists)
            randomRol = random.randint(2,6)
            new_admins = f'{randomRol} 0 {total[randomRol]}' 

            now = datetime.datetime.now()
            midnight = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1)
            time_until_midnight = midnight - now            
            delete_time = datetime.datetime.now() + time_until_midnight 
                                                    
            await self.bot.db.execute(f'UPDATE casual SET quests = $1, daily = $2 WHERE player_id = $3', new_admins,delete_time, member_id)

        check1 = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', member_id)
        if check1[0]['quests'] == None:
            pass
        else:
            flists = str(check1[0]['quests'])
            new_admins = ''
            admins_list = listing(flists)
            strs = [ 'Complete 5 casual duel', 'Win 3 casual duel','Complete 5 ranked duels', 'Win 3 ranked duel','Complete 5 ranked with commons' , 'Complete 5 ranked with rares','Trade 3 times with another user in Dom Bot']

            for p,admin in enumerate(admins_list):
        
                if p == 0:
                    new_admins += str(admin)
                elif p == 1:

                    if int(admins_list[0]) in m:   
                        if admin == admins_list[2]:
                            pass
                        elif int(admin) == (int(admins_list[2])-1):
                            await ctx.send(f"Completed Daily Quest | {strs[int(admins_list[0])]}\n Awarded **50dc** to <@{member_id}>")
                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1', member_id) 
                            admin = int(admin) + 1

                            registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member_id)
                            nflists = str(registered_check[0]['achievements'])
                            nnew_admins = ''
                            nadmins_list = listing(nflists)
                            for np,nadmin in enumerate(nadmins_list):
                                if np == 0:
                                    nnew_admins += str(nadmin)
                                elif np == 18:
                                    if int(nadmin) == 19:
                                        nadmins_list[19] = 1
                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member_id)
                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  member_id)
                                        await ctx.send("**Bronze Achievement Completed! ✦ Complete 20 daily quest ✦**\n*10dc rewarded & Lootbox rewarded*")
                                    elif int(nadmin) == 49:
                                        nadmins_list[19] = 2
                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member_id)
                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  member_id)
                                        await ctx.send("**Silver Achievement Completed! ✦✦ Complete 50 daily quest ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                    elif int(nadmin) == 99:
                                        nadmins_list[19] = 3
                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member_id)
                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  member_id)
                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Complete 100 daily quest ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                    nadmin = int(nadmin) + 1
                                    nnew_admins += f' {nadmin}'                                                         
                                else:
                                    nnew_admins += f' {nadmin}'  
                            
                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', nnew_admins, member_id)
                        else:
                            admin = int(admin) + 1
                        new_admins += f' {admin}'   
                    else:
                        new_admins += f' {admin}'                                                  
                else:
                    new_admins += f' {admin}'  

            await self.bot.db.execute(f'UPDATE casual SET quests = $1 WHERE player_id = $2', new_admins, member_id)   


class RPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 8
    numbre : int = 0
    sort_option = "gained"
    change = 'no'


    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb, self.stat)

    async def create_embed(self, data,lb,stat ):
        lb = self.lb
        bot = self.stat

        gamble = 'Gamble Leaderbaord'

        if self.change == 'no':
            pass
        else:
            self.numbre = 0

        scoreStr = ''        
        lb_embed = discord.Embed(
            title = gamble,
            description = f'Click the buttons to change pages.',
            colour = color
        )


        if self.sort_option == 'wins':
            lb = await bot.db.fetch('SELECT * FROM gamble WHERE player_name IS NOT NULL AND played >= 0 ORDER BY won DESC')
            for i in data:
                scoreStr = f"**Wins 》 **{lb[self.numbre]['won']}\n**Matches 》 **{lb[self.numbre]['played']}"
                name = lb[self.numbre]['player_name']
                lb_embed.add_field(name = f"{self.numbre+1}# {name} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1
                
                
        elif self.sort_option == 'games':
            lb = await bot.db.fetch('SELECT * FROM gamble WHERE player_name IS NOT NULL AND played >= 0 ORDER BY played DESC')
            for i in data:
                scoreStr = f"**Gambles 》 **{lb[self.numbre]['played']}\n**Wins 》 **{lb[self.numbre]['won']}"
                name = lb[self.numbre]['player_name']
                lb_embed.add_field(name = f"{self.numbre+1}# {name} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1            
            
        elif self.sort_option == 'streak':
            lb = await bot.db.fetch('SELECT * FROM gamble WHERE player_name IS NOT NULL AND played >= 0 ORDER BY streak DESC')

            for i in data:
            
                scoreStr = f"**Streak 》 **{lb[self.numbre]['streak']}\n**Wins 》 **{lb[self.numbre]['won']}"
                name = lb[self.numbre]['player_name']
                lb_embed.add_field(name=f"{self.numbre + 1}# {name}", value=f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1   

        elif self.sort_option == 'highest':
            lb = await bot.db.fetch('SELECT * FROM gamble WHERE player_name IS NOT NULL AND played >= 0 ORDER BY highest DESC')
            for i in data:
                scoreStr = f"**Highest Gambled 》 **{'{:,}'.format(lb[self.numbre]['highest'])}\n**Gambles 》 **{lb[self.numbre]['played']}"
                name = lb[self.numbre]['player_name']
                lb_embed.add_field(name = f"{self.numbre+1}# {name} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1     

        elif self.sort_option == 'gained':
            lb = await bot.db.fetch('SELECT * FROM gamble WHERE player_name IS NOT NULL AND played >= 0 ORDER BY total DESC')
            for i in data:
                scoreStr = f"**Total Earned 》 **{'{:,}'.format(lb[self.numbre]['total'])}\n**Gambles 》 **{lb[self.numbre]['played']}"
                name = lb[self.numbre]['player_name']
                lb_embed.add_field(name = f"{self.numbre+1}# {name} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1     

        elif self.sort_option == 'lost':
            lb = await bot.db.fetch('SELECT * FROM gamble WHERE player_name IS NOT NULL AND played >= 0 ORDER BY net DESC')
            for i in data:
                scoreStr = f"**Total Lost 》 **{'{:,}'.format(lb[self.numbre]['net'])}\n**Gambles 》 **{lb[self.numbre]['played']}"
                name = lb[self.numbre]['player_name']
                lb_embed.add_field(name = f"{self.numbre+1}# {name} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1  

        elif self.sort_option == 'ticket':
            lb = await bot.db.fetch('SELECT * FROM gamble WHERE player_name IS NOT NULL AND played >= 0 ORDER BY ticket DESC')

            for i in data:
                scoreStr = f"**🎟️ 》 **{lb[self.numbre]['ticket']}\n**Gambles 》 **{lb[self.numbre]['played']}"
                name = lb[self.numbre]['player_name']
                lb_embed.add_field(name = f"{self.numbre+1}# {name} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1  

        self.change = 'no'

        lb_embed.set_footer(text = f'Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')



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

        delete = 16
        if int(len(self.data)) < self.sep * self.current_page:
            new = int(len(self.data)) - self.sep * (self.current_page -1)
            delete = new + 8
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

    @discord.ui.select(placeholder="Sort by..", min_values=1, max_values=1,
                       options=[
                           discord.SelectOption(label="Games played", value="games"),
                           discord.SelectOption(label="Total Wins", value="wins"),
                           discord.SelectOption(label="Win Streak", value="streak"),
                           discord.SelectOption(label="Highest Gambled", value="highest"),
                           discord.SelectOption(label="Total Gained", value="gained"),
                           discord.SelectOption(label="Total Lost", value="lost"),
                       ])
    

    async def sort_dropdown(self, select: discord.ui.Select, interaction: discord.Interaction):
        await interaction.response.defer()
        self.sort_option = select.values[0]
        self.change = 'yes'
        self.current_page = 1
        await self.update_message(self.get_current_page_data(), self.lb, self.stat)



class RollForfeit(discord.ui.View):
    def __init__(self, member : discord.Member):
        super().__init__(timeout = 120)

        self.value = None
        self.member = member

    @discord.ui.button(label = "Roll", style = discord.ButtonStyle.red, emoji = "🎲" )
    async def confirm_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = True
        self.stop()
                
        for i in self.children:
            i.disabled = True

        await interaction.response.edit_message(view = self)
            
    @discord.ui.button(label = "Forfeit", style = discord.ButtonStyle.blurple, emoji = "🏳️" )
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

class SPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 6
    numbre : int = 0
    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb, self.stat)

    async def create_embed(self, data,lb,stat ):
        lb = self.lb
        stat = self.stat
        stat = stat.lower()
        if (stat == 'borders') or (stat == 'border') or (stat == 'bo'):
            title = 'Border Player-based Market'
            desc = "Use the Item ID when when buying items\nFilter using `S`,`A`,`B`,`C`,`D` or search the item\nSort using `price` or enter a range using `>number` or `<number`."     
        elif (stat == 'avaborders') or (stat == 'avaborder') or (stat == 'a'):
            title = "AvaBorder Player-based Market"
            desc = "Use the Item ID when when buying items\nFilter using `S`,`A`,`B`,`C`,`D` or search the item\nSort using `price` or enter a range using `>number` or `<number`."
        else:
            title = 'Banner Player-based Market'
            desc = "Use the Item ID when when buying items\nFilter using `SS`,`S`,`A`,`B`,`C`,`D` or search the item\nSort using `price` or enter a range using `>number` or `<number`."
        lb_embed = discord.Embed(
            title = title,
            description = desc,
            colour = color
        )
     
        for i in data:
            lb_embed.add_field(name = f'{lb[self.numbre]["item_name"].title()}', value = f'Rank | **{lb[self.numbre]["rank"].title()}**\nItem ID | **{lb[self.numbre]["item_id"]}**\nCost | x**{lb[self.numbre]["price"]} Dc**')
            self.numbre = self.numbre + 1

        lb_embed.set_footer(text = f'Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')

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
                       style=discord.ButtonStyle.blurple,emoji="🔹")
    async def prev_button(self,  button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()

        delete =  int(len(self.data)) - self.sep * self.current_page
        delete = 12
        if int(len(self.data)) < self.sep * self.current_page:
            new = int(len(self.data)) - self.sep * (self.current_page -1)
            delete = new + 6
        self.current_page -= 1
        self.numbre -= delete
        await self.update_message(self.get_current_page_data(), self.lb, self.stat)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple,emoji="🔹")
    async def next_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data(), self.lb, self.stat)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red,emoji="♦️")
    async def last_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page = math.ceil(len(self.data) / self.sep)
        self.numbre = (self.sep * (self.current_page -1))
        await self.update_message(self.get_current_page_data(), self.lb, self.stat)

class MPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 6
    numbre : int = 0
    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb, self.stat)

    async def create_embed(self, data,lb,stat ):
        lb = self.lb
        stat = self.stat
        stat = stat.lower()

        title = 'My listed items'
        desc = "You have listed the following items"
        lb_embed = discord.Embed(
            title = title,
            description = desc,
            colour = color
        )
     
        for i in data:
            lb_embed.add_field(name = f'{lb[self.numbre]["item_name"].title()}', value = f'Rank | **{lb[self.numbre]["rank"].title()}**\nItem ID | **{lb[self.numbre]["item_id"]}**\nCost | x**{lb[self.numbre]["price"]} Dc**')
            self.numbre = self.numbre + 1

        lb_embed.set_footer(text = f'Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')

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
                       style=discord.ButtonStyle.blurple,emoji="🔹")
    async def prev_button(self,  button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()

        delete =  int(len(self.data)) - self.sep * self.current_page
        delete = 12
        if int(len(self.data)) < self.sep * self.current_page:
            new = int(len(self.data)) - self.sep * (self.current_page -1)
            delete = new + 6
        self.current_page -= 1
        self.numbre -= delete
        await self.update_message(self.get_current_page_data(), self.lb, self.stat)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple,emoji="🔹")
    async def next_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data(), self.lb, self.stat)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red,emoji="♦️")
    async def last_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page = math.ceil(len(self.data) / self.sep)
        self.numbre = (self.sep * (self.current_page -1))
        await self.update_message(self.get_current_page_data(), self.lb, self.stat)
async def id1_generator(size=2, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

async def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

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

class TradeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        
    @commands.command(name ='trade', aliases = ['t'])
    async def trade(self, ctx, member: discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if member is None:
                em = discord.Embed(
                    title = 'Trade',
                    description = '**Trade items with an user.**\n\nd!trade [mention]',
                    colour = color
                )

                await ctx.send(embed = em)

            else:
                if ctx.author == member:
                    await ctx.send("You can't trade with yourself!")
                else:
                    member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                    if member_registered:
                        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)
                        player_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', member.id)

                
                        if user_ban_list:
                            await ctx.send('You are banned from the bot.')
                        elif player_ban_list:
                            await ctx.send('They are banned from the bot.')

                        else:

                            if member_registered[0]['trade'] == 'yes':
                                await ctx.send("Member is already in a trade!")
                            elif registered_check[0]['trade'] == 'yes':
                                await ctx.send("You are already in a trade!")
                            else:
                                trade = 'yes'
                                await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, member.id)
                                await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id)                             
                                view = ConfirmCancel(member)
                                await ctx.send(f"{ctx.author.mention} wants to trade with {member.mention}, accept trade?", view = view)
                                await view.wait()
                        
                                if view.value == True:
                                    if member_registered[0]['trade'] == 'yes':
                                        await ctx.send("Too many requests!")
                                    elif registered_check[0]['trade'] == 'yes':
                                        await ctx.send("Too many requests!")
                                    else:
                                        em = discord.Embed(
                                            title = 'Trade',
                                            description = '**ADD** items using `d!add [item type] [item]`\n**REMOVE** items using `d!remove [item type] [item]`\n**ACCEPT** using `d!accept`\n\n➜ Cross Trading is NOT allowed, if caught you will be banned from the bot.',
                                            colour = color
                                        )

                                        await ctx.send(f"{member.mention} has accepted the trade.",embed = em)


                                        show1_items = ['Dom Coins', 0,  'LootBoxes', 0, 'Keys', 0]
                                        show2_items = ['Dom Coins', 0, 'LootBoxes', 0, 'Keys', 0]
                                        trade_items = {ctx.author: [], member: []}

                                        while True:
                                            try:
                                                msg = await self.bot.wait_for('message', check=lambda message: message.author in [ctx.author, member] and message.content.lower().startswith('d!'), timeout=300.0)
                                            except asyncio.TimeoutError:
                                                trade = 'no'
                                                await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, member.id)
                                                await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id) 
                                                await ctx.send("Trade timed out.")
                                                return

                                            if (msg.content.lower().startswith("d!add")) or (msg.content.lower().startswith("d.add")):

                                                item = msg.content.split()
                                                if len(item) != 3:
                                                    await ctx.send("Incorrect format, `d!add [Item type] [Item name/amt]`")
                                                else:
                                                    try:
                                                        trade_items[ctx.author].remove("done")
                                                    except KeyError as e:
                                                        pass
                                                    except ValueError as e:
                                                        pass
                                                    try:
                                                        trade_items[member].remove("done")
                                                    except KeyError as e:
                                                        pass
                                                    except ValueError as e:
                                                        pass

                                                    if (item[1].lower() == 'domcoins') or (item[1].lower() == 'dcs') or (item[1].lower() == 'domcoin'):
                                                        item[1] = 'dc'
                                                    if (item[1].lower() == 'key'):
                                                        item[1] = 'keys'
                                                    if (item[1].lower() == 'lbs') or (item[1].lower() == 'lb') or (item[1].lower() == 'lootbox'):
                                                        item[1] = 'lootboxes'
                                                    if (item[1].lower() == 'b'):
                                                        item[1] = 'banners'
                                                    if (item[1].lower() == 'bo'):
                                                        item[1] = 'border'
                                                    if (item[1].lower() == 'a') or (item[1].lower() == 'avatarborder') or (item[1].lower() == 'avatarborders'):
                                                        item[1] = 'avaborder'

                                                    if (item[1].lower() == 'title') or (item[1].lower() == 'titles') or (item[1].lower() == 't'):
                                                        await ctx.send("Titles can't be traded.")
                                                    elif (item[1].lower() == 'banner') or (item[1].lower() == 'banners') or (item[1].lower() == 'borders') or (item[1].lower() == 'border') or (item[1].lower() == 'avaborder') or (item[1].lower() == 'avaborders') or (item[1].lower() == 'dc') or (item[1].lower() == 'keys')or (item[1].lower() == 'lootboxes'):
                                                        if item[1].lower()== 'dc':
                                                            if item[2].isnumeric():
                                                                if msg.author == ctx.author:
                                                                    amt = registered_check[0]["banner_pieces"]
                                                
                                                                    total = int(show1_items[1]) + int(item[2])
                                                                    if total > amt:
                                                                        await ctx.send("You don't have enough Dc!")
                                                                    else:
                                                                        show1_items[1] =  int(show1_items[1]) + int(item[2])
                                                                    
                                                                else:
                                                                    amt = member_registered[0]["banner_pieces"]
                                                                    total = int(show2_items[1]) + int(item[2])
                                                                    if total > amt:
                                                                        await ctx.send("You don't have enough Dc!")
                                                                    else:
                                                                        show2_items[1] =  int(show2_items[1]) + int(item[2])
                                                            else:
                                                                await ctx.send("Dc must be a number!")
                                                        elif item[1].lower()== 'keys':
                                                            if item[2].isnumeric():
                                                                if msg.author == ctx.author:
                                                                    amt = registered_check[0]["scraps"]
                                                
                                                                    total = int(show1_items[5]) + int(item[2])
                                                                    if total > amt:
                                                                        await ctx.send("You don't have enough Keys!")
                                                                    else:
                                                                        show1_items[5] =  int(show1_items[5]) + int(item[2])
                                                                    
                                                                else:
                                                                    amt = member_registered[0]["scraps"]
                                                                    total = int(show2_items[5]) + int(item[2])
                                                                    if total > amt:
                                                                        await ctx.send("You don't have enough Keys!")
                                                                    else:
                                                                        show2_items[5] =  int(show2_items[5]) + int(item[2])
                                                            else:
                                                                await ctx.send("Keys must be a number!")
                                                        elif item[1].lower()== 'lootboxes':
                                                            if item[2].isnumeric():
                                                                if msg.author == ctx.author:
                                                                    amt = registered_check[0]["wishes"]
                                                
                                                                    total = int(show1_items[3]) + int(item[2])
                                                                    if total > amt:
                                                                        await ctx.send("You don't have enough LootBoxes!")
                                                                    else:
                                                                        show1_items[3] =  int(show1_items[3]) + int(item[2])
                                                                    
                                                                else:
                                                                    amt = member_registered[0]["wishes"]
                                                                    total = int(show2_items[3]) + int(item[2])
                                                                    if total > amt:
                                                                        await ctx.send("You don't have enough LootBoxes!")
                                                                    else:
                                                                        show2_items[3] =  int(show2_items[3]) + int(item[2])
                                                            else:
                                                                await ctx.send("LootBoxes must be a number!")
                                                        else:
                                                            stat = str(item[1].lower())
                                                            banner_name = str(item[2])

                                                            if (stat == 'border') or (stat == 'borders'):
                                                                stats = 'borders'
                                                                lists = 'border_list'
                                                                name = 'border_name'
                                                                current = 'banner_border'
                                                            elif (stat == 'avaborders') or (stat == 'avaborder'):
                                                                stats = 'avatar_borders'
                                                                lists = 'avaborder_list'
                                                                name = 'banner_name'
                                                                current = 'avatar_border'
                                                            elif (stat == 'banner') or (stat == 'banners'):
                                                                stats = 'banners'
                                                                lists = 'banner_list'
                                                                name = 'banner_name'
                                                                current = 'current_banner'

                                                            banners = await self.bot.db.fetch(f'SELECT * FROM {stats}')
                                                            banner_list = []
                                                            for i in range(len(banners)):
                                                                banner_list.append(banners[i][name])

                                                            if banner_name.lower() in banner_list:    
                                                                if msg.author == ctx.author:
                                                                    flists = str(registered_check[0][lists])
                                                                else:
                                                                    flists = str(member_registered[0][lists])
                                                                
                                                                my_banner_list = self.listing(flists)
                                                                if banner_name.lower() in my_banner_list:
                                                                    badlist = ['bronze2','silver2','gold2','platinum2','dominant2','bronze','silver','gold','platinum','dominant']
                                                                
                                                                    if banner_name.lower() in badlist:
                                                                        await ctx.send("This item is not tradable")
                                                                    else:
                                                                        if msg.author == ctx.author:
                                                                            ind = int(my_banner_list.index(banner_name.lower()))
                                                                            realind = my_banner_list[ind+1]
                                                                            add =0
                                                                            for i in show1_items:
                                                                                if i is None:
                                                                                    pass
                                                                                else:
                                                                                    if i == banner_name.title():
                                                                                        add += 1
                                                                
                                                                            if int(realind) - add > 0:
                                                                                show1_items.append(item[1].title())
                                                                                show1_items.append(item[2].title())
                                                                            else:
                                                                                await ctx.send("You don't have more of this item!")
                                                                            
                                                                        else:
                                                                            ind = int(my_banner_list.index(banner_name.lower()))
                                                                            realind = my_banner_list[ind+1]
                                                                            add =0
                                                                            for i in show2_items:
                                                                                if i is None:
                                                                                    pass
                                                                                else:
                                                                                    if i == banner_name.title():
                                                                                        add += 1
                                                                            if int(realind) - add > 0:
                                                                                show2_items.append(item[1].title())
                                                                                show2_items.append(item[2].title())
                                                                            else:
                                                                                await ctx.send("You don't have more of this item!")
                                                                else:
                                                                    await ctx.send('You do not own that item.')

                                                            else:
                                                                await ctx.send('Item not found.')

                                                        embed = discord.Embed(title="Trade", color=discord.Color.green())
                                                        embedstr1 = ''
                                                        embedstr2 = ''
                                                        test1 = 0
                                                        test2 = 0
                                                        for i in show1_items:
                                                            
                                                            if test1%2 == 0:
                                                                if show1_items[test1+1] == 0:
                                                                    pass
                                                                else:
                                                                    embedstr1 += f'{show1_items[test1]} **{show1_items[test1+1]}**\n'
                                                            else:
                                                                pass
                                                            test1 += 1
                                                        for i in show2_items:
                                                            if test2%2 == 0:
                                                                if show2_items[test2+1] == 0:
                                                                    pass
                                                                else:
                                                                    embedstr2 += f'{show2_items[test2]} **{show2_items[test2+1]}**\n'
                                                            else:
                                                                pass
                                                            
                                                            test2 += 1
                                                        if embedstr1 == '':
                                                            embedstr1 = 'None'
                                                        if embedstr2 == '':
                                                            embedstr2 = 'None'

                                                        if "done" in trade_items[ctx.author]:
                                                            emoji1 = ':green_circle:'
                                                        else:
                                                            emoji1 = ':red_circle:'
                                                        if "done" in trade_items[member]:
                                                            emoji2 = ':green_circle:'
                                                        else:
                                                            emoji2 = ':red_circle:'
                                                        embed.add_field(name=f"{emoji1} {ctx.author.display_name}'s Items", value=embedstr1, inline=True)
                                                        embed.add_field(name=f"{emoji2} {member.display_name}'s Items", value=embedstr2, inline=True)
                                                        await msg.channel.send(embed=embed)
                                                    else:
                                                        await ctx.send("Incorrect format, `d!add [Item type] [Item name/amt]`")

                                            elif (msg.content.lower().startswith("d!remove")) or (msg.content.lower().startswith("d.remove")):

                                                item = msg.content.split()
                                                if len(item) != 3:
                                                    await ctx.send("Incorrect format, `d!remove [Item type] [Item name/amt]`")
                                                else:
                                                    try:
                                                        trade_items[ctx.author].remove("done")
                                                    except KeyError as e:
                                                        pass
                                                    except ValueError as e:
                                                        pass
                                                    try:
                                                        trade_items[member].remove("done")
                                                    except KeyError as e:
                                                        pass
                                                    except ValueError as e:
                                                        pass

                                                    if (item[1].lower() == 'domcoins') or (item[1].lower() == 'dcs') or (item[1].lower() == 'domcoin'):
                                                        item[1] = 'dc'
                                                    if (item[1].lower() == 'key'):
                                                        item[1] = 'keys'
                                                    if (item[1].lower() == 'lbs') or (item[1].lower() == 'lb') or (item[1].lower() == 'lootbox'):
                                                        item[1] = 'lootboxes'
                                                    if (item[1].lower() == 'b'):
                                                        item[1] = 'banners'
                                                    if (item[1].lower() == 'bo'):
                                                        item[1] = 'border'
                                                    if (item[1].lower() == 'a') or (item[1].lower() == 'avatarborder') or (item[1].lower() == 'avatarborders'):
                                                        item[1] = 'avaborder'

                                                    if (item[1].lower() == 'title') or (item[1].lower() == 'titles') or (item[1].lower() == 't'):
                                                        await ctx.send("Titles can't be traded.")
                                                    elif (item[1].lower() == 'banner') or (item[1].lower() == 'banners') or (item[1].lower() == 'borders') or (item[1].lower() == 'border') or (item[1].lower() == 'avaborder') or (item[1].lower() == 'avaborders') or (item[1].lower() == 'dc') or (item[1].lower() == 'keys')or (item[1].lower() == 'lootboxes'):
                                                        if item[1].lower()== 'dc':
                                                            if item[2].isnumeric():
                                                                if msg.author == ctx.author:
                                                                    amt = registered_check[0]["banner_pieces"]
                                                
                                                                    if int(show1_items[1]) - int(item[2]) < 0:
                                                                        await ctx.send("Not enough added in the trade.")
                                                                    else:
                                                                        show1_items[1] = show1_items[1] - int(item[2])
                                                                            
                                                                    
                                                                else:
                                                                    amt = member_registered[0]["banner_pieces"]

                                                                    if int(show2_items[1]) - int(item[2])< 0:
                                                                        await ctx.send("Not enough added in the trade.")
                                                                    else:
                                                                        show2_items[1] = show2_items[1] - int(item[2])
                                                            else:
                                                                await ctx.send("Dc must be a number!")
                                                        elif item[1].lower()== 'keys':
                                                            if item[2].isnumeric():
                                                                if msg.author == ctx.author:
                                                                    amt = registered_check[0]["scraps"]
                                                
                                                                    if int(show1_items[5]) - int(item[2]) < 0:
                                                                        await ctx.send("Not enough added in the trade.")
                                                                    else:
                                                                        show1_items[5] = show1_items[5] - int(item[2])
                                                                            
                                                                    
                                                                else:
                                                                    amt = member_registered[0]["banner_pieces"]

                                                                    if int(show2_items[5]) - int(item[2])< 0:
                                                                        await ctx.send("Not enough added in the trade.")
                                                                    else:
                                                                        show2_items[5] = show2_items[5] - int(item[2])
                                                            else:
                                                                await ctx.send("Keys must be a number!")
                                                        elif item[1].lower()== 'lootboxes':
                                                            if item[2].isnumeric():
                                                                if msg.author == ctx.author:
                                                                    amt = registered_check[0]["wishes"]
                                                
                                                                    if int(show1_items[3]) - int(item[2]) < 0:
                                                                        await ctx.send("Not enough added in the trade.")
                                                                    else:
                                                                        show1_items[3] = show1_items[3] - int(item[2])
                                                                            
                                                                    
                                                                else:
                                                                    amt = member_registered[0]["banner_pieces"]

                                                                    if int(show2_items[3]) - int(item[2])< 0:
                                                                        await ctx.send("Not enough added in the trade.")
                                                                    else:
                                                                        show2_items[3] = show2_items[3] - int(item[2])
                                                            else:
                                                                await ctx.send("Lootboxes must be a number!")
                                                        else:
                                                            stat = str(item[1].lower())
                                                            banner_name = str(item[2])
                                                            if (stat == 'border') or (stat == 'borders'):
                                                                stats = 'borders'
                                                                lists = 'border_list'
                                                                name = 'border_name'
                                                                current = 'banner_border'
                                                            elif (stat == 'avaborders') or (stat == 'avaborder'):
                                                                stats = 'avatar_borders'
                                                                lists = 'avaborder_list'
                                                                name = 'banner_name'
                                                                current = 'avatar_border'
                                                            elif (stat == 'banner') or (stat == 'banners'):
                                                                stats = 'banners'
                                                                lists = 'banner_list'
                                                                name = 'banner_name'
                                                                current = 'current_banner'

                                                            banners = await self.bot.db.fetch(f'SELECT * FROM {stats}')
                                                            banner_list = []
                                                            for i in range(len(banners)):
                                                                banner_list.append(banners[i][name])

                                                            if banner_name.lower() in banner_list:       
                                                                if msg.author == ctx.author:
                                                                    flists = str(registered_check[0][lists])
                                                                else:
                                                                    flists = str(member_registered[0][lists])
                                                                
                                                                my_banner_list = self.listing(flists)
                                                                if banner_name.lower() in my_banner_list:

                                                                    if msg.author == ctx.author:
                                                                        ind = int(my_banner_list.index(banner_name.lower()))
                                                                        realind = my_banner_list[ind+1]
                                                                        add =0
                                                                        for i in show1_items:
                                                                            if i is None:
                                                                                pass
                                                                            else:
                                                                                if i == banner_name.title():
                                                                                    add += 1
                                                            
                                                                        if int(realind) - add >= 0:

                                                                            show1_items.remove(item[1].title())
                                                                            show1_items.remove(item[2].title())
                                                                        else:
                                                                            await ctx.send("You don't have more of this item!")
                                                                        
                                                                    else:
                                                                        ind = int(my_banner_list.index(banner_name.lower()))
                                                                        realind = my_banner_list[ind+1]
                                                                        add =0
                                                                        for i in show2_items:
                                                                            if i is None:
                                                                                pass
                                                                            else:
                                                                                if i == banner_name.title():
                                                                                    add += 1
                                                                        if int(realind) - add >= 0:
            
                                                                            show2_items.remove(item[1].title())
                                                                            show2_items.remove(item[2].title())
                                                                        else:
                                                                            await ctx.send("You don't have more of this item!")
                                                                else:
                                                                    await ctx.send('You do not own that item.')

                                                            else:
                                                                await ctx.send('Item not found.')

                                                        embed = discord.Embed(title="Trade", color=discord.Color.green())
                                                        embedstr1 = ''
                                                        embedstr2 = ''
                                                        test1 = 0
                                                        test2 = 0
                                                        for i in show1_items:
                                                            
                                                            if test1%2 == 0:
                                                                if show1_items[test1+1] == 0:
                                                                    pass
                                                                else:
                                                                    embedstr1 += f'{show1_items[test1]} **{show1_items[test1+1]}**\n'
                                                            else:
                                                                pass
                                                            test1 += 1
                                                        for i in show2_items:
                                                            if test2%2 == 0:
                                                                if show2_items[test2+1] == 0:
                                                                    pass
                                                                else:
                                                                    embedstr2 += f'{show2_items[test2]} **{show2_items[test2+1]}**\n'
                                                            else:
                                                                pass
                                                            
                                                            test2 += 1
                                                        if embedstr1 == '':
                                                            embedstr1 = 'None'
                                                        if embedstr2 == '':
                                                            embedstr2 = 'None'

                                                        if "done" in trade_items[ctx.author]:
                                                            emoji1 = ':green_circle:'
                                                        else:
                                                            emoji1 = ':red_circle:'
                                                        if "done" in trade_items[member]:
                                                            emoji2 = ':green_circle:'
                                                        else:
                                                            emoji2 = ':red_circle:'

                                                        embed.add_field(name=f"{emoji1} {ctx.author.display_name}'s Items", value=embedstr1, inline=True)
                                                        embed.add_field(name=f"{emoji2} {member.display_name}'s Items", value=embedstr2, inline=True)
                                                        await msg.channel.send(embed=embed)
                                                    else:
                                                        await ctx.send("Incorrect format, `d!remove [Item type] [Item name/amt]`")

                                            elif (msg.content.lower() == "d!accept") or  (msg.content.lower() == "d.accept"):
                                                trade_items[msg.author].append("done")
                                                if "done" in trade_items[ctx.author]:
                                                    emoji1 = ':green_circle:'
                                                else:
                                                    emoji1 = ':red_circle:'
                                                if "done" in trade_items[member]:
                                                    emoji2 = ':green_circle:'
                                                else:
                                                    emoji2 = ':red_circle:'
                                                embed = discord.Embed(title="Trade", color=discord.Color.green())
                                                embedstr1 = ''
                                                embedstr2 = ''
                                                test1 = 0
                                                test2 = 0
                                                for i in show1_items:
                                                    
                                                    if test1%2 == 0:
                                                        if show1_items[test1+1] == 0:
                                                            pass
                                                        else:
                                                            embedstr1 += f'{show1_items[test1]} **{show1_items[test1+1]}**\n'
                                                    else:
                                                        pass
                                                    test1 += 1
                                                for i in show2_items:
                                                    if test2%2 == 0:
                                                        if show2_items[test2+1] == 0:
                                                            pass
                                                        else:
                                                            embedstr2 += f'{show2_items[test2]} **{show2_items[test2+1]}**\n'
                                                    else:
                                                        pass
                                                    
                                                    test2 += 1
                                                if embedstr1 == '':
                                                    embedstr1 = 'None'
                                                if embedstr2 == '':
                                                    embedstr2 = 'None'
                                                embed.add_field(name=f"{emoji1} {ctx.author.display_name}'s Items", value=embedstr1, inline=True)
                                                embed.add_field(name=f"{emoji2} {member.display_name}'s Items", value=embedstr2, inline=True)
                                                if "done" in trade_items[ctx.author] and "done" in trade_items[member]:
                                                    #cash
                                                    await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', member.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', ctx.author.id)
                                                    dc1 = show1_items[1]
                                                    dc2 = show2_items[1]
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {dc2} WHERE player_id = $1', ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {dc1} WHERE player_id = $1', member.id)

                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - {dc1} WHERE player_id = $1', ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - {dc2} WHERE player_id = $1', member.id)
                                                    key1 = show1_items[5]
                                                    key2 = show2_items[5]
                                                    await self.bot.db.execute(f'UPDATE registered SET scraps = scraps + {key2} WHERE player_id = $1', ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET scraps = scraps + {key1} WHERE player_id = $1', member.id)

                                                    await self.bot.db.execute(f'UPDATE registered SET scraps = scraps - {key1} WHERE player_id = $1', ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET scraps = scraps - {key2} WHERE player_id = $1', member.id)
                                                    lb1 = show1_items[3]
                                                    lb2 = show2_items[3]
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + {lb2} WHERE player_id = $1', ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + {lb1} WHERE player_id = $1', member.id)

                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes - {lb1} WHERE player_id = $1', ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes - {lb2} WHERE player_id = $1', member.id)
                                                    #itemj.ml

                                                    previous_was_type = False
                                                    lists = ''
                                                    check = 0
                                                    for i in show1_items:
                                                        check += 1
                                                        if previous_was_type is False:
                                                            if check > 2:
                                                                if i == 'Banners':
                                                                    i = 'Banner'
                                                                elif i == 'Borders':
                                                                    i = 'Border'
                                                                elif i == 'Avaborders':
                                                                    i = 'Avaborder'

                                                                if (i == 'Banner') or (i == 'Border') or (i == 'Avaborder'):
                                                                    if i == 'Banner':
                                                                        stats = 'banners'
                                                                        lists = 'banner_list'
                                                                        name = 'banner_name'
                                                                        current = 'current_banner'
                                                                        count = 'banner_count'

                                                                        previous_was_type = True
                                                                    elif i == 'Border':
                                                                        stats = 'borders'
                                                                        lists = 'border_list'
                                                                        name = 'border_name'
                                                                        current = 'banner_border'
                                                                        count = 'border_count'
                                                                        previous_was_type = True
                                                                    elif i == 'Avaborder':
                                                                        stats = 'avatar_borders'
                                                                        lists = 'avaborder_list'
                                                                        name = 'banner_name'
                                                                        current = 'avatar_border'
                                                                        count = 'avaborder_count'
                                                                        previous_was_type = True
                                                        else:
                                                            await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', member.id)
                                                            s = 1
                                                            registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                                                            member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)


                                                            flists = str(member_registered[0][lists])
                                                            listbuy = self.listing(flists)

                                                            if i.lower() in listbuy:
                                                                new_admins = ''
                                                                admins_list = self.listing(flists)
                                                                for admin in admins_list:
                                                                    if admins_list.index(admin) == 0:
                                                                
                                                                        if s == 0:   
                                                                            admin = int(admin) + 1
                                                                            s += 1
                                                                        if admin == i.lower():
                                                                            s = 0
                                                                        new_admins += str(admin)
                                                                    

                                                                    else:
                                                                        if s == 0:
                                                                            admin = int(admin) + 1
                                                                            s+=1
                                                                        if admin == i.lower():
                                                                            s = 0

                                                                        new_admins += f' {admin}'

                                                                await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, member.id) 
                                                            else:                                                    
                                                                itemcode = await id_generator()
                                                                
                                                                a = f'{i.lower()}'
                            
                                                                b = 1
                                                                c = f"{itemcode}"
                                                                if member_registered[0][lists] is None:
                                                                    admins_list = self.listing(flists)
                                                                    new_admins = f' {a}' + f' {b}' + f' {c}'
                            
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, member.id)
            

                                                                else:
                                                                    
                                                                    new_admins = str(flists) + f' {a}' + f' {b}' + f' {c}'
                            
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, member.id)

                                                            await self.bot.db.execute(f'UPDATE registered SET {count} = {count} - 1 WHERE player_id = $1', ctx.author.id)
                                                            s = 1
                                                            t = 1
                                                            flists = str(registered_check[0][lists])
                                                            listbuy = self.listing(flists)
                                            
                                                            if i.lower() in listbuy:
                                                    
                                                                new_admins = ''
                                                                admins_list = self.listing(flists)
                                                                for p,admin in enumerate(admins_list):

                                                                    if admins_list.index(admin) == 0:
                                                                        if t == 0:
                                                                            admin = ''
                                                                            t = 1
                                                                        if s == 0:
                                                                            if int(admin) == 1:
                                                                                admin = ''
                                                                                t = 0
                                                                            else: 
                                                                                admin = int(admin) - 1
                                                                            s += 1
                                                                        if admin == i.lower():
                                                                            if int(admins_list[p+1]) == 1:
                                                                                admin = ''
                                                                            s = 0
                                                                        new_admins += str(admin)
                                                                    

                                                                    else:
                                                                        if t == 0:
                                                                            admin = ''
                                                                            t = 1
                                                                        if s == 0:
                                                                            if int(admin) == 1:
                                                                                admin = ''
                                                                                t = 0

                                                                            else: 
                                                                                admin = int(admin) - 1
                                                                            s += 1
                                                                        if admin == i.lower():
                                                                            if int(admins_list[p+1]) == 1:
                                                                                admin = ''
                                                                            s = 0
                                                                        if admin == '':
                                                                            pass
                                                                        else:
                                                                            new_admins += f' {admin}'
                                                                
                                                                if new_admins == '':
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = NULL WHERE player_id = $1', ctx.author.id) 
                                                                else:
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id) 
                
                                                            previous_was_type = False

                                                    previous_was_type = False
                                                    check = 0
                                                    for i in show2_items:
                                                        check += 1
                                                        if previous_was_type is False:
                                                            if check > 2:
                                                                if i == 'Banners':
                                                                    i = 'Banner'
                                                                elif i == 'Borders':
                                                                    i = 'Border'
                                                                elif i == 'Avaborders':
                                                                    i = 'Avaborder'


                                                                if (i == 'Banner') or (i == 'Border') or (i == 'Avaborder'):
                                                                    if i == 'Banner':
                                                                        stats = 'banners'
                                                                        lists = 'banner_list'
                                                                        name = 'banner_name'
                                                                        current = 'current_banner'
                                                                        count = 'banner_count'

                                                                        previous_was_type = True
                                                                    elif i == 'Border':
                                                                        stats = 'borders'
                                                                        lists = 'border_list'
                                                                        name = 'border_name'
                                                                        current = 'banner_border'
                                                                        count = 'border_count'
                                                                        previous_was_type = True
                                                                    elif i == 'Avaborder':
                                                                        stats = 'avatar_borders'
                                                                        lists = 'avaborder_list'
                                                                        name = 'banner_name'
                                                                        current = 'avatar_border'
                                                                        count = 'avaborder_count'
                                                                        previous_was_type = True
                                                        else:
                                                            await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                            s = 1
                                                            registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                                                            member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)
                                                            flists = str(registered_check[0][lists])
                                                            listbuy = self.listing(flists)
                                                            if i.lower() in listbuy:
                                                                new_admins = ''
                                                                admins_list = self.listing(flists)
                                                                for admin in admins_list:
                                                                    if admins_list.index(admin) == 0:
                                                                
                                                                        if s == 0:   
                                                                            admin = int(admin) + 1
                                                                            s += 1
                                                                        if admin == i.lower():
                                                                            s = 0
                                                                        new_admins += str(admin)
                                                                    

                                                                    else:
                                                                        if s == 0:
                                                                            admin = int(admin) + 1
                                                                            s+=1
                                                                        if admin == i.lower():
                                                                            s = 0
            
                                                                        new_admins += f' {admin}'
                                                                    
                        
                                                                await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id) 
                                                            else:                                                    
                                                                itemcode = await id_generator()
                                                                
                                                                a = f'{i.lower()}'
                            
                                                                b = 1
                                                                c = f"{itemcode}"
                                                                if member_registered[0][lists] is None:
                                                                    admins_list = self.listing(flists)
                                                                    new_admins = f' {a}' + f' {b}' + f' {c}'
                                    
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins),  ctx.author.id)
            

                                                                else:
                                                                    new_admins = str(flists) + f' {a}' + f' {b}' + f' {c}'
                                        
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins,  ctx.author.id)

                                                            await self.bot.db.execute(f'UPDATE registered SET {count} = {count} - 1 WHERE player_id = $1', member.id)
                                                            s = 1
                                                            t = 1
                                                            flists = str(member_registered[0][lists])
                                                            listbuy = self.listing(flists)
                                                            if i.lower() in listbuy:
                                                                new_admins = ''
                                                                admins_list = self.listing(flists)
                                                                for p, admin in enumerate(admins_list):
                                                                    if admins_list.index(admin) == 0:
                                    
                                                                        if t == 0:
                                                                            admin = ''
                                                                            t = 1
                                                                        if s == 0:
                                                                            if int(admin) == 1:
                                                                                admin = ''
                                                                                t = 0

                                                                            else: 
                                                                                admin = int(admin) - 1
                                                                            s += 1
                                                                        if admin == i.lower():
                                                                            if int(admins_list[p+1]) == 1:
                                                                                admin = ''
                                                                            s = 0
                                                                            
                                                                        new_admins += str(admin)
                                                                    

                                                                    else:

                                                                        if t == 0:
                                                                            admin = ''
                                                                            t = 1
                                                                        if s == 0:
                                                                            if int(admin) == 1:
                                                                                admin = ''
                                                                                t = 0
                                                                            else: 
                                                                                admin = int(admin) - 1
                                                                            s += 1
                                                                        if admin == i.lower():
                                                                            if int(admins_list[p+1]) == 1:
                                                                                admin = ''
                                                                            s = 0
                                                                        if admin == '':
                                                                            pass
                                                                        else:
                                                                            new_admins += f' {admin}'
                                                                if new_admins == '':
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = NULL WHERE player_id = $1', member.id) 
                                                                else:
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, member.id) 
                
                                                            previous_was_type = False
                                                    trade = 'no'
                                                    await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, member.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id) 
                                                    await ctx.send(f"Trade between {ctx.author.mention} and {member.mention} is complete!")

                                                    author_id = ctx.author.id
                                                    member_id = member.id
                                                    a = [6]
                                                    m = [6]
                                                    await quests(self,ctx, a, author_id, m,member_id)
                                                    return
                                                else:
                                                    await ctx.send(embed = embed)
                                                
                                            elif (msg.content.lower().startswith("d!cancel")) or (msg.content.lower().startswith("d!x")) or (msg.content.lower().startswith("d.cancel")) or (msg.content.lower().startswith("d.x")):
                                                trade = 'no'
                                                await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id) 
                                                await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade,member.id) 

                                                return
                                if view.value == False:
                                    await ctx.send(f"{member.mention} did not accept the trade.")
                                    trade = 'no'
                                    await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, member.id)
                                    await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id) 
                                else:
                                    trade = 'no'
                                    await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, member.id)
                                    await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id) 
                                    await ctx.send(f"Trade timed out.")

                    else:
                        await ctx.send('That person has not registered yet! Use `d!start` to register.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name ='cancel', aliases = ['x'])
    async def can_trade(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if registered_check[0]['trade'] == 'no':
                await ctx.send("You're not in a trade")
            else:
                trade = 'no'
                await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id) 
                await ctx.send("Cancelled the trade.")

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.group(name = 'market', aliases = ['m'], invoke_without_command = True)
    async def market_command(self, ctx, stat : str = None, *, filters : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)
   
  
        if user_ban_list:
            await ctx.send('You are banned from the bot.')

        else:
            if registered_check:
                if stat is None:
                    em1 = discord.Embed(
                        title = 'Market [Aliases: m]',
                        description = 'Commands related to the market',
                        colour = color
                    )

                    em1.add_field(name = 'd!market [item type] [filter]', value = 'View the market.\n[item type] banner, border, avaborder\n[filter] S,A,B,C,D, price, >(number), <(number) name of item',inline=False)

                    em1.add_field(name = 'd!marketadd [item type] [item name] [price]', value = 'Add items to the market.',inline=False)

                    em1.add_field(name = 'd!marketremove [item type] [item ID]', value = 'Remove items from the market.',inline=False)

                    em1.add_field(name = 'd!marketbuy [item type] [item ID]', value = 'Buy items from the market.',inline=False)

                    em1.add_field(name = 'd!marketmine', value = 'My items listed in the market.',inline=False)
                    
                    await ctx.send(embed = em1)
                else:
                    if (stat == 'border') or (stat == 'borders') or (stat == 'bo'):
                        stats = 'borders'
                        lists = 'border_list'
                        name = 'border_name'
                        current = 'banner_border'
                    elif (stat == 'avaborders') or (stat == 'avaborder') or (stat == 'a'):
                        stats = 'avatar_borders'
                        lists = 'avaborder_list'
                        name = 'banner_name'
                        current = 'avatar_border'
                    elif (stat == 'banner') or (stat == 'banners') or (stat == 'b'):
                        stats = 'banners'
                        lists = 'banner_list'
                        name = 'banner_name'
                        current = 'current_banner'
                    else:
                        await ctx.send("Incorrect item type. banner/border/avaborder")
                        return
                    if filters is None:
                        pass
                    else:
                        filters = filters.title()
                    
                    if filters is None:
                        lb = await self.bot.db.fetch(f'SELECT * FROM market WHERE item_type = $1 ORDER BY added DESC', stats)
                    elif filters == 'Price':
                        lb = await self.bot.db.fetch(f'SELECT * FROM market WHERE item_type = $1 ORDER BY price ASC',stats)
                    elif filters.startswith(">"):
                        sfilters = int(filters[1:])
                        lb = await self.bot.db.fetch(f'SELECT * FROM market WHERE item_type = $1 AND price >= {sfilters} ORDER BY price ASC',stats)
                    elif filters.startswith("<"):
                        sfilters = int(filters[1:])
                        lb = await self.bot.db.fetch(f'SELECT * FROM market WHERE item_type = $1 AND price <= {sfilters} ORDER BY price DESC',stats)                    
                    elif (filters == 'SS') or (filters == 'S') or (filters == 'A') or (filters == 'B') or (filters == 'C') or (filters == 'D'):
                        lb = await self.bot.db.fetch(f'SELECT * FROM market WHERE rank = $1 AND item_type = $2 ORDER BY added DESC',filters, stats)
                    else:
                        filters = filters.lower()
                        start = f'{filters}%'
                        lb = await self.bot.db.fetch(f'SELECT * FROM market WHERE item_type = $1 AND LIKE $2 ORDER BY added DESC', stats, start)
                    if lb == []:
                        await ctx.send(f"Your search for **{filters}** didn't return any results. Were you trying to use a filter? `S`, `A`, `B`, `C`, `D`\nTo sort by price use the `price` filter or enter a range using `>number` or `<number`.")
                    else:
                        data = []
                        for faction in lb:
                            data.append(faction['item_id'])

                        pagination_view = SPaginationView()
                        pagination_view.data = data
                        pagination_view.lb = lb
                        pagination_view.stat = stat
                        pagination_view.registered_check = registered_check

                        await pagination_view.send(ctx)
            else:
                await ctx.send('You have not registered yet! Use `d!start` to register.')

    @market_command.command(name = 'add', aliases = ['ma'])
    async def market_add_command(self,ctx,stat : str = None,  item_name : str = None, price : int = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if (stat is None) or (item_name is None) or (price is None):
                em = discord.Embed(
                    title = 'Market',
                    description = '**Add items to the market.**\n\nd!market add [item type] [item name] [price]',
                    colour = color
                )

                await ctx.send(embed = em)
            else:
                if (stat == 'title') or (stat == 'titles') or (stat == 't'):
                    stats = 'titles'
                    lists = 'title_list'
                    name = 'title_place'
                    current = 'title'
                elif (stat == 'border') or (stat == 'borders') or (stat == 'bo'):
                    stats = 'borders'
                    lists = 'border_list'
                    name = 'border_name'
                    current = 'banner_border'
                elif (stat == 'avaborders') or (stat == 'avaborder') or (stat == 'a'):
                    stats = 'avatar_borders'
                    lists = 'avaborder_list'
                    name = 'banner_name'
                    current = 'avatar_border'
                elif (stat == 'banner') or (stat == 'banners') or (stat == 'b'):
                    stats = 'banners'
                    lists = 'banner_list'
                    name = 'banner_name'
                    current = 'current_banner'
                else:
                    await ctx.send("Incorrect item type. **border/banner/avaborder/title**")
                banners = await self.bot.db.fetch(f'SELECT * FROM {stats}')
                banner_list = []
                for i in range(len(banners)):
                    banner_list.append(banners[i][name])

                if item_name.lower() in banner_list:
                    badlist = ['bronze2','silver2','gold2','platinum2','dominant2','bronze','silver','gold','platinum','dominant']
                
                    if item_name.lower() in badlist:
                        await ctx.send("This item cannot be sold!")
                    else:         
                        flists = str(registered_check[0][lists])
                        admins_list = self.listing(flists)
                        if item_name.lower() in admins_list:
                            if price > 100000:
                                await ctx.send("The price is too high!")
                            else:
                                view = ConfirmCancel(ctx.author)
                                await ctx.send(f'{ctx.author.mention} are you sure you want to list **{item_name.title()}** for **{"{:,}".format(price)}dc**?', view = view)
                                await view.wait()
                                if view.value == True:
                                    registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                                    flists = str(registered_check[0][lists])
                                    admins_list = self.listing(flists)
                                    if item_name.lower() in admins_list:
                                        new_admins = ''
                                        tofindrank = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE {name} = $1', item_name.lower())
                                        rank = tofindrank[0]['rank']
                                        s = 1
                                        t = 1
                                        id1 = await id1_generator()
                                        for p, admin in enumerate(admins_list):
                                            if admins_list.index(admin) == 0:
                                                if t == 0:
                                                    itemid = f'{id1}{admin}'
                                                    t = 1

                                                if s == 0:
                                                    if int(admin) == 1:
                                                        admin = ''
                                                        t = 0

                                                    else: 
                                                        admin = int(admin) - 1
                                                        t = 0
                                                    s += 1
                                                if admin == item_name.lower():
                                                    if int(admins_list[p+1]) == 1:
                                                        admin = ''
                                                    s = 0
                                                    
                                                new_admins += str(admin)
                                            

                                            else:

                                                if t == 0:
                                                    itemid = f'{id1}{admin}'
                                                    t = 1
                                                if s == 0:
                                                    if int(admin) == 1:
                                                        admin = ''
                                                        t = 0
                                                    else: 
                                                        admin = int(admin) - 1
                                                        t = 0
                                                    s += 1
                                                if admin == item_name.lower():
                                                    if int(admins_list[p+1]) == 1:
                                                        admin = ''
                                                    s = 0

                                                if admin == '':
                                                    pass
                                                else:
                                                    new_admins += f' {admin}'
                                        await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id) 
                                        await self.bot.db.execute('INSERT INTO market (item_id, item_name, item_type, price, rank, player_id) VALUES ($1, $2, $3, $4, $5, $6)', itemid, item_name.lower(), stats, price, rank, ctx.author.id)
                                        await ctx.send("Item added.")
                                    else:
                                        await ctx.send("Too many requests!")

                                elif view.value == False:
                                    await ctx.send("Cancelled.")
                                else:
                                    await ctx.send("Timed out.")
                        else:
                            await ctx.send('You do not own that item.')

                else:
                    await ctx.send('Item not found.')
                


    @market_command.command(name = 'remove', aliases = ['mr'])
    async def market_removde_command(self,ctx,stat : str = None,  item_id : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if (stat is None) or (item_id is None) :
                em = discord.Embed(
                    title = 'Market',
                    description = '**Remove items to the market.**\n\nd!market remove [item type] [item ID]',
                    colour = color
                )

                await ctx.send(embed = em)
            else:
                if (stat == 'title') or (stat == 'titles') or (stat == 't'):
                    stats = 'titles'
                    lists = 'title_list'
                    name = 'title_place'
                    current = 'title'
                elif (stat == 'border') or (stat == 'borders') or (stat == 'bo'):
                    stats = 'borders'
                    lists = 'border_list'
                    name = 'border_name'
                    current = 'banner_border'
                elif (stat == 'avaborders') or (stat == 'avaborder') or (stat == 'a'):
                    stats = 'avatar_borders'
                    lists = 'avaborder_list'
                    name = 'banner_name'
                    current = 'avatar_border'
                elif (stat == 'banner') or (stat == 'banners') or (stat == 'b'):
                    stats = 'banners'
                    lists = 'banner_list'
                    name = 'banner_name'
                    current = 'current_banner'
                else:
                    await ctx.send("Incorrect item type. **border/banner/avaborder/title**")
                market = await self.bot.db.fetch(f'SELECT * FROM market')
                banner_list = []
                for i in range(len(market)):
                    banner_list.append(market[i]['item_id'])
                if item_id in banner_list:         
                    flists = str(registered_check[0][lists])
                    admins_list = self.listing(flists)
                    if item_id[2:] in admins_list:

                            view = ConfirmCancel(ctx.author)
                            await ctx.send(f'{ctx.author.mention} are you sure you want to remove this item?', view = view)
                            await view.wait()
                            if view.value == True:
                                registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                                flists = str(registered_check[0][lists])
                                admins_list = self.listing(flists)
                                if item_id[2:] in admins_list:
                                    item = await self.bot.db.fetch(f'SELECT * FROM market WHERE item_id = $1', item_id)
                                    new_admins = ''
                                    for p,admin in enumerate(admins_list):
                                        if admins_list.index(admin) == 0:
                                            
                                            if admin == item[0]['item_name']:   
                                                admins_list[p+1] = 1 + int(admins_list[p+1])
                                                
                                            elif admin == item_id[2:]:
                                                admin = f"{item[0]['item_name']} 1 {item_id[2:]}"
                                                
                                            new_admins += str(admin)
                                        

                                        else:
                                            if admin == item[0]['item_name']:   
                                                admins_list[p+1] = 1 + int(admins_list[p+1])
                                            
                                            elif admin == item_id[2:]:
                                                admin = f" {item[0]['item_name']} 1 {item_id[2:]}"

                                            new_admins += f' {admin}'
                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id) 
                                    await self.bot.db.execute(f'DELETE FROM market WHERE item_id = $1', item_id)
                                    await ctx.send("Item removed.")
                                else:
                                    await ctx.send("Too many requests.")

                            elif view.value == False:
                                await ctx.send("Cancelled.")
                            else:
                                await ctx.send("Timed out.")
                    else:
                        await ctx.send('You do not own that item.')

                else:
                    await ctx.send('Item not found.')

    @market_command.command(name = 'buy', aliases = ['mb'])
    async def market_buy_command(self, ctx, stat : str = None,*, itemid : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        
        if registered_check:
                if (stat is None) or (itemid is None):
                    em = discord.Embed(
                        title = 'Trading',
                        description = '**Buy from Market**\nd!market buy [item type] [item ID]\n[item type] banner,border,avaborder,title',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:

                    if (stat == 'titles') or (stat == 'title'):
                        stats = 'titles'
                        lists = 'title_list'
                        name = 'title_place'
                        count = 'title_count'
                    elif (stat == 'borders') or (stat == 'border'):
                        stats = 'borders'
                        lists = 'border_list'
                        name = 'border_name'
                        count = 'border_count'
                    elif (stat == 'avaborders') or (stat == 'avaborder'):
                        stats = 'avatar_borders'
                        lists = 'avaborder_list'
                        name = 'banner_name'
                        count = 'avaborder_count'
                    elif (stat == 'banners') or (stat == 'banner'):
                        stats = 'banners'
                        lists = 'banner_list'
                        name = 'banner_name'
                        count = 'banner_count'
                    else:
                        await ctx.send("Incorrect item type. **banner/border/avaborder/title**")
                        return

                    lbtrue = await self.bot.db.fetch(f'SELECT * FROM market')
                    slist = []

                    for i in range(len(lbtrue)):
                        slist.append(lbtrue[i]["item_id"])
                    if itemid in slist:
                        lb = await self.bot.db.fetch(f'SELECT * FROM market WHERE item_id = $1',itemid)
                        
                        if lb == []:
                            await ctx.send("This item isn't listed in the shop")
                        else:
                            price = lb[0]["price"]
                            pay = lb[0]["player_id"]
                            if pay == ctx.author.id:
                                await ctx.send("You can't buy your own item! Please use the d!market remove command instead.")
                            else:
                                if registered_check[0]["banner_pieces"] < price:
                                    await ctx.send("You don't have enough Dom Coins!")
                                else:
                                    flists = str(registered_check[0][lists])
                                    listbuy = self.listing(flists)
                                    view = ConfirmCancel(ctx.author)
                                    await ctx.send (f'Are you sure you want to buy **{lb[0]["item_name"].title()}**?', view = view)
                                    await view.wait()
                                    if view.value is True:
                                        flists = str(registered_check[0][lists])
                                        listbuy = self.listing(flists)
                                        lb = await self.bot.db.fetch(f'SELECT * FROM market WHERE item_id = $1',itemid)
                                        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                                        if (lb == []) or (registered_check[0]["banner_pieces"] < price):
                                            await ctx.send("Too many requests!")
                                        else:
                                            await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                            s = 1
                                            if lb[0]["item_name"] in listbuy:
                                                new_admins = ''
                                                admins_list = self.listing(flists)
                                                for admin in admins_list:
                                            
                                                    if admins_list.index(admin) == 0:
                                                
                                                        if s == 0:
                                                            
                                                            admin = int(admin) + 1
                                                            s += 1
                                                        if admin == lb[0]["item_name"]:
                                                
                                                            s = 0
                                                        new_admins += str(admin)
                                                    

                                                    else:
                                                        if s == 0:
                                                            
                                                            admin = int(admin) + 1
                                                            s+=1
                                                        if admin == lb[0]["item_name"]:
                                                    
                                                            s = 0

                                                                        
                                                        new_admins += f' {admin}'
                                                    
                                            
                                                await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - {price} WHERE player_id = $1', ctx.author.id)  
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {price} WHERE player_id = $1', int(pay)) 
                                                await self.bot.db.execute(f'DELETE FROM market WHERE item_id = $1', itemid)
                                                await ctx.send("Item bought!")                                          
                                            else:
                                                
                                                itemcode = await id_generator()
                                                
                                                a = f'{lb[0]["item_name"]}'
            
                                                b = 1
                                                c = f"{itemcode}"
                                                if registered_check[0][lists] is None:
                                                    admins_list = self.listing(flists)
                                                    new_admins = f' {a}' + f' {b}' + f' {c}'
                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - {price} WHERE player_id = $1', ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {price} WHERE player_id = $1', int(pay)) 
                                                    await self.bot.db.execute(f'DELETE FROM market WHERE item_id = $1', itemid)
                                                    await ctx.send("Item bought!") 

                                                else:
                                                    new_admins = str(flists) + f' {a}' + f' {b}' + f' {c}'
                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - {price} WHERE player_id = $1', ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {price} WHERE player_id = $1', int(pay)) 
                                                    await self.bot.db.execute(f'DELETE FROM market WHERE item_id = $1', itemid)
                                                    await ctx.send("Item bought!")
                                            member = lb[0]["player_id"]
                                            member_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member)
                                            flists = str(member_check[0][lists])
                                            admins_list = self.listing(flists)
                                            new_admins = ''
                                            for p, admin in enumerate(admins_list):
                                                if admins_list.index(admin) == 0:

                                                    if admin == itemid[2:]:
                                                        admin = ''

                                                    if admin == '':
                                                        pass
                                                    else:
                                                        new_admins += str(admin)
                                                
                                                else:

                                                    if (admin == itemid[2:]) and (admins_list[p-2] is not lb[0]["item_name"]):
                                                        admin = ''

                                                    if admin == '':
                                                        pass
                                                    else:
                                                        new_admins += f' {admin}'
                                            if new_admins == '':
                                                await self.bot.db.execute(f'UPDATE registered SET {lists} = NULL WHERE player_id = $1', member) 
                                            else:
                                                await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, member) 

                                    elif view.value is False:
                                        await ctx.send('Cancelled.')
                                    else:
                                        await ctx.send('Timed Out')    

                    else:
                        await ctx.send("Item not found.")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')


    @market_command.command(name = 'mine', aliases = ['mmi'])
    async def market_mine_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)


        if user_ban_list:
            await ctx.send('You are banned from the bot.')

        else:
            if registered_check:
                lb = await self.bot.db.fetch(f'SELECT * FROM market WHERE player_id = $1 ORDER BY added DESC', ctx.author.id)
                if lb == []:
                    await ctx.send(f"You don't have any items listed.")
                else:
                    data = []
                    for faction in lb:
                        data.append(faction['item_id'])
                    stat = 'banners'
                    pagination_view = MPaginationView()
                    pagination_view.data = data
                    pagination_view.lb = lb
                    pagination_view.stat = stat
                    pagination_view.registered_check = registered_check

                    await pagination_view.send(ctx)
            else:
                await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'roll', alias=['r'])
    async def roll_command(self, ctx, member: discord.User = None, rounds : int = None, mode : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:

            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

    
            if user_ban_list:
                await ctx.send('You are banned from the bot.')
                return

            if (member == None) and (rounds == None) and (mode == None):
                
                randomRol = random.randint(1,100)

         
                await ctx.send(f'{ctx.author.name} rolled... **{randomRol}** 🎲')
            elif member == None:
                em = discord.Embed(
                    title = "Help 🛠️",
                    description = '**d!roll [Mention] [Number of rounds] [high/mid/low]** Default is bo3 high',
                    colour = color
                )
                await ctx.send(embed = em)
            else:
                user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)
                player_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', member.id)

        
                if user_ban_list:
                    await ctx.send('You are banned from the bot.')
                elif player_ban_list:
                    await ctx.send('They are banned from the bot.')

                else:
           

                    member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)
                    if member_registered:
                        if member == ctx.author:
                            await ctx.end("You can't gamble with yourself!")
                        else:
                            if member_registered[0]['trade'] == 'yes':
                                await ctx.send("Member is already in a trade or gamble!")
                            elif registered_check[0]['trade'] == 'yes':
                                await ctx.send("You are already in a trade or gamble!")
                            else:
                                view = ConfirmCancel(member)
                                await ctx.send(f"{ctx.author.mention} wants to gamble with {member.mention}, accept gamble?", view = view)
                                trade = 'yes'
                                await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, member.id)
                                await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id) 
                                await view.wait()
                        
                                if view.value == True:
                                    em = discord.Embed(
                                        title = 'Gamble',
                                        description = "**ADD** items using `d!add [item type] [item]`\n**REMOVE** items using `d!remove [item type] [item]`\n**ACCEPT** using `d!accept`\n\n➜ Cross Trading is NOT allowed, if caught you will be banned from the bot.\n➜ After accepting the gamble, the gamble will begin instantly and you cannot back out. The items will be trading automatically so make sure you're ready before accepting.",
                                        colour = color
                                    )
                                    await ctx.send(f"{member.mention} has accepted the gamble.",embed = em)


                                    show1_items = ['Dom Coins', 0]
                                    show2_items = ['Dom Coins', 0]
                                    trade_items = {ctx.author: [], member: []}

                                    while True:
                                        try:
                                            msg = await self.bot.wait_for('message', check=lambda message: message.author in [ctx.author, member] and message.content.lower().startswith('d!'), timeout=300.0)
                                        except asyncio.TimeoutError:
                                            trade = 'no'
                                            await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, member.id)
                                            await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id) 
                                            await ctx.send("Trade timed out.")
                                            return

                                        if (msg.content.lower().startswith("d!add")) or (msg.content.lower().startswith("d.add")):

                                            item = msg.content.split()
                                            if len(item) != 3:
                                                await ctx.send("Incorrect format, `d!add [Item type] [Item name/amt]`")
                                            else:
                                                try:
                                                    trade_items[ctx.author].remove("done")
                                                except KeyError as e:
                                                    pass
                                                except ValueError as e:
                                                    pass
                                                try:
                                                    trade_items[member].remove("done")
                                                except KeyError as e:
                                                    pass
                                                except ValueError as e:
                                                    pass

                                                if (item[1].lower() == 'domcoins') or (item[1].lower() == 'dcs') or (item[1].lower() == 'domcoin'):
                                                    item[1] = 'dc'
                                                if (item[1].lower() == 'key'):
                                                    item[1] = 'keys'
                                                if (item[1].lower() == 'lbs') or (item[1].lower() == 'lb') or (item[1].lower() == 'lootbox'):
                                                    item[1] = 'lootboxes'
                                                if (item[1].lower() == 'b'):
                                                    item[1] = 'banners'
                                                if (item[1].lower() == 'bo'):
                                                    item[1] = 'border'
                                                if (item[1].lower() == 'a') or (item[1].lower() == 'avatarborder') or (item[1].lower() == 'avatarborders'):
                                                    item[1] = 'avaborder'

                                                if (item[1].lower() == 'title') or (item[1].lower() == 'titles'):
                                                    await ctx.send("Titles can't be traded.")
                                                elif (item[1].lower() == 'banner') or (item[1].lower() == 'banners') or (item[1].lower() == 'borders') or (item[1].lower() == 'border') or (item[1].lower() == 'avaborder') or (item[1].lower() == 'avaborders') or (item[1].lower() == 'dc') :
                                                    if item[1].lower()== 'dc':
                                                        if item[2].isnumeric():
                                                            if msg.author == ctx.author:
                                                                amt = registered_check[0]["banner_pieces"]
                                            
                                                                total = int(show1_items[1]) + int(item[2])
                                                                if total > amt:
                                                                    await ctx.send("You don't have enough Dc!")
                                                                else:
                                                                    show1_items[1] =  int(show1_items[1]) + int(item[2])
                                                                
                                                            else:
                                                                amt = member_registered[0]["banner_pieces"]
                                                                total = int(show2_items[1]) + int(item[2])
                                                                if total > amt:
                                                                    await ctx.send("You don't have enough Dc!")
                                                                else:
                                                                    show2_items[1] =  int(show2_items[1]) + int(item[2])
                                                        else:
                                                            await ctx.send("Dc must be a number!")
                                                    else:
                                                        stat = str(item[1].lower())
                                                        banner_name = str(item[2])
                                                        if (stat == 'border') or (stat == 'borders'):
                                                            stats = 'borders'
                                                            lists = 'border_list'
                                                            name = 'border_name'
                                                            current = 'banner_border'
                                                        elif (stat == 'avaborders') or (stat == 'avaborder'):
                                                            stats = 'avatar_borders'
                                                            lists = 'avaborder_list'
                                                            name = 'banner_name'
                                                            current = 'avatar_border'
                                                        elif (stat == 'banner') or (stat == 'banners'):
                                                            stats = 'banners'
                                                            lists = 'banner_list'
                                                            name = 'banner_name'
                                                            current = 'current_banner'

                                                        banners = await self.bot.db.fetch(f'SELECT * FROM {stats}')
                                                        banner_list = []
                                                        for i in range(len(banners)):
                                                            banner_list.append(banners[i][name])

                                                        if banner_name.lower() in banner_list:    
                                                            if msg.author == ctx.author:
                                                                flists = str(registered_check[0][lists])
                                                            else:
                                                                flists = str(member_registered[0][lists])
                                                            
                                                            my_banner_list = self.listing(flists)
                                                            if banner_name.lower() in my_banner_list:
                                                                badlist = ['bronze','silver','gold','platinum','dominant','bronze2','silver2','gold2','platinum2','dominant2']
                                                            
                                                                if banner_name.lower() in badlist:
                                                                    await ctx.send("This item is not tradable")
                                                                else:
                                                                    if msg.author == ctx.author:
                                                                        ind = int(my_banner_list.index(banner_name.lower()))
                                                                        realind = my_banner_list[ind+1]
                                                                        add =0
                                                                        for i in show1_items:
                                                                            if i is None:
                                                                                pass
                                                                            else:
                                                                                if i == banner_name.title():
                                                                                    add += 1
                                                            
                                                                        if int(realind) - add > 0:
                                                                            show1_items.append(item[1].title())
                                                                            show1_items.append(item[2].title())
                                                                        else:
                                                                            await ctx.send("You don't have more of this item!")
                                                                        
                                                                    else:
                                                                        ind = int(my_banner_list.index(banner_name.lower()))
                                                                        realind = my_banner_list[ind+1]
                                                                        add =0
                                                                        for i in show2_items:
                                                                            if i is None:
                                                                                pass
                                                                            else:
                                                                                if i == banner_name.title():
                                                                                    add += 1
                                                                        if int(realind) - add > 0:
                                                                            show2_items.append(item[1].title())
                                                                            show2_items.append(item[2].title())
                                                                        else:
                                                                            await ctx.send("You don't have more of this item!")
                                                            else:
                                                                await ctx.send('You do not own that item.')

                                                        else:
                                                            await ctx.send('Item not found.')

                                                    embed = discord.Embed(title="Gamble", color=discord.Color.green())
                                                    embedstr1 = ''
                                                    embedstr2 = ''
                                                    test1 = 0
                                                    test2 = 0
                                                    for i in show1_items:
                                                        
                                                        if test1%2 == 0:
                                                            embedstr1 += f'{show1_items[test1]} **{show1_items[test1+1]}**\n'
                                                        else:
                                                            pass
                                                        test1 += 1
                                                    for i in show2_items:
                                                        if test2%2 == 0:
                                                            embedstr2 += f'{show2_items[test2]} **{show2_items[test2+1]}**\n'
                                                        else:
                                                            pass
                                                        
                                                        test2 += 1
                                                    if "done" in trade_items[ctx.author]:
                                                        emoji1 = ':green_circle:'
                                                    else:
                                                        emoji1 = ':red_circle:'
                                                    if "done" in trade_items[member]:
                                                        emoji2 = ':green_circle:'
                                                    else:
                                                        emoji2 = ':red_circle:'
                                                    embed.add_field(name=f"{emoji1} {ctx.author.display_name}'s Items", value=embedstr1, inline=True)
                                                    embed.add_field(name=f"{emoji2} {member.display_name}'s Items", value=embedstr2, inline=True)
                                                    await msg.channel.send(embed=embed)
                                                else:
                                                    await ctx.send("Incorrect format, `d!add [Item type] [Item name/amt`]")

                                        elif (msg.content.lower().startswith("d!remove")) or (msg.content.lower().startswith("d.remove")):

                                            item = msg.content.split()
                                            if len(item) != 3:
                                                await ctx.send("Incorrect format, `d!remove [Item type] [Item name/amt]`")
                                            else:
                                                try:
                                                    trade_items[ctx.author].remove("done")
                                                except KeyError as e:
                                                    pass
                                                except ValueError as e:
                                                    pass
                                                try:
                                                    trade_items[member].remove("done")
                                                except KeyError as e:
                                                    pass
                                                except ValueError as e:
                                                    pass

                                                if (item[1].lower() == 'domcoins') or (item[1].lower() == 'dcs') or (item[1].lower() == 'domcoin'):
                                                    item[1] = 'dc'
                                                if (item[1].lower() == 'key'):
                                                    item[1] = 'keys'
                                                if (item[1].lower() == 'lbs') or (item[1].lower() == 'lb') or (item[1].lower() == 'lootbox'):
                                                    item[1] = 'lootboxes'
                                                if (item[1].lower() == 'b'):
                                                    item[1] = 'banners'
                                                if (item[1].lower() == 'bo'):
                                                    item[1] = 'border'
                                                if (item[1].lower() == 'a') or (item[1].lower() == 'avatarborder') or (item[1].lower() == 'avatarborders'):
                                                    item[1] = 'avaborder'


                                                if (item[1].lower() == 'banner') or (item[1].lower() == 'border') or (item[1].lower() == 'avaborder')  or (item[1].lower() == 'dc') :
                                                    if item[1].lower()== 'dc':
                                                        if item[2].isnumeric():
                                                            if msg.author == ctx.author:
                                                                amt = registered_check[0]["banner_pieces"]
                                            
                                                                if int(show1_items[1]) - int(item[2]) < 0:
                                                                    await ctx.send("Not enough added in the trade.")
                                                                else:
                                                                    show1_items[1] = show1_items[1] - int(item[2])
                                                                        
                                                                
                                                            else:
                                                                amt = member_registered[0]["banner_pieces"]

                                                                if int(show2_items[1]) - int(item[2])< 0:
                                                                    await ctx.send("Not enough added in the trade.")
                                                                else:
                                                                    show2_items[1] = show2_items[1] - int(item[2])
                                                        else:
                                                            await ctx.send("Dc must be a number!")
                                                    else:
                                                        stat = str(item[1].lower())
                                                        banner_name = str(item[2])
                                                        if (stat == 'border') or (stat == 'borders'):
                                                            stats = 'borders'
                                                            lists = 'border_list'
                                                            name = 'border_name'
                                                            current = 'banner_border'
                                                        elif (stat == 'avaborders') or (stat == 'avaborder'):
                                                            stats = 'avatar_borders'
                                                            lists = 'avaborder_list'
                                                            name = 'banner_name'
                                                            current = 'avatar_border'
                                                        elif (stat == 'banner') or (stat == 'banners'):
                                                            stats = 'banners'
                                                            lists = 'banner_list'
                                                            name = 'banner_name'
                                                            current = 'current_banner'

                                                        banners = await self.bot.db.fetch(f'SELECT * FROM {stats}')
                                                        banner_list = []
                                                        for i in range(len(banners)):
                                                            banner_list.append(banners[i][name])

                                                        if banner_name.lower() in banner_list:       
                                                            if msg.author == ctx.author:
                                                                flists = str(registered_check[0][lists])
                                                            else:
                                                                flists = str(member_registered[0][lists])
                                                            
                                                            my_banner_list = self.listing(flists)
                                                            if banner_name.lower() in my_banner_list:

                                                                if msg.author == ctx.author:
                                                                    ind = int(my_banner_list.index(banner_name.lower()))
                                                                    realind = my_banner_list[ind+1]
                                                                    add =0
                                                                    for i in show1_items:
                                                                        if i is None:
                                                                            pass
                                                                        else:
                                                                            if i == banner_name.title():
                                                                                add += 1
                                                        
                                                                    if int(realind) - add >= 0:

                                                                        show1_items.remove(item[1].title())
                                                                        show1_items.remove(item[2].title())
                                                                    else:
                                                                        await ctx.send("You don't have more of this item!")
                                                                    
                                                                else:
                                                                    ind = int(my_banner_list.index(banner_name.lower()))
                                                                    realind = my_banner_list[ind+1]
                                                                    add =0
                                                                    for i in show2_items:
                                                                        if i is None:
                                                                            pass
                                                                        else:
                                                                            if i == banner_name.title():
                                                                                add += 1
                                                                    if int(realind) - add >= 0:

                                                                        show2_items.remove(item[1].title())
                                                                        show2_items.remove(item[2].title())
                                                                    else:
                                                                        await ctx.send("You don't have more of this item!")
                                                            else:
                                                                await ctx.send('You do not own that item.')

                                                        else:
                                                            await ctx.send('Item not found.')

                                                    embed = discord.Embed(title="Gamble", color=discord.Color.green())
                                                    embedstr1 = ''
                                                    embedstr2 = ''
                                                    test1 = 0
                                                    test2 = 0
                                                    for i in show1_items:
                                                        
                                                        if test1%2 == 0:
                                                            embedstr1 += f'{show1_items[test1]} **{show1_items[test1+1]}**\n'
                                                        else:
                                                            pass
                                                        test1 += 1
                                                    for i in show2_items:
                                                        if test2%2 == 0:
                                                            embedstr2 += f'{show2_items[test2]} **{show2_items[test2+1]}**\n'
                                                        else:
                                                            pass
                                                        
                                                        test2 += 1
                                                    if "done" in trade_items[ctx.author]:
                                                        emoji1 = ':green_circle:'
                                                    else:
                                                        emoji1 = ':red_circle:'
                                                    if "done" in trade_items[member]:
                                                        emoji2 = ':green_circle:'
                                                    else:
                                                        emoji2 = ':red_circle:'

                                                    embed.add_field(name=f"{emoji1} {ctx.author.display_name}'s Items", value=embedstr1, inline=True)
                                                    embed.add_field(name=f"{emoji2} {member.display_name}'s Items", value=embedstr2, inline=True)
                                                    await msg.channel.send(embed=embed)
                                                else:
                                                    await ctx.send("Incorrect format, `d!remove [Item type] [Item name/amt]`")

                                        elif (msg.content.lower() == "d!accept") or  (msg.content.lower() == "d.accept"):

                                            # trading items
                                            trade_items[msg.author].append("done")
                                            if "done" in trade_items[ctx.author]:
                                                emoji1 = ':green_circle:'
                                            else:
                                                emoji1 = ':red_circle:'
                                            if "done" in trade_items[member]:
                                                emoji2 = ':green_circle:'
                                            else:
                                                emoji2 = ':red_circle:'
                                            embed = discord.Embed(title="Gamble", color=discord.Color.green())
                                            embedstr1 = ''
                                            embedstr2 = ''
                                            test1 = 0
                                            test2 = 0
                                            for i in show1_items:
                                                
                                                if test1%2 == 0:
                                                    embedstr1 += f'{show1_items[test1]} **{show1_items[test1+1]}**\n'
                                                else:
                                                    pass
                                                test1 += 1
                                            for i in show2_items:
                                                if test2%2 == 0:
                                                    embedstr2 += f'{show2_items[test2]} **{show2_items[test2+1]}**\n'
                                                else:
                                                    pass
                                                
                                                test2 += 1
                                            embed.add_field(name=f"{emoji1} {ctx.author.display_name}'s Items", value=embedstr1, inline=True)
                                            embed.add_field(name=f"{emoji2} {member.display_name}'s Items", value=embedstr2, inline=True)



                                            if "done" in trade_items[ctx.author] and "done" in trade_items[member]:

                                                await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', member.id)
                                                await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', ctx.author.id)
                                                
                                                # roll
                                                if rounds == None:
                                                    rounds = 3
                                                if mode == None:
                                                    mode = 'high'

                                                td = 0
                                                score1 = 0
                                                score2 = 0
                                                randomRoll1 = 0
                                                randomRoll2 = 0
                                                win = math.ceil(rounds/2)        
                                                timeout = 0
                                                while rounds > 0:

                                                    view = RollForfeit(member)
                                                    
                                                    em = discord.Embed(
                                                        title = f"{member.name}'s Turn",
                                                        description = f'**Score : {score1} - {score2}**\nClick on 🎲 to Roll\nClick on 🏳️ to Forfeit ',
                                                        colour = color
                                                    )
                                                    em.set_footer(text=f'{rounds-1} Round(s) remaining')

                                                    await ctx.send(embed = em, view = view)
                                                    await view.wait()           
                                                        
                                                    if view.value is True:
                                                        timeout = 1
                                                        randomRoll1 = random.randint(1,100)
                                                        
                                                        await ctx.send(f'{member.name} rolled... {randomRoll1} 🎲')
                                                        view = RollForfeit(ctx.author)

                                                        em = discord.Embed(
                                                            title = f"{ctx.author.name}'s Turn",
                                                            description = f'**Score : {score1} - {score2}**\nClick on 🎲 to Roll\nClick on 🏳️ to Forfeit ',
                                                            colour = color
                                                        )
                                                        em.set_footer(text=f'{rounds-1} Round(s) remaining')

                                                        await ctx.send(embed = em, view = view)
                                                        await view.wait()
                                    
                                                        
                                                        if view.value is True:
                                                        
                                                                randomRoll2 = random.randint(1,100)
                                                        
                                                                await ctx.send(f'{ctx.author.name} rolled... {randomRoll2} 🎲')
                                                            
                                                        elif view.value is False:
                                                            td = 1
                                                            rounds = 0
                                                            thewon = member
                                                            await ctx.send(f'{ctx.author.mention} Forfeits.')

                                                        else:
                                                            td = 1
                                                            rounds = 0
                                                            thewon = member
                                                            await ctx.send('Timed Out.')
                                                        
                                                    elif view.value is False:
                                                        td = 1
                                                        rounds = 0
                                                        thewon = ctx.author
                                                        await ctx.send(f'{member.mention} Forfeits.')
                                                        
                                                    else:
                                                        td = 1
                                                        rounds = 0
                                                        if timeout == 0:
                                                            trade = 'no'
                                                            await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, member.id)
                                                            await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id) 
                                                            await ctx.send('Timed-out.')
                                                            return
                                                        else:
                                                            thewon = ctx.author
                                                            await ctx.send('Timed-out.')
                                                        
                                                    if td == 1:
                                                        pass
                                                    else:
                                                        if mode == 'high':
                                                            if randomRoll1 > randomRoll2:
                                                                score1 += 1
                                                                await ctx.send(f'{member.mention} Won the round!')
                                                            elif randomRoll2 > randomRoll1:
                                                                score2 += 1 
                                                                await ctx.send(f'{ctx.author.mention} Won the round!')
                                                            elif randomRoll1 == randomRoll2:
                                                                await ctx.send('Nobody won the round.')
                                                        elif mode == 'low':
                                                            if randomRoll1 < randomRoll2:
                                                                score1 += 1
                                                                await ctx.send(f'{member.mention} Won the round!')
                                                            elif randomRoll2 < randomRoll1:
                                                                score2 += 1 
                                                                await ctx.send(f'{ctx.author.mention} Won the round!')
                                                            elif randomRoll1 == randomRoll2:
                                                                await ctx.send('Nobody won the round.')
                                                        elif mode == 'mid':
                                                            if randomRoll1 > 50:
                                                                randomRoll1 -= 50
                                                            elif randomRoll1 < 50:
                                                                randomRoll1 = 50-randomRoll1
                                                            if randomRoll2 > 50:
                                                                randomRoll2 -= 50
                                                            elif randomRoll2 < 50:
                                                                randomRoll2 = 50-randomRoll2                         
                                                            if randomRoll1 < randomRoll2:
                                                                score1 += 1
                                                                await ctx.send(f'{member.mention} Won the round!')
                                                            elif randomRoll2 < randomRoll1:
                                                                score2 += 1 
                                                                await ctx.send(f'{ctx.author.mention} Won the round!')
                                                            elif randomRoll1 == randomRoll2:
                                                                await ctx.send('Nobody won the round.')
                                                    
                                                    if score1 == win or score2 == win:
                                                        rounds = 0
                                                    
                                                    if rounds == 0:
                                                        break
                                                    rounds -= 1
                                                
                                                if td == 1:
                                                    pass
                                                else:
                                                    if score1 > score2:
                                                        await ctx.send(f'{member.mention} Won the gamble!')
                                                        thewon = member
                                                        thelose = ctx.author
                                                    if score2 > score1:
                                                        await ctx.send(f'{ctx.author.mention} Won the gamble!')
                                                        thewon = ctx.author
                                                        thelose = member
                                                    elif score1 == score2:
                                                        trade = 'no'
                                                        await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, member.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id) 
                                                        await ctx.send(f'Its a tie!')
                                                        return
                                                    
                                                #cash
                                                dc1 = show1_items[1]
                                                dc2 = show2_items[1]
                                                if thewon == ctx.author:
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {dc2} WHERE player_id = $1', ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - {dc2} WHERE player_id = $1', member.id)
                                                elif thewon == member:
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {dc1} WHERE player_id = $1', member.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - {dc1} WHERE player_id = $1', ctx.author.id)
                                            

                                                #item

                                                previous_was_type = False
                                                lists = ''
                                                check = 0
                                                if thewon == member:
                                                    for i in show1_items:
                                                        check += 1
                                                        if previous_was_type is False:
                                                            if check > 2:

                                                                if i == 'Banners':
                                                                    i = 'Banner'
                                                                elif i == 'Borders':
                                                                    i = 'Border'
                                                                elif i == 'Avaborders':
                                                                    i = 'Avaborder'

                                                                if (i == 'Banner') or (i == 'Border') or (i == 'Avaborder'):
                                                                    if i == 'Banner':
                                                                        stats = 'banners'
                                                                        lists = 'banner_list'
                                                                        name = 'banner_name'
                                                                        current = 'current_banner'
                                                                        count = 'banner_count'

                                                                        previous_was_type = True
                                                                    elif i == 'Border':
                                                                        stats = 'borders'
                                                                        lists = 'border_list'
                                                                        name = 'border_name'
                                                                        current = 'banner_border'
                                                                        count = 'border_count'
                                                                        previous_was_type = True
                                                                    elif i == 'Avaborder':
                                                                        stats = 'avatar_borders'
                                                                        lists = 'avaborder_list'
                                                                        name = 'banner_name'
                                                                        current = 'avatar_border'
                                                                        count = 'avaborder_count'
                                                                        previous_was_type = True
                                                        else:

                                                            await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', member.id)
                                                            s = 1
                                                            registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                                                            member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)


                                                            flists = str(member_registered[0][lists])
                                                            listbuy = self.listing(flists)

                                                            if i.lower() in listbuy:
                                                                new_admins = ''
                                                                admins_list = self.listing(flists)
                                                                for admin in admins_list:
                                                                    if admins_list.index(admin) == 0:
                                                                
                                                                        if s == 0:   
                                                                            admin = int(admin) + 1
                                                                            s += 1
                                                                        if admin == i.lower():
                                                                            s = 0
                                                                        new_admins += str(admin)
                                                                    

                                                                    else:
                                                                        if s == 0:
                                                                            admin = int(admin) + 1
                                                                            s+=1
                                                                        if admin == i.lower():
                                                                            s = 0

                                                                        new_admins += f' {admin}'

                                                                await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, member.id) 
                                                            else:                                                    
                                                                itemcode = await id_generator()
                                                                
                                                                a = f'{i.lower()}'
                            
                                                                b = 1
                                                                c = f"{itemcode}"
                                                                if member_registered[0][lists] is None:
                                                                    admins_list = self.listing(flists)
                                                                    new_admins = f' {a}' + f' {b}' + f' {c}'
                            
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, member.id)


                                                                else:
                                                                    
                                                                    new_admins = str(flists) + f' {a}' + f' {b}' + f' {c}'
                                
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, member.id)

                                                            await self.bot.db.execute(f'UPDATE registered SET {count} = {count} - 1 WHERE player_id = $1', ctx.author.id)
                                                            s = 1
                                                            t = 1
                                                            flists = str(registered_check[0][lists])
                                                            listbuy = self.listing(flists)
                                                
                                                            if i.lower() in listbuy:
                                                        
                                                                new_admins = ''
                                                                admins_list = self.listing(flists)
                                                                for p,admin in enumerate(admins_list):

                                                                    if admins_list.index(admin) == 0:
                                                                        if t == 0:
                                                                            admin = ''
                                                                            t = 1
                                                                        if s == 0:
                                                                            if int(admin) == 1:
                                                                                admin = ''
                                                                                t = 0
                                                                            else: 
                                                                                admin = int(admin) - 1
                                                                            s += 1
                                                                        if admin == i.lower():
                                                                            if int(admins_list[p+1]) == 1:
                                                                                admin = ''
                                                                            s = 0
                                                                        new_admins += str(admin)
                                                                    

                                                                    else:
                                                                        if t == 0:
                                                                            admin = ''
                                                                            t = 1
                                                                        if s == 0:
                                                                            if int(admin) == 1:
                                                                                admin = ''
                                                                                t = 0

                                                                            else: 
                                                                                admin = int(admin) - 1
                                                                            s += 1
                                                                        if admin == i.lower():
                                                                            if int(admins_list[p+1]) == 1:
                                                                                admin = ''
                                                                            s = 0
                                                                        if admin == '':
                                                                            pass
                                                                        else:
                                                                            new_admins += f' {admin}'
                                                                
                                                                if new_admins == '':
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = NULL WHERE player_id = $1', ctx.author.id) 
                                                                else:
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id) 

                                                            previous_was_type = False

                                                previous_was_type = False
                                                check = 0
                                                if thewon == ctx.author:
                                                    for i in show2_items:
                                                        check += 1
                                                        if previous_was_type is False:
                                                            if check > 2:

                                                                if i == 'Banners':
                                                                    i = 'Banner'
                                                                elif i == 'Borders':
                                                                    i = 'Border'
                                                                elif i == 'Avaborders':
                                                                    i = 'Avaborder'

                                                                if (i == 'Banner') or (i == 'Border') or (i == 'Avaborder'):
                                                                    if i == 'Banner':
                                                                        stats = 'banners'
                                                                        lists = 'banner_list'
                                                                        name = 'banner_name'
                                                                        current = 'current_banner'
                                                                        count = 'banner_count'

                                                                        previous_was_type = True
                                                                    elif i == 'Border':
                                                                        stats = 'borders'
                                                                        lists = 'border_list'
                                                                        name = 'border_name'
                                                                        current = 'banner_border'
                                                                        count = 'border_count'
                                                                        previous_was_type = True
                                                                    elif i == 'Avaborder':
                                                                        stats = 'avatar_borders'
                                                                        lists = 'avaborder_list'
                                                                        name = 'banner_name'
                                                                        current = 'avatar_border'
                                                                        count = 'avaborder_count'
                                                                        previous_was_type = True
                                                        else:
                                                            await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                            s = 1
                                                            registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                                                            member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)
                                                            flists = str(registered_check[0][lists])
                                                            listbuy = self.listing(flists)
                                                            if i.lower() in listbuy:
                                                                new_admins = ''
                                                                admins_list = self.listing(flists)
                                                                for admin in admins_list:
                                                                    if admins_list.index(admin) == 0:
                                                                
                                                                        if s == 0:   
                                                                            admin = int(admin) + 1
                                                                            s += 1
                                                                        if admin == i.lower():
                                                                            s = 0
                                                                        new_admins += str(admin)
                                                                    

                                                                    else:
                                                                        if s == 0:
                                                                            admin = int(admin) + 1
                                                                            s+=1
                                                                        if admin == i.lower():
                                                                            s = 0

                                                                        new_admins += f' {admin}'
                                                                    
                        
                                                                await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id) 
                                                            else:                                                    
                                                                itemcode = await id_generator()
                                                                
                                                                a = f'{i.lower()}'
                            
                                                                b = 1
                                                                c = f"{itemcode}"
                                                                if member_registered[0][lists] is None:
                                                                    admins_list = self.listing(flists)
                                                                    new_admins = f' {a}' + f' {b}' + f' {c}'
                                    
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins),  ctx.author.id)


                                                                else:
                                                                    new_admins = str(flists) + f' {a}' + f' {b}' + f' {c}'
                                        
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins,  ctx.author.id)

                                                            await self.bot.db.execute(f'UPDATE registered SET {count} = {count} - 1 WHERE player_id = $1', member.id)
                                                            s = 1
                                                            t = 1
                                                            flists = str(member_registered[0][lists])
                                                            listbuy = self.listing(flists)
                                                            if i.lower() in listbuy:
                                                                new_admins = ''
                                                                admins_list = self.listing(flists)
                                                                for p, admin in enumerate(admins_list):
                                                                    if admins_list.index(admin) == 0:
                                    
                                                                        if t == 0:
                                                                            admin = ''
                                                                            t = 1
                                                                        if s == 0:
                                                                            if int(admin) == 1:
                                                                                admin = ''
                                                                                t = 0

                                                                            else: 
                                                                                admin = int(admin) - 1
                                                                            s += 1
                                                                        if admin == i.lower():
                                                                            if int(admins_list[p+1]) == 1:
                                                                                admin = ''
                                                                            s = 0
                                                                            
                                                                        new_admins += str(admin)
                                                                    

                                                                    else:

                                                                        if t == 0:
                                                                            admin = ''
                                                                            t = 1
                                                                        if s == 0:
                                                                            if int(admin) == 1:
                                                                                admin = ''
                                                                                t = 0
                                                                            else: 
                                                                                admin = int(admin) - 1
                                                                            s += 1
                                                                        if admin == i.lower():
                                                                            if int(admins_list[p+1]) == 1:
                                                                                admin = ''
                                                                            s = 0
                                                                        if admin == '':
                                                                            pass
                                                                        else:
                                                                            new_admins += f' {admin}'
                                                                if new_admins == '':
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = NULL WHERE player_id = $1', member.id) 
                                                                else:
                                                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, member.id) 

                                                            previous_was_type = False
                                                trade = 'no'
                                                await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, member.id)
                                                await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id) 
                                                await ctx.send(f"Trade between {ctx.author.mention} and {member.mention} is complete!")
                                                return
                                            else:
                                                await ctx.send(embed = embed)
                                            
                                        elif (msg.content.lower().startswith("d!cancel")) or (msg.content.lower().startswith("d!x")) or (msg.content.lower().startswith("d.cancel")) or (msg.content.lower().startswith("d.x")):
                                            trade = 'no'
                                            await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id) 
                                            await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade,member.id) 

                                            return
                                if view.value == False:
                                    await ctx.send(f"{member.mention} did not accept the gamble.")
                                    trade = 'no'
                                    await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, member.id)
                                    await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id) 
                                else:
                                    trade = 'no'
                                    await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, member.id)
                                    await self.bot.db.execute(f'UPDATE registered SET trade = $1 WHERE player_id = $2', trade, ctx.author.id) 
                                    await ctx.send(f"Timed out.")

                                        
                    else:
                        await ctx.send("Member haven't registered yet!")                
        else:
            await ctx.send("You haven't registered yet!")

    @commands.command(name = 'rand')
    async def rand(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if registered_check:

            with open('/home/ubuntu/bot_files/database/pokedex.csv', mode='r', encoding='ISO-8859-1') as file:
                reader = csv.reader(file)
                data = list(reader)

            random_pokemon = random.choice(data[1:])
            name = random_pokemon[1]
            height = random_pokemon[2]
            weight = random_pokemon[3]
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
            embed = discord.Embed(title=f'{name.capitalize()} #{random_pokemon[0]}', description=description, color=0xff5988)
            embed.set_image(url=f"attachment://{image_url}")
            embed.add_field(name='Base Stats', value=f'**HP:** {hp}\n**Attack:** {attack}\n**Defense:** {defense}\n**Sp. Atk:** {sp_atk}\n**Sp. Def:** {sp_def}\n**Speed:** {speed}\n**Total:** {total}', inline=True)
            embed.add_field(name='Type', value=type_str_formatted, inline=True)
            embed.add_field(name='Appearance', value=f'**Height:** {height}m\n**Weight:** {weight}', inline=True)
            embed.set_footer(text=f'Requested by {ctx.author.name}')


            await ctx.send(file = discord.File(image_url) ,embed = embed)
        else:
            await ctx.send("You haven't registered yet!")            



    @commands.command(name = 'gambleleaderboard', aliases = ['glb'])
    async def ggleaderboard_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
       
        if registered_check:


            lb = await self.bot.db.fetch('SELECT * FROM gamble WHERE player_name IS NOT NULL AND ticket >= 0 ORDER BY ticket DESC')

            data = []
            for faction in lb:
                data.append(faction['player_name'])

            stats = None

            pagination_view = RPaginationView()
            pagination_view.data = data
            pagination_view.lb = lb
            pagination_view.stat = self.bot
            pagination_view.stats = stats
            await pagination_view.send(ctx)

                

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'weeklyreset')
    async def weekly_command(self, ctx, stat : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if str(ctx.author.id) in admins_list:
                stats = ['rare', 'common', 'gamble']
                if stat in stats:
                    view = ConfirmCancel(ctx.author)
                    await ctx.send (f'Are you sure you want to reset the {stat} week and reward them?', view = view)
                    await view.wait()
                    if view.value is True:
                        if stat == 'gamble':
                            stut = 'gamble'
                            lb = await self.bot.db.fetch('SELECT * FROM gamble WHERE player_name IS NOT NULL AND played >= 0 ORDER BY weekly DESC LIMIT 8')
                        elif stat == 'rare':
                            stut = 'rank_system'
                            lb = await self.bot.db.fetch('SELECT * FROM rank_system WHERE matches_played >= 0 ORDER BY weekly DESC LIMIT 8')
                        elif stat == 'common':
                            stut = 'common_system'
                            lb = await self.bot.db.fetch('SELECT * FROM common_system WHERE matches_played >= 0 ORDER BY weekly DESC LIMIT 8')

                        else:
                            await ctx.send("Error.")
                            return
                        player = [row['player_id'] for row in lb]
                        playerstr = ''

                        for t,v in enumerate(player):
                            if t == 0:
                                dc = 300
                            elif t == 1:
                                dc = 225
                            elif t == 2:
                                dc = 150
                            elif t == 3:
                                dc = 100
                            elif t == 4:
                                dc = 80
                            elif t== 5:
                                dc = 60
                            elif t == 6:
                                dc = 40
                            elif t == 7:
                                dc = 30

                            
                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {dc} WHERE player_id = $1', player[t])
                            
                            registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', player[t])
                            flists = str(registered_check[0]['achievements'])
                            new_admins = ''
                            admins_list = self.listing(flists)
                            for p,admin in enumerate(admins_list):
                                if p == 0:
                                    new_admins += str(admin)
                                elif p == 16:
                                    if int(admin) == 0:
                                        admins_list[17] = 1
                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  player[t])
                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  player[t])
                                        await ctx.send("**Bronze Achievement Completed! ✦ End top 8 in a weekly leaderboard ✦**\n*10dc rewarded & Lootbox rewarded*")
                                    elif int(admin) == 2:
                                        admins_list[17] = 2
                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  player[t])
                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  player[t])
                                        await ctx.send("**Silver Achievement Completed! ✦✦ End top 8 in a weekly leaderboard 3 times ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                    elif int(admin) == 4:
                                        admins_list[17] = 3
                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  player[t])
                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  player[t])
                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ End top 8 in a weekly leaderboard 5 times ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                    admin = int(admin) + 1
                                    new_admins += f' {admin}'                                                         
                                else:
                                    new_admins += f' {admin}'  

                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, player[t])                                                                                                                                                                                                   
                            playerstr += f'<@{v}> Won **{dc}dc**\n'


                        await self.bot.db.execute(f'UPDATE {stut} SET weekly = 0')
                        channel = self.bot.get_channel(1208198326378307676)
                        await channel.send(f'The {stat.title()} Week has ended! Here are the results..\n{playerstr}')
                        
                    elif view.value is False:
                        await ctx.send("Cancelled.")
                    else:
                        await ctx.send("Timed out.")                
                else:
                    await ctx.send("Incorrect Lb.")
            else:
                await ctx.send("You can't use this command!")


        else:
             await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name='apc')
    async def addpc_command(self, ctx, member : discord.Member = None, pc : str = None, weekly : str = None):
        guild = self.bot.get_guild(774883579472904222)
        role = guild.get_role(786448967172882442)
        role2 = guild.get_role(1090438349455622204)
        role3 = guild.get_role(781452019578961921)
        if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles) or (ctx.author.id == 0):
            if (pc == None) or (member == None):
                em = discord.Embed(
                    title = "Help 🛠️",
                    description = '**d!apc [user] [pc]**',
                    colour = color
                )
                await ctx.send(embed = em)
                
            else:
                registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                member_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)
                if registered_check:

                    if member_check:
                        if weekly == None:
                            await self.bot.db.execute(f'UPDATE gamble SET total = total + {pc} WHERE player_id = $1', member.id)
                            await ctx.send(f"{pc} added from {member}")
                        else:
                            await self.bot.db.execute(f'UPDATE gamble SET weekly = weekly + {pc} WHERE player_id = $1', member.id)
                            await ctx.send(f"{pc} added from {member} WEEKLY")
                    else:
                        await ctx.send('Member has not registered yet! Use `d!start` to register.')

                else:
                    await ctx.send('You have not registered yet! Use `d!start` to register.')


        else:
            await ctx.send("You can't use this command!") 

    @commands.command(name='rpc')
    async def rpc_command(self, ctx, member : discord.Member = None, pc : str = None, weekly : str = None):
        guild = self.bot.get_guild(774883579472904222)
        role = guild.get_role(786448967172882442)
        role2 = guild.get_role(1090438349455622204)
        role3 = guild.get_role(781452019578961921)
        if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles) or (ctx.author.id == 0):
            if (pc == None) or (member == None):
                em = discord.Embed(
                    title = "Help 🛠️",
                    description = '**d!rpc [user] [pc]**',
                    colour = color
                )
                await ctx.send(embed = em)
                
            else:
                registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                member_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)
                if registered_check:

                    if member_check:
                        if weekly == None:
                            await self.bot.db.execute(f'UPDATE gamble SET total = total - {pc} WHERE player_id = $1', member.id)
                            await ctx.send(f"{pc} removed from {member}")
                        else:
                            await self.bot.db.execute(f'UPDATE gamble SET weekly = weekly - {pc} WHERE player_id = $1', member.id)
                            await ctx.send(f"{pc} removed from {member} WEEKLY")
                    else:
                        await ctx.send('Member has not registered yet! Use `d!start` to register.')

                else:
                    await ctx.send('You have not registered yet! Use `d!start` to register.')


        else:
            await ctx.send("You can't use this command!") 

def setup(bot):
    bot.add_cog(TradeCommands(bot))

