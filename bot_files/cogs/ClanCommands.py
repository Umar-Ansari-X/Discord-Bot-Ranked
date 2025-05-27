import discord
from discord.ext import commands
import datetime
from datetime import timezone
import asyncpg
import asyncio
import json
import time
from pymongo import MongoClient
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from io import BytesIO
import math
import re
import random
import aiohttp
import string
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


color = 0x32006e

async def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




class Members(discord.ui.View):
    doc = 0
    current_page : int = 1
    sep : int = 9
    numbre : int = 0
    cluster = MongoClient("####")
    database = cluster['discord']
    collection = database["faction"]
    cd_mapping = commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.member)
    


    def listing(self, str1):
        if str1 is not None:
            list_str = str1.split()

            if list_str[0] == '':
                list_str.remove(list_str[0])

            list_num = []

            for e in list_str:
                list_num.append(e.strip())

            return list_num
        
        elif str1 is None:
            list1 = []

            return list1

    def listing1(self, str1 : str):
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

    async def send(self, ctx):
        if self.doc == 0:
            self.message = await ctx.send("**Generating...**")
        else:
            self.message = await ctx.send("**Generating...**", view = self)
        self.doc += 1
        await self.update_message(self.data[:self.sep], self.lb, self.stat,self.bot)

    async def create_embed(self, data,lb,stat,bot ):
        lb = self.lb            


        othernumbre = 0  
        tier = self.stat[0]
        slots = self.stat[1]
        clan_name = self.stat[2]

        if tier == 0:
            background = Image.open('clanbronze.png')
        elif tier == 1:
            background = Image.open('clanbronze.png')        
        elif tier == 2:
            background = Image.open('clansilver.png')
        elif tier == 3:
            background = Image.open('clangold.png')
        elif tier == 4:
            background = Image.open('clanplatinum.png')
        elif tier == 5:
            background = Image.open('clandiamond.png')
        elif tier == 6:
            background = Image.open('clandominant.png')

        background = background.convert("RGBA")

        guild = self.bot.get_guild(774883579472904222)
        role = guild.get_role(798548690860113982)        
        for i in data:
            othernumbre += 1
            if type(i) == str:
                pass
            else:
                author = await self.bot.fetch_user(i)
                member = guild.get_member(i)

            
        
            if type(i) == str:
                if (self.numbre < 18) and (slots < (self.numbre+ 1) ):
                    
                    profile = Image.open('lock.png')

                    xvalue = (othernumbre-1) % 3
                    yvalue = (othernumbre-1) // 3

                    if xvalue == 0:
                        ok = 18
                    elif xvalue == 1:
                        ok = 82
                    else:
                        ok = 147
                    if yvalue == 0:
                        okk = 18
                    elif yvalue == 1:
                        okk = 34
                    else:
                        okk = 50

                    profile = profile.resize((905,383))
                    profile = profile.convert("RGBA")


                    background.paste(profile, (ok+ (xvalue*905),okk + (yvalue*383)), profile)

                self.numbre += 1
                pass

            elif (member == None) or (author == None):
                
                self.collection.update_one({"_id": stat[2]}, {"$pull": {"members": i}})
                await self.bot.db.execute('UPDATE registered SET clan_1 = NULL, current_banner = NULL, title = NULL, banner_border = NULL, avatar_border = NULL WHERE player_id = $1', i)
                self.numbre += 1                
                         

            else:




                
                author_id = i

                registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', author_id)
                users = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', author_id)                
                commers = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', author_id)  
                items = ['banner','border','avaborder']
                if author_id == 0:
                    pass
                else:
                    for s in items:
                        if s == 'border':
                            current = 'banner_border'
                            lists = 'border_list'
                            name = 'border_name'
                        elif s == 'avaborder':
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
                            listbuy = self.listing1(flists)
                            if banner_name in listbuy:
                                pass
                            else:
                                await self.bot.db.execute(f'UPDATE registered SET {current} = NULL WHERE player_id = $1', author_id)

                if registered_check[0]['current_banner'] is None:
                    profile = Image.open("default.png")
                    
                else:                                                    
                    banner = await self.bot.db.fetch('SELECT * FROM banners WHERE banner_name = $1', registered_check[0]['current_banner'])
                    banneris = banner[0]["banner_place"]
                    
                    if banneris.lower().endswith(('.gif')):
                        profile = Image.open(banneris)
                        profile = profile.convert("RGBA")
                        profile = profile.resize((1440,608))
                    else:
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
                    borderis = borderis.convert("RGBA")
                if registered_check[0]['avatar_border'] is None:
                    
                    avaborderis = Image.open("profile2.png")
                    
                else:
                
                    avaborder = await self.bot.db.fetch('SELECT * FROM avatar_borders WHERE banner_name = $1', registered_check[0]['avatar_border'])
                    avaborderis = f'{avaborder[0]["avatar_place"]}'
                    avaborderis = Image.open(avaborderis)
                    avaborderis = avaborderis.convert("RGBA")
                player_clan_1 = ''
                font = ImageFont.truetype("BebasNeue-Regular.ttf", 160)
                font2 =  ImageFont.truetype("BebasNeue-Regular.ttf", 80)
                font3 =  ImageFont.truetype("BebasNeue-Regular.ttf", 40)                    

                name = f'{author.display_name}'
                if len(name) > 15:
                    name = name[:15] + ".."


                tata = BytesIO(await author.display_avatar.read())
                pfp = Image.open(tata)
                pfp.convert('RGBA')
                pfp = pfp.resize((300,300))
                mask_im = Image.new("L", pfp.size, 0)
                draw = ImageDraw.Draw(mask_im)
                draw.rounded_rectangle((0, 0, 300, 300), fill=255,width=3, radius=15)
                


                

                if role in member.roles:

                    h = registered_check[0]["embed_colour"]
                    if h is None:
                        tup = (255,255,255)
                        stroke = 0
                    else:
                        tup = tuple(int(h[t:t+2], 16) for t in (0, 2, 4))
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

                if registered_check[0]['refer'] == 'False':
                    gift = True
                    box = Image.open("giftbox.png")
                    box = box.resize((80,80))
                else:
                    gift = False
                    

                if des == 1:
                    profile.paste(design, (20,0), design) 
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
                draw.text((373, 240), text=titleis, fill='black', font=font2)
                blurred = blurred.filter(ImageFilter.BoxBlur(10))
                profile.paste(blurred,blurred)
                draw2 = ImageDraw.Draw(profile)
                draw2.text((373, 240), titleis, tup, font = font2,stroke_width=stroke, stroke_fill='black')
                blurred = Image.new('RGBA', profile.size)
                draw = ImageDraw.Draw(blurred)
                draw.text((52, 353), text=player_clan_1, fill='black', font=font3)
                blurred = blurred.filter(ImageFilter.BoxBlur(7))
                profile.paste(blurred,blurred)
                draw5 = ImageDraw.Draw(profile)
                draw5.text((52, 353), player_clan_1, tup, font = font3,stroke_width=stroke, stroke_fill='black')

                xvalue = (othernumbre-1) % 3
                yvalue = (othernumbre-1) // 3

                if xvalue == 0:
                    ok = 18
                elif xvalue == 1:
                    ok = 82
                else:
                    ok = 147
                if yvalue == 0:
                    okk = 18
                elif yvalue == 1:
                    okk = 34
                else:
                    okk = 50

                profile = profile.resize((905,383))
                profile = profile.convert("RGBA")
            
                background.paste(profile, (ok+ (xvalue*905),okk + (yvalue*383)), profile)

                self.numbre += 1

        if self.numbre > 18:
            clan_name = data[0]
            clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(clan_name.title()))

            date_created = clan[0]['date_created']
            members = list(self.collection.find( {"_id": clan_name.title()}, {"_id": 0, "members": 1}))

            leaders = clan[0]['leaders']

            leaders_list = self.listing(leaders)

            leaders_str = ''

            if leaders_list is not None:
                for leader in leaders_list:
                    if leaders_list.index(leader) == 0:
                        leaders_str += f'<@{leader}>'

                    else:
                        leaders_str += f', <@{leader}>'

            same = clan[0]['clan_name']
            same = same.lower()
            embed = discord.Embed(
                title = f'{to_title(same)} clan',
                description = f'Created on {date_created}',
                colour = color
            )
            
            if clan[0]['avatar']:
                clanpfp = clan[0]['avatar']
            else:
                clanpfp = 'clandefault.png'

            embed.set_thumbnail(url=f"attachment://{clanpfp}")
                        
            if leaders_str == '':
                embed.add_field(name = 'Leader(s):', value = 'None')

            else:
                embed.add_field(name = 'Leader(s):', value = leaders_str)
            memberStr = ""
            for i in members[0]['members']:
                member  = await self.bot.fetch_user(i)
                memberStr += f"`{member.name}` "
            embed.add_field(name = 'Members: ', value = memberStr, inline=False)
            dfile = None
            return embed,dfile,clanpfp
        else:
            
            bytes = BytesIO()
            rgb_img = background.convert("RGBA")
            rgb_img = rgb_img.resize((1440,608))
            rgb_img.save(bytes, format="PNG", quality=25)
            bytes.seek(0)
            dfile = discord.File(bytes, filename= "rgb_img.png")
            embed = None
            clanpfp = None

            return embed,dfile,clanpfp

    async def update_message(self,data, lb, stat,bot):
        
        
        embed,dfile,clanpfp = await self.create_embed( data, lb, stat,bot)
        if dfile == None:
            self.update_buttons()
            await self.message.edit(content='' ,embed=embed,attachments=[],file=discord.File(clanpfp), view=self)
            
        else:
            self.update_buttons()
            await self.message.edit(content='',attachments=[],file=dfile,embed=None,  view=self)
            

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

    def updated_buttons(self):

        self.first_page_button.disabled = True
        self.prev_button.disabled = True
        self.first_page_button.style = discord.ButtonStyle.gray
        self.prev_button.style = discord.ButtonStyle.gray

        self.last_page_button.disabled = True
        self.next_button.disabled = True
        self.last_page_button.style = discord.ButtonStyle.gray
        self.next_button.style = discord.ButtonStyle.gray


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
        

        interaction.message.author = interaction.user
        bucket = self.cd_mapping.get_bucket(interaction.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return await interaction.response.send_message(f"Slow down.. Try again in **{round(retry_after,1)}s**", ephemeral=True)

        await interaction.response.defer()
        self.updated_buttons()
        await self.message.edit(view=self)
        self.current_page = 1
        self.numbre = 0

        await self.update_message(self.get_current_page_data(), self.lb,self.stat,self.bot)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple,emoji='🔹')
    async def prev_button(self,  button: discord.ui.Button, interaction:discord.Interaction):
        

        interaction.message.author = interaction.user
        bucket = self.cd_mapping.get_bucket(interaction.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return await interaction.response.send_message(f"Slow down.. Try again in **{round(retry_after,1)}s**", ephemeral=True)

        await interaction.response.defer()
        self.updated_buttons()
        await self.message.edit(view=self)

        delete = 18
        if int(len(self.data)) < self.sep * self.current_page:
            new = int(len(self.data)) - self.sep * (self.current_page -1)
            delete = new + 9
        self.current_page -= 1
        self.numbre -= delete
        await self.update_message(self.get_current_page_data(), self.lb, self.stat,self.bot)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple,emoji='🔹')
    async def next_button(self, button: discord.ui.Button, interaction:discord.Interaction):

        interaction.message.author = interaction.user
        bucket = self.cd_mapping.get_bucket(interaction.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return await interaction.response.send_message(f"Slow down.. Try again in **{round(retry_after,1)}s**", ephemeral=True)

        await interaction.response.defer()    
        self.updated_buttons()
        await self.message.edit(view=self)
        self.current_page += 1
        await self.update_message(self.get_current_page_data(), self.lb, self.stat,self.bot)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red,emoji='♦️')
    async def last_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        

        interaction.message.author = interaction.user
        bucket = self.cd_mapping.get_bucket(interaction.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return await interaction.response.send_message(f"Slow down.. Try again in **{round(retry_after,1)}s**", ephemeral=True)

        await interaction.response.defer()
        self.updated_buttons()
        await self.message.edit(view=self)
        self.current_page = math.ceil(len(self.data) / self.sep)
        self.numbre = (self.sep * (self.current_page -1))
        await self.update_message(self.get_current_page_data(), self.lb, self.stat,self.bot)


class Career(discord.ui.View):
    current_page : int = 1
    sep : int = 8
    numbre : int = 0
    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb, self.stat)

    async def create_embed(self, data,lb,stat ):
        lb = self.lb    

        careerStr = ""
        for i in data:
            
            careerStr = ""
            for i in data:
                careerStr  += f'{i}\n'
        
        clan_name = lb[0]['_id']
        em = discord.Embed(
        title = f"{clan_name.title()} Career",
        description = f"{clan_name.title()}'s past wars will be shown here.\n\n{careerStr}",
        colour = color
        )

        
        em.set_thumbnail(url=f"attachment://{stat}")
        em.set_footer(text=f'Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')
        return em

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



class LPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 1
    numbre : int = 0
    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb, self.stat)

    async def create_embed(self, data,lb,stat ):
        lb = self.lb
        stat = self.stat


        title = 'Clan Shop'
        desc = ""
        lb_embed = discord.Embed(
            title = title,
            description = desc,
            colour = color
        )

        othernumbre = 0   
        for i in data:
            othernumbre += 1

                
            banneris = lb[self.numbre]['item_place']
            profile = Image.open(banneris)
            banners =lb[self.numbre]["item_name"]
            name = 'Clan Name'
            if lb[self.numbre]["shop"] == 'False':
                owned = 'No one'
            else:
                clan = lb[self.numbre]["clan"]
                owned = clan.title()
            lb_embed.add_field(name = f'{lb[self.numbre]["item_name"].title()} ', value = f'Cost | x**{lb[self.numbre]["price"]} cc**\nOwned by | **{owned}**')

            if banners == 'bluelock':
                profile = Image.open("xbluelock.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("Evogria.otf", 80)
                tup = (6, 0, 189)
                cord = (50, 490)

                draw = ImageDraw.Draw(profile)
                draw.text(cord, name, tup, font = font, stroke_width=5, stroke_fill=(181, 248, 255))       

            elif banners == 'mha':

                profile = Image.open("xmha.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("mhafont.otf", 90)
                tup = (255, 255, 255)
                cord = (50, 50)

                name = 'CLAN NAME'

                draw = ImageDraw.Draw(profile)
                left, top, right, bottom = draw.textbbox(cord, name, font=font)
                draw.rectangle((left-5, top-5, right+5, bottom+5), fill="red")
                draw.text(cord, name, tup, font = font)    

            elif banners == 'fireforce':
                profile = Image.open("xfireforce.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("Blazed.ttf", 70)
                tup = (255, 219, 128)
                cord = (100, 50)


                draw = ImageDraw.Draw(profile)
                draw.text(cord, name, tup, font = font, stroke_fill=(255, 51, 15),stroke_width=3)

            elif banners == 'sololevelling':
                profile = Image.open("jinwooteam.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("SoloLevelDemo.otf", 120)
                tup = (0, 0, 0)
                cord = (20, 475)
                name = 'Clan Name'

                draw = ImageDraw.Draw(profile)
                draw.text(cord, name, tup, font = font, stroke_fill=(154, 110, 255),stroke_width=5)

            elif banners == 'dunk':

                profile = Image.open("dunk.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("Basketball.otf", 90)
                tup = (255, 255, 255)
                cord = (50, 100)
                name = 'CLAN NAME'

                draw = ImageDraw.Draw(profile)
                draw.text(cord, name, tup, font = font, stroke_fill='black',stroke_width=2)  

            elif banners == 'marvel':

                profile = Image.open("xmarvel.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("Marvel-Regular.ttf", 100)
                tup = (255, 255, 255)
                cord = (720, 530)
                
                name = 'CLAN NAME'
                draw = ImageDraw.Draw(profile)
                left, top, right, bottom = draw.textbbox(cord, name, font=font, anchor='mm')
                draw.rectangle((left-5, top-5, right+5, bottom+5), fill="red")
                draw.text(cord, name, tup, font = font, anchor='mm')  
                
            elif banners == 'bleach':

                profile = Image.open("xbleach.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("FontBleach.ttf", 70)
                tup = (255, 255, 255)
                cord = (720, 530)
                name = 'CLAN NAME'
                draw = ImageDraw.Draw(profile)
                draw.text(cord, name, tup, font = font, stroke_fill=(3, 12, 46),stroke_width=10, anchor='mm')         

            elif banners == 'genshin':

                profile = Image.open("genshin.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("genshin.ttf", 80)
                tup = (255, 204, 233)
                cord = (720, 530)
                name = 'CLAN NAME'
                draw = ImageDraw.Draw(profile)
                draw.text(cord, name, tup, font = font, stroke_fill=(38, 38, 38),stroke_width=5, anchor='mm')     

            elif banners == 'peakyblinders':

                profile = Image.open("oppenheimer.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("Metropolis-Bold.ttf", 90)
                tup = (255, 208, 128)
                cord = (720, 530)
                name = 'CLAN NAME'
                draw = ImageDraw.Draw(profile)
                draw.text(cord, name, tup, font = font, anchor='mm')   

            elif banners == 'onepiece':
                profile = Image.open("xonepiece.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("one piece font.ttf", 110)
                tup = (255, 255, 255)
                cord = (1430, 590)

                name = 'CLAN NAME'
                draw = ImageDraw.Draw(profile)
                draw.text(cord, name, tup, font = font, stroke_fill=(42, 163, 250),stroke_width=6, anchor='rs')  
            elif banners == 'demonslayer':
                profile = Image.open("xdemonslayer.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("bloodcrowc.ttf", 110)
                tup = (255, 204, 233)
                cord = (1390, 560)


                draw = ImageDraw.Draw(profile)
                draw.text(cord, name, tup, font = font, stroke_fill='white',stroke_width=2, anchor='rs')  

            elif banners == 'girlscafe':
                profile = Image.open("girlscafe.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("barbie.ttf", 110)
                tup = (0, 0, 0)
                cord = (1390, 560)


                draw = ImageDraw.Draw(profile)
                draw.text(cord, name, tup, font = font, stroke_fill=(255, 255, 255),stroke_width=2, anchor='rs')  


            elif banners == 'jjk':
                profile = Image.open("xjjk.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("Jujutsu Kaisen.ttf", 110)
                tup = (0, 0, 0)
                cord = (1390, 560)



                draw = ImageDraw.Draw(profile)
                draw.text(cord, name, tup, font = font, stroke_fill='yellow',stroke_width=2, anchor='rs') 

            elif banners == 'akatsuki':

                profile = Image.open("xakatsuki.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("njnaruto.ttf", 80)
                tup = (255, 255, 255)
                cord = (720, 530)


                draw = ImageDraw.Draw(profile)
                draw.text(cord, name, tup, font = font, stroke_fill='black',stroke_width=8, anchor='mm')  
    
            elif banners == 'paranoia':

                profile = Image.open("paranoia.png")
                profile.convert('RGBA')  
                font = ImageFont.truetype("Wild2GhixmNcBold-3m5z.ttf", 120)
                tup = (255, 255, 255)
                cord = (720, 530)


                draw = ImageDraw.Draw(profile)
                draw.text(cord, name, tup, font = font, stroke_fill=(27, 27, 33),stroke_width=8, anchor='mm')  


            self.numbre = self.numbre + 1

        bytes = BytesIO()
        profile.save(bytes, format="PNG")
        bytes.seek(0)
        

        lb_embed.set_image(url=f"attachment://profile.png")
        dfile = discord.File(bytes,"profile.png")
        lb_embed.set_footer(text = f'Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')

        return lb_embed, dfile

    async def update_message(self,data, lb, stat):
        self.update_buttons()
        embed,dfile = await self.create_embed(data, lb, stat)
        if dfile == None:
            await self.message.edit(embed=embed, view=self)
        else:
            await self.message.edit(file=dfile, embed=embed, view=self)

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

        await self.update_message(self.get_current_page_data(), self.lb, self.stat)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple,emoji='🔹')
    async def prev_button(self,  button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()

        delete =  int(len(self.data)) - self.sep * self.current_page
        delete = 2
        if int(len(self.data)) < self.sep * self.current_page:
            new = int(len(self.data)) - self.sep * (self.current_page -1)
            delete = new + 1
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
                       style=discord.ButtonStyle.red, emoji='♦️')
    async def last_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page = math.ceil(len(self.data) / self.sep)
        self.numbre = (self.sep * (self.current_page -1))
        await self.update_message(self.get_current_page_data(), self.lb, self.stat)

class ClanProfile(discord.ui.View):
    def __init__(self, member : discord.Member):
        super().__init__(timeout = 60)

        self.value = None
        self.member = member

    @discord.ui.button(label = "", style = discord.ButtonStyle.blurple, emoji = "👥" )
    async def confirm_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = 'True'
        self.stop()

        for i in self.children:
            i.disabled = True
        try:
            await interaction.response.edit_message(view=self)
        except discord.errors.InteractionResponded:
            return
        
    @discord.ui.button(label = "", style = discord.ButtonStyle.red, emoji = "🎯" )
    async def stat_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = 'Stuff'
        self.stop()
                
        for i in self.children:
            i.disabled = True
        try:
            await interaction.response.edit_message(view=self)
        except discord.errors.InteractionResponded:
            return
        
    @discord.ui.button(label = "", style = discord.ButtonStyle.green, emoji = "📁" )
    async def carrer_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = 'False'
        self.stop()
                
        for i in self.children:
            i.disabled = True
        try:
            await interaction.response.edit_message(view=self)
        except discord.errors.InteractionResponded:
            return
        

        

    async def interaction_check(self, interaction : discord.Interaction):
        return interaction.user == self.member
                                        
    async def on_timeout(self):
        self.value = None

        for i in self.children:
            i.disabled = True

def to_title(string):
    regex = re.compile("[a-z]+('[a-z]+)?", re.I)
    return regex.sub(lambda grp: grp.group(0)[0].upper() + grp.group(0)[1:].lower(),
                    string)
async def get_clan_data():
    with open("clans.json", "r") as f:
        clans = json.load(f)
    
    return clans

class CPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 6
    numbre : int = 0
    sort_option = "wins"
    change = 'no'

    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb, self.bot)

    def listing(self, str1):
        if str1 is not None:
            list_str = str1.split()

            if list_str[0] == '':
                list_str.remove(list_str[0])

            list_num = []

            for e in list_str:
                list_num.append(e.strip())

            return list_num
        
        elif str1 is None:
            list1 = []

            return list1
    async def calculate_winrate(self, lb):
        winrate_data = []

        for faction in lb:
            played = faction['played']
            points = faction['points']
            winrate = round(points / played * 100, 2) if played > 0 else 0.0
            winrate_data.append((winrate, faction))

        sorted_lb = sorted(winrate_data, key=lambda x: x[0], reverse=True)

        return [faction for _, faction in sorted_lb]
    
    async def create_embed(self, data,lb,bot):
        lb = self.lb
        bot = self.bot

        lb_embed = discord.Embed(
            title = 'Clan Leaderboard',
            description = 'Click the buttons to change pages.',
            colour = color
        )
        if self.change == 'no':
            pass
        else:
            self.numbre = 0

        if self.sort_option == 'wins':
            for i in data:
                scoreStr = f"**Wins 》 **{lb[self.numbre]['points']}\n**Matches 》 **{lb[self.numbre]['played']}"
                name = lb[self.numbre]['clan_name']
                name = name.lower()
                lb_embed.add_field(name = f"{self.numbre+1}# {to_title(name)} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1

        elif self.sort_option == 'new':
            lb_embed = discord.Embed(
                title = 'Season Leaderboard',
                description = 'Click the buttons to change pages.',
                colour = color
            )

            for i in data:
                scoreStr = f"**Season Wins 》 **{lb[self.numbre]['event']}\n**Matches 》 **{lb[self.numbre]['event_played']}"
                name = lb[self.numbre]['clan_name']
                name = name.lower()
                lb_embed.add_field(name = f"{self.numbre+1}# {to_title(name)} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1                
                
        elif self.sort_option == 'played':
            lb = await bot.db.fetch('SELECT * FROM clans ORDER BY played DESC')
            for i in data:
                scoreStr = f"**Matches 》 **{lb[self.numbre]['played']}\n**Wins 》 **{lb[self.numbre]['points']}"
                name = lb[self.numbre]['clan_name']
                name = name.lower()
                lb_embed.add_field(name = f"{self.numbre+1}# {to_title(name)} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1            
            
        elif self.sort_option == 'winrate':
            lb = await bot.db.fetch('SELECT * FROM clans')
            lb = await self.calculate_winrate(lb)

            for i in data:
                winrate = round(lb[self.numbre]['points'] / lb[self.numbre]['played'] * 100, 2) if lb[self.numbre]['played'] > 0 else 0.0
                scoreStr = f"**Winrate 》 **{winrate}%\n**Wins 》 **{lb[self.numbre]['points']}\n**Matches 》 **{lb[self.numbre]['played']}"
                name = lb[self.numbre]['clan_name']
                name = name.lower()
                lb_embed.add_field(name=f"{self.numbre + 1}# {to_title(name)}", value=f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1   

        self.change = 'no'

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

    @discord.ui.select(placeholder="Sort by..", min_values=1, max_values=1,
                       options=[
                           discord.SelectOption(label="Wins", value="wins"),
                           discord.SelectOption(label="Matches Played", value="played"),
                           discord.SelectOption(label="Win Rate", value="winrate"),
                           
                       ])
    async def sort_dropdown(self, select: discord.ui.Select, interaction: discord.Interaction):
        await interaction.response.defer()
        self.sort_option = select.values[0]
        self.current_page = 1
        self.change = 'yes'
        await self.update_message(self.get_current_page_data(), self.lb,self.bot)
        
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

class ConfirmChange(discord.ui.View):
    def __init__(self, member : discord.Member):
        super().__init__(timeout = 15)

        self.value = None
        self.member = member

    @discord.ui.button(label = "Win Score", style = discord.ButtonStyle.green, emoji = "⚔" )
    async def confirm_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = True
        self.stop()
                
        for i in self.children:
            i.disabled = True

        await interaction.response.edit_message(view = self)
            
    @discord.ui.button(label = "Number of Players", style = discord.ButtonStyle.red, emoji = "✨" )
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

class ClanCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = MongoClient("####")
        database = self.cluster['discord']
        self.collection = database["faction"]
        self.faction = database["wars"]

    def find_matching_name(self, pokemon1, allnames):

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

    def listingt(self, str1 : str):
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

    def listing(self, str1 : str):
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

    def limit(self, seq : list, lim : int):
        if seq is not None:   
            if len(seq) < lim:
                return seq

            elif len(seq) >= lim:
                return seq[:lim:]
    

    @commands.command(name = 'clans')
    async def clans_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

  
        if user_ban_list:
            await ctx.send('You are banned from the bot.')
            return

        if registered_check:

            lb = await self.bot.db.fetch('SELECT * FROM clans ORDER BY points DESC')

            data = []
            for faction in lb:
                data.append(faction['clan_name'])
   
    
            pagination_view = CPaginationView()
            pagination_view.data = data
            pagination_view.lb = lb
            pagination_view.bot = self.bot
   
            await pagination_view.send(ctx)

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.group(name = 'clan', aliases = ['cl'], invoke_without_command = True)
    async def clan_command(self, ctx, *, clan_name = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if clan_name is None:
            pass
        else:
            clan_name = clan_name.replace("’", "'")
        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

  
        if user_ban_list:
            await ctx.send('You are banned from the bot.')
            return

        else:
            if registered_check:

                if clan_name is None:
                    em1 = discord.Embed(
                        title = 'Clans [Aliases: cl]',
                        description = 'Commands related to clans *(Page 1/2)*:',
                        colour = color
                    )

                    em1.add_field(name = 'd!clans', value = 'View the top 8 official clans, their rankings and points.',inline=False)
                    em1.add_field(name = 'd!clan [clan name]', value = 'View the info about a clan.')

                    em1.add_field(name = 'd!clan add|a [clan name]', value = 'Add a new clan.*(Admin exclusive)*',inline=False)

                    em1.add_field(name = 'd!clan remove|r [clan name]', value = 'Remove an exisiting clan. Removing an existing clan resets their points to zero.*(Admin exclusive)*',inline=False)

                    em1.add_field(name = 'd!clan givepoints|givep|gp [amount] [clan name]', value = 'Give any amount of points to a clan.*(Admin exclusive)*',inline=False)

                    em1.add_field(name = 'd!clan takepoints|takep|tp [amount] [clan name]', value = 'Take away any amount of points from a clan. Taking away more points than the clan has will result in the clan getting negative points.*(Admin exclusive)*',inline=False)

                    em1.add_field(name = 'd!clan memberenable|me [channel]', value = 'Enable a channel to log member joins and leaves.*(Admin exclusive)*',inline=False)

                    em1.add_field(name = 'd!clan memberadd|ma [mention] [clan name]', value = 'Add a new member to a clan and log it.*(Admin and leader exclusive)*',inline=False)


                    await ctx.send(embed = em1)

                else:
                    clans = await self.bot.db.fetch('SELECT * FROM clans')
                    allclans = []
                    for i in clans:
                        allclans.append(i['clan_name'])

                    clan_name = self.find_matching_name(clan_name.title(), allclans)


                    clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(clan_name.title()))
                    if clan:
                        banners = clan[0]['items']

                        if banners is None:
                            
                            profile = Image.open("clandb.png")
                            profile.convert('RGBA')
                            font = ImageFont.truetype("Pacifico-Regular.ttf", 120)
                            tup = (255,255,255)
                            cord = (720, 500)

                            name = to_title(clan_name)

                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font,anchor="mm")

                        elif banners == 'bluelock':

                            profile = Image.open("xbluelock.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("Evogria.otf", 80)
                            tup = (6, 0, 189)
                            cord = (50, 490)

                            name = to_title(clan_name)

                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font, stroke_width=5, stroke_fill=(181, 248, 255))       

                        elif banners == 'mha':

                            profile = Image.open("xmha.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("mhafont.otf", 90)
                            tup = (255, 255, 255)
                            cord = (50, 50)
                            name = clan_name.upper()

                            draw = ImageDraw.Draw(profile)
                            left, top, right, bottom = draw.textbbox(cord, name, font=font)
                            draw.rectangle((left-5, top-5, right+5, bottom+5), fill="red")
                            draw.text(cord, name, tup, font = font)    

                        elif banners == 'genshin':

                            profile = Image.open("genshin.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("genshin.ttf", 80)
                            tup = (255, 204, 233)
                            cord = (720, 530)
                            name = clan_name.upper()
                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font, stroke_fill=(38, 38, 38),stroke_width=5, anchor='mm')     

                        elif banners == 'girlscafe':
                            profile = Image.open("girlscafe.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("barbie.ttf", 110)
                            tup = (0, 0, 0)
                            cord = (1390, 560)

                            name = to_title(clan_name)


                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font, stroke_fill=(255, 255, 255),stroke_width=2, anchor='rs')  


                        elif banners == 'fireforce':
                            profile = Image.open("xfireforce.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("Blazed.ttf", 70)
                            tup = (255, 219, 128)
                            cord = (100, 50)

                            name = to_title(clan_name)

                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font, stroke_fill=(255, 51, 15),stroke_width=3)


                        elif banners == 'dunk':

                            profile = Image.open("dunk.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("Basketball.otf", 90)
                            tup = (255, 255, 255)
                            cord = (50, 100)
                            name = clan_name.upper()

                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font, stroke_fill='black',stroke_width=2)  

                        elif banners == 'bleach':

                            profile = Image.open("xbleach.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("FontBleach.ttf", 100)
                            tup = (255, 255, 255)
                            cord = (720, 530)
                            
                            name = clan_name.upper()
                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font, stroke_fill=(3, 12, 46),stroke_width=10, anchor='mm')   



                        elif banners == 'marvel':

                            profile = Image.open("xmarvel.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("Marvel-Regular.ttf", 100)
                            tup = (255, 255, 255)
                            cord = (720, 530)
                            
                            name = clan_name.upper()
                            draw = ImageDraw.Draw(profile)
                            left, top, right, bottom = draw.textbbox(cord, name, font=font, anchor='mm')
                            draw.rectangle((left-5, top-5, right+5, bottom+5), fill="red")
                            draw.text(cord, name, tup, font = font, anchor='mm')  

                        elif banners == 'peakyblinders':

                            profile = Image.open("oppenheimer.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("Metropolis-Bold.ttf", 70)
                            tup = (255, 208, 128)
                            cord = (720, 530)
                            name = clan_name.upper()
                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font, anchor='mm')  

                        elif banners == 'sololevelling':
                            profile = Image.open("jinwooteam.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("SoloLevelDemo.otf", 120)
                            tup = (0, 0, 0)
                            cord = (20, 475)
                            name = to_title(clan_name)

                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font, stroke_fill=(154, 110, 255),stroke_width=5)

                        elif banners == 'onepiece':
                            profile = Image.open("xonepiece.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("one piece font.ttf", 110)
                            tup = (255, 255, 255)
                            cord = (1430, 590)

                            name = to_title(clan_name)
                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font, stroke_fill=(42, 163, 250),stroke_width=6, anchor='rs')  
                        elif banners == 'demonslayer':
                            profile = Image.open("xdemonslayer.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("bloodcrowc.ttf", 110)
                            tup = (0, 0, 0)
                            cord = (1390, 560)

                            name = to_title(clan_name)

                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font, stroke_fill='white',stroke_width=2, anchor='rs')  

                        elif banners == 'jjk':
                            profile = Image.open("xjjk.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("Jujutsu Kaisen.ttf", 110)
                            tup = (0, 0, 0)
                            cord = (1390, 560)

                            name = to_title(clan_name)


                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font, stroke_fill='yellow',stroke_width=2, anchor='rs') 

                        elif banners == 'akatsuki':

                            profile = Image.open("xakatsuki.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("njnaruto.ttf", 80)
                            tup = (255, 255, 255)
                            cord = (720, 530)

                            name = to_title(clan_name)

                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font, stroke_fill='black',stroke_width=8, anchor='mm')  
                         
                        elif banners == 'paranoia':

                            profile = Image.open("paranoia.png")
                            profile.convert('RGBA')  
                            font = ImageFont.truetype("Wild2GhixmNcBold-3m5z.ttf", 120)
                            tup = (255, 255, 255)
                            cord = (720, 530)

                            name = to_title(clan_name)

                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font, stroke_fill=(27, 27, 33),stroke_width=8, anchor='mm')          

                        else:
                            profile = Image.open("clandb.png")
                            profile.convert('RGBA')
                            font = ImageFont.truetype("Pacifico-Regular.ttf", 120)
                            tup = (255,255,255)
                            cord = (720, 530)

                            name = to_title(clan_name)

                            draw = ImageDraw.Draw(profile)
                            draw.text(cord, name, tup, font = font,anchor="mm")
                        
                        
        

                        bytes = BytesIO()
                        profile.save(bytes, format="PNG")
                        bytes.seek(0)
                        dfile = discord.File(bytes, filename= "profile.png")
                        view = ClanProfile(ctx.author)

                        embed_msg = await ctx.send(file = dfile, view = view)
                        await view.wait()
                        if view.value == 'True':

                            members = list(self.collection.find( {"_id": clan_name.title()}, {"_id": 1, "members": 1}))
                            data = members[0]['members']
                            
                            stat = None
                            lb = await self.bot.db.fetch('SELECT * FROM registered WHERE clan_1 = $1', str(clan_name.title()))
                            stat = [clan[0]['tier']]


                            stat.append(clan[0]['slots'])
                            stat.append(str(clan_name.title()))
                            num = 19 - len(data) 
                            while num > 0:       
                                data.append(clan_name)  
                                num -= 1
                                if num ==0:
                                    break                   
                            pagination_view = Members()
                            pagination_view.data = data
                            pagination_view.lb = lb
                            pagination_view.stat = stat
                            pagination_view.bot = self.bot
                            await pagination_view.send(ctx)

                        elif view.value == 'False':
                            if self.collection.count_documents({ "_id": clan_name.title(), "career":{"$exists":True, "$size":0}}, limit = 1):
                                em = discord.Embed(
                                title = f"{clan_name.title()} Career",
                                description = f"{clan_name.title()}'s past wars will be shown here.",
                                colour = color
                                )

                                if clan[0]['avatar']:
                                    clanpfp = clan[0]['avatar']
                                else:
                                    clanpfp = 'clandefault.png'
                                em.set_thumbnail(url=f"attachment://{clanpfp}")
                                
                                em.add_field(name = 'This Clan has no past records', value = "War with other Clans")
                                
                                await ctx.send(embed = em)

                            else:
                                career = list(self.collection.find( {"_id": clan_name.title()}, {"_id": 1, "career": 1}))

                                data = career[0]['career']

                                if clan[0]['avatar']:
                                    stat = clan[0]['avatar']
                                else:
                                    stat = 'clandefault.png'                                
                                
                                lb = career
                                stats = None
                    
                                pagination_view = Career()
                                pagination_view.data = data
                                pagination_view.lb = lb
                                pagination_view.stat = stat
                                pagination_view.stats = stats
                                await pagination_view.send(ctx)

                        elif view.value == 'Stuff':

                            avatar = clan[0]['avatar']
                            if avatar is None:
                                pfp = Image.open('clandefault.png')
                            else:
                                pfp = Image.open(avatar)


                            #wins
                            win = clan[0]['points']
                            dc = clan[0]['dc']
                            cc = clan[0]['cc']

                            #matches
                            matche = clan[0]['played']

                            #wr
                            if int(clan[0]['played']) ==0:
                                wrr = '0%'
                            else:
        
                                w = (int(win)/int(matche))*100
                                wrr = f'{round(w, 2)}%'                
                            #position
                            clans = await self.bot.db.fetch('SELECT clan_name FROM clans ORDER BY points DESC')
                            clans_position = []
                            for i in range(len(clans)):
                                clans_position.append(clans[i]['clan_name']) 
                            position = self.cardinal(clans_position.index(clan[0]['clan_name']) + 1)

                            #streak

                            streak = clan[0]['streak']

                            slots = clan[0]['slots']


                            #members
                            members = list(self.collection.find( {"_id": clan_name.title()}, {"_id": 0, "members": 1}))
                            memberss = len(members[0]["members"])


                            #total rnkd

                            em = discord.Embed(
                            title = f"{clan_name.title()} Stats",
                            description = f"**Wars** » {matche}\n**Wins** » {win}\n**Position** » {position} \n**Win Rate** » {wrr} \n**Streak** » {streak} \n**Members** » {memberss}\n**Slots Unlocked** » {slots}\n**Cc** » {cc}",
                            colour = color
                            )
                            if clan[0]['avatar']:
                                clanpfp = clan[0]['avatar']
                            else:
                                clanpfp = 'clandefault.png'
                            em.set_thumbnail(url=f"attachment://{clanpfp}")
                            await ctx.send(embed = em, file = discord.File(clanpfp))
                            
                        else:
                            pass

                    else:
                        await ctx.send('That clan is not officially registered!')

            else:
                await ctx.send('You have not registered yet! Use `d!start` to register.')
        
    @clan_command.command(name = 'set', aliases = ['s'])
    async def clan_set_command(self, ctx, banner_name :str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        clan_name = registered_check[0]['clan_1']

        if registered_check:
            if clan_name:

                if (banner_name is None):
                    em = discord.Embed(
                        title = 'Clan',
                        description = '*Set your clan profile.**\n\nd!clan set [profile name]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                    if not clan:
                        await ctx.send(f'{clan_name.title} is not a registered clan.')

                    else:


                        admins = clan[0]['leaders']
                        admins_list = self.listing(admins)

                        if int(ctx.author.id) in admins_list:

                            banners = await self.bot.db.fetch(f'SELECT * FROM clan_shop')
                            banner_list = []
                            for i in range(len(banners)):
                                banner_list.append(banners[i]['item_name'])

                            if banner_name.lower() in banner_list:    
                                pass
                            else:
                                await ctx.send("Profile doesn't exist.")
                                return 

                            banner = await self.bot.db.fetch('SELECT * FROM clan_shop WHERE item_name = $1', banner_name.lower()) 
                            
                            if banner[0]['shop'] =='True':
                                await ctx.send("Already owned by another clan.")
                                return
                            else:
                                pass

                            if int(banner[0]['price']) > int(clan[0]['cc']):
                                await ctx.send("Your clan doesn't have enough cc.")
                                return
                            else:
                                pass
                            current_name = clan[0]['items']
                            if current_name == None:
                                pass
                            else:
                                shop = 'False'
                                await self.bot.db.execute(f'UPDATE clan_shop SET shop = $1, clan = NULL WHERE item_name = $2', shop, current_name.lower())

                            new_admins = banner_name.lower()
                            reqcc = int(banner[0]['price'])
                            await self.bot.db.execute(f'UPDATE clans SET items = $1, cc = cc - {reqcc} WHERE clan_name = $2', new_admins, clan_name.title())
                            shop = 'True'
                            clan = clan_name.title()

                            await self.bot.db.execute(f'UPDATE clan_shop SET shop = $1, clan = $2  WHERE item_name = $3', shop,clan, banner_name.lower())
                            await ctx.send(f'Set as {banner_name.title()}')        

                        else:
                                await ctx.send("You don't have permission to use this command")

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @clan_command.command(name = 'add', aliases = ['a'])
    async def clan_add_command(self, ctx, leader_name1 : discord.Member = None, *, clan_name = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if clan_name is None:
            pass
        else:
            clan_name = clan_name.replace("’", "'")
        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if int(ctx.author.id) in admins_list:
                if (clan_name is None) or (leader_name1 is None):
                    em = discord.Embed(
                        title = 'Clan',
                        description = '**Add a new clan.**\n\nd!clan add [clan name]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    clans = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(clan_name.title()))
                    if clans:
                        await ctx.send('That clan is already registered!')

                    else:
                        leader_name = leader_name1.id
                        faction_name = str(clan_name.title())
                        registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', leader_name1.id)

                        if registered:
                            if self.collection.count_documents({ "leader": leader_name }, limit = 1):
                                await ctx.send(f"{leader_name1} Already leads a clan")
                            elif self.collection.count_documents({ "members": leader_name }, limit = 1):
                                await ctx.send(f"{leader_name1} Already is in a clan")
                            else:
                            
                                log_channel = await self.bot.db.fetch('SELECT member_log_channel FROM server_constants WHERE guild_id = $1', guild_id)

                                clan_channel_id = log_channel[0]['member_log_channel']

                                clan_channel = self.bot.get_channel(clan_channel_id)

                                player_clans = [registered[0]['clan_1']]
                                if str(clan_name.title()) in player_clans:
                                    await ctx.send('That person is already a member of a clan.')

                                elif str(clan_name.title()) not in player_clans:
                                    view = ConfirmCancel(ctx.author)
                                    await ctx.send (f'Are you sure you want to create **{faction_name}**? This will take **500dc** from their account.', view = view)
                                    await view.wait()
                                    t = datetime.datetime.now()
                                    current_time = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
                                    if view.value is True:
                                        if registered[0]['banner_pieces'] < 500:
                                            await ctx.send("The user doesn't have 500dc.")
                                            return
                                        items = 'clan bronze bronze'
                                        ready = "False"
                                        opted = str(datetime.datetime.now().date())
                                        self.collection.insert_one({"_id": str(faction_name.title()), "leader": [leader_name], "members" : [leader_name], "career": [], "rank": "Trainers", "score": 0, "bonus": ":brown_square: **Trainer Rank**","time": current_time,"wars": 0, "wins": 0,})
                                        await self.bot.db.execute('INSERT INTO clans (clan_name, points, date_created, leaders, played,items,cc,streak,ready_for_war,tier,dc,slots, opted, event, event_played) VALUES ($1, 0, $2, $3, 0,$4,0,0,$5,0,0,10,$6,0,0)', str(clan_name.title()), str(datetime.datetime.now().date()), str(leader_name), items,ready, opted)
                                        await ctx.send(f'**{str(clan_name.title())}** has been registered as an official clan.')
                                        await self.bot.db.execute('UPDATE registered SET clan_1 = $2, banner_pieces = banner_pieces - 500 WHERE player_id = $1', leader_name1.id, str(clan_name.title()))
                                        await self.bot.db.execute('UPDATE registered SET date_1 = $2 WHERE player_id = $1', leader_name1.id, str(datetime.datetime.now().date()))

                                        em = discord.Embed(
                                            title = f'Member Joined {str(clan_name.title())}',
                                            description = f'{leader_name1.mention} joined {str(clan_name.title())} on {datetime.datetime.now().date()}',
                                            colour = color
                                        )            

                                        await clan_channel.send(embed = em)
                                        await ctx.send('Member has been added.')
                                        
                                    elif view.value is False:
                                        await ctx.send('Cancelled.')
                                    else:
                                        await ctx.send('Timed Out')                                        

                            
                        else:
                            await ctx.send('That person has not registered yet! Use `d!start` to register.')
                        


            else:
                await ctx.send('You do not have permissions to use that command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @clan_command.command(name = 'remove', aliases = ['r'])
    async def clan_remove_command(self, ctx, *, clan_name = None):
        if clan_name is None:
            pass
        else:
            clan_name = clan_name.replace("’", "'")        
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if int(ctx.author.id) in admins_list:
                if clan_name is None:
                    em = discord.Embed(
                        title = 'Clan',
                        description = '**Remove an existing clan.**\n\nd!clan remove [clan name]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:

                    clans = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(clan_name.title()))

                    if not clans:
                        await ctx.send(f'{clan_name.title()} is not a registered clan.')

                    else:
                        view = ConfirmCancel(ctx.author)
                        await ctx.send (f'Are you sure you want to delete **{clan_name}**?', view = view)
                        await view.wait()

                        if view.value is True:

                            members = list(self.collection.find( {"_id": clan_name.title()}, {"_id": 0, "members": 1}))
                            guild = self.bot.get_guild(774883579472904222)
                            await ctx.send("This will take some time.. Please do not use the command again.")
                            for i in members[0]['members']:

                                member = guild.get_member(i)
                                await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', i) 
                                for old_role_id in [1128305779754139699, 1128306111309688924, 1128322228438708224, 1128325733895393391, 1128331490099462256, 1128331588070027384]:
                                    old_role = guild.get_role(old_role_id)
                                    for role in member.roles:
                                        if role.id == old_role_id:
                                            await member.remove_roles(old_role)

                            self.collection.delete_one({"_id": str(clan_name.title())})

                            await self.bot.db.execute('DELETE FROM clans WHERE clan_name = $1', str(clan_name.title()))

                            await self.bot.db.execute('UPDATE registered SET clan_1 = NULL WHERE clan_1 = $1', str(clan_name.title()))
                            

                            await ctx.send(f'**{str(clan_name.title())}** is no longer an official clan.')

                        elif view.value is False:
                            await ctx.send("Cancelled.")
                        else:
                            await ctx.send("Timed Out.")


            else:
                await ctx.send('You do not have permissions to use that command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @clan_command.command(name = 'change', aliases = ['ch'])
    async def clan_name_command(self, ctx, *, clan_name = None):
        if clan_name is None:
            pass
        else:
            clan_name = clan_name.replace("’", "'")        
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if int(ctx.author.id) in admins_list:
                if clan_name is None:
                    em = discord.Embed(
                        title = 'Clan',
                        description = '**Change the name of an existing clan.**\n\nd!clan change [clan name]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:

                    clans = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(clan_name.title()))

                    if not clans:
                        await ctx.send(f'{clan_name.title()} is not a registered clan.')

                    else:
                        await ctx.send(f"{ctx.author.mention} Please specify the New Clan name.")
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
                            view = ConfirmCancel(ctx.author)
                            if clan_2 is None:
                                pass
                            else:
                                clan_2 = clan_2.replace("’", "'")
                            await ctx.send (f'Are you sure you want to name it to **{clan_2.title()}**?', view = view)
                            await view.wait()
                            if view.value == True:

                                query = {"_id": clan_name.title()}
                                document = self.collection.find_one(query)
                                cloned_document = document.copy()
                                cloned_document["_id"] = str(clan_2.title())
                                self.collection.insert_one(cloned_document)
                                self.collection.delete_one(query)

                                await self.bot.db.execute(f'UPDATE clans SET clan_name = $1 WHERE clan_name = $2',  str(clan_2.title()), str(clan_name.title()))
                                await self.bot.db.execute(f'UPDATE registered SET clan_1 = $1 WHERE clan_1 = $2',  str(clan_2.title()), str(clan_name.title()))

                                await ctx.send(f'**{str(clan_name.title())}** is now **{clan_2.title()}**.')

                            elif view.value is False:
                                await ctx.send("Cancelled.")
                            else:
                                await ctx.send("Timed Out.")


            else:
                await ctx.send('You do not have permissions to use that command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @clan_command.command(name = 'warlog', aliases = ['wl'])
    async def give_points_command(self, ctx, mvp : discord.Member = None,*, score = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        member_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', mvp.id)
        if registered_check:
            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(786448967172882442)
            role2 = guild.get_role(1090438349455622204)
            role3 = guild.get_role(781452019578961921)
            if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles):
                if (score is None) or (mvp is None):
                    em = discord.Embed(
                        title = 'Clan',
                        description = '**Log between 2 clans.**\n\nd!clan warlog [mvp] [score]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    await ctx.send(f"{ctx.author.mention} Please specify the **WINNING** Clan name.")
                    try:
                        winne = await self.bot.wait_for(
                            'message',
                            timeout = 60,
                            check = lambda message: message.author == ctx.author and message.channel == ctx.channel
                        )

                    except asyncio.TimeoutError:
                        await ctx.send('Timed-out.')

                    else:
                        winner = winne.content
                        await ctx.send(f"{ctx.author.mention} Please specify the **LOSING** Clan name.")
                        try:
                            lose = await self.bot.wait_for(
                                'message',
                                timeout = 60,
                                check = lambda message: message.author == ctx.author and message.channel == ctx.channel
                            )

                        except asyncio.TimeoutError:
                            await ctx.send('Timed-out.')

                        else:
                            loser = lose.content

                            clans1 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(winner.title()))
                            clans2 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(loser.title()))
                            if not clans1:
                                await ctx.send(f'{str(winner.title())} is not a registered clan.')
                            elif not clans2:
                                await ctx.send(f'{str(loser.title())} is not a registered clan.')
                            else:
                                view = ConfirmCancel(ctx.author)

                                await ctx.send (f'{ctx.author.mention} Are you sure? **{str(winner.title())}** Will be the winner.', view = view)
                                await view.wait()
                                if view.value == True:
                                    clan_points = clans1[0]['points']
                                    clan_played1 = clans1[0]['played']

                                    await self.bot.db.execute('UPDATE registered SET clan_2 = NULL WHERE clan_name = $1', str(winner.title()))
                                    await self.bot.db.execute('UPDATE registered SET clan_2 = NULL WHERE clan_name = $1', str(loser.title()))

                                    
                                    await self.bot.db.execute('UPDATE clans SET points = $1 WHERE clan_name = $2', clan_points + 1, str(winner.title()))
                                    await self.bot.db.execute('UPDATE clans SET played = $1 WHERE clan_name = $2', clan_played1 + 1, str(winner.title()))
                                    clan_played2 = clans2[0]['played']
                                    await self.bot.db.execute('UPDATE clans SET played = $1 WHERE clan_name = $2', clan_played2 + 1, str(loser.title()))


                                    self.collection.update_one({"_id":str(winner.title())}, {"$addToSet": {"career": f":green_circle: **Won** against `{str(loser.title())}` with score `{score}` on *{datetime.datetime.now().date()}*\n《**MVP**》{mvp.mention}"}})
                                    self.collection.update_one({"_id":str(loser.title())}, {"$addToSet": {"career": f":red_circle: **Lost** against `{str(winner.title())}` with score `{score}` on *{datetime.datetime.now().date()}*\n《**MVP**》{mvp.mention}"}})
                                    await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1', mvp.id)
                                    embedScore = discord.Embed(
                                    title = f"Logged {str(winner.title())} won vs {str(loser.title())}",
                                    description = f'',
                                    colour = color
                                    )
                                    embedScore.add_field(name = f'Results', value = f'**{str(winner.title())}** Won against **{str(loser.title())}** with score **{score}** on *{datetime.datetime.now().date()}*', inline=False)
                                    embedScore.add_field(name = f'Special Stats', value = f'**MVP** was {mvp.mention} **+25**dc', inline=False)
                                    flists = str(member_check[0]['achievements'])
                                    new_admins = ''
                                    admins_list = self.listing(flists)
                                    for p,admin in enumerate(admins_list):
                                        if p == 0:
                                            new_admins += str(admin)
                                        elif p == 34:
                                            if int(admin) == 0:
                                                admins_list[35] = 1
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  mvp.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  mvp.id)
                                                await ctx.send("**Bronze Achievement Completed! ✦ Get MVP in a war ✦**\n*10dc rewarded & Lootbox rewarded*")
                                            elif int(admin) == 2:
                                                admins_list[35] = 2
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  mvp.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  mvp.id)
                                                await ctx.send("**Silver Achievement Completed! ✦✦ Get 3 MVPs ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                            elif int(admin) == 9:
                                                admins_list[35] = 3
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  mvp.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  mvp.id)
                                                await ctx.send("**Gold Achievement Completed! ✦✦✦ Get 10 MVPs ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                            admin = int(admin) + 1
                                            new_admins += f' {admin}'                                                       
                                        else:
                                            new_admins += f' {admin}'  

                                    await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, mvp.id)  
                                    await ctx.send(embed = embedScore)

                                elif view.value == False:
                                    await ctx.send("Cancelled.")
                                else:
                                    await ctx.send("Timed Out.")

            else:
                await ctx.send('You do not have permissions to use that command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')


    @clan_command.command(name = 'memberenable', aliases = ['me'])
    async def clan_member_enable_command(self, ctx, channel : discord.TextChannel = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if clan_name is None:
            pass
        else:
            clan_name = clan_name.replace("’", "'")
        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if int(ctx.author.id) in admins_list:
                if channel is None:
                    em = discord.Embed(
                        title = 'Clan',
                        description = '**Enable a channel to log member joins and leaves for clans.**\n\nd!clan memberenable [channel]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    await self.bot.db.execute('UPDATE server_constants SET member_log_channel = $1 WHERE guild_id = $2', channel.id, guild_id)

                    await ctx.send(f'Clan leaves and joins will be logged in {channel.mention}.')

            else:
                await ctx.send('You do not have permissions to use that command!')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @clan_command.command(name = 'cooldown', aliases =['cd'])
    async def ccooldown_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if registered_check:
            datewhenjoin = registered_check[0]['date_1']
            current_date = datetime.datetime.now()
            if datewhenjoin == None:
                await ctx.send("You have no **Cooldown**")
            elif ((current_date - datetime.datetime.strptime(datewhenjoin, "%Y-%m-%d")).days) >= 7:
                await ctx.send("You have no **Cooldown**")

            else:
                cooldown = 7 - ((current_date - datetime.datetime.strptime(datewhenjoin, "%Y-%m-%d")).days)
                await ctx.send(f"You have a cooldown of **{cooldown}** days left")                
                        
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')
    @clan_command.command(name = 'memberadd', aliases =['ma'])
    async def clan_member_add_command(self, ctx, member : discord.Member = None, *, clan_name = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if clan_name is None:
            pass
        else:
            clan_name = clan_name.replace("’", "'")
        if registered_check:
            guild_id = ctx.guild.id

            if (member is None) or (clan_name is None):
                em = discord.Embed(
                    title = 'Clan',
                    description = '**Add a member to a clan and log it.**\n\nd!clan memberadd [mention] [clan name]',
                    colour = color
                )

                await ctx.send(embed = em)
            
            else:
                registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                if registered:

                    clans = await self.bot.db.fetch('SELECT * FROM clans')
                    allclans = []
                    for i in clans:
                        allclans.append(i['clan_name'])

                    clan_name = self.find_matching_name(clan_name.title(), allclans)

                    clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(clan_name.title()))

                    if not clan:
                        await ctx.send(f'{str(clan_name.title())} is not a registered clan.')

                    else:

                        guild = self.bot.get_guild(774883579472904222)
                        role = guild.get_role(786448967172882442)
                        role2 = guild.get_role(1090438349455622204)
                        role3 = guild.get_role(781452019578961921)
                        admins = clan[0]['leaders']
                        admins_list = self.listing(admins)

                        if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles) or (int(ctx.author.id) in admins_list):

                            log_channel = await self.bot.db.fetch('SELECT member_log_channel FROM server_constants WHERE guild_id = $1', guild_id)

                            clan_channel_id = log_channel[0]['member_log_channel']

                            clan_channel = self.bot.get_channel(clan_channel_id)

                            player_clans = [registered[0]['clan_1']]

                            player_clans_execute = {
                                1:'UPDATE registered SET clan_1 = $1 WHERE player_id = $2',
                                10:'UPDATE registered SET date_1 = $1 WHERE player_id = $2',
                            }

                            if str(clan_name.title()) in player_clans:
                                await ctx.send('That person is already in the clan!')

                            else:
                                members = list(self.collection.find( {"_id": clan_name.title()}, {"_id": 0, "members": 1}))
                                memberss = len(members[0]["members"])
                                slot = clan[0]['slots']
                                if memberss == slot:
                                    await ctx.send("This clan already has the maximum number of members it can hold. Unlock more slots using `d!clan upgrade slot`")
                                    return
                                elif memberss == 18:
                                    await ctx.send("This clan already has the maximum number of members it can hold.")
                                    return
                                else:
                                    pass

                                view = ConfirmCancel(member)

                                await ctx.send (f'Do you want to join **{clan_name}**? {member.mention}', view = view)
                                await view.wait()
                                if view.value == True:

                                    datewhenjoin = registered[0]['date_1']
                                    current_date = datetime.datetime.now()
                                    if datewhenjoin == None:
                                        pass
                                    elif ((current_date - datetime.datetime.strptime(datewhenjoin, "%Y-%m-%d")).days) >= 7:
                                        pass
                                    else:
                                        cooldown = 7 - ((current_date - datetime.datetime.strptime(datewhenjoin, "%Y-%m-%d")).days)
                                        dc = cooldown*100
                                        view = ConfirmCancel(member)
                                        await ctx.send(f"{member.mention} has a cooldown of **{cooldown}** still left, Would you like to pay **{dc}dc** to bypass this?", view = view)
                                        await view.wait()

                                        if view.value == True:
                                            if registered[0]['banner_pieces'] >= dc:
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - {dc} WHERE player_id = $1', member.id)
                                                pass
                                            else:
                                                await ctx.send("You don't have enough dc!")
                                                return
                                        elif view.value == False:
                                            await ctx.send("Cancelled.")
                                            return
                                        else:
                                            await ctx.send("Timed out.")
                                            return
                            

                                    await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', member.id)

                                    for i in range(len(player_clans)):
                                        if player_clans[i] is None:
                                            await self.bot.db.execute(player_clans_execute[i+1], str(clan_name.title()), member.id)
                                            self.collection.update_one({"_id": str(clan_name.title())}, {"$addToSet": {"members": member.id}})

                                            await self.bot.db.execute(player_clans_execute[i+10], str(datetime.datetime.now().date()), member.id)
                                            await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', member.id) 
                                            em = discord.Embed(
                                                title = f'Member joined {str(clan_name.title())}',
                                                description = f'{member.mention} joined {str(clan_name.title())} on {datetime.datetime.now().date() }',
                                                colour = color
                                            )
                                            
                                            await ctx.send('Member has been added.')
                                            await clan_channel.send(embed = em)
                                            break
                                                
                                    else:
                                        await ctx.send('That person is already in a clan!')
                                elif view.value == False:
                                    await ctx.send("The member declined.")
                                else:
                                    await ctx.send("Timed out.")

                        else:
                            await ctx.send('You do not have permissions to use that command.')

                else:
                    await ctx.send('That person has not registered yet! Use `d!start` to register.')
        
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @clan_command.command(name = 'memberremove', aliases =['mr'])
    async def clan_member_remove_command(self, ctx, member : discord.Member = None, *, clan_name = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if clan_name is None:
            pass
        else:
            clan_name = clan_name.replace("’", "'")
        if registered_check:
            guild_id = ctx.guild.id

            if (member is None) or (clan_name is None):
                em = discord.Embed(
                    title = 'Clan',
                    description = '**Remove a member from a clan and log it.**\n\nd!clan memberremove [mention] [clan name]',
                    colour = color
                )

                await ctx.send(embed = em)

            else:
                registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                if registered:


                    clans = await self.bot.db.fetch('SELECT * FROM clans')
                    allclans = []
                    for i in clans:
                        allclans.append(i['clan_name'])

                    clan_name = self.find_matching_name(clan_name.title(), allclans)

                    clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(clan_name.title()))

                    if not clan:
                        await ctx.send(f'{str(clan_name.title())} is not a registered clan.')

                    else:
                        leaders = clan[0]['leaders']

                        if leaders is not None:
                            leaders_list = self.listing(leaders)

                        elif leaders is None:
                            leaders_list = []

                        guild = self.bot.get_guild(774883579472904222)
                        role = guild.get_role(786448967172882442)
                        role2 = guild.get_role(1090438349455622204)
                        role3 = guild.get_role(781452019578961921)
                        admins = clan[0]['leaders']
                        admins_list = self.listing(admins)

                        if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles) or (int(ctx.author.id) in admins_list):
                            log_channel = await self.bot.db.fetch('SELECT member_log_channel FROM server_constants WHERE guild_id = $1', guild_id)

                            clan_channel_id = log_channel[0]['member_log_channel']

                            clan_channel = self.bot.get_channel(clan_channel_id)

                            player_clans = [registered[0]['clan_1']]

                            view = ConfirmCancel(ctx.author)
                            await ctx.send(f"Are you sure you want to remove {member.mention}?", view = view)
                            await view.wait()

                            if view.value == True:
                                pass
                            elif view.value == False:
                                await ctx.send("Cancelled.")
                                return
                            else:
                                await ctx.send("Timed out.")
                                return

                            if str(clan_name.title()) not in player_clans:
                                await ctx.send('That person is not a member of that clan.')

                            elif str(clan_name.title()) in player_clans:

                                member_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                                if member_check[0]['clan_2'] is None:
                                    pass
                                else:
                                    await ctx.send("That player is still in a war.")
                                    return

                                if str(clan_name.title()) == registered[0]['clan_1']:
                                    self.collection.update_one({"_id": str(clan_name.title())}, {"$pull": {"members": member.id}})
                                    await self.bot.db.execute('UPDATE registered SET clan_1 = NULL WHERE player_id = $1', member.id)
                                    await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', member.id) 
                                    em = discord.Embed(
                                        title = f'Member left {str(clan_name.title())}',
                                        description = f'{member.mention} left {str(clan_name.title())} on {datetime.datetime.now().date()}',
                                        colour = color
                                    )        

                                    
                                    for old_role_id in [1128305779754139699, 1128306111309688924, 1128322228438708224, 1128325733895393391, 1128331490099462256, 1128331588070027384]:
                                        old_role = guild.get_role(old_role_id)

                                        for role in member.roles:
                                            if role.id == old_role_id:
                                                await member.remove_roles(old_role)

                                    await clan_channel.send(embed = em)
                                    await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', member.id)
                                    await ctx.send('Member has been removed.')
                                    
                        else:
                            await ctx.send('You do not have permissions to use that command.')

                else:
                    await ctx.send('That person has not registered yet! Use `d!start` to register.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @clan_command.command(name = 'leave', aliases =['lv'])
    async def clan_member_leave_command(self, ctx, *, clan_name = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if clan_name is None:
            pass
        else:
            clan_name = clan_name.replace("’", "'")
        member = ctx.author
        if registered_check:
            guild_id = ctx.guild.id

            if (clan_name is None):
                em = discord.Embed(
                    title = 'Clan',
                    description = '**Leave a clan.**\n\nd!clan leave [clan name]',
                    colour = color
                )

                await ctx.send(embed = em)

            else:
                registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                if registered:

                    clans = await self.bot.db.fetch('SELECT * FROM clans')
                    allclans = []
                    for i in clans:
                        allclans.append(i['clan_name'])

                    clan_name = self.find_matching_name(clan_name.title(), allclans)


                    clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(clan_name.title()))
                    if not clan:
                        await ctx.send(f'{str(clan_name.title())} is not a registered clan.')

                    else:

                        guild = self.bot.get_guild(774883579472904222)

                        log_channel = await self.bot.db.fetch('SELECT member_log_channel FROM server_constants WHERE guild_id = $1', guild_id)

                        clan_channel_id = log_channel[0]['member_log_channel']

                        clan_channel = self.bot.get_channel(clan_channel_id)

                        player_clans = [registered[0]['clan_1']]

                        if str(clan_name.title()) not in player_clans:
                            await ctx.send('You are not a member of that clan.')

                        elif str(clan_name.title()) in player_clans:

                            view = ConfirmCancel(ctx.author)

                            await ctx.send (f'Do you want to leave **{clan_name}**? {member.mention}', view = view)
                            await view.wait()
                            if view.value == True:
                                if registered[0]['clan_2'] is None:
                                    pass
                                else:
                                    await ctx.send("You cannot leave the clan while you're in a war.")
                                    return
                                
                                if str(clan_name.title()) == registered[0]['clan_1']:
                                    self.collection.update_one({"_id": str(clan_name.title())}, {"$pull": {"members": member.id}})
                                    await self.bot.db.execute('UPDATE registered SET clan_1 = NULL WHERE player_id = $1', member.id)

                                    em = discord.Embed(
                                        title = f'Member left {str(clan_name.title())}',
                                        description = f'{member.mention} left {str(clan_name.title())} on {datetime.datetime.now().date()}',
                                        colour = color
                                    )        

                                    
                                    for old_role_id in [1128305779754139699, 1128306111309688924, 1128322228438708224, 1128325733895393391, 1128331490099462256, 1128331588070027384]:
                                        old_role = guild.get_role(old_role_id)

                                        for role in member.roles:
                                            if role.id == old_role_id:
                                                await member.remove_roles(old_role)

                                    await clan_channel.send(embed = em)
                                    await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', member.id)
                                    await ctx.send('Member has been removed.')
                            elif view.value == False:
                                await ctx.send("Cancelled.")
                            else:
                                await ctx.send("Timed out.")


                else:
                    await ctx.send('That person has not registered yet! Use `d!start` to register.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')


    @clan_command.command(name = 'leaderadd', aliases = ['lda'])
    async def clan_leader_add_command(self, ctx, member : discord.Member = None, *, clan_name = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if clan_name is None:
            pass
        else:
            clan_name = clan_name.replace("’", "'")
        if registered_check:
            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(786448967172882442)
            role2 = guild.get_role(1090438349455622204)
            role3 = guild.get_role(781452019578961921)
            if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles):
                if (member is None) or (clan_name is None):
                    em = discord.Embed(
                        title = 'Clan',
                        description = '**Add a leader to a clan.**\n\nd!leaderadd [mention] [clan name]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                    if registered:
                        member_id = member.id

                        clans = await self.bot.db.fetch('SELECT * FROM clans')
                        allclans = []
                        for i in clans:
                            allclans.append(i['clan_name'])

                        clan_name = self.find_matching_name(clan_name.title(), allclans)

                        clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                        if clan:
                            clan_leader = clan[0]['leaders']

                            clan_leaders_list = self.listing(clan_leader)

                            if (clan_leaders_list is None) or (int(member_id) not in clan_leaders_list):
                                if clan_leader is None:
                                    new_leader = str(member_id)
                                    
                                    await self.bot.db.execute('UPDATE clans SET leaders = $1 WHERE clan_name = $2', new_leader, clan_name.title())

                                else:
                                    new_leader = str(clan_leader) + f' {member_id}'

                                    await self.bot.db.execute('UPDATE clans SET leaders = $1 WHERE clan_name = $2', new_leader, clan_name.title())
                                self.collection.update_one({"_id": str(clan_name.title())}, {"$addToSet": {"leader": member.id}})
                                await ctx.send(f"{member.name} has been added as a leader for {clan_name.title()}, if the person isn't added as a member please add them as a member as well")

                            elif int(member_id) in clan_leaders_list:
                                await ctx.send('That person is already a leader of the clan!')

                        else:
                            await ctx.send('That clan has not been registered officially!')
                    
                    else:
                        await ctx.send('That person has not registered yet! Use `d!start` to register.')

            else:
                await ctx.send('You do not have permissions to use that command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @clan_command.command(name = 'leaderremove', aliases = ['ldr'])
    async def clan_leader_remove_command(self, ctx, member : discord.Member = None, *, clan_name = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if clan_name is None:
            pass
        else:
            clan_name = clan_name.replace("’", "'")
        if registered_check:
            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(786448967172882442)
            role2 = guild.get_role(1090438349455622204)
            role3 = guild.get_role(781452019578961921)
            if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles):
                if (member is None) or (clan_name is None):
                    em = discord.Embed(
                        title = 'Clan',
                        description = '**Remove a leader from a clan.**\n\nd!leaderremove [mention] [clan name]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                    if registered:
                        member_id = member.id

                        clans = await self.bot.db.fetch('SELECT * FROM clans')
                        allclans = []
                        for i in clans:
                            allclans.append(i['clan_name'])

                        clan_name = self.find_matching_name(clan_name.title(), allclans)

                        clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                        if clan:
                            clan_leader = clan[0]['leaders']

                            clan_leader_list = self.listing(clan_leader)
                            
                            if (clan_leader_list is None) or (int(member_id) not in clan_leader_list):
                                await ctx.send('That person is not a leader of the clan!')

                            elif int(member_id) in clan_leader_list:
                                clan_leader_list.remove(int(member_id))

                                if len(clan_leader_list) == 0:
                                    await self.bot.db.execute('UPDATE clans SET leaders = NULL WHERE clan_name = $1', clan_name.title())

                                else:
                                    new_leader = ''

                                    for leader in clan_leader_list:
                                        if clan_leader_list.index(leader) == 0:
                                            new_leader += str(leader)

                                        else:
                                            new_leader += f' {leader}'

                                    await self.bot.db.execute('UPDATE clans SET leaders = $1 WHERE clan_name = $2', new_leader, clan_name.title())
                                self.collection.update_one({"_id": str(clan_name.title())}, {"$pull": {"leader": member.id}})
                                await ctx.send(f'{member.name} has been removed as a leader of {clan_name.title()}.')

                        else:
                            await ctx.send('That clan has not been registered officially!')

                    else:
                        await ctx.send('That person has not registered yet! Use `d!start` to register.')
            
            else:
                await ctx.send('You do not have permissions to use that command.')
        
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @clan_command.command(name = 'memberdass', aliases = ['m'])
    async def clan_members_command(self, ctx, *, clan_name = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if clan_name is None:
            pass
        else:
            clan_name = clan_name.replace("’", "'")
        if registered_check:
            if clan_name is None:
                em = discord.Embed(
                    title = 'Clan',
                    description = '**View all the members in a clan.**\n\nd!clan members [clan name]',
                    colour = color
                )

                await ctx.send(embed = em)

            else:
                clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(clan_name.title()))

                if clan:
                    members_str = ''

                    clan_members_1 = await self.bot.db.fetch('SELECT * FROM registered WHERE clan_1 = $1', str(clan_name.title()))

                    clan_members_2 = await self.bot.db.fetch('SELECT * FROM registered WHERE clan_2 = $1', str(clan_name.title()))

                    if clan_members_1:
                        for i in clan_members_1:
                            username = self.bot.get_user(i['player_id'])

                            members_str += f' `{str(username)[:-5:]}`'

                    if clan_members_2:
                        for i in clan_members_2:
                            username = self.bot.get_user(i['player_id'])

                            members_str += f' `{str(username)[:-5:]}`'

                    member_embed = discord.Embed(
                        title = f'Members of {str(clan_name.title())}',
                        description = members_str,
                        colour = color
                    )

                    member_embed.set_footer(text = f'Total members: {len(clan_members_1) + len(clan_members_2)}')
                    await ctx.send(embed = member_embed)
                else:
                    await ctx.send('That clan has not been registered!')
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @clan_command.command(name = 'setavatar', aliases = ['setav'])
    async def clan_set_avatar_command(self, ctx, image = None, *, clan_name = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if clan_name is None:
            pass
        else:
            clan_name = clan_name.replace("’", "'")
        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if (image is None) or (clan_name is None):
                em = discord.Embed(
                    title = 'Clan',
                    description = '**Set an avatar for your clan.**\n\nd!clan setavatar [link] [clan name]',
                    colour = color
                )

                await ctx.send(embed = em)

            else:
                clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                if not clan:
                    await ctx.send(f'{clan_name.title} is not a registered clan.')

                else:

                    if int(ctx.author.id) in admins_list:
                        
                            await self.bot.db.execute('UPDATE clans SET avatar = $1 WHERE clan_name = $2', image, clan_name.title())

                            await ctx.send(f'Avatar set for {clan_name.title()} clan.')


                    else:
                        await ctx.send('You do not have permissions to use that command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')




    @clan_command.command(name = 'caddtoshop')
    async def clanaddtoshop_command(self,ctx, item_name :str = None,item_place :str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if int(ctx.author.id) in admins_list:
                if (item_name is None) or (item_place is None):
                    em = discord.Embed(
                        title = 'Misc',
                        description = '**Add to shop**\n\nd!clan addtoshop name place',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:

                    shop = 'False'
                    await self.bot.db.execute('INSERT INTO clan_shop (price,item_name,shop,item_place) VALUES (2000,$1,$2,$3)',item_name,shop,item_place)
                    await ctx.send("Item added to the shop!")
            else:
                await ctx.send("You don't have the permission to perform this command!")

    @clan_command.command(name = 'shop', aliases = ['sh'])
    async def clan_shoppp_command(self,ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if registered_check:
          

            lb = await self.bot.db.fetch(f'SELECT * FROM clan_shop')
            if lb == []:
                await ctx.send(f"There are no items listed right now..")
                return
            
            lb.reverse()
            
            data = []
            for faction in lb:
                data.append(faction['item_name'])
            
            stat = None

            pagination_view = LPaginationView()
            pagination_view.data = data
            pagination_view.lb = lb
            pagination_view.stat = stat
            pagination_view.registered_check = registered_check
            await pagination_view.send(ctx)   

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @clan_command.command(name = 'inventory', aliases = ['inv'])
    async def clan_shop_command(self,ctx,stat : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        clan_name = registered_check[0]['clan_1']

        if registered_check:
            if clan_name:

                clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                if not clan:
                    await ctx.send(f'{clan_name.title} is not a registered clan.')

                else:


                    admins = clan[0]['leaders']
                    admins_list = self.listing(admins)

                    if int(ctx.author.id) in admins_list:
                        em = discord.Embed(
                            title = f'{clan_name.title()} Balance',
                            description = '',
                            colour = color
                        )
                        current = clan[0]['cc']
                        dc = clan[0]['dc']
                        em.add_field(name='Clan Coins', value=f'{current}')
                        em.add_field(name='Dom Coins', value=f'{dc}')
                        avatar = clan[0]['avatar']
                        if avatar is None:
                            pfp = 'clandefault.png'
                        else:
                            pfp = avatar

                        em.set_thumbnail(url=f"attachment://{pfp}")


                        await ctx.send(file = discord.File(pfp),embed = em)
                    else:
                        await ctx.send("You're not a leader!")
            else:
                await ctx.send("You're not in a clan!")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @clan_command.command(name = 'optasdadas')
    async def opt(self,ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        clan_name = registered_check[0]['clan_1']

        if registered_check:
            if clan_name:

                clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                if not clan:
                    await ctx.send(f'{clan_name.title} is not a registered clan.')

                else:


                    admins = clan[0]['leaders']
                    admins_list = self.listing(admins)

                    if int(ctx.author.id) in admins_list:
                        
                        if (clan[0]['ready_for_war'] == 'True') or (clan[0]['ready_for_war'] == 'False'):
                            pass
                        else:
                            await ctx.send("You cannot change this while you're in a war.")
                            return

                        if clan[0]['opted'] == 'False':
                            delete_time = str(datetime.datetime.now().date())
                            await self.bot.db.execute(f'UPDATE clans SET opted = $1 WHERE clan_name = $2',delete_time, clan_name.title())
                            await ctx.send("Opted in! Your members can now queue up as a Blade.. you will not be able to opt out for the next **7** days.")

                        else:
                            datewhenjoin = clan[0]['opted']
                            current_date = datetime.datetime.now()
                            if ((current_date - datetime.datetime.strptime(datewhenjoin, "%Y-%m-%d")).days) >= 7:
                                delete_time = 'False'
                                await self.bot.db.execute(f'UPDATE clans SET opted = $1 WHERE clan_name = $2',delete_time, clan_name.title())
                                await ctx.send("Opted out. Your members can no longer queue up as a Blade.. you can opt back in at anytime.")
                            else:
                                cooldown = 7 - ((current_date - datetime.datetime.strptime(datewhenjoin, "%Y-%m-%d")).days)
                                await ctx.send(f"You still have a cooldown of **{cooldown}** days!")
                    else:
                        await ctx.send("You're not a leader!")
            else:
                await ctx.send("You're not in a clan!")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')


    @clan_command.command(name = 'give', aliases = ['g'])
    async def cdc_shop_command(self,ctx,dc : int = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        clan_name = registered_check[0]['clan_1']

        if registered_check:
            if dc == None:
                em = discord.Embed(
                    title = 'Clan',
                    description = '**Give Dc to your clan.**\n\nd!clan give [dc]',
                    colour = color
                )

                await ctx.send(embed = em)                
            else:
                if clan_name:

                    clans = await self.bot.db.fetch('SELECT * FROM clans')
                    allclans = []
                    for i in clans:
                        allclans.append(i['clan_name'])

                    clan_name = self.find_matching_name(clan_name.title(), allclans)

                    clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                    if not clan:
                        await ctx.send(f'{clan_name.title} is not a registered clan.')

                    else:

                        view = ConfirmCancel(ctx.author)
                        await ctx.send(f"Are you sure you want to give **{dc}dc** to your clan? You will not be able to retrieve it later.",view = view)

                        await view.wait()

                        if view.value == True:
                            registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                            if registered_check[0]['banner_pieces'] < dc:
                                await ctx.send("You don't have enough Dc for that!")
                            else:
                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - {dc} WHERE player_id = $1', ctx.author.id)
                                await self.bot.db.execute(f'UPDATE clans SET dc = dc + {dc} WHERE clan_name = $1', clan_name.title())
                                await ctx.send(f"Gave **{dc}dc** to **{clan_name.title()}**")

                        elif view.value == False:
                            await ctx.send("Cancelled")
                        else:
                            await ctx.send("Timed out.")
                else:
                    await ctx.send("You're not in a clan!")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')    

    @clan_command.command(name = 'tiers', aliases = ['tier'])
    async def clan_tier_command(self,ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        clan_name = registered_check[0]['clan_1']

        if registered_check:
            if clan_name:

                clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                if not clan:
                    await ctx.send(f'{clan_name.title} is not a registered clan.')

                else:


                    admins = clan[0]['leaders']
                    admins_list = self.listing(admins)

                    if int(ctx.author.id) in admins_list:

                        em = discord.Embed(
                            title = 'Clan Tiers',
                            description = '',
                            colour = color
                        )
                        if clan[0]['tier'] >= 1:
                            current = '**Obtained ✅**'
                        elif clan[0]['tier'] == 0:
                            current = '**Upgrade 🔺**'
                        else:
                            current = '**Locked 🔒**'
                        em.add_field(name='Bronze Tier <:bronze_tier:1128305580533100554>', value=f'Price | **500 cc**\n{current}')
                        if clan[0]['tier'] >= 2:
                            current = '**Obtained ✅**'
                        elif clan[0]['tier'] == 1:
                            current = '**Upgrade 🔺**'
                        else:
                            current = '**Locked 🔒**'                        
                        em.add_field(name='Silver Tier <:silver_tier:1128303815758721114>', value=f'Price | **1,000 cc**\n{current}')
                        if clan[0]['tier'] >= 3:
                            current = '**Obtained ✅**'
                        elif clan[0]['tier'] == 2:
                            current = '**Upgrade 🔺**'
                        else:
                            current = '**Locked 🔒**'
                        em.add_field(name='Gold Tier <:gold_tier:1128321998532116480>', value=f'Price | **2,000 cc**\n{current}')
                        if clan[0]['tier'] >= 4:
                            current = '**Obtained ✅**'
                        elif clan[0]['tier'] == 3:
                            current = '**Upgrade 🔺**'
                        else:
                            current = '**Locked 🔒**'
                        em.add_field(name='Platinum Tier <:platinum_tier:1128329484794347653>', value=f'Price | **4,000 cc**\n{current}')
                        if clan[0]['tier'] >= 5:
                            current = '**Obtained ✅**'
                        elif clan[0]['tier'] == 4:
                            current = '**Upgrade 🔺**'
                        else:
                            current = '**Locked 🔒**'
                        em.add_field(name='Diamond Tier <:diamond_tier:1172865298051903550>', value=f'Price | **7,500 cc**\n{current}')
                        if clan[0]['tier'] >= 6:
                            current = '**Obtained ✅**'
                        elif clan[0]['tier'] == 5:
                            current = '**Upgrade 🔺**'
                        else:
                            current = '**Locked 🔒**'
                        em.add_field(name='Dominant Tier <:dominant_tier:1128335433173045258> ', value=f'Price | **10,000 cc**\n{current}')

                        em.set_footer(text='d!clan upgrade')
                        await ctx.send(embed = em)                        
                    
                    else:
                        em = discord.Embed(
                            title = 'Clan Tiers',
                            description = '',
                            colour = color
                        )

                        current = '**Locked 🔒**'
                        em.add_field(name='Bronze Tier <:bronze_tier:1128305580533100554>', value=f'Price | **500 cc**\n{current}')
                            
                        em.add_field(name='Silver Tier <:silver_tier:1128303815758721114>', value=f'Price | **1,000 cc**\n{current}')

                        em.add_field(name='Gold Tier <:gold_tier:1128321998532116480>', value=f'Price | **2,000 cc**\n{current}')

                        em.add_field(name='Platinum Tier <:platinum_tier:1128329484794347653>', value=f'Price | **4,000 cc**\n{current}')

                        em.add_field(name='Diamond Tier <:diamond_tier:1172865298051903550>', value=f'Price | **7,500 cc**\n{current}')

                        em.add_field(name='Dominant Tier <:dominant_tier:1128335433173045258> ', value=f'Price | **10,000 cc**\n{current}')

                        em.set_footer(text='d!clan upgrade')
                        await ctx.send(embed = em)  
            else:
                em = discord.Embed(
                    title = 'Clan Tiers',
                    description = '',
                    colour = color
                )

                current = '**Locked 🔒**'
                em.add_field(name='Bronze Tier <:bronze_tier:1128305580533100554>', value=f'Price | **500 cc**\n{current}')
                    
                em.add_field(name='Silver Tier <:silver_tier:1128303815758721114>', value=f'Price | **1,000 cc**\n{current}')

                em.add_field(name='Gold Tier <:gold_tier:1128321998532116480>', value=f'Price | **2,000 cc**\n{current}')

                em.add_field(name='Platinum Tier <:platinum_tier:1128329484794347653>', value=f'Price | **4,000 cc**\n{current}')

                em.add_field(name='Diamond Tier <:diamond_tier:1172865298051903550>', value=f'Price | **7,500 cc**\n{current}')

                em.add_field(name='Dominant Tier <:dominant_tier:1128335433173045258> ', value=f'Price | **10,000 cc**\n{current}')

                em.set_footer(text='d!clan upgrade')
                await ctx.send(embed = em)  
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @clan_command.command(name = 'slots', aliases = ['slot'])
    async def clan_sssscommand(self,ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        clan_name = registered_check[0]['clan_1']

        if registered_check:
            
            if clan_name:

                clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())
                
                if not clan:
                    await ctx.send(f'{clan_name.title} is not a registered clan.')

                else:
                
                    if clan[0]['slots'] >= 11:
                        current1 = '**✅**'
                    elif clan[0]['slots'] == 10:
                        current1 = '**🔺**'
                    else:
                        current1 = '**🔒**'

                    if clan[0]['slots'] >= 12:
                        current2 = '**✅**'
                    elif clan[0]['slots'] == 11:
                        current2 = '**🔺**'
                    else:
                        current2 = '**🔒**'      

                    if clan[0]['slots'] >= 13:
                        current3 = '**✅**'
                    elif clan[0]['slots'] == 12:
                        current3 = '**🔺**'
                    else:
                        current3 = '**🔒**'

                    if clan[0]['slots'] >= 14:
                        current4 = '**✅**'
                    elif clan[0]['slots'] == 13:
                        current4 = '**🔺**'
                    else:
                        current4 = '**🔒**'

                    if clan[0]['slots'] >= 15:
                        current5 = '**✅**'
                    elif clan[0]['slots'] == 14:
                        current5 = '**🔺**'
                    else:
                        current5 = '**🔒**'

                    if clan[0]['slots'] >= 16:
                        current6 = '**✅**'
                    elif clan[0]['tier'] == 15:
                        current6 = '**🔺**'
                    else:
                        current6 = '**🔒**'

                    if clan[0]['slots'] >= 17:
                        current7 = '**✅**'
                    elif clan[0]['tier'] == 16:
                        current7 = '**🔺**'
                    else:
                        current7 = '**🔒**'

                    if clan[0]['slots'] >= 18:
                        current8 = '**✅**'
                    elif clan[0]['tier'] == 17:
                        current8 = '**🔺**'
                    else:
                        current8 = '**🔒**'

                    em = discord.Embed(
                        title = 'Clan Slots',
                        description = f'**11 |** **500 Dc** : MUST BE **BRONZE+** {current1}\n**12 |** **800 Dc** : MUST BE **SILVER+** {current2}\n**13 |** **1300 Dc** : MUST BE **SILVER+** {current3}\n**14 |** **2000 Dc** : MUST BE **GOLD+** {current4}\n**15 |** **3000dc** : MUST BE **GOLD+** {current5}\n**16 |** **4000dc** : MUST BE **PLATINUM+** {current6}\n**17 |** **5000dc** : MUST BE **PLATINUM+** {current7}\n**18 |** **7000dc** : MUST BE **DIAMOND+** {current8}\n',
                        colour = color
                    )


                    em.set_footer(text='d!clan upgrade slot')
                    await ctx.send(embed = em)                        
                    
            else:
                if clan[0]['slots'] >= 11:
                    current = '**🔒**'
                elif clan[0]['slots'] == 10:
                    current = '**🔒**'
                else:
                    current = '**🔒**'

                if clan[0]['slots'] >= 12:
                    current = '**🔒**'
                elif clan[0]['slots'] == 11:
                    current = '**🔒**'
                else:
                    current = '**🔒**'      

                if clan[0]['slots'] >= 13:
                    current = '**🔒**'
                elif clan[0]['slots'] == 12:
                    current = '**🔒**'
                else:
                    current = '**🔒**'

                if clan[0]['slots'] >= 14:
                    current = '**🔒**'
                elif clan[0]['slots'] == 13:
                    current = '**🔒**'
                else:
                    current = '**🔒**'

                if clan[0]['slots'] >= 15:
                    current = '**🔒**'
                elif clan[0]['slots'] == 14:
                    current = '**🔒**'
                else:
                    current = '**🔒**'

                if clan[0]['slots'] >= 16:
                    current = '**🔒**'
                elif clan[0]['tier'] == 15:
                    current = '**🔒**'
                else:
                    current = '**🔒**'

                if clan[0]['slots'] >= 17:
                    current = '**🔒**'
                elif clan[0]['tier'] == 16:
                    current = '**🔒**'
                else:
                    current = '**🔒**'

                if clan[0]['slots'] >= 18:
                    current = '**🔒**'
                elif clan[0]['tier'] == 17:
                    current = '**🔒**'
                else:
                    current = '**🔒**'

                em = discord.Embed(
                    title = 'Clan Tiers',
                    description = f'**11 |** **500 Dc** : MUST BE **BRONZE+** {current}\n**12 |** **800 Dc** : MUST BE **SILVER+** {current}\n**13 |** **1300 Dc** : MUST BE **SILVER+** {current}\n**14 |** **2000 Dc** : MUST BE **GOLD+** {current}\n**15 |** **3000 Dc** : MUST BE **GOLD+** {current}\n**16 |** **4000 Dc** : MUST BE **PLATINUM+** {current}\n**17 |** **5000 Dc** : MUST BE **PLATINUM+** {current}\n**18 |** **7000 Dc** : MUST BE **DIAMOND+** {current}\n',
                    colour = color
                )


                em.set_footer(text='d!clan upgrade slot')
                await ctx.send(embed = em)    
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')


            
    @clan_command.command(name = 'upgrade', aliases = ['u'])
    async def upgrade_tier_command(self,ctx, thing : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        clan_name = registered_check[0]['clan_1']

        if registered_check:
            if clan_name:

                clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                if not clan:
                    await ctx.send(f'{clan_name.title} is not a registered clan.')

                else:

                    
                    admins = clan[0]['leaders']
                    admins_list = self.listing(admins)

                    if int(ctx.author.id) in admins_list:

                        if thing == None:
                            em = discord.Embed(
                                title = 'Clan',
                                description = "**Upgrade your clan's tier or unlock a slot**\n\nd!clan upgrade [tier/slot]",
                                colour = color
                            )

                            await ctx.send(embed = em)   
                            return      

                        else:
                            pass                     
                        
                        if thing == 'tier':
                            currentier = clan[0]['tier']

                            nexttier = clan[0]['tier'] + 1

                            if nexttier == 1:
                                price = 500
                            elif nexttier == 2:
                                price = 1000
                            elif nexttier == 3:
                                price = 2000                       
                            elif nexttier == 4:
                                price = 4000
                            elif nexttier == 5:
                                price = 7500
                            elif nexttier == 6:
                                price = 10000
                            else:
                                await ctx.send("Your clan is at the max tier")
                                return
                            
                            if clan[0]['cc'] < price:
                                await ctx.send(f"You don't have enough cc for the next tier! You need **{price}dc** for the next tier.")
                            else:
                                if currentier == 0:
                                    role = 1128305779754139699
                                elif currentier == 1:
                                    role = 1128306111309688924
                                elif currentier == 2:
                                    role = 1128322228438708224                       
                                elif currentier == 3:
                                    role = 1128325733895393391
                                elif currentier == 4:
                                    role = 1128331490099462256
                                elif currentier == 5:
                                    role = 1128331588070027384       

                                members = list(self.collection.find( {"_id": clan_name.title()}, {"_id": 0, "members": 1}))
                                guild = self.bot.get_guild(774883579472904222)
                                roled = guild.get_role(role)
                                if clan[0]['cc'] < price:
                                    await ctx.send(f"You don't have enough cc for the next tier! You need **{price}dc** for the next tier.")
                                    return
                                else:
                                    pass
                                await ctx.send("This will take some time.. Please do not use the command again.")
                                for i in members[0]['members']:
                                    member = guild.get_member(i)
                                    for old_role_id in [1128305779754139699, 1128306111309688924, 1128322228438708224, 1128325733895393391, 1128331490099462256, 1128331588070027384]:
                                        old_role = guild.get_role(old_role_id)

                                        for role in member.roles:
                                            if role.id == old_role_id:
                                                await member.remove_roles(old_role)

                                    await member.add_roles(roled)    

                                await self.bot.db.execute(f'UPDATE clans SET tier = tier + 1, cc = cc -{price} WHERE clan_name = $1', clan_name.title())
                                
                                await ctx.send(f"Upgraded to next tier!")
                        elif thing == 'slot':
                            currentier = clan[0]['slots']

                            nexttier = clan[0]['slots'] + 1

                            if nexttier == 11:
                                price = 500
                                tier = 1
                            elif nexttier == 12:
                                price = 800
                                tier = 2
                            elif nexttier == 13:
                                price = 1300      
                                tier = 2                 
                            elif nexttier == 14:
                                price = 2000
                                tier = 3
                            elif nexttier == 15:
                                price = 3000
                                tier = 3
                            elif nexttier == 16:
                                price = 4000
                                tier = 4
                            elif nexttier == 17:
                                price = 5000
                                tier = 4
                            elif nexttier == 18:
                                price = 7000
                                tier = 5
                            else:
                                await ctx.send("Your clan has unlocked all slots")
                                return
                            
                            if clan[0]['dc'] < price:
                                await ctx.send(f"Your clan don't have enough dc for the next slot! You need **{price}dc** for the next slot.")
                            else:                            
                                view = ConfirmCancel(ctx.author)
                                await ctx.send(f"Are you sure you want to unlock another slot? For **{price}dc**",view = view)

                                await view.wait()

                                if view.value == True:
                                    clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())
                                    if clan[0]['dc'] < price:
                                        await ctx.send(f"Your clan don't have enough dc for the next slot! You need **{price}dc** for the next slot.")
                                        return
                                    else:
                                        pass 

                                    if clan[0]['tier'] < tier:
                                        await ctx.send(f"Your clan need to be at a higher tier for this slot!")
                                        return
                                    else:
                                        pass 
                                    await self.bot.db.execute(f'UPDATE clans SET dc = dc - {price}, slots = slots + 1 WHERE clan_name = $1', clan_name.title())
                                    await ctx.send(f"Upgraded to **{nexttier}** slots for **{clan_name.title()}**.")

                                elif view.value == False:
                                    await ctx.send("Cancelled")
                                else:
                                    await ctx.send("Timed out.")
                        
                    else:
                        await ctx.send("You're not a leader!")
            else:
                await ctx.send("You're not in a clan!")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.group(name = 'war', aliases = ['wr'], invoke_without_command = True)
    async def war_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if registered_check:
            em1 = discord.Embed(
                title = 'Wars [Aliases: wr]',
                description = 'Commands related to wars:',
                colour = color
            )

            em1.add_field(name = 'd!wars', value = 'View all the current wars.',inline=False)

            em1.add_field(name = 'd!war queue', value = 'Queue your clan for war.',inline=False)

            em1.add_field(name = 'd!war start', value = 'Start a war.')

            em1.add_field(name = 'd!war settings', value = 'View your war settings.',inline=False)

            em1.add_field(name = 'd!war change', value = 'Change the war settings.',inline=False)

            em1.add_field(name = 'd!war add', value = 'Add war participants for your clan.',inline=False)

            em1.add_field(name = 'd!war replace', value = 'Substitute members in a war.',inline=False)

            em1.add_field(name = 'd!war extend', value = 'Extend a war *(Admin exclusive)*',inline=False)

            em1.add_field(name = 'd!war cancel', value = 'Cancel a war *(Admin exclusive)*',inline=False)

            em1.add_field(name = 'd!war reset', value = 'Reset queue for a clan *(Admin exclusive)*',inline=False)

            await ctx.send(embed = em1)
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @war_command.command(name = 'cancel')
    async def forfeiasdt_command(self,ctx, warid = None):
        guild = self.bot.get_guild(774883579472904222)
        role = guild.get_role(786448967172882442)
        role2 = guild.get_role(1090438349455622204)
        role3 = guild.get_role(781452019578961921)
        if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles):
            if warid == None:
                em = discord.Embed(
                    title = "Help 🛠️",
                    description = '**d!war cancel [War ID]**',
                    colour = color
                )
                await ctx.send(embed = em)
                
            else:
                registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                if registered_check:
                    if self.faction.count_documents({"_id": warid}, limit = 1):
                        view = ConfirmCancel(ctx.author)
                        await ctx.send (f'{ctx.author.mention} Are you sure?', view = view)
                        await view.wait()
                        if view.value == True:

                            ready = 'False'

                            clans = await self.bot.db.fetch('SELECT * FROM clans WHERE ready_for_war = $1', warid) 
     
                            if clans:
                                await self.bot.db.execute('UPDATE clans SET ready_for_war = $1 WHERE clan_name = $2', ready, clans[0]['clan_name'])
                                await self.bot.db.execute('UPDATE clans SET ready_for_war = $1 WHERE clan_name = $2', ready, clans[1]['clan_name'])
                                await self.bot.db.execute('UPDATE clans SET warmembers = NULL WHERE clan_name = $1', clans[0]['clan_name'])
                                await self.bot.db.execute('UPDATE clans SET warmembers = NULL WHERE clan_name = $1', clans[1]['clan_name'])          
                            else:
                                pass    
                                          
                            self.faction.delete_one({"_id": warid})
                            await ctx.send("War cancelled.")
                        elif view.value == False:
                            await ctx.send("Cancelled.")
                        else:
                            await ctx.send('Timed out.')
                    else:
                        await ctx.send("Incorrect War ID.")
                else:
                    await ctx.send("You haven't registered yet! do `d!start` to register.")
        else:
            await ctx.send("You can't use this command!")

    @war_command.command(name = 'reset')
    async def cancelone(self,ctx, warid = None):
        guild = self.bot.get_guild(774883579472904222)
        role = guild.get_role(786448967172882442)
        role2 = guild.get_role(1090438349455622204)
        role3 = guild.get_role(781452019578961921)
        if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles):
            if warid == None:
                em = discord.Embed(
                    title = "Help 🛠️",
                    description = '**d!war reset [War ID]**',
                    colour = color
                )
                await ctx.send(embed = em)
                
            else:
                registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                if registered_check:
                    clans = await self.bot.db.fetch('SELECT * FROM clans WHERE ready_for_war = $1', warid)   
                    if clans:
                        view = ConfirmCancel(ctx.author)
                        await ctx.send (f'{ctx.author.mention} Are you sure?', view = view)
                        await view.wait()
                        if view.value == True:

                            ready = 'False'

                            clans = await self.bot.db.fetch('SELECT * FROM clans WHERE ready_for_war = $1', warid)       

                            await self.bot.db.execute('UPDATE clans SET ready_for_war = $1 WHERE clan_name = $2', ready, clans[0]['clan_name'])
                            await self.bot.db.execute('UPDATE clans SET ready_for_war = $1 WHERE clan_name = $2', ready, clans[1]['clan_name'])
                            await self.bot.db.execute('UPDATE clans SET warmembers = NULL WHERE clan_name = $1', clans[0]['clan_name'])
                            await self.bot.db.execute('UPDATE clans SET warmembers = NULL WHERE clan_name = $1', clans[1]['clan_name'])    

                            await ctx.send("War cancelled.")
                        elif view.value == False:
                            await ctx.send("Cancelled.")
                        else:
                            await ctx.send('Timed out.')
                    else:
                        await ctx.send("Incorrect War ID.")
                else:
                    await ctx.send("You haven't registered yet! do `d!start` to register.")
        else:
            await ctx.send("You can't use this command!")


    @war_command.command(name = 'settings', aliases = ['s'])
    async def warstafdadfffarq_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        clan_name = registered_check[0]['clan_1']

        if registered_check:
            if clan_name:

                if (clan_name is None):
                    em = discord.Embed(
                        title = 'War',
                        description = '**Check your war settings**\n\nd!war settings',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                    if not clan:
                        await ctx.send(f'{clan_name.title} is not a registered clan.')

                    else:
                        admins = clan[0]['leaders']
                        admins_list = self.listing(admins)
                        if int(ctx.author.id) in admins_list:
                            if (clan[0]['ready_for_war'] == 'False') or (clan[0]['ready_for_war'] == 'True'):
                                await ctx.send("Your clan isn't in a war.")
                                return
                            else:
                                pass
                            warid = clan[0]['ready_for_war']
                            clans = await self.bot.db.fetch('SELECT * FROM clans WHERE ready_for_war = $1', warid)

                            preference = clan[0]['preference']
                            ft = preference.split()[2]
                            em = discord.Embed(
                                title = f"{clans[0]['clan_name']} VS {clans[1]['clan_name']}",
                                description = f'Battle Royale - First to **{int(ft)}**',
                                colour = color
                            )
                            check1 = clans[0]['warmembers']
                            check1 = check1.split()
                            clan1list = ''
                            for i in check1:
                                if i == '0':
                                    pass
                                else:
                                    clan1list += f'<@{i}>'

                            check2 = clans[1]['warmembers']
                            check2 = check2.split()
                            clan2list = ''
                            for i in check2:
                                if i == '0':
                                    pass
                                else:
                                    clan2list += f'<@{i}>'
                            if clan1list == None:
                                clan1list = 'None added'
                            if clan2list == None:
                                clan2list = 'None added'
                            em.add_field(name=f"{clans[0]['clan_name']} Members | MAX {preference[3]}", value= clan1list)
                            em.add_field(name=f"{clans[1]['clan_name']} Members | MAX {preference[3]}", value= clan2list)
                            em.set_footer(text='Start the war using *d!war start*')

                            await ctx.send(embed = em)


                        else:
                            await ctx.send("You're not a leader!")
            else:
                await ctx.send("You're not in a clan!")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @war_command.command(name = 'start')
    async def warstartrq_command(self, ctx, member : discord.Member = None ,*, stringthey = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        clan_name = registered_check[0]['clan_1']

        if registered_check:
            if clan_name:

                if (clan_name is None) or (member is None) or (stringthey is None):
                    em = discord.Embed(
                        title = 'War',
                        description = '**Start a war**\n\nd!war start [mention opponent leader] [special remarks ex: No gen9 p0]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                    if not clan:
                        await ctx.send(f'{clan_name.title} is not a registered clan.')

                    else:

                        admins = clan[0]['leaders']
                        admins_list = self.listing(admins)

                        if int(ctx.author.id) in admins_list:
                            if (clan[0]['ready_for_war'] == 'False') or (clan[0]['ready_for_war'] == 'True'):
                                await ctx.send("Your clan isn't in a war.")
                                return
                            else:
                                pass

                            warid = clan[0]['ready_for_war']
                            clans = await self.bot.db.fetch('SELECT * FROM clans WHERE ready_for_war = $1', warid)
                            if clans[0]['clan_name'] == clan[0]['clan_name']: 
                                clan3 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clans[1]['clan_name'])
                            else:
                                clan3 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clans[0]['clan_name'])

                            sadmins = clan3[0]['leaders']
                            sadmins_list = self.listing(sadmins)
                            if int(member.id) in sadmins_list:
                                pass
                            else:
                                await ctx.send("The person you mentioned isn't a leader in the opposing clan.")
                                return



                            alist = clans[0]['warmembers']
                            aalist = alist.split()
                            alliesList = [int(x) for x in aalist]
                            faction_name = clans[0]['clan_name']

                            elist = clans[1]['warmembers']
                            eelist = elist.split()
                            enemiesList = [int(x) for x in eelist]                            
                            efaction_name = clans[1]['clan_name']

                            prefernce = clan[0]['preference']
                            winscore = prefernce.split()[2]
                            
                            warmembers = clans[0]['warmembers']
                            
                            zero_count = warmembers.split().count('0')

                            if int(zero_count) >= 1:
                                await ctx.send(f"**{clans[0]['clan_name']}** still has vacant places!")
                                return
                            
                            warmembers = clans[1]['warmembers']
                            
                            zero_count = warmembers.split().count('0')

                            if int(zero_count) >= 1:
                                await ctx.send(f"**{clans[1]['clan_name']}** still has vacant places!")
                                return                           

                            enemyitems = len(enemiesList)
                            enemyscore = [0] * enemyitems
                            enemyscored = [0] * enemyitems
                            
                            allyitems = len(alliesList)
                            allyscore = [0] * allyitems
                            allyscored = [0] * allyitems
                            to = datetime.datetime.now(timezone.utc)
                            timenewe = int(time.mktime(to.timetuple()) + to.microsecond / 1E6)


                            view = ConfirmCancel(member)
                            await ctx.send(f'{member.mention} Are you sure? This will be a **BR** first to reach **{winscore}** wins between **{faction_name}** and **{efaction_name}**', view = view)
                            
                            await view.wait()

                            if view.value is True: 
                                powerups = 'no'                                                                          

                                time_change = datetime.timedelta(days=7)
                                t = datetime.datetime.now(timezone.utc) + time_change
                                timenew = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
                                enemiesListname = ''
                                alliesListname = ''


                                for i in alliesList:
                                        
                                    nun  = await self.bot.fetch_user(i)
                                    alliesListname += f"`{nun.name}` "
                                    reg_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', i)
                                    if (reg_check[0]['clan_1'] == faction_name):
                                        pass
                                    else:
                                        pass


                                oppmemberStr = ""
                                for i in enemiesList:
                                    nun  = await self.bot.fetch_user(i)
                                    enemiesListname += f"`{nun.name}` "
                                warid = clan[0]['ready_for_war']
                                history = []
                                power = '97551132211'
                                self.faction.insert_one({"_id": warid, "allyscore": 0, "enemyscore" : 0, "allymembers": alliesList, "enemymembers": enemiesList,"allymembersname": alliesListname, "enemymembersname": enemiesListname, "allyplayerscored": allyscored, "enemyplayerscored": enemyscored,"allyplayerscore": allyscore, "enemyplayerscore": enemyscore, "winscore" : int(winscore), "time" : timenew,"teamone": faction_name, "teamtwo":efaction_name,  "faction": True, "wartype": 'br',"history": history,"powerups": powerups, "1powerup": power, "2powerup" : power })
                                allymemberStr = ""
                                for i in alliesList:
                                        allymemberStr += f"<@{i}> "
                                oppmemberStr = ""
                                for i in enemiesList:
                                        oppmemberStr += f"<@{i}> "
                                war = discord.Embed(
                                title = f"⚔️ {faction_name} VS {efaction_name} First to get {winscore} wins",
                                description = f'To log wins do d!wlog **{warid}** [Opponent]\nd!viewwar **{warid}** to view this war.',
                                colour = color
                                )
                                war.add_field(name = f'{faction_name}', value = allymemberStr, inline=False)
                                war.add_field(name = f'{efaction_name}', value = oppmemberStr, inline=False)
                                war.add_field(name = f'Special Remarks', value= stringthey, inline=False)
                                war.set_footer(text = f'Ends in 7 Day(s).')
                                channel = self.bot.get_channel(807513833554968576)
                                mentions = f'{allymemberStr}' +' ' + f'{oppmemberStr}'
                                await channel.send(f"{mentions}",embed = war)
                            
                            elif view.value is False:
                                await ctx.send("Denied.")
                            else:
                                await ctx.send("Timed out.")


                        else:
                            await ctx.send("You're not a leader!")
            else:
                await ctx.send("You're not in a clan!")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')


    @war_command.command(name = 'change')
    async def warsettings_command(self, ctx, member : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        clan_name = registered_check[0]['clan_1']

        if registered_check:
            if clan_name:

                if (clan_name is None) or (member is None):
                    em = discord.Embed(
                        title = 'War',
                        description = '**Change your war settings**\n\nd!war change [opponent leader mention]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                    if not clan:
                        await ctx.send(f'{clan_name.title} is not a registered clan.')

                    else:
                        warid = clan[0]['ready_for_war']
                        clans = await self.bot.db.fetch('SELECT * FROM clans WHERE ready_for_war = $1', warid)
                        if clans[0]['clan_name'] == clan[0]['clan_name']: 
                            clan3 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clans[1]['clan_name'])
                        else:
                            clan3 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clans[0]['clan_name'])

                        sadmins = clan3[0]['leaders']
                        sadmins_list = self.listing(sadmins)
                        if int(member.id) in sadmins_list:
                            pass
                        else:
                            await ctx.send("The person you mentioned isn't a leader in the opposing clan.")
                            return
                        admins = clan[0]['leaders']
                        admins_list = self.listing(admins)

                        if int(ctx.author.id) in admins_list:
                            if (clan[0]['ready_for_war'] == 'False') or (clan[0]['ready_for_war'] == 'True'):
                                await ctx.send("Your clan isn't in a war.")
                                return
                            else:
                                pass
                            view = ConfirmChange(ctx.author)
                            await ctx.send("What would you like to change?", view = view)
                            await view.wait()

                            if view.value is True:  
                                tochange = 'Win Score'
                            elif view.value is False:
                                tochange = 'Player Count'
                            else:
                                await ctx.send('Timed out.')
                                return


                            await ctx.send(f"Please enter the new value for **{tochange}**")
                            try:
                                enemies = await self.bot.wait_for(
                                    'message',
                                    timeout = 15,
                                    check = lambda message: message.author == ctx.author and message.channel == ctx.channel
                                )

                            except asyncio.TimeoutError:
                                await ctx.send('Timed-out.')

                            else:
                                try:
                                    int(enemies.content)
                                    pass
                                except ValueError:
                                    await ctx.send("Please only send numerical values.")
                                    return
                                enemies = int(enemies.content)
                                if tochange == 'Win Score':
                                    if enemies > 150:
                                        await ctx.send("You can't have a **Win Score** of more than 150!")
                                        return
                                    elif enemies < 40:
                                        await ctx.send("You can't have a **Win Score** of less than 40!")
                                        return                                        
                                    else:
                                        preference = clan[0]['preference']
                                        splitted = preference.split()
                                        splitted[2] = str(enemies)
                                        result = ' '.join(splitted)
                                        view = ConfirmCancel(member)

                                        await ctx.send(f"Do you accept this change? {member.mention}", view = view)
                                        await view.wait()
                                        if view.value is True:
                                            await self.bot.db.execute('UPDATE clans SET preference = $1 WHERE preference = $2', result, preference)
                                            await ctx.send(f"The {tochange} was changed to **{enemies}**!")
                                        elif view.value is False:
                                            await ctx.send("Denied.")
                                        else:
                                            await ctx.send("Timed out")

                                    
                                elif tochange == 'Player Count':
                                    if enemies > 15:
                                        await ctx.send("You can't have a **Player Count** of more than 15!")
                                        return                                    
                                    elif enemies < 5:
                                        await ctx.send("You can't have a **Player Count** of less than 5!")
                                        return
                                    else:
                                        preference = clan[0]['preference']
                                        ogpref = int(preference[3])
                                        result = preference
                                        result_list = list(result)
                                        result_list[3] = str(enemies) 
                                        result = ''.join(result_list)
                                        
                                        numbers1 = clans[0]['warmembers']
                                        numbers1 = numbers1.split()
                                        actual1 = []
                                        no = 0

                                        if len(numbers1) < int(enemies):
                                            actual1 = numbers1
                                            while len(actual1) < int(enemies):
                                                actual1.append('0')

                                            
                                        else:
                                            for i in numbers1:
                                                actual1.append(i)
                                                no += 1
                                                if no == int(enemies):
                                                    break
                                        
                                        updated_string1 = ' '.join(actual1)                                        
 
                                        numbers2 = clans[1]['warmembers']
                                        numbers2 = numbers2.split()
                                        actual2 = []
                                        no = 0
                                        if len(numbers2) < int(enemies):
                                            actual2 = numbers2
                                            while len(actual2) < int(enemies):
                                                actual2.append('0')

                                        else:
                                            for i in numbers2:
                                                actual2.append(i)
                                                no += 1

                                                if no == int(enemies):
                                                    break

                                        updated_string2 = ' '.join(actual2)  

                                        view = ConfirmCancel(member)
                                        await ctx.send(f"Do you accept this change? {member.mention}", view = view)
                                        await view.wait()
                                        if view.value is True:
                                            clan1 = clans[0]['clan_name']
                                            clan2 = clans[1]['clan_name']
                                            await self.bot.db.execute('UPDATE clans SET warmembers = $1 WHERE clan_name = $2', updated_string2, clan2)
                                            await self.bot.db.execute('UPDATE clans SET warmembers = $1 WHERE clan_name = $2', updated_string1, clan1)
                                            await self.bot.db.execute('UPDATE clans SET preference = $1 WHERE ready_for_war = $2', result, warid)
                                            await ctx.send(f"The {tochange} was changed to **{enemies}**!")
                                        elif view.value is False:
                                            await ctx.send("Denied.")
                                        else:
                                            await ctx.send("Timed out")                                        

                        else:
                            await ctx.send("You're not a leader!")
            else:
                await ctx.send("You're not in a clan!")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @war_command.command(name = 'add', aliases = ['a'])
    async def warstafdadfarq_command(self, ctx, member : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        clan_name = registered_check[0]['clan_1']

        if registered_check:
            if clan_name:

                if (clan_name is None) or (member is None):
                    em = discord.Embed(
                        title = 'War',
                        description = '**Add a member to the war**\n\nd!war add [mention]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                    if not clan:
                        await ctx.send(f'{clan_name.title} is not a registered clan.')

                    else:

                        admins = clan[0]['leaders']
                        admins_list = self.listing(admins)

                        if int(ctx.author.id) in admins_list:
                            if (clan[0]['ready_for_war'] == 'False') or (clan[0]['ready_for_war'] == 'True'):
                                await ctx.send("Your clan isn't in a war.")
                                return
                            else:
                                pass
                            member_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)
                            if member_check:
                                if member_check[0]['clan_1'] == clan_name:
                                    pass
                                else:
                                    await ctx.send("The member you're trying to add is not in your clan!")
                                    return
                            else:
                                await ctx.send("The member you're trying to add has not registered!")
                                return


                            prefernce = clan[0]['preference']
                            warmembers = clan[0]['warmembers']
                            
                            zero_count = warmembers.split().count('0')
                            if str(member.id) in warmembers.split():
                                await ctx.send("This person is already in the war.")
                                return
                            
                            if int(zero_count) >= 1:

                                channelist = [1187774201810145361]
                                if ctx.channel.id not in channelist:
                                    await ctx.send("You can only use this command in <#1187774201810145361>")
                                    return
                                else:
                                    pass
                                view = ConfirmCancel(ctx.author)
                                await ctx.send(f'Are you sure you want to add **{member.name}**?', view = view)
                            
                                await view.wait()

                                if view.value is True:  
                                    if str(member.id) in warmembers.split():
                                        await ctx.send("This person is already in the war.")
                                        return

                                    
                                    wardd = 'war'
                                    await self.bot.db.execute(f'UPDATE registered SET clan_2 = $1 WHERE player_id = $2', wardd, member.id)


                                    parts = warmembers.split()
                                    index_of_zero = parts.index('0')
                                    parts[index_of_zero] = str(member.id)
                                    result_string = ' '.join(parts)
                                    await self.bot.db.execute('UPDATE clans SET warmembers = $1 WHERE clan_name = $2', result_string, clan_name.title())
                               
                                    await ctx.send(f"{member.mention} was added to the war.")
                                elif view.value is False:
                                    await ctx.send("Declined.")
                                else:
                                    await ctx.send("Timed Out.")





                            else:
                                await ctx.send("You already have the max amount of members added in this war, if you want to change this use the command `d!war change`.")


                        else:
                            await ctx.send("You're not a leader!")
            else:
                await ctx.send("You're not in a clan!")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @war_command.command(name = 'remove', aliases = ['r'])
    async def warafcadfarq_command(self, ctx, member : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        clan_name = registered_check[0]['clan_1']

        if registered_check:
            if clan_name:

                if (clan_name is None) or (member is None):
                    em = discord.Embed(
                        title = 'War',
                        description = '**Remove a member from the war**\n\nd!war remove [mention]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                    if not clan:
                        await ctx.send(f'{clan_name.title} is not a registered clan.')

                    else:

                        admins = clan[0]['leaders']
                        admins_list = self.listing(admins)

                        if int(ctx.author.id) in admins_list:
                            if (clan[0]['ready_for_war'] == 'False') or (clan[0]['ready_for_war'] == 'True'):
                                await ctx.send("Your clan isn't in a war.")
                                return
                            else:
                                pass
                            member_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)
                            if member_check:
                                pass
                            else:
                                await ctx.send("The member you're remove has not registered!")
                                return


                            prefernce = clan[0]['preference']
                            warmembers = clan[0]['warmembers']
                            
                            zero_count = warmembers.split().count(str(member.id))
                            if int(zero_count) == 0:
                                await ctx.send("The member you're trying to remove isn't in the war.")
                            else:
                                warcheck = member_check[0]['clan_2']

                                if warcheck == 'war':
                                    pass
                                elif warcheck == None:
                                    if member_check[0]['blade'] == clan[0]['ready_for_war']:
                                        await ctx.send("You cannot remove this user from this war as they are a **Blade**.")
                                        return
                                    else:
                                        pass
                                    await ctx.send("This member isn't in a war.")
                                    return
                                
                                if member_check[0]['blade'] == None:
                                    pass
                                else:
                                    if member_check[0]['blade'] == clan[0]['ready_for_war']:
                                        await ctx.send("You cannot remove this user from this war as they are a **Blade**.")
                                        return
                                    else:
                                        pass
                                
                                view = ConfirmCancel(ctx.author)
                                await ctx.send(f'{ctx.author.mention} would you like to remove this user from the war?', view = view)
                            
                                await view.wait()

                                if view.value is True:
                                    zero_count = warmembers.split().count(str(member.id))
                                    if int(zero_count) == 0:
                                        await ctx.send("The member you're trying to remove isn't in the war.")
                                    else:
                                        parts = warmembers.split()
                                        index_of_zero = parts.index(str(member.id))
                                        parts[index_of_zero] = '0'
                                        result_string = ' '.join(parts)
                                        await self.bot.db.execute(f'UPDATE registered SET clan_2 = NULL WHERE player_id = $1',member.id)
                                        await self.bot.db.execute('UPDATE clans SET warmembers = $1 WHERE clan_name = $2', result_string, clan_name.title())                         
                                        await ctx.send(f"{member.mention} was removed from the war.")
                                elif view.value is False:
                                    await ctx.send("Declined.")
                                    return
                                else:
                                    await ctx.send("Timed Out.")
                                    return



                        else:
                            await ctx.send("You're not a leader!")
            else:
                await ctx.send("You're not in a clan!")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @war_command.command(name = 'queue', aliases = ['q'])
    async def warstarq_command(self, ctx, pref : str = None, player : int = None, num : int = None, ):

        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        clan_name = registered_check[0]['clan_1']

        if registered_check:
            if clan_name:

                if (clan_name is None):
                    em = discord.Embed(
                        title = 'Clan',
                        description = '**Get your clan in war**\n\nd!war queue',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())

                    if not clan:
                        await ctx.send(f'{clan_name.title} is not a registered clan.')

                    else:


                        admins = clan[0]['leaders']
                        admins_list = self.listing(admins)

                        if int(ctx.author.id) in admins_list:
                            ready = clan[0]['ready_for_war']
                            if ready == 'True':
                                ready = 'False'
                                await self.bot.db.execute('UPDATE clans SET ready_for_war = $1 WHERE clan_name = $2', ready, clan_name.title())
                                mesage = await ctx.send(f'Dequeued.')     
                                await mesage.delete(delay=3)                   
                            elif ready == 'False':
                                ready = 'True'
                                clans = await self.bot.db.fetch('SELECT * FROM clans WHERE ready_for_war = $1', ready)
                                if clans:
                                    if pref == None:
                                        await ctx.send("You need to enter a format preference, **BR**, **KOTH**. `d!clan queue [format] [no. players] (if br)[wins]`")
                                        return
                                    elif player == None:
                                        await ctx.send("You need to enter the number of players you prefer. `d!clan queue [format] [no. players] (if br)[wins]`")
                                        return
                                    elif player < 5:
                                        await ctx.send("The number of players can't be lower than 5. `d!clan queue [format] [no. players] (if br)[wins]`")
                                        return
                                    elif player > 16:
                                        await ctx.send("The number of players can't be lower than 5. `d!clan queue [format] [no. players] (if br)[wins]`")
                                        return
                                    if pref == 'br':
                                        if num == None:
                                            await ctx.send("You need to enter the number of wins you prefer. `d!clan queue [format] [no. players] (if br)[wins]`")
                                            return
                                        elif num > 150:
                                            await ctx.send("The number of wins can't exceed 150. `d!clan queue [format] [no. players] (if br)[wins]`")
                                            return
                                    clan_opp = clans[0]['clan_name']

                                    if clans[0]['comeback'] == None:
                                        pass
                                    else:
                                        if clans[0]['comeback'] == clan[0]['clan_name']:
                                            await ctx.send("You've already played with the clan that's queued up... please wait for another clan to queue.")
                                            return
                                    if clan[0]['comeback'] == None:
                                        pass
                                    else:    
                                        if clan[0]['comeback'] == clans[0]['clan_name']:
                                            await ctx.send("You've already played with the clan that's queued up... please wait for another clan to queue.")
                                            return

                                    
                                    prefe = f'{pref.lower()} {player} {num}'

                                    
                                    ready = 'False'
                                    await self.bot.db.execute('UPDATE clans SET ready_for_war = $1 WHERE clan_name = $2', ready, clan_name.title())
                                    await self.bot.db.execute('UPDATE clans SET ready_for_war = $1 WHERE clan_name = $2', ready, clan_opp)
                                    clan_leader = clans[0]['leaders']
                                    leader_list = self.listing(clan_leader)
                                    sclan_leader = clan[0]['leaders']
                                    sleader_list = self.listing(sclan_leader)
                                    mentionlist = ''
                                    smentionlist = ''

                                    for i in leader_list:
                                        mentionlist += f' <@{i}>'
                                    for i in sleader_list:
                                        smentionlist += f' <@{i}>'

                                    clan_pref = prefe
                                    clan_preference = clan_pref.split(" ")
                                    clan_format = clan_preference[0]
                                    clan_player = int(clan_preference[1])
                                    if clan_preference[2] != 'None':
                                        clan_wins = int(clan_preference[2])
                                    else:
                                        clan_wins = None
                                    
                                    sclan_pref = clans[0]['preference']
                                    sclan_preference = sclan_pref.split(" ")
                                    sclan_format = sclan_preference[0]
                                    sclan_player = int(sclan_preference[1])
                                    if sclan_preference[2] != 'None':
                                        sclan_wins = int(sclan_preference[2])
                                    else:
                                        sclan_wins = None
                                    if sclan_format.lower() != clan_format.lower():
                                        formats = [sclan_format.lower(), clan_format.lower()]
                                        formats = random.choice(formats)
                                    else:
                                        formats = clan_format.lower()
                                    if sclan_player != clan_player:
                                        players = (sclan_player + clan_player)/2
                                        members = list(self.collection.find( {"_id": clan_name.title()}, {"_id": 0, "members": 1}))
                                        clanint = len(members[0]["members"])
                                        smembers = list(self.collection.find( {"_id": clan_opp.title()}, {"_id": 0, "members": 1}))
                                        sclanint = len(smembers[0]["members"])
                                        if (players > clanint):
                                            players = clanint
                                        elif (players > sclanint):
                                            players = sclanint
                                        else:
                                            pass
                                    else:
                                        players = clan_player
                                    
                                    warid = await id_generator()
                                    if clan_wins == None:
                                        wins = sclan_wins
                                    elif sclan_wins == None:
                                        wins = clan_wins
                                    else:
                                        wins = (sclan_wins + clan_wins)/2
                                    
                                    warmemberslist = [0] * int(players)
                                    zeros_string = ' '.join(map(str, warmemberslist))

                                    zeros_string1 = zeros_string
                                    zeros_string2 = zeros_string
                                    opt1 = clan[0]['opted']
                                    opt2 = clans[0]['opted']

                
                                    if opt1 != opt2:
                                        sad = ['True', 'False']
                                        opted = random.choice(sad)
                                    else:
                                        opted = opt1

                                    if opted != 'False':

                                        inq = 'True'
                                        war = await self.bot.db.fetch('SELECT * FROM wars WHERE inq = $1 ORDER BY added ASC', inq)
                                        correctlist = []
                                        flag = False
                                        for i in war:
                                            check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', i['player_id'])
                                            if check[0]['clan_1'] == None:
                                                correctlist.append(check[0]['player_id'])
                                            else:

                                                if (check[0]['clan_1'] == clan_name.title()) or (check[0]['clan_1'] == clan_opp):
                                                    pass
                                                else:
                                                    correctlist.append(check[0]['player_id'])

                                            if len(correctlist) == 2:
                                                flag = True
                                                break
                                        
                                        if flag == True:
                                            if int(players) == 10:
                                                newstring = zeros_string.split()
                                                newstring[0] = correctlist[0] 
                                                zeros_string1 = ' '.join(newstring)

                                                newstring = zeros_string.split()
                                                newstring[0] = correctlist[1] 
                                                zeros_string2 = ' '.join(newstring)
                                                players = int(players)                                           
                                            else:
                                                zeros_string1 = f'{correctlist[0]} {zeros_string}'
                                                zeros_string2 = f'{correctlist[1]} {zeros_string}'
                                                players = int(players) + 1

                                            preference = f'br {int(players)} {int(wins)}'
                                            await self.bot.db.execute('UPDATE registered SET blade = $1 WHERE player_id = $2', warid, correctlist[0])
                                            await self.bot.db.execute('UPDATE registered SET blade = $1 WHERE player_id = $2', warid, correctlist[1])
                                            
                                            await self.bot.db.execute('UPDATE wars SET inq = NULL, added = NULL WHERE player_id = $1', correctlist[0])
                                            await self.bot.db.execute('UPDATE wars SET inq = NULL, added = NULL WHERE player_id = $1', correctlist[1])

                                            extra = f'Blades Chosen! **{clan_name}** With <@{correctlist[0]}> | **{clan_opp}** With <@{correctlist[1]}>\n'
                                            member1  = await self.bot.fetch_user(correctlist[0])
                                            member2  = await self.bot.fetch_user(correctlist[1])
                                            try:
                                                await member1.send(f"You have been selected as a blade for **{clan_name}**.")
                                            except Exception as e:
                                                pass                                             
                                            try:
                                                await member2.send(f"You have been selected as a blade for **{clan_opp}**.")
                                            except Exception as e:
                                                pass                                             

                                        else:
                                            preference = f'br {int(players)} {int(wins)}'
                                            extra = ''
                                    else:
                                        extra = ''
                                        preference = f'br {int(players)} {int(wins)}'

                                    await self.bot.db.execute('UPDATE clans SET ready_for_war = $1, preference = $2, warmembers = $3 WHERE clan_name = $4', warid, preference, zeros_string1, clan_name.title())
                                    await self.bot.db.execute('UPDATE clans SET ready_for_war = $1, preference = $2, warmembers = $3 WHERE clan_name = $4', warid, preference, zeros_string2,  clan_opp)
                                    channel = self.bot.get_channel(1187774201810145361)

                                    if formats == 'br':

                                        await channel.send(f"Opponent Clan found! The war will be.. **{clan_name}** VS **{clan_opp}**\n\n**{clan_opp}**:{mentionlist}\n\n**{clan_name}**:{smentionlist}\n\nFormat will be : **{formats.title()}**\nNumber of Players : **{int(players)}vs{int(players)}**\n{extra}\nFirst to : **{int(wins)}**\n\nFor more war commands use `d!war` | **WAR ID : {warid}** ")

                                    else:
                                        await channel.send(f"Opponent Clan found! The war will be.. **{clan_name}** VS **{clan_opp}**\n\n**{clan_opp}**:{mentionlist}\n\n**{clan_name}**:{smentionlist}\n\nFormat will be : **{formats.title()}**\nNumber of Players : **{int(players)}vs{int(players)}**\n\nFor more war commands use `d!war` | **WAR ID : {warid}** ")
                                else: 
                                    ready = 'True'
                                    if pref == None:
                                        await ctx.send("You need to enter a format preference, **BR**, **KOTH**. `d!clan queue [format] [no. players] (if br)[wins]`")
                                        return
                                    elif player == None:
                                        await ctx.send("You need to enter the number of players you prefer. `d!clan queue [format] [no. players] (if br)[wins]`")
                                        return
                                    elif player < 5:
                                        await ctx.send("The number of players can't be lower than 5. `d!clan queue [format] [no. players] (if br)[wins]`")
                                        return
                                    if pref == 'br':
                                        if num == None:
                                            await ctx.send("You need to enter the number of wins you prefer. `d!clan queue [format] [no. players] (if br)[wins]`")
                                            return
                                        elif num > 150:
                                            await ctx.send("The number of wins can't exceed 150. `d!clan queue [format] [no. players] (if br)[wins]`")
                                            return

                                    prefe = f'{pref.lower()} {player} {num}'

                                    await self.bot.db.execute('UPDATE clans SET ready_for_war = $1, preference = $2 WHERE clan_name = $3', ready,prefe, clan_name.title())
                                    message = await ctx.send(f'Queued up!')
                                    await ctx.message.delete()
                                    await message.delete(delay=3)
                            else:
                                clan = await self.bot.db.fetch('SELECT * FROM clans WHERE ready_for_war = $1', ready)
                                await ctx.send(f"You are already in a war! Please complete that war first before you queue again.")
                                    


                        else:
                            await ctx.send("You're not a leader!")
            else:
                await ctx.send("You're not in a clan!")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @war_command.command(name='replace')
    async def log_faffdadn_command(self,ctx,warid =None, opponent1 : discord.Member = None, replace2 : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if registered_check:

            if (warid == None) or (opponent1 == None) or (replace2 == None) :
                em = discord.Embed(
                    title = "Help 🛠️",
                    description = '**d!war replace warid [tobereplaced] [substitute]**',
                    colour = color
                )
                await ctx.send(embed = em)
            
            else:
                if self.faction.count_documents({"_id": warid}, limit = 1):

                    war_data = self.faction.find_one({"_id": warid}, {
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
                        "allyplayerscored": 1,
                        "enemymembers": 1,
                        "enemyplayerscored": 1,
                        "enemyplayerscore": 1,
                        'wartype': 1
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
                    formats = war_data['wartype']

                    guild = self.bot.get_guild(774883579472904222)
                    role = guild.get_role(786448967172882442)
                    role2 = guild.get_role(1090438349455622204)
                    role3 = guild.get_role(781452019578961921)

                    clan1 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(faction_name.title()))
                    admins = clan1[0]['leaders']
                    admins_list = self.listing(admins)  


                    clan2 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(efaction_name.title()))
                    admins2 = clan2[0]['leaders']
                    admins_list2 = self.listing(admins2)    

                    if registered_check[0]['clan_1'] == clan1[0]['clan_name']:
                        list3 = admins_list
                    else:
                        list3 = admins_list2
                    if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles) or (int(ctx.author.id) in list3):

                        if (opponent1.id in allymembers) or (opponent1.id in enemymembers):
                            pass
                        else:
                            await ctx.send("The player you want to be replaced isn't in the war.")
                            return
                        
                        if opponent1 == replace2:
                            await ctx.send("You need 2 different players.")
                            return
                        member_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', replace2.id)
                        other_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', opponent1.id)
                        if other_check[0]['clan_2'] == None:
                            othercheck = 'n'
                        else:
                            othercheck = other_check[0]['clan_2']
                        if other_check[0]['blade'] == None:
                            bladecheck = 'n'
                        else:
                            bladecheck = other_check[0]['blade']                        
                        if self.faction.count_documents({"_id": warid, "enemymembers": opponent1.id,}, limit = 1):
                            
                            if warid == bladecheck:
                                await ctx.send("You can't replace a Blade!")
                                return
                            else:                           
                                if efaction_name == member_check[0]['clan_1']:
                                    pass
                                else:
                                    await ctx.send("That person is not in the clan!")
                                    return

                            if efaction_name == registered_check[0]['clan_1']:
                                pass
                            else:
                                await ctx.send("You are not in that clan!")
                                return

                            view = ConfirmCancel(ctx.author)
                            await ctx.send(f"Are you sure? **{opponent1.name}** will be replaced by **{replace2.name}**", view = view)
                            await view.wait()

                            if view.value == True:
                                pass
                            elif view.value == False:
                                await ctx.send("Cancelled.")
                                return
                            else:
                                await ctx.send("Timed out.")
                                return
                            war = 'war'
                            await self.bot.db.execute('UPDATE registered SET clan_2 = $1 WHERE player_id = $2', war, replace2.id)
                            await self.bot.db.execute('UPDATE registered SET clan_2 = NULL WHERE player_id = $1', opponent1.id)

                            actualenemy = []
                            for i in enemymembers:
                                actualenemy.append(i)
                            indexenemy = actualenemy.index(opponent1.id)
                            actualenemy = war_data["enemymembers"]
                            actualenemy[indexenemy] = replace2.id
                            enemyscore[indexenemy] = 0
                            enemyscored[indexenemy] = 0

                            self.faction.update_one({"_id":warid}, {"$set": {"enemymembers": actualenemy}})
                            self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscored": enemyscored}})
                            self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscore": enemyscore}})

                            await ctx.send("Replaced!")
                            channel = self.bot.get_channel(1093609140921843802)
                            await channel.send(f'{opponent1.mention} Was Replaced by {replace2.mention} in War **{warid}** \n\n*-By {ctx.author.mention}*')
                        else:
                            if warid == bladecheck:
                                await ctx.send("You can't replace a Blade!")
                                return
                            else: 
                                if faction_name == member_check[0]['clan_1']:
                                    pass
                                else:
                                    await ctx.send("That person is not in the clan!")
                                    return
                            
                            if faction_name == registered_check[0]['clan_1']:
                                pass
                            else:
                                await ctx.send("You are not in that clan!")
                                return                            

                            view = ConfirmCancel(ctx.author)
                            await ctx.send(f"Are you sure? **{opponent1.name}** will be replaced by **{replace2.name}**", view = view)
                            await view.wait()

                            if view.value == True:
                                pass
                            elif view.value == False:
                                await ctx.send("Cancelled.")
                                return
                            else:
                                await ctx.send("Timed out.")
                                return

                            war = 'war'

                            await self.bot.db.execute('UPDATE registered SET clan_2 = $1 WHERE player_id = $2', war, replace2.id)
                            await self.bot.db.execute('UPDATE registered SET clan_2 = NULL WHERE player_id = $1', opponent1.id)

                            actualenemy = []
                            for i in allymembers:
                                actualenemy.append(i)
                            indexenemy = actualenemy.index(opponent1.id)
                            actualenemy = war_data["allymembers"]
                            actualenemy[indexenemy] = replace2.id

                            allyscore[indexenemy] = 0
                            allyscored[indexenemy] = 0

                            self.faction.update_one({"_id":warid}, {"$set": {"allymembers": actualenemy}})  
                            self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscored": allyscored}})
                            self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscore": allyscore}})
                            
                            await ctx.send("Replaced!")   
                            channel = self.bot.get_channel(1093609140921843802)
                            await channel.send(f'{opponent1.mention} Was Replaced by {replace2.mention} in War **{warid}** \n\n*-By {ctx.author.mention}*')
                    else:
                        await ctx.send("You don't have permission to use this command.")                   

                else:                       
                    await ctx.send(f"Incorrect War ID.")
        else:
            await ctx.send("Register first.")  

def setup(bot):
    bot.add_cog(ClanCommands(bot))