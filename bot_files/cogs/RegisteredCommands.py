import discord
from discord.ext import commands
import asyncpg
import asyncio
import re
import string

from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageSequence
from io import BytesIO
import numpy as np
import os
import aiohttp
import concurrent.futures
import random
from concurrent.futures import ThreadPoolExecutor
import gc

import psutil

color = 0x32006e



async def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class ConfirmCancel(discord.ui.View):
    def __init__(self, member : discord.Member):
        super().__init__(timeout = 15)

        self.value = None
        self.member = member


    @discord.ui.button(label = "Yes", style = discord.ButtonStyle.green, emoji = "✅" )
    async def confirm_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = True
        self.stop()
                
        for i in self.children:
            i.disabled = True
        try:
            await interaction.response.edit_message(view=self)
        except discord.errors.NotFound as e:

            pass
            
            
    @discord.ui.button(label = "No", style = discord.ButtonStyle.red, emoji = "❌" )
    async def cancel_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = False
        self.stop()
                
        for i in self.children:
            i.disabled = True
        try:
            await interaction.response.edit_message(view=self)
        except discord.errors.NotFound as e:
            pass
                            
        
    async def interaction_check(self, interaction : discord.Interaction):
        return interaction.user == self.member
                                        
    async def on_timeout(self):
        self.value = None

        for i in self.children:
            i.disabled = True

class RareCommon(discord.ui.View):
    def __init__(self,buttoner, member : discord.Member,commers,compositions,users,positions,gamers,casual,positions2,wars):
        super().__init__(timeout = 30)
        self.commers = commers
        self.casual = casual
        self.compositions = compositions
        self.users = users
        self.positions = positions
        self.member = member
        self.buttoner = buttoner
        self.gamers = gamers
        self.value = None
        self.disable_buttons = False
        self.positions2 = positions2
        self.wars = wars

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
    def cardinal(self, num : int):
        if (num >= 11) and (num <= 20):
            cardinal_num = f'{num}th'

        else:
            if str(num).endswith('1') is True:
                cardinal_num = f'{num}st'

            elif str(num).endswith('2') is True:
                cardinal_num = f'{num}nd'

            elif str(num).endswith('3') is True:
                cardinal_num = f'{num}rd'

            else:
                cardinal_num = f'{num}th'

        return cardinal_num
    

            
    pokeball = '<:pokeball:919647297808240680>'
    @discord.ui.button(label = "", style = discord.ButtonStyle.red, emoji = pokeball )
    async def confirm_button(self, button: discord.Button, interaction : discord.Interaction):
        try:
            self.disable_buttons = True
            common_positions = []
            index_number = 0
            for i in range(len(self.compositions)):
                common_positions.append(self.compositions[index_number]['player_id'])
                index_number += 1

            user_placement = common_positions.index(self.member.id)
            if  self.commers[0]['matches_played'] >= 10:
                rank = self.commers[0]['player_rank']
                points = self.commers[0]['points']

            else:
                rank = '*Unranked*'
                points = '*Unranked*'

            played = self.commers[0]['matches_played']
            wins = self.commers[0]['wins']
            
            if self.commers[0]['matches_played'] == 0:
                rate = '0%'

            else:
                win_rate = (self.commers[0]['wins']/self.commers[0]['matches_played'])*100
                win_rate_rounded = round(win_rate, 2)
                rate = f'{win_rate_rounded}%'

            if self.commers[0]['matches_played'] >= 10:
                position = self.cardinal(user_placement + 1)

            else:
                position = '*Unranked*'

            floor  = self.commers[0]["weekly"]
            if floor > 0:
                floor = f'+{"{:,}".format(floor)}'
            elif floor < 0:
                floor = f'{"{:,}".format(floor)}'
            else:
                floor = 0
            streak = self.commers[0]['streak']
            strsus = f"**Rank** » {rank} \n**Points** » {points} \n**Position** » {position} \n**Played** » {played} \n**Wins** » {wins} \n**Win Rate** » {rate} \n**Streak** » {streak} \n**Weekly** » {floor} "
            common_embed = discord.Embed(
                title = f"{self.member.name}'s Common Ranked Profile",
                description = strsus,
                colour = discord.Colour.red()
            )
            await interaction.response.edit_message(embed=common_embed, attachments=interaction.message.attachments)
            self.disable_buttons = False


        except discord.errors.InteractionResponded:
            return
    masterball = '<:MasterBall:1097952840045039677>'     
    @discord.ui.button(label = "", style = discord.ButtonStyle.blurple, emoji = masterball )
    async def cancel_button(self, button: discord.Button, interaction : discord.Interaction):
        try:
            self.disable_buttons = True
            common_positions = []
            index_number = 0
            for i in range(len(self.positions)):
                common_positions.append(self.positions[index_number]['player_id'])
                index_number += 1

            user_placement = common_positions.index(self.member.id)
            if  self.users[0]['matches_played'] >= 10:
                rank = self.users[0]['player_rank']
                points = self.users[0]['points']

            else:
                rank = '*Unranked*'
                points = '*Unranked*'

            played = self.users[0]['matches_played']
            wins = self.users[0]['wins']
            
            if self.users[0]['matches_played'] == 0:
                rate = '0%'

            else:
                win_rate = (self.users[0]['wins']/self.users[0]['matches_played'])*100
                win_rate_rounded = round(win_rate, 2)
                rate = f'{win_rate_rounded}%'

            if self.users[0]['matches_played'] >= 10:
                position = self.cardinal(user_placement + 1)

            else:
                position = '*Unranked*'

            floor  = self.users[0]["weekly"]
            if floor > 0:
                floor = f'+{"{:,}".format(floor)}'
            elif floor < 0:
                floor = f'{"{:,}".format(floor)}'
            else:
                floor = 0
            streak = self.users[0]['streak']
            strsus = f"**Rank** » {rank} \n**Points** » {points} \n**Position** » {position} \n**Played** » {played} \n**Wins** » {wins} \n**Win Rate** » {rate} \n**Streak** » {streak} \n**Weekly** » {floor} "
            common_embed = discord.Embed(
                title = f"{self.member.name}'s Rare Ranked Profile",
                description = strsus,
                colour = discord.Colour.blurple()
            )


            await interaction.response.edit_message(embed=common_embed, attachments=interaction.message.attachments)
            self.disable_buttons = False

        except discord.errors.InteractionResponded:
            return

    @discord.ui.button(label = "", style = discord.ButtonStyle.grey, emoji = '⚔️' )
    async def warcancel_button(self, button: discord.Button, interaction : discord.Interaction):
        try:
            self.disable_buttons = True

            rankvalue = self.wars[0]['rank_value']
            if rankvalue == 0:
                rank = 'Bronze'
            elif rankvalue == 1:
                rank = 'Silver'
            elif rankvalue == 2:
                rank = 'Gold'
            elif rankvalue == 3:
                rank = 'Platinum'
            elif rankvalue == 4:
                rank = 'Dominant' 

            points = self.wars[0]['points']     

            wwon = self.wars[0]['warswon']     

            wlost = self.wars[0]['warslost'] 
            wplayed =  wwon + wlost   

            if wplayed == 0:
                warrate = '0%'

            else:
                win_rate = (self.wars[0]['warswon']/wplayed)*100
                win_rate_rounded = round(win_rate, 2)
                warrate = f'{win_rate_rounded}%'

            dwon = self.wars[0]['wins'] 

            dplayed = dwon + self.wars[0]['loses'] 

            duelwl = dwon - self.wars[0]['loses'] 

            if duelwl >= 0:
                duelwl = f'+{duelwl}'

            streak = self.wars[0]['streak'] 
            mvps = self.wars[0]['mvps'] 
            
            


            strsus = f"**Rank** » {rank} \n**Points** » {points} \n**Wars Won** » {wwon} \n**Wars Played** » {wplayed} \n**War Winrate** » {warrate} \n**Duels Won** » {dwon}\n**Duels Played** » {dplayed} \n**Duels W/L** » {duelwl}  \n**War Streak** » {streak}\n**MVPs** » {mvps}"
            common_embed = discord.Embed(
                title = f"{self.member.name}'s War Profile",
                description = strsus,
                colour = 0x0f0f0f
            )


            await interaction.response.edit_message(embed=common_embed, attachments=interaction.message.attachments)
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



class RegisteredCommands(commands.Cog):
        
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        

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

    def cardinal(self, num : int):
        if (num >= 11) and (num <= 20):
            cardinal_num = f'{num}th'

        else:
            if str(num).endswith('1') is True:
                cardinal_num = f'{num}st'

            elif str(num).endswith('2') is True:
                cardinal_num = f'{num}nd'

            elif str(num).endswith('3') is True:
                cardinal_num = f'{num}rd'

            else:
                cardinal_num = f'{num}th'

        return cardinal_num

    def modulus(self, num : int):
        if num is not None:
            if num >= 0:
                modulus_num = num

            elif num < 0:
                modulus_num = num*-1

            return modulus_num

    @commands.command(name = 'start')
    async def start_command(self, ctx):
    
        profile = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if profile:
            await ctx.send('You have already registered!')

        else:

            author_name = ctx.author.name
            bronze1 = 'Bronze I'
            bronze_value = 1
            trade = 'no'
            badge = '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'
            device = 'pc'
            refer = 'False'
            voted = 'no'
            ping = 'yes'
            await self.bot.db.execute('INSERT INTO rank_system (player_id, player_name, matches_played, points, player_rank, rank_value, wins, streak, floor, weekly, daily) VALUES ($1, $2, 0, 150, $3, $4, 0, 0, 0, 0,0)', ctx.author.id, author_name, bronze1, bronze_value)
            await self.bot.db.execute('INSERT INTO casual (player_id, player_name, matches_played, points, wins, streak, votes, voted) VALUES ($1, $2, 0, 0, 0, 0, 0 , $3)', ctx.author.id, author_name, voted)
            await self.bot.db.execute('INSERT INTO wars (player_id, player_name, rank_value, warswon, warslost, wins, loses, mvps, streak, points) VALUES ($1, $2, 0, 0, 0, 0, 0, 0, 0, 0)', ctx.author.id, author_name)
            await self.bot.db.execute('INSERT INTO common_system (player_id, player_name, matches_played, points, player_rank, rank_value, wins, streak, floor, weekly,daily) VALUES ($1, $2, 0, 150, $3, $4, 0, 0, 0, 0,0)', ctx.author.id, author_name, bronze1, bronze_value)
            await self.bot.db.execute('INSERT INTO gamble (player_id, played, won,highest, total, net, streak, weekly, player_name,ticket) VALUES ($1, 0,  0, 0, 0, 0, 0, 0, $2,0)',ctx.author.id, ctx.author.global_name)
            await self.bot.db.execute('INSERT INTO registered (player_id,scraps,banner_pieces,banner_count,wishes,border_count,avaborder_count,title_count,trade,achievements,ribbon,device,special,refer,wl,lwar,wwar,player_name,mvps,gold,purple,ping) VALUES ($1,0,0,0,0,0,0,0,$2,$3,$4,$5,0,$6,0,0,0,$7,0,0,0,$8)', ctx.author.id,trade,badge,trade,device,refer,author_name,ping)
            await ctx.send('Succesfully registered! Please do `d!profile` if you want to open your profile.')         

    @commands.command(name = 'update')
    async def startg_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:   
            profile = await self.bot.db.fetch('SELECT * FROM gamble WHERE player_id = $1', ctx.author.id)
            
            if profile:
                await self.bot.db.execute(f'UPDATE casual SET player_name = $1 WHERE player_id = $2', ctx.author.name, ctx.author.id)

                await self.bot.db.execute(f'UPDATE rank_system SET player_name = $1 WHERE player_id = $2', ctx.author.name, ctx.author.id)
                await self.bot.db.execute(f'UPDATE common_system SET player_name = $1 WHERE player_id = $2', ctx.author.name, ctx.author.id)
                await self.bot.db.execute(f'UPDATE registered SET player_name = $1 WHERE player_id = $2', ctx.author.name, ctx.author.id)
                await self.bot.db.execute(f'UPDATE wars SET player_name = $1 WHERE player_id = $2', ctx.author.name, ctx.author.id)
                await self.bot.db.execute(f'UPDATE casual SET player_name = $1 WHERE player_id = $2', ctx.author.name, ctx.author.id)
                
                if ctx.author.nick == None:
                    if ctx.author.global_name == None:
                        await self.bot.db.execute(f'UPDATE gamble SET player_name = $1 WHERE player_id = $2', ctx.author.name, ctx.author.id)
                    else:
                        await self.bot.db.execute(f'UPDATE gamble SET player_name = $1 WHERE player_id = $2', ctx.author.global_name, ctx.author.id)
                else:
                    await self.bot.db.execute(f'UPDATE gamble SET player_name = $1 WHERE player_id = $2', ctx.author.nick, ctx.author.id)

                await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', ctx.author.id) 



                await ctx.send('Updated User Data!')
            else:

                await ctx.send('Error')
        else:
            await ctx.send("You haven't registered yet! Please do `d!start` do register.")


    @commands.command(name = 'profile')
    @commands.cooldown(1, 10 , commands.BucketType.user)
    async def profile_command(self, ctx, member : discord.Member = None):
        
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            global bronze1, bronze2, bronze3, bronze_value
            global silver1, silver2, silver3, silver_value
            global gold1, gold2, gold3, gold_value
            global platinum1, platinum2, platinum3, platinum_value
            global dominant, dominant_value

            bronze1 = 'Bronze I'
            bronze2 = 'Bronze II'
            bronze3 = 'Bronze III'

            silver1 = 'Silver I'
            silver2 = 'Silver II'
            silver3 = 'Silver III'

            gold1 = 'Gold I'
            gold2 = 'Gold II'
            gold3 = 'Gold III'

            platinum1 = 'Platinum I'
            platinum2 = 'Platinum II'
            platinum3 = 'Platinum III'

            dominant = 'Dominant'

            bronze_value = 1

            silver_value = 2

            gold_value = 3
            
            platinum_value = 4

            dominant_value = 5

            author_id = ctx.author.id

            author_name = ctx.author.name

            users = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', author_id)

            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', author_id)

            all_banners = await self.bot.db.fetch('SELECT * FROM banners')

            
            if member is None:
                if user_ban_list:
                    await ctx.send('You are banned from the bot.')

                else:
                    if users:                        
                        # Create a list to store each frame with text
                        
                        font = ImageFont.truetype("BebasNeue-Regular.ttf", 150)
                        font2 =  ImageFont.truetype("BebasNeue-Regular.ttf", 70)
                        font3 =  ImageFont.truetype("BebasNeue-Regular.ttf", 50)
                        stroke = 0

                        
                        gif_identifier = registered_check[0]['profile']


                        if gif_identifier:
                            if gif_identifier == 1:
                                await ctx.send("Profile is still rendering!")
                            else:

                                
                                member = ctx.author
                                buttoner = ctx.author
                                commers = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', ctx.author.id) 
                                compositions = await self.bot.db.fetch('SELECT player_id FROM common_system ORDER BY points DESC')
                                users = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', ctx.author.id)

                                positions = await self.bot.db.fetch('SELECT player_id FROM rank_system ORDER BY points DESC')
                                casual = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', ctx.author.id)

                                gamers = await self.bot.db.fetch('SELECT * FROM gamble WHERE player_id = $1', ctx.author.id)
                                positions2 = await self.bot.db.fetch('SELECT player_id FROM casual ORDER BY points DESC')

                                wars = await self.bot.db.fetch('SELECT * FROM wars WHERE player_id = $1', ctx.author.id)

                                
                                view = RareCommon(buttoner, member,commers,compositions,users,positions,gamers,casual,positions2,wars)


                                channel = self.bot.get_channel(1196406780327116860)
                                gif_message = await channel.fetch_message(gif_identifier)
                                gif_url = gif_message.attachments[0].url

                                if registered_check[0]['device'] == 'phone':
                                    
                                    await ctx.send(gif_url,view = view)
                                else:
                                    items = ['banner','border','avaborder']
                                    if ctx.author.id == 0:
                                        pass
                                    else:
                                        for i in items:
                                            if i == 'border':
                                                current = 'banner_border'
                                                lists = 'border_list'
                                                name = 'border_name'
                                            elif i == 'avaborder':
                                                current = 'avatar_border'
                                                lists = 'avaborder_list'
                                                name = 'banner_name'
                                            else:
                                                current = 'current_banner'
                                                lists = 'banner_list'
                                                name = 'banner_name'
                                                
                                            banner_name = registered_check[0][current]

                                            if banner_name is None:
                                                pass
                                            else:
                                                flists = str(registered_check[0][lists])
                                                listbuy = self.listing(flists)

                                                if banner_name in listbuy:
                                                    pass
                                                else:
                                                    await self.bot.db.execute(f'UPDATE registered SET {current} = NULL, profile = NULL WHERE player_id = $1', ctx.author.id)
                                                    await ctx.send("Something was changed in your inventory, please use `d!profile` again...")
                                                    return
                                    try:
                                        async with self.session.get(gif_url) as response:
                                            if response.status == 200:
                                                gif_bytes = await response.content.read()
                                            else:
                                                await ctx.send("An Error Occured.")
                                        if gif_bytes[:4] == b'\x89PNG':
                                            # The bytes represent a PNG file
                                            await ctx.send(file=discord.File(BytesIO(gif_bytes), filename='temp.png'),view = view)
                                        elif gif_bytes[:6] in (b'GIF87a', b'GIF89a'):
                                            # The bytes represent a GIF file
                                            await ctx.send(file=discord.File(BytesIO(gif_bytes), filename='temp.gif'),view = view)
                                        

                                    except discord.NotFound:
                                        await ctx.send("Profile not found, please contact a staff member.")
                        else:
                            render = 1
                            await self.bot.db.execute(f'UPDATE registered SET profile = $1 WHERE player_id = $2', render, ctx.author.id)

                            channel = self.bot.get_channel(1196406780327116860)
                        
                            items = ['banner','border','avaborder']
                            if ctx.author.id == 0:
                                pass
                            else:
                                for i in items:
                                    yes = 1
                                    if i == 'border':
                                        current = 'banner_border'
                                        lists = 'border_list'
                                        name = 'border_name'
                                    elif i == 'avaborder':
                                        current = 'avatar_border'
                                        lists = 'avaborder_list'
                                        name = 'banner_name'
                                    else:
                                        current = 'current_banner'
                                        lists = 'banner_list'
                                        name = 'banner_name'
                                        
                                    banner_name = registered_check[0][current]
                                    if banner_name is None:
                                        pass
                                    else:
                                        flists = str(registered_check[0][lists])
                                        listbuy = self.listing(flists)
                                        if banner_name in listbuy:
                                            pass
                                        else:
                                            await self.bot.db.execute(f'UPDATE registered SET {current} = NULL WHERE player_id = $1', ctx.author.id)

                            commers = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', author_id)      
                            if registered_check[0]['current_banner'] is None:
                                profile = Image.open("default.png")
                                gifyes = 'no'
                                
                            else:                                                    
                                banner = await self.bot.db.fetch('SELECT * FROM banners WHERE banner_name = $1', registered_check[0]['current_banner'])
                                banneris = banner[0]["banner_place"]
                                
                                if banneris.lower().endswith(('.gif')):
                                    gifyes = "yes"
                                else:
                                    gifyes = 'no'
                            
                                profile = Image.open(banneris)
                                

                                

                            if registered_check[0]['title'] is None:
                                titleis = 'Player'
                                
                            else:
                                titleis = registered_check[0]['title']
                            
                                            
                            if registered_check[0]['banner_border'] is None:
                                
                                borderis = Image.open("profile1.png")
                                
                            else:
                            
                                border = await self.bot.db.fetch('SELECT * FROM borders WHERE border_name = $1', registered_check[0]['banner_border'])
                                borderis = f'{border[0]["border_place"]}'
                                borderis = Image.open(borderis)
                            
                            borderis = borderis.convert('RGBA')

                            if registered_check[0]['avatar_border'] is None:
                                
                                avaborderis = Image.open("profile2.png")
                                
                            else:
                            
                                avaborder = await self.bot.db.fetch('SELECT * FROM avatar_borders WHERE banner_name = $1', registered_check[0]['avatar_border'])
                                avaborderis = f'{avaborder[0]["avatar_place"]}'
                                avaborderis = Image.open(avaborderis)
                            
                            avaborderis = avaborderis.convert('RGBA')
                                                                            
                            player_clan_1 = ''
                            
                            if registered_check[0]['clan_1'] is not None:
                                player_clan_1 += f'Clan | {registered_check[0]["clan_1"]}'
                                

                            if registered_check[0]['clan_1'] is None:
                                player_clan_1 += 'Clan | None'
                            font = ImageFont.truetype("BebasNeue-Regular.ttf", 150)
                            font2 =  ImageFont.truetype("BebasNeue-Regular.ttf",70)
                            font3 =  ImageFont.truetype("BebasNeue-Regular.ttf", 50)      

                        
                            
                            name = f'{ctx.author.display_name}'
                            if len(name) > 15:
                                name = name[:15] + ".."
                            data = BytesIO(await ctx.author.display_avatar.read())
                            pfp = Image.open(data)
                            pfp.convert('RGBA')
                            pfp = pfp.resize((300,300))
                            mask_im = Image.new("L", pfp.size, 0)
                            draw = ImageDraw.Draw(mask_im)
                            draw.rounded_rectangle((0, 0, 300, 300), fill=255,width=3, radius=15)
                            

                            guild = self.bot.get_guild(774883579472904222)
                            role = guild.get_role(798548690860113982)
                            if (role in ctx.author.roles) or (ctx.author.id == 0) or (ctx.author.id == 1209502516715192332):
                                
                                h = registered_check[0]["embed_colour"]
                                if h is None:
                                    tup = (255,255,255)
                                    stroke = 0
                                else:
                                    tup = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                                    stroke = 0
                            else:
                                stroke = 0
                                tup = (255,255,255)

                            if registered_check[0]['ribbon'] == 'no':

                                if (users[0]['matches_played'] >= 10) or (commers[0]['matches_played'] >= 10):
                                    rank = users[0]['player_rank']
                                    crank = commers[0]['player_rank']

                                    if (rank == 'Bronze I') or (rank == 'Bronze II') or (rank == 'Bronze III') or (crank == 'Bronze I') or (crank == 'Bronze II') or (crank == 'Bronze III'):
                                        design = Image.open("designbronze.png")
                                    if (rank == 'Silver I') or (rank == 'Silver II') or (rank == 'Silver III') or (crank == 'Silver I') or (crank == 'Silver II') or (crank == 'Silver III'):
                                        design = Image.open("designsilver.png")
                                    if (rank == 'Gold I') or (rank == 'Gold II') or (rank == 'Gold III') or (crank == 'Gold I') or (crank == 'Gold II') or (crank == 'Gold III'):
                                        design = Image.open("designgold.png")
                                    if (rank == 'Platinum I') or (rank == 'Platinum II') or (rank == 'Platinum III') or (crank == 'Platinum I') or (crank == 'Platinum II') or (crank == 'Platinum III'):
                                        design = Image.open("designplat.png")
                                    if (rank == 'Dominant') or (crank == 'Dominant'):
                                        design = Image.open("designdom.png")
                                    
                                    des = 1
                                else:
                                    design = None
                                    des = 0


                                        
                            else:
                                des = 0
                                design = None

                            if  commers[0]['matches_played'] >= 10:
                                comrank = f"Comm | {commers[0]['player_rank']} "

                            else:
                                comrank = f"Comm | Unranked "
                            if users[0]['matches_played'] >= 10:
                                rarerank = f"Rares | {users[0]['player_rank']} "

                            else:
                                rarerank = f"Rares | Unranked "
                            
                            if registered_check[0]['refer'] == 'False':
                                gift = True
                                box = Image.open("giftbox.png")
                                box = box.resize((80,80))
                            else:
                                box = None
                                gift = False

                            member = ctx.author
                            buttoner = ctx.author
                            commers = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', ctx.author.id) 
                            compositions = await self.bot.db.fetch('SELECT player_id FROM common_system ORDER BY points DESC')
                            users = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', ctx.author.id)

                            positions = await self.bot.db.fetch('SELECT player_id FROM rank_system ORDER BY points DESC')
                            casual = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', ctx.author.id)

                            gamers = await self.bot.db.fetch('SELECT * FROM gamble WHERE player_id = $1', ctx.author.id)
                            positions2 = await self.bot.db.fetch('SELECT player_id FROM casual ORDER BY points DESC')

                            wars = await self.bot.db.fetch('SELECT * FROM wars WHERE player_id = $1', ctx.author.id)

                            
                            view = RareCommon(buttoner, member,commers,compositions,users,positions,gamers,casual,positions2,wars)


                            if gifyes == 'yes':
                                    
                                def run_conversion(profile,design,pfp,mask_im,borderis,avaborderis,name,tup,font,font2,font3,titleis,stroke,player_clan_1,rarerank,comrank,des):
                                    
                                    framess = []  

                                    base_frame = Image.new("RGBA", (1440, 608))

                                    if des == 1:
                                        base_frame.paste(design, (0,0), design)
                                    
                                    base_frame.paste(pfp, (40,30), mask_im)
                                    base_frame.paste(borderis, (0,0), borderis)
                                    base_frame.paste(avaborderis, (0,0), avaborderis)
                                    if gift:
                                        base_frame.paste(box, (1340,20), box)

                                            
                                    blurred = Image.new('RGBA', base_frame.size)
                                    draw = ImageDraw.Draw(blurred)
                                    draw.text((370, 70), text=name, fill='black', font=font)
                                    blurred = blurred.filter(ImageFilter.BoxBlur(10))
                                    base_frame.paste(blurred,blurred)
                                    draw = ImageDraw.Draw(base_frame)
                                    draw.text((370, 70), name, tup, font = font,stroke_width=stroke, stroke_fill='black')

                                    blurred.close()
                                    blurred = Image.new('RGBA', base_frame.size)
                                    draw = ImageDraw.Draw(blurred)
                                    draw.text((373, 210), text=titleis, fill='black', font=font2)
                                    blurred = blurred.filter(ImageFilter.BoxBlur(10))
                                    base_frame.paste(blurred,blurred)
                                    draw2 = ImageDraw.Draw(base_frame)
                                    draw2.text((373, 210), titleis, tup, font = font2,stroke_width=stroke, stroke_fill='black')

                                    blurred.close()
                                    blurred = Image.new('RGBA', base_frame.size)
                                    draw = ImageDraw.Draw(blurred)
                                    draw.text((52, 363), text=player_clan_1, fill='black', font=font3)
                                    blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                    base_frame.paste(blurred,blurred)
                                    draw5 = ImageDraw.Draw(base_frame)
                                    draw5.text((52, 363), player_clan_1, tup, font = font3,stroke_width=stroke, stroke_fill='black')
                                    blurred.close()
                                    
                                    
                                    blurred = Image.new('RGBA', base_frame.size)
                                    draw = ImageDraw.Draw(blurred)
                                    draw.text((32, 420), text=rarerank, fill='black', font=font3)
                                    blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                    base_frame.paste(blurred,blurred)
                                    draw3 = ImageDraw.Draw(base_frame)
                                    draw3.text((32, 420), rarerank, tup, font = font3,stroke_width=stroke, stroke_fill='black')
                                    blurred.close()
                                    blurred = Image.new('RGBA', base_frame.size)
                                    draw = ImageDraw.Draw(blurred)
                                    draw.text((36, 477), text=comrank, fill='black', font=font3)
                                    blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                    base_frame.paste(blurred,blurred)
                                    draw4 = ImageDraw.Draw(base_frame)
                                    draw4.text((36, 477), comrank, tup, font = font3,stroke_width=stroke, stroke_fill='black')
                                    blurred.close()

                                    base_frame = base_frame.resize(( 855,365))


                                    for frame in ImageSequence.Iterator(profile):
                                        
                                        
                                        frames = frame.copy().convert('RGBA')
                                        frames.paste(base_frame, (0, 0), base_frame)
                                        
                                        framess.append(frames)

                                        


                                    del base_frame
                                    del frames


                                    bytes = BytesIO()
                                    framess[0].save(
                                        bytes,
                                        format="GIF",
                                        save_all=True,
                                        append_images=framess[1:],
                                        duration=profile.info["duration"],
                                        loop=profile.info["loop"],
                                        optimize =True,
                                    )
                                    for frame in framess:
                                        frame.close()

                                    
                                    bytes.seek(0)

                                    return bytes
                            
                                gif_bytes = run_conversion(profile, design, pfp, mask_im, borderis, avaborderis, name, tup, font, font2, font3, titleis, stroke, player_clan_1, rarerank, comrank, des)

                                dfile = discord.File(gif_bytes, filename="output.gif")
                                gif_message = await channel.send(file=dfile)

                                await self.bot.db.execute(f'UPDATE registered SET profile = $1 WHERE player_id = $2', gif_message.id, ctx.author.id)
                                gif_bytes.seek(0)
                                await ctx.send(file=dfile, view = view)
                                gif_bytes.close()

                                await asyncio.sleep(0)  

                        

                                        

                            else:
                                
                                if des == 1:
                                    profile.paste(design, (0,0), design) 
                                profile.paste(pfp, (40,30), mask_im)
                                profile.paste(borderis, (0,0), borderis)
                                profile.paste(avaborderis, (0,0), avaborderis)
                                if gift:
                                    profile.paste(box, (1340,20), box)
                                        
                                blurred = Image.new('RGBA', profile.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((370, 70), text=name, fill='black', font=font)
                                blurred = blurred.filter(ImageFilter.BoxBlur(10))
                                profile.paste(blurred,blurred)
                                draw = ImageDraw.Draw(profile)
                                draw.text((370, 70), name, tup, font = font,stroke_width=stroke, stroke_fill='black')
                                blurred = Image.new('RGBA', profile.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((373, 210), text=titleis, fill='black', font=font2)
                                blurred = blurred.filter(ImageFilter.BoxBlur(10))
                                profile.paste(blurred,blurred)
                                draw2 = ImageDraw.Draw(profile)
                                draw2.text((373, 210), titleis, tup, font = font2,stroke_width=stroke, stroke_fill='black')
                                blurred = Image.new('RGBA', profile.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((52, 363), text=player_clan_1, fill='black', font=font3)
                                blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                profile.paste(blurred,blurred)
                                draw5 = ImageDraw.Draw(profile)
                                draw5.text((52, 363), player_clan_1, tup, font = font3,stroke_width=stroke, stroke_fill='black')

                        
                                #image ranks tuff


                                blurred = Image.new('RGBA', profile.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((32, 420), text=rarerank, fill='black', font=font3)
                                blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                profile.paste(blurred,blurred)
                                draw3 = ImageDraw.Draw(profile)
                                draw3.text((32, 420), rarerank, tup, font = font3,stroke_width=stroke, stroke_fill='black')
                                blurred = Image.new('RGBA', profile.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((36, 477), text=comrank, fill='black', font=font3)
                                blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                profile.paste(blurred,blurred)
                                draw4 = ImageDraw.Draw(profile)
                                draw4.text((36, 477), comrank, tup, font = font3,stroke_width=stroke, stroke_fill='black')

                                bytes = BytesIO()
                                rgb_img = profile.convert("RGB")
                                rgb_img.save(bytes, format="PNG", quality=25)
                                bytes.seek(0)
                                dfile = discord.File(bytes, filename= "rgb_img.png")
                                
                                gif_message = await channel.send(file=dfile)
                                
                                await self.bot.db.execute(f'UPDATE registered SET profile = $1 WHERE player_id = $2', gif_message.id, ctx.author.id)

                                bytes.seek(0)
                                await ctx.send(file=dfile, view = view)



                            

                       


                    else:
                        await ctx.send("You haven't registered yet! Please do `d!start` do register.")

            else:
                member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                member_id = member.id

                member_name = member.name

                players = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', member_id)

                player_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', member_id)

                if player_ban_list:
                    await ctx.send('That person is banned from ranked battles.')

                else:
                    if players:
                        # Create a list to store each frame with text
                        
                        font = ImageFont.truetype("BebasNeue-Regular.ttf", 150)
                        font2 =  ImageFont.truetype("BebasNeue-Regular.ttf",70)
                        font3 =  ImageFont.truetype("BebasNeue-Regular.ttf", 50)   
                        stroke = 0

                        
                        gif_identifier = member_registered[0]['profile']
                        

                        if gif_identifier:
                            if gif_identifier == 1:
                                await ctx.send("Profile is still rendering!")
                            else:
                                

                                member = member
                                buttoner = ctx.author
                                commers = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', member.id) 
                                compositions = await self.bot.db.fetch('SELECT player_id FROM common_system ORDER BY points DESC')
                                users = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', member.id)

                                positions = await self.bot.db.fetch('SELECT player_id FROM rank_system ORDER BY points DESC')
                                casual = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', member.id)

                                gamers = await self.bot.db.fetch('SELECT * FROM gamble WHERE player_id = $1', member.id)
                                positions2 = await self.bot.db.fetch('SELECT player_id FROM casual ORDER BY points DESC')

                                wars = await self.bot.db.fetch('SELECT * FROM wars WHERE player_id = $1', member.id)
                                view = RareCommon(buttoner, member,commers,compositions,users,positions,gamers,casual,positions2,wars)

                                channel = self.bot.get_channel(1196406780327116860)
                                gif_message = await channel.fetch_message(gif_identifier)
                                gif_url = gif_message.attachments[0].url
                                if registered_check[0]['device'] == 'phone':
                                    
                                    await ctx.send(gif_url,view = view)
                                else:
                                    items = ['banner','border','avaborder']
                                    if ctx.author.id == 0:
                                        pass
                                    else:
                                        for i in items:
                                            if i == 'border':
                                                current = 'banner_border'
                                                lists = 'border_list'
                                                name = 'border_name'
                                            elif i == 'avaborder':
                                                current = 'avatar_border'
                                                lists = 'avaborder_list'
                                                name = 'banner_name'
                                            else:
                                                current = 'current_banner'
                                                lists = 'banner_list'
                                                name = 'banner_name'
                                                
                                            banner_name = member_registered[0][current]

                                            if banner_name is None:
                                                pass
                                            else:
                                                flists = str(member_registered[0][lists])
                                                listbuy = self.listing(flists)

                                                if banner_name in listbuy:
                                                    pass
                                                else:
                                                    await self.bot.db.execute(f'UPDATE registered SET {current} = NULL, profile = NULL WHERE player_id = $1', member.id)
                                                    await ctx.send("Something was changed in their inventory, please use `d!profile` again...")
                                                    return
                                    try:
                                        async with self.session.get(gif_url) as response:
                                            if response.status == 200:
                                                gif_bytes = await response.content.read()
                                            else:
                                                await ctx.send("An Error Occured.")
                                        if gif_bytes[:4] == b'\x89PNG':
                                            # The bytes represent a PNG file
                                            await ctx.send(file=discord.File(BytesIO(gif_bytes), filename='temp.png'),view = view)
                                        elif gif_bytes[:6] in (b'GIF87a', b'GIF89a'):
                                            # The bytes represent a GIF file
                                            await ctx.send(file=discord.File(BytesIO(gif_bytes), filename='temp.gif'),view = view)
                                        

                                    except discord.NotFound:
                                        await ctx.send("Profile not found, please contact a staff member.")
                        else:
                            registered_check = member_registered
                            render = 1
                            await self.bot.db.execute(f'UPDATE registered SET profile = $1 WHERE player_id = $2', render, member.id)

                            channel = self.bot.get_channel(1196406780327116860)
                        
                            items = ['banner','border','avaborder']
                            if ctx.author.id == 0:
                                pass
                            else:
                                for i in items:
                                    yes = 0
                                    if i == 'border':
                                        current = 'banner_border'
                                        lists = 'border_list'
                                        name = 'border_name'
                                    elif i == 'avaborder':
                                        current = 'avatar_border'
                                        lists = 'avaborder_list'
                                        name = 'banner_name'
                                    else:
                                        current = 'current_banner'
                                        lists = 'banner_list'
                                        name = 'banner_name'
                                        
                                    banner_name = registered_check[0][current]
                                    if banner_name is None:
                                        pass
                                    else:
                                        flists = str(registered_check[0][lists])
                                        listbuy = self.listing(flists)

                                        if banner_name in listbuy:
                                            pass
                                        else:
                                            await self.bot.db.execute(f'UPDATE registered SET {current} = NULL WHERE player_id = $1', member.id)
                            commers = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', member.id)    
                            users = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', member.id)

                            if registered_check[0]['current_banner'] is None:
                                profile = Image.open("default.png")
                                gifyes = 'no'
                                
                            else:                                                    
                                banner = await self.bot.db.fetch('SELECT * FROM banners WHERE banner_name = $1', registered_check[0]['current_banner'])
                                banneris = banner[0]["banner_place"]
                                
                                if banneris.lower().endswith(('.gif')):
                                    gifyes = "yes"
                                else:
                                    gifyes = 'no'
                            
                                profile = Image.open(banneris)

                                

                            if registered_check[0]['title'] is None:
                                titleis = 'Player'
                                
                            else:
                                titleis = registered_check[0]['title']
                                
                                            
                            if registered_check[0]['banner_border'] is None:
                                
                                borderis = Image.open("profile1.png")
                                
                            else:
                            
                                border = await self.bot.db.fetch('SELECT * FROM borders WHERE border_name = $1', registered_check[0]['banner_border'])
                                borderis = f'{border[0]["border_place"]}'
                                borderis = Image.open(borderis)

                            borderis = borderis.convert('RGBA')

                            if registered_check[0]['avatar_border'] is None:
                                
                                avaborderis = Image.open("profile2.png")
                                
                            else:
                            
                                avaborder = await self.bot.db.fetch('SELECT * FROM avatar_borders WHERE banner_name = $1', registered_check[0]['avatar_border'])
                                avaborderis = f'{avaborder[0]["avatar_place"]}'
                                avaborderis = Image.open(avaborderis)

                            avaborderis = avaborderis.convert('RGBA')
                                                                            
                            player_clan_1 = ''
                            
                            if registered_check[0]['clan_1'] is not None:
                                player_clan_1 += f'Clan | {registered_check[0]["clan_1"]}'
                                

                            if registered_check[0]['clan_1'] is None:
                                player_clan_1 += 'Clan | None'
                            font = ImageFont.truetype("BebasNeue-Regular.ttf", 150)
                            font2 =  ImageFont.truetype("BebasNeue-Regular.ttf", 70)
                            font3 =  ImageFont.truetype("BebasNeue-Regular.ttf", 50)                 
                            
                        
                            name = f'{member.display_name}'
                            if len(name) > 15:
                                name = name[:15] + ".."
        
                            data = BytesIO(await member.display_avatar.read())
                            pfp = Image.open(data)
                            pfp.convert('RGBA')
                            pfp = pfp.resize((300,300))
                            mask_im = Image.new("L", pfp.size, 0)
                            draw = ImageDraw.Draw(mask_im)
                            draw.rounded_rectangle((0, 0, 300, 300), fill=255,width=3, radius=15)
                            

                            guild = self.bot.get_guild(774883579472904222)
                            role = guild.get_role(798548690860113982)
                            if (role in member.roles) or (member.id == 0) or (member.id == 1209502516715192332):
                                
                                h = registered_check[0]["embed_colour"]
                                if h is None:
                                    tup = (255,255,255)
                                    stroke = 0
                                else:
                                    tup = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                                    stroke = 0
                            else:
                                stroke = 0
                                tup = (255,255,255)

                            if registered_check[0]['ribbon'] == 'no':

                                if (users[0]['matches_played'] >= 10) or (commers[0]['matches_played'] >= 10):
                                    rank = users[0]['player_rank']
                                    crank = commers[0]['player_rank']

                                    if (rank == 'Bronze I') or (rank == 'Bronze II') or (rank == 'Bronze III') or (crank == 'Bronze I') or (crank == 'Bronze II') or (crank == 'Bronze III'):
                                        design = Image.open("designbronze.png")
                                    if (rank == 'Silver I') or (rank == 'Silver II') or (rank == 'Silver III') or (crank == 'Silver I') or (crank == 'Silver II') or (crank == 'Silver III'):
                                        design = Image.open("designsilver.png")
                                    if (rank == 'Gold I') or (rank == 'Gold II') or (rank == 'Gold III') or (crank == 'Gold I') or (crank == 'Gold II') or (crank == 'Gold III'):
                                        design = Image.open("designgold.png")
                                    if (rank == 'Platinum I') or (rank == 'Platinum II') or (rank == 'Platinum III') or (crank == 'Platinum I') or (crank == 'Platinum II') or (crank == 'Platinum III'):
                                        design = Image.open("designplat.png")
                                    if (rank == 'Dominant') or (crank == 'Dominant'):
                                        design = Image.open("designdom.png")
                                    
                                    des = 1
                                else:
                                    design = None
                                    des = 0


                                        
                            else:
                                des = 0
                                design = None

                            if  commers[0]['matches_played'] >= 10:
                                comrank = f"Comm | {commers[0]['player_rank']} "

                            else:
                                comrank = f"Comm | Unranked "
                            if users[0]['matches_played'] >= 10:
                                rarerank = f"Rares | {users[0]['player_rank']} "

                            else:
                                rarerank = f"Rares | Unranked "

                            if registered_check[0]['refer'] == 'False':
                                gift = True
                                box = Image.open("giftbox.png")
                                box = box.resize((80,80))
                            else:
                                box = None
                                gift = False


                            member = member
                            buttoner = ctx.author
                            commers = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', member.id) 
                            compositions = await self.bot.db.fetch('SELECT player_id FROM common_system ORDER BY points DESC')
                            users = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', member.id)

                            positions = await self.bot.db.fetch('SELECT player_id FROM rank_system ORDER BY points DESC')
                            casual = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', member.id)

                            gamers = await self.bot.db.fetch('SELECT * FROM gamble WHERE player_id = $1', member.id)
                            positions2 = await self.bot.db.fetch('SELECT player_id FROM casual ORDER BY points DESC')

                            wars = await self.bot.db.fetch('SELECT * FROM wars WHERE player_id = $1', member.id)
                            view = RareCommon(buttoner, member,commers,compositions,users,positions,gamers,casual,positions2,wars)

                            if gifyes == 'yes':
                               
                            
                                def run_conversion(profile,design,pfp,mask_im,borderis,avaborderis,name,tup,font,font2,font3,titleis,stroke,player_clan_1,rarerank,comrank,des):
                                    
                                    framess = []  

                                    base_frame = Image.new("RGBA", (1440, 608))

                                    if des == 1:
                                        base_frame.paste(design, (0,0), design)
                                    
                                    base_frame.paste(pfp, (40,30), mask_im)
                                    base_frame.paste(borderis, (0,0), borderis)
                                    base_frame.paste(avaborderis, (0,0), avaborderis)
                                    if gift:
                                        base_frame.paste(box, (1340,20), box)

                                            
                                    blurred = Image.new('RGBA', base_frame.size)
                                    draw = ImageDraw.Draw(blurred)
                                    draw.text((370, 70), text=name, fill='black', font=font)
                                    blurred = blurred.filter(ImageFilter.BoxBlur(10))
                                    base_frame.paste(blurred,blurred)
                                    draw = ImageDraw.Draw(base_frame)
                                    draw.text((370, 70), name, tup, font = font,stroke_width=stroke, stroke_fill='black')

                                    blurred.close()
                                    blurred = Image.new('RGBA', base_frame.size)
                                    draw = ImageDraw.Draw(blurred)
                                    draw.text((373, 210), text=titleis, fill='black', font=font2)
                                    blurred = blurred.filter(ImageFilter.BoxBlur(10))
                                    base_frame.paste(blurred,blurred)
                                    draw2 = ImageDraw.Draw(base_frame)
                                    draw2.text((373, 210), titleis, tup, font = font2,stroke_width=stroke, stroke_fill='black')

                                    blurred.close()
                                    blurred = Image.new('RGBA', base_frame.size)
                                    draw = ImageDraw.Draw(blurred)
                                    draw.text((52, 363), text=player_clan_1, fill='black', font=font3)
                                    blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                    base_frame.paste(blurred,blurred)
                                    draw5 = ImageDraw.Draw(base_frame)
                                    draw5.text((52, 363), player_clan_1, tup, font = font3,stroke_width=stroke, stroke_fill='black')
                                    blurred.close()
                                    
                                    
                                    blurred = Image.new('RGBA', base_frame.size)
                                    draw = ImageDraw.Draw(blurred)
                                    draw.text((32, 420), text=rarerank, fill='black', font=font3)
                                    blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                    base_frame.paste(blurred,blurred)
                                    draw3 = ImageDraw.Draw(base_frame)
                                    draw3.text((32, 420), rarerank, tup, font = font3,stroke_width=stroke, stroke_fill='black')
                                    blurred.close()
                                    blurred = Image.new('RGBA', base_frame.size)
                                    draw = ImageDraw.Draw(blurred)
                                    draw.text((36, 477), text=comrank, fill='black', font=font3)
                                    blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                    base_frame.paste(blurred,blurred)
                                    draw4 = ImageDraw.Draw(base_frame)
                                    draw4.text((36, 477), comrank, tup, font = font3,stroke_width=stroke, stroke_fill='black')
                                    blurred.close()

                                    base_frame = base_frame.resize(( 855,365))


                                    for frame in ImageSequence.Iterator(profile):
                                        
                                        
                                        frames = frame.copy().convert('RGBA')
                                        frames.paste(base_frame, (0, 0), base_frame)
                                        
                                        framess.append(frames)

                                        


                                    del base_frame
                                    del frames


                                    bytes = BytesIO()
                                    framess[0].save(
                                        bytes,
                                        format="GIF",
                                        save_all=True,
                                        append_images=framess[1:],
                                        duration=profile.info["duration"],
                                        loop=profile.info["loop"],
                                        optimize =True,
                                    )
                                    for frame in framess:
                                        frame.close()

                                    
                                    bytes.seek(0)

                                    return bytes
                                

                                gif_bytes = run_conversion(profile, design, pfp, mask_im, borderis, avaborderis, name, tup, font, font2, font3, titleis, stroke, player_clan_1, rarerank, comrank, des)

                                dfile = discord.File(gif_bytes, filename="output.gif")
                                gif_message = await channel.send(file=dfile, view = view)

                                await self.bot.db.execute(f'UPDATE registered SET profile = $1 WHERE player_id = $2', gif_message.id, member.id)
                                gif_bytes.seek(0)
                                await ctx.send(file=dfile, view = view)    
                                gif_bytes.close()



                                        

                            else:

                                if des == 1:
                                    profile.paste(design, (0,0), design) 
                                profile.paste(pfp, (40,30), mask_im)
                                profile.paste(borderis, (0,0), borderis)
                                profile.paste(avaborderis, (0,0), avaborderis)

                                if gift:
                                    profile.paste(box, (1340,20), box)

                                blurred = Image.new('RGBA', profile.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((370, 70), text=name, fill='black', font=font)
                                blurred = blurred.filter(ImageFilter.BoxBlur(10))
                                profile.paste(blurred,blurred)
                                draw = ImageDraw.Draw(profile)
                                draw.text((370, 70), name, tup, font = font,stroke_width=stroke, stroke_fill='black')
                                blurred = Image.new('RGBA', profile.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((373, 210), text=titleis, fill='black', font=font2)
                                blurred = blurred.filter(ImageFilter.BoxBlur(10))
                                profile.paste(blurred,blurred)
                                draw2 = ImageDraw.Draw(profile)
                                draw2.text((373, 210), titleis, tup, font = font2,stroke_width=stroke, stroke_fill='black')
                                blurred = Image.new('RGBA', profile.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((52, 363), text=player_clan_1, fill='black', font=font3)
                                blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                profile.paste(blurred,blurred)
                                draw5 = ImageDraw.Draw(profile)
                                draw5.text((52, 363), player_clan_1, tup, font = font3,stroke_width=stroke, stroke_fill='black')

                        
                                #image ranks tuff


                                blurred = Image.new('RGBA', profile.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((32, 420), text=rarerank, fill='black', font=font3)
                                blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                profile.paste(blurred,blurred)
                                draw3 = ImageDraw.Draw(profile)
                                draw3.text((32, 420), rarerank, tup, font = font3,stroke_width=stroke, stroke_fill='black')
                                blurred = Image.new('RGBA', profile.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((36, 477), text=comrank, fill='black', font=font3)
                                blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                profile.paste(blurred,blurred)
                                draw4 = ImageDraw.Draw(profile)
                                draw4.text((36, 477), comrank, tup, font = font3,stroke_width=stroke, stroke_fill='black')

                                bytes = BytesIO()
                                rgb_img = profile.convert("RGB")
                                rgb_img.save(bytes, format="PNG", quality=25)
                                bytes.seek(0)
                                dfile = discord.File(bytes, filename= "rgb_img.png")
                                
                                                
                                gif_message = await channel.send(file=dfile)
                    
                                await self.bot.db.execute(f'UPDATE registered SET profile = $1 WHERE player_id = $2', gif_message.id, member.id)
                                bytes.seek(0)
                                await ctx.send(file=dfile, view = view)



            
                    else:
                        await ctx.send('That person is not in the database! Ask them to type d!profile to register.')
        
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')
    @commands.command(name = 'test', aliases = ['testt'])
    async def srt_tes_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        gif_identifier = registered_check[0]['profile']
        channel = self.bot.get_channel(1196406780327116860)
        gif_message = await channel.fetch_message(gif_identifier)
        gif_url = gif_message.attachments[0].url

        await ctx.send(gif_url)

        

    @commands.command(name ='toggleribbon', aliases = ['tr'])
    async def can_trade(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', ctx.author.id)
            if registered_check[0]['ribbon'] == 'no':
                trade = 'yes'
                await self.bot.db.execute(f'UPDATE registered SET ribbon = $1 WHERE player_id = $2', trade, ctx.author.id) 
                await ctx.send("Set Ribbon to `disabled`")
            else:
                trade = 'no'
                await self.bot.db.execute(f'UPDATE registered SET ribbon = $1 WHERE player_id = $2', trade, ctx.author.id) 
                await ctx.send("Set Ribbon to `enabled`")

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name ='toggledevice', aliases = ['td'])
    async def togglecan_tradeDd(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if registered_check[0]['device'] == 'phone':
                device = 'pc'
                await self.bot.db.execute(f'UPDATE registered SET device = $1 WHERE player_id = $2', device, ctx.author.id) 
                await ctx.send("Set Profile type for `PC`")
            else:
                device = 'phone'
                await self.bot.db.execute(f'UPDATE registered SET device = $1 WHERE player_id = $2', device, ctx.author.id) 
                await ctx.send("Set Profile type for `MOBILE`")

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'setcolor', aliases = ['setcolour'])
    async def set_embed_command(self, ctx, colour = None):
        profile = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if profile:
            if colour is None:
                em = discord.Embed(
                    title = 'Set Color',
                    description = '**Set your player profile Text color.**\n\nd!setcolor [colour in hexadecimal with the #]\nSearch "Color picker" on google and use the hex code.',
                    colour = color
                )

                await ctx.send(embed = em)

            else:
                match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', colour)

                if match:
                    await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', ctx.author.id)
                    await self.bot.db.execute('UPDATE registered SET embed_colour = $1 WHERE player_id = $2', (str(colour)[1::]).lower(), ctx.author.id)

                    await ctx.send(f'Your player profile colour has been set to {colour.capitalize()}. \nThis feature is only for boosters, activate this feature by boosting the server!')

                else:
                    await ctx.send('Invalid Hexadecimal code.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'render')
    @commands.cooldown(1, 15 , commands.BucketType.user)
    async def render_command(self, ctx):
        
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            global bronze1, bronze2, bronze3, bronze_value
            global silver1, silver2, silver3, silver_value
            global gold1, gold2, gold3, gold_value
            global platinum1, platinum2, platinum3, platinum_value
            global dominant, dominant_value

            bronze1 = 'Bronze I'
            bronze2 = 'Bronze II'
            bronze3 = 'Bronze III'

            silver1 = 'Silver I'
            silver2 = 'Silver II'
            silver3 = 'Silver III'

            gold1 = 'Gold I'
            gold2 = 'Gold II'
            gold3 = 'Gold III'

            platinum1 = 'Platinum I'
            platinum2 = 'Platinum II'
            platinum3 = 'Platinum III'

            dominant = 'Dominant'

            bronze_value = 1

            silver_value = 2

            gold_value = 3
            
            platinum_value = 4

            dominant_value = 5

            author_id = ctx.author.id

            author_name = ctx.author.name

            users = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', author_id)

            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', author_id)

            all_banners = await self.bot.db.fetch('SELECT * FROM banners')

            


            if user_ban_list:
                await ctx.send('You are banned from the bot.')

            else:
                if users:                        
                    # Create a list to store each frame with text
                    
                    font = ImageFont.truetype("BebasNeue-Regular.ttf", 150)
                    font2 =  ImageFont.truetype("BebasNeue-Regular.ttf",70)
                    font3 =  ImageFont.truetype("BebasNeue-Regular.ttf", 50)   
                    stroke = 0

                    
                    gif_identifier = registered_check[0]['profile']

                    if gif_identifier is None:
                        await ctx.send("Create a profile first! Use the command `d!profile`")

                    else:

                        render = 1
                        await self.bot.db.execute(f'UPDATE registered SET profile = $1 WHERE player_id = $2', render, ctx.author.id)

                        channel = self.bot.get_channel(1196406780327116860)
                    
                        items = ['banner','border','avaborder']
                        if ctx.author.id == 0:
                            pass
                        else:
                            for i in items:
                                if i == 'border':
                                    current = 'banner_border'
                                    lists = 'border_list'
                                    name = 'border_name'
                                elif i == 'avaborder':
                                    current = 'avatar_border'
                                    lists = 'avaborder_list'
                                    name = 'banner_name'
                                else:
                                    current = 'current_banner'
                                    lists = 'banner_list'
                                    name = 'banner_name'
                                    
                                banner_name = registered_check[0][current]

                                if banner_name is None:
                                    pass
                                else:
                                    flists = str(registered_check[0][lists])
                                    listbuy = self.listing(flists)

                                    if banner_name in listbuy:
                                        pass
                                    else:
                                        await self.bot.db.execute(f'UPDATE registered SET {current} = NULL, profile = NULL WHERE player_id = $1', ctx.author.id)
                                        await ctx.send("Something was changed in your inventory, please use `d!profile` again...")
                                        return
                        commers = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', author_id)      
                        if registered_check[0]['current_banner'] is None:
                            profile = Image.open("default.png")
                            gifyes = 'no'
                            
                        else:                                                    
                            banner = await self.bot.db.fetch('SELECT * FROM banners WHERE banner_name = $1', registered_check[0]['current_banner'])
                            banneris = banner[0]["banner_place"]
                            
                            if banneris.lower().endswith(('.gif')):
                                gifyes = "yes"
                            else:
                                gifyes = 'no'
                        
                            profile = Image.open(banneris)

                            

                        if registered_check[0]['title'] is None:
                            titleis = 'Player'
                            
                        else:
                            titleis = registered_check[0]['title']
                            
                                        
                        if registered_check[0]['banner_border'] is None:
                            
                            borderis = Image.open("profile1.png")
                            
                        else:
                        
                            border = await self.bot.db.fetch('SELECT * FROM borders WHERE border_name = $1', registered_check[0]['banner_border'])
                            borderis = f'{border[0]["border_place"]}'
                            borderis = Image.open(borderis)

                        borderis = borderis.convert('RGBA')
                        if registered_check[0]['avatar_border'] is None:
                            
                            avaborderis = Image.open("profile2.png")
                            
                        else:
                        
                            avaborder = await self.bot.db.fetch('SELECT * FROM avatar_borders WHERE banner_name = $1', registered_check[0]['avatar_border'])
                            avaborderis = f'{avaborder[0]["avatar_place"]}'
                            avaborderis = Image.open(avaborderis)
                        
                        avaborderis = avaborderis.convert('RGBA')
                                                                        
                        player_clan_1 = ''
                        
                        if registered_check[0]['clan_1'] is not None:
                            player_clan_1 += f'Clan | {registered_check[0]["clan_1"]}'
                            

                        if registered_check[0]['clan_1'] is None:
                            player_clan_1 += 'Clan | None'
                        font = ImageFont.truetype("BebasNeue-Regular.ttf", 150)
                        font2 =  ImageFont.truetype("BebasNeue-Regular.ttf", 70)
                        font3 =  ImageFont.truetype("BebasNeue-Regular.ttf", 50)                  
                        
                        
                        name = f'{ctx.author.display_name}'
                        if len(name) > 15:
                            name = name[:15] + ".."

                        data = BytesIO(await ctx.author.display_avatar.read())
                        pfp = Image.open(data)
                        pfp.convert('RGBA')
                        pfp = pfp.resize((300,300))
                        mask_im = Image.new("L", pfp.size, 0)
                        draw = ImageDraw.Draw(mask_im)
                        draw.rounded_rectangle((0, 0, 300, 300), fill=255,width=3, radius=15)
                        

                        guild = self.bot.get_guild(774883579472904222)
                        role = guild.get_role(798548690860113982)
                        
                        if (role in ctx.author.roles) or (ctx.author.id == 0) or (ctx.author.id == 1209502516715192332):
                            
                            h = registered_check[0]["embed_colour"]
                            if h is None:
                                tup = (255,255,255)
                                stroke = 0
                            else:
                                tup = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                                stroke = 0
                        else:
                            stroke = 0
                            tup = (255,255,255)

                        if registered_check[0]['ribbon'] == 'no':
                        
                            if (users[0]['matches_played'] >= 10) or (commers[0]['matches_played'] >= 10):
                                rank = users[0]['player_rank']
                                crank = commers[0]['player_rank']

                                if (rank == 'Bronze I') or (rank == 'Bronze II') or (rank == 'Bronze III') or (crank == 'Bronze I') or (crank == 'Bronze II') or (crank == 'Bronze III'):
                                    design = Image.open("designbronze.png")
                                if (rank == 'Silver I') or (rank == 'Silver II') or (rank == 'Silver III') or (crank == 'Silver I') or (crank == 'Silver II') or (crank == 'Silver III'):
                                    design = Image.open("designsilver.png")
                                if (rank == 'Gold I') or (rank == 'Gold II') or (rank == 'Gold III') or (crank == 'Gold I') or (crank == 'Gold II') or (crank == 'Gold III'):
                                    design = Image.open("designgold.png")
                                if (rank == 'Platinum I') or (rank == 'Platinum II') or (rank == 'Platinum III') or (crank == 'Platinum I') or (crank == 'Platinum II') or (crank == 'Platinum III'):
                                    design = Image.open("designplat.png")
                                if (rank == 'Dominant') or (crank == 'Dominant'):
                                    design = Image.open("designdom.png")
                                
                                des = 1
                            else:
                                design = None
                                des = 0


                                        
                        else:
                            des = 0
                            design = None

                        if  commers[0]['matches_played'] >= 10:
                            comrank = f"Comm | {commers[0]['player_rank']} "

                        else:
                            comrank = f"Comm | Unranked "
                        if users[0]['matches_played'] >= 10:
                            rarerank = f"Rares | {users[0]['player_rank']} "

                        else:
                            rarerank = f"Rares | Unranked "
                            
                        if registered_check[0]['refer'] == 'False':
                            gift = True
                            box = Image.open("giftbox.png")
                            box = box.resize((80,80))
                        else:
                            gift = False

                        if gifyes == 'yes':
                            def run_conversion(profile,design,pfp,mask_im,borderis,avaborderis,name,tup,font,font2,font3,titleis,stroke,player_clan_1,rarerank,comrank,des):
                                
                                framess = []  

                                base_frame = Image.new("RGBA", (1440, 608))

                                if des == 1:
                                    base_frame.paste(design, (0,0), design)
                                
                                base_frame.paste(pfp, (40,30), mask_im)
                                base_frame.paste(borderis, (0,0), borderis)
                                base_frame.paste(avaborderis, (0,0), avaborderis)
                                if gift:
                                    base_frame.paste(box, (1340,20), box)

                                        
                                blurred = Image.new('RGBA', base_frame.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((370, 70), text=name, fill='black', font=font)
                                blurred = blurred.filter(ImageFilter.BoxBlur(10))
                                base_frame.paste(blurred,blurred)
                                draw = ImageDraw.Draw(base_frame)
                                draw.text((370, 70), name, tup, font = font,stroke_width=stroke, stroke_fill='black')

                                blurred.close()
                                blurred = Image.new('RGBA', base_frame.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((373, 210), text=titleis, fill='black', font=font2)
                                blurred = blurred.filter(ImageFilter.BoxBlur(10))
                                base_frame.paste(blurred,blurred)
                                draw2 = ImageDraw.Draw(base_frame)
                                draw2.text((373, 210), titleis, tup, font = font2,stroke_width=stroke, stroke_fill='black')

                                blurred.close()
                                blurred = Image.new('RGBA', base_frame.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((52, 363), text=player_clan_1, fill='black', font=font3)
                                blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                base_frame.paste(blurred,blurred)
                                draw5 = ImageDraw.Draw(base_frame)
                                draw5.text((52, 363), player_clan_1, tup, font = font3,stroke_width=stroke, stroke_fill='black')
                                blurred.close()
                                
                                
                                blurred = Image.new('RGBA', base_frame.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((32, 420), text=rarerank, fill='black', font=font3)
                                blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                base_frame.paste(blurred,blurred)
                                draw3 = ImageDraw.Draw(base_frame)
                                draw3.text((32, 420), rarerank, tup, font = font3,stroke_width=stroke, stroke_fill='black')
                                blurred.close()
                                blurred = Image.new('RGBA', base_frame.size)
                                draw = ImageDraw.Draw(blurred)
                                draw.text((36, 477), text=comrank, fill='black', font=font3)
                                blurred = blurred.filter(ImageFilter.BoxBlur(7))
                                base_frame.paste(blurred,blurred)
                                draw4 = ImageDraw.Draw(base_frame)
                                draw4.text((36, 477), comrank, tup, font = font3,stroke_width=stroke, stroke_fill='black')
                                blurred.close()

                                base_frame = base_frame.resize(( 855,365))


                                for frame in ImageSequence.Iterator(profile):
                                    
                                    
                                    frames = frame.copy().convert('RGBA')
                                    frames.paste(base_frame, (0, 0), base_frame)
                                    
                                    framess.append(frames)

                                    


                                del base_frame
                                del frames


                                bytes = BytesIO()
                                framess[0].save(
                                    bytes,
                                    format="GIF",
                                    save_all=True,
                                    append_images=framess[1:],
                                    duration=profile.info["duration"],
                                    loop=profile.info["loop"],
                                    optimize =True,
                                )
                                for frame in framess:
                                    frame.close()

                                
                                bytes.seek(0)

                                return bytes
                        
                            gif_bytes = run_conversion(profile, design, pfp, mask_im, borderis, avaborderis, name, tup, font, font2, font3, titleis, stroke, player_clan_1, rarerank, comrank, des)

                            
                            gif_bytes.seek(0)
                            dfile = discord.File(gif_bytes, filename="output.gif")
                            gif_message = await channel.send(file=dfile)
                            gif_bytes.close()



                            await self.bot.db.execute(f'UPDATE registered SET profile = $1 WHERE player_id = $2', gif_message.id, ctx.author.id)
                            await ctx.send("Render complete! Use `d!profile` again to view your profile")


                        

                                    

                        else:

                            if des == 1:
                                profile.paste(design, (0,0), design) 
                            profile.paste(pfp, (40,30), mask_im)
                            profile.paste(borderis, (0,0), borderis)
                            profile.paste(avaborderis, (0,0), avaborderis)

                            if gift:
                                profile.paste(box, (1340,20), box)
                                    
                            blurred = Image.new('RGBA', profile.size)
                            draw = ImageDraw.Draw(blurred)
                            draw.text((370, 70), text=name, fill='black', font=font)
                            blurred = blurred.filter(ImageFilter.BoxBlur(10))
                            profile.paste(blurred,blurred)
                            draw = ImageDraw.Draw(profile)
                            draw.text((370, 70), name, tup, font = font,stroke_width=stroke, stroke_fill='black')
                            blurred = Image.new('RGBA', profile.size)
                            draw = ImageDraw.Draw(blurred)
                            draw.text((373, 210), text=titleis, fill='black', font=font2)
                            blurred = blurred.filter(ImageFilter.BoxBlur(10))
                            profile.paste(blurred,blurred)
                            draw2 = ImageDraw.Draw(profile)
                            draw2.text((373, 210), titleis, tup, font = font2,stroke_width=stroke, stroke_fill='black')
                            blurred = Image.new('RGBA', profile.size)
                            draw = ImageDraw.Draw(blurred)
                            draw.text((52, 363), text=player_clan_1, fill='black', font=font3)
                            blurred = blurred.filter(ImageFilter.BoxBlur(7))
                            profile.paste(blurred,blurred)
                            draw5 = ImageDraw.Draw(profile)
                            draw5.text((52, 363), player_clan_1, tup, font = font3,stroke_width=stroke, stroke_fill='black')

                    
                            #image ranks tuff


                            blurred = Image.new('RGBA', profile.size)
                            draw = ImageDraw.Draw(blurred)
                            draw.text((32, 420), text=rarerank, fill='black', font=font3)
                            blurred = blurred.filter(ImageFilter.BoxBlur(7))
                            profile.paste(blurred,blurred)
                            draw3 = ImageDraw.Draw(profile)
                            draw3.text((32, 420), rarerank, tup, font = font3,stroke_width=stroke, stroke_fill='black')
                            blurred = Image.new('RGBA', profile.size)
                            draw = ImageDraw.Draw(blurred)
                            draw.text((36, 477), text=comrank, fill='black', font=font3)
                            blurred = blurred.filter(ImageFilter.BoxBlur(7))
                            profile.paste(blurred,blurred)
                            draw4 = ImageDraw.Draw(profile)
                            draw4.text((36, 477), comrank, tup, font = font3,stroke_width=stroke, stroke_fill='black')


                            bytes = BytesIO()
                            rgb_img = profile.convert("RGB")
                            rgb_img.save(bytes, format="PNG", quality=25)
                            dfile = discord.File(bytes, filename= "rgb_img.png")
                            bytes.seek(0)
                                            
                            gif_message = await channel.send(file=dfile)
                            
                            await self.bot.db.execute(f'UPDATE registered SET profile = $1 WHERE player_id = $2', gif_message.id, ctx.author.id)

                            
                            await ctx.send("Render complete! Use `d!profile` again to view your profile")
                  

                else:
                    await ctx.send("You haven't registered yet! Please do `d!start` do register.")

    @commands.group(name ='refer', aliases = ['ref'], invoke_without_command = True)
    async def refer_command(self, ctx,member : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if registered_check[0]['refer'] == 'False':
                if member == None:
                    await ctx.send("Please mention the user who referred you to us. `d!refer @mention`")
                else:
                    member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)
                    if member_registered:
                        if member_registered[0]['refer'] == 'False':
                            await ctx.send("The member you're trying to mention is still not eligible to receive a box, ask them to refer first.")
                            return
                        referbox = '1'
                        await self.bot.db.execute(f'UPDATE registered SET refer = $1 WHERE player_id = $2', referbox, ctx.author.id) 
                        current_count = int(member_registered[0]['refer'])
                        referbox = str(current_count + 1)
                        await self.bot.db.execute(f'UPDATE registered SET refer = $1 WHERE player_id = $2', referbox, member.id)
                        await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', ctx.author.id) 
                        await ctx.send(f"Welcome to **Dominant** {ctx.author}\n\n*+1 referral box {member.mention} and {ctx.author.mention}*") 
                    else:
                        await ctx.send("The player you mentioned hasn't registered to the bot yet.")
            else:

                current_count = int(registered_check[0]['refer'])
                inv_embed = discord.Embed(
                    title = f"{ctx.author.name}'s Referrals",
                    description = '',
                    colour = color
                )

                
                inv_embed.add_field(name = f'Refer more people to get more boxes!', value = f'You have **{registered_check[0]["refer"]}** referral boxes.\n\nReferral boxes can contain,\n**Lootboxes, <:s:1126546706721415320> <:a:1126546710332710943> <:b:1126546712283066479> <:c:1126546716200542378> <:d_:1126546717978919033> items and even Dc!**\n*Use `d!refer open` to open boxes*')


                banneris = 'gift.png'
                inv_embed.set_image(url=f"attachment://{banneris}")
                inv_embed.set_thumbnail(url = ctx.author.display_avatar)
                inv_embed.set_footer(text='Get a new user who just signed up to do the command d!refer @mentionyou')



                await ctx.send(file = discord.File(banneris) ,embed = inv_embed)                
                

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @refer_command.command(name ='open', aliases = ['o'])
    async def refer_open_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if registered_check[0]['refer'] == 'False':
                await ctx.send("Set Profile type for `PC`")
            else:
                current_count = int(registered_check[0]['refer'])
                if current_count > 0:
                    view = ConfirmCancel(ctx.author)
                    await ctx.send("Would you like to open a referral box?", view = view)
                    await view.wait()
                    if view.value == True:
                        current_count = int(registered_check[0]['refer'])
                        if current_count > 0:
                            referbox = str(current_count - 1)
                            await self.bot.db.execute(f'UPDATE registered SET refer = $1 WHERE player_id = $2', referbox, ctx.author.id) 

                            roll = random.randint(1,1000)


                            typed = ['banners', 'borders', 'avatar_borders']
                            stats = random.choice(typed)

                            if stats == 'banners':
                                types = 'Banner'
                                lists = 'banner_list'
                                name = 'banner_name'
                            elif stats == 'borders':
                                types = 'Border'
                                lists = 'border_list'
                                name = 'border_name'
                            else:
                                types = "Avatar Border"
                                name = 'banner_name'
                                lists = 'avaborder_list'


                            flists = str(registered_check[0][lists])
                            listbuy = self.listing(flists)
                            shop = 'True'


                            if (roll >= 0) and (roll < 50):
                                rank = 'D'
                                lbtrue = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE rank = $1 AND shop = $2', rank, shop)
                                slist = []
                                for i in range(len(lbtrue)):
                                    slist.append(lbtrue[i][f'{name}'])
                                item = random.choice(slist)


                            elif (roll >= 50) and (roll < 90):
                                rank = 'C'
                                lbtrue = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE rank = $1 AND shop = $2', rank, shop)
                                slist = []
                                for i in range(len(lbtrue)):
                                    slist.append(lbtrue[i][f'{name}'])

                                item = random.choice(slist)

                            
                            elif (roll >= 90) and (roll < 120):
                                rank = 'B'
                                lbtrue = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE rank = $1 AND shop = $2', rank, shop)
                                slist = []
                                for i in range(len(lbtrue)):
                                    slist.append(lbtrue[i][f'{name}'])
                                item = random.choice(slist)

                            elif (roll >= 120) and (roll < 140):
                                rank = 'A'    
                                lbtrue = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE rank = $1 AND shop = $2', rank, shop)
                                slist = []
                                for i in range(len(lbtrue)):
                                    slist.append(lbtrue[i][f'{name}'])

                                item = random.choice(slist)


                            elif (roll >= 140) and (roll < 145):
                                rank = 'S'
                                lbtrue = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE rank = $1 AND shop = $2', rank, shop)
                                slist = []
                                for i in range(len(lbtrue)):
                                    slist.append(lbtrue[i][f'{name}'])

                                item = random.choice(slist)


                            elif (roll >= 145) and (roll < 155):
                                rank =None
                                item = 'lootbox'
                                
                            elif (roll >= 155) and (roll < 255):
                                rank =None
                                item = '50 Dc'

                            elif (roll >= 255) and (roll < 500):
                                rank =None
                                item = '30 Dc'

                            elif (roll >= 500) and (roll < 1001):
                                rank =None
                                item = '15 Dc'

                            if rank == None:
                                if item == 'lootbox':
                                    rarity = 'SUPER RARE'
                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                elif item == '50 Dc':
                                    rarity = 'UNCOMMON'
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                elif item == '30 Dc':
                                    rarity = 'COMMON'
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 30 WHERE player_id = $1',  ctx.author.id)
                                elif item == '15 Dc':
                                    rarity = 'COMMON'
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 15 WHERE player_id = $1',  ctx.author.id)     

                                wish_embed_1 = discord.Embed(
                                    title = f'{ctx.author.name} is opening a Referral box!!',
                                    description = '',
                                    colour = color
                                )

                                bozo = 'https://media.tenor.com/KGwWGVz9-XQAAAAC/genshin-impact-wish.gif'

                                wish_embed_1.set_image(url=bozo)
                                wish_embed_1.set_footer(text = 'Inventory updated: -1 Referral Box')    
                                await ctx.send(embed = wish_embed_1)   
                                await asyncio.sleep(6)   

                                await ctx.send(f"{rarity} | You got **{item}** from the Referral Box! Try inviting more people to win something big!")                      
                                                       
                            else:
                                item = None
                                excluded_items = ['bronze','silver','gold','platinum','dominant','bronze2','silver2','gold2','platinum2','dominant2','clan','casual']
                                while item is None or item in excluded_items:
                                    item = random.choice(slist)

                                wish_embed_1 = discord.Embed(
                                    title = f'{ctx.author.name} is opening a Referral box!!',
                                    description = '',
                                    colour = color
                                )
                                if (rank == 'S') or (rank == 'A'):
                                    bozo = 'https://media.tenor.com/szDO6RwgxMMAAAAC/wish.gif'
                                else:
                                    bozo = 'https://media.tenor.com/JcMSVVkgfgMAAAAC/genshin-wish.gif'


                                wish_embed_1.set_image(url=bozo)
                                wish_embed_1.set_footer(text = 'Inventory updated: -1 Referral Box')


                                await ctx.send(embed = wish_embed_1)

                                await asyncio.sleep(6)
                                if item.lower() in listbuy:
                                    s = 1
                                    new_admins = ''
                                    admins_list = self.listing(flists)
                                    for admin in admins_list:
                                
                                        if admins_list.index(admin) == 0:
                                    
                                            if s == 0:
                                                
                                                admin = int(admin) + 1
                                                s += 1
                                            if admin == item.lower():
                                    
                                                s = 0
                                            new_admins += str(admin)
                                        

                                        else:
                                            if s == 0:
                                                
                                                admin = int(admin) + 1
                                                s+=1
                                            if admin == item.lower():
                                        
                                                s = 0

                                                            
                                            new_admins += f' {admin}'
                                        
                                
                                    await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)

                                else:
                                    
                                    itemcode = await id_generator()
                                    
                                    a = f'{item.lower()}'

                                    b = 1
                                    c = f"{itemcode}"
                                    if registered_check[0][lists] is None:
                                        admins_list = self.listing(flists)
                                        new_admins = f' {a}' + f' {b}' + f' {c}'
                                        await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)

                                    else:
                                        new_admins = str(flists) + f' {a}' + f' {b}' + f' {c}'
                                        await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)

                                if (rank == 'SS'):
                                    
                                    rank = '✪✪✪<:ss:1126547376719532112>✪✪✪'
                                elif (rank == 'S'):
                                    rarity = 'SUPER RARE'
                                    rank = '✦✦✦<:s_:1126546706721415320>✦✦✦'
                                elif (rank == 'A'):
                                    rarity = 'VERY RARE'
                                    rank = '★★<:a:1126546710332710943>★★'
                                elif (rank == 'B'):
                                    rarity = 'VERY RARE'
                                    rank = '★<:b:1126546712283066479>★'
                                elif (rank == 'C'):
                                    rarity = 'RARE'
                                    rank = '✲<:c:1126546716200542378>✲'
                                else:
                                    rarity = 'RARE'
                                    rank = '✕<:d:1126546717978919033>✕'              

                                await ctx.send(f"{rarity} | You got a {rank} **{types} {item}** from the Referral Box!")







                        else:
                            await ctx.send("You don't have enough referral boxes!")
                        
                    elif view.value == False:
                        await ctx.send("Cancelled.")
                    else:
                        await ctx.send("Timed Out.")
                else:
                    await ctx.send("You don't have enough referral boxes!")
                

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'transfer')
    async def transfer_command(self, ctx, member : discord.Member =None, newmember : discord.Member =None):
    
        profile = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if ctx.author.id in [0]:
            if (member == None) and (newmember == None):
                await ctx.send("d!transfer transferfrom totransfer")
            else:
                await self.bot.db.execute('DELETE FROM rank_system WHERE player_id = $1',newmember.id)
                await self.bot.db.execute('DELETE FROM casual WHERE player_id = $1', newmember.id)
                await self.bot.db.execute('DELETE FROM common_system WHERE player_id = $1', newmember.id)
                await self.bot.db.execute('DELETE FROM gamble WHERE player_id = $1', newmember.id)
                await self.bot.db.execute('DELETE FROM registered WHERE player_id = $1',newmember.id)
                await self.bot.db.execute('DELETE FROM wars WHERE player_id = $1', newmember.id)

                author_name = newmember.name
                await self.bot.db.execute('UPDATE rank_system SET player_id = $1, player_name = $2 WHERE player_id = $3', newmember.id, author_name, member.id)
                await self.bot.db.execute('UPDATE casual SET player_id = $1, player_name = $2 WHERE player_id = $3', newmember.id, author_name, member.id)

                await self.bot.db.execute('UPDATE common_system SET player_id = $1, player_name = $2 WHERE player_id = $3', newmember.id, author_name, member.id)
                await self.bot.db.execute('UPDATE gamble SET player_id = $1, player_name = $2 WHERE player_id = $3', newmember.id, author_name, member.id)
                await self.bot.db.execute(f'UPDATE registered SET player_id = $1 WHERE player_id = $2', newmember.id, member.id)
                await self.bot.db.execute(f'UPDATE wars SET player_id = $1 WHERE player_id = $2', newmember.id, member.id)

                await ctx.send('Succesfully transferred!')   
        
        else:
            await ctx.send("You can't use this command.")

def setup(bot):


    bot.add_cog(RegisteredCommands(bot))