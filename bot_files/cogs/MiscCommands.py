import asyncio
from http.client import OK
import discord
from discord.ext import commands
import random
import time
import math
import string
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from io import BytesIO
from datetime import datetime, timedelta
from functools import lru_cache


color = 0x32006e

@lru_cache(maxsize=None)
async def get_image_file(filename):
    # Load image file from disk
    with open(filename, 'rb') as f:
        return f.read()


class Tryout(discord.ui.View):
    def __init__(self, member : discord.Member):
        super().__init__(timeout = 15)

        self.value = None
        self.member = member

    @discord.ui.button(label = "Try out", style = discord.ButtonStyle.red, emoji = "🎩" )
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

class Filters(discord.ui.View):
    def __init__(self, member : discord.Member):
        super().__init__(timeout = 15)

        self.value = None
        self.member = member
        self.checks = []


        
    @discord.ui.select(placeholder="Select filters..", min_values=1, max_values=9,options=[
                           discord.SelectOption(label="SS", value="ss"),discord.SelectOption(label="S", value="s"),discord.SelectOption(label="A", value="a"),discord.SelectOption(label="B", value="b"),discord.SelectOption(label="C", value="c"),discord.SelectOption(label="d", value="D"),discord.SelectOption(label="Not Owned", value="notowned"),discord.SelectOption(label="Purchasable ", value="purchaseable"),discord.SelectOption(label="Non-Purchasable", value="nonpurchasable")])
    async def sort_dropdown(self, select: discord.ui.Select, interaction: discord.Interaction):
        await interaction.response.defer()
        for i in select.values:
            self.checks.append(i)
        self.value = self.checks
        self.sort_dropdown.disabled = True

        await interaction.edit_original_response(view = self)


    @discord.ui.select(placeholder="Select a sorting method..", min_values=1, max_values=1,options=[
                           discord.SelectOption(label="Price Ascending", value="price+"),discord.SelectOption(label="Price Descending", value="price-"),discord.SelectOption(label="Rarity Ascending", value="rarity+"),discord.SelectOption(label="Rarity Descending", value="rarity-")])
    async def filter_dropdown(self, select: discord.ui.Select, interaction: discord.Interaction):
        await interaction.response.defer()
        for i in select.values:
            
            self.checks.append(i)
        self.value = self.checks

        self.filter_dropdown.disabled = True
        await interaction.edit_original_response(view = self)

    @discord.ui.button(label = "Save", style = discord.ButtonStyle.green)
    async def confirm_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = self.checks
        self.stop()
                
        for i in self.children:
            i.disabled = True


    async def interaction_check(self, interaction : discord.Interaction):
        return interaction.user == self.member
                                        
    async def on_timeout(self):
        self.value = None

        for i in self.children:
            i.disabled = True

        self.stop()



class bannersembed(discord.ui.View):
    def __init__(self, member : discord.Member, registered_check : str, bot, ctx):
        super().__init__(timeout = 120)

        self.value = None
        self.member = member
        self.registered_check = registered_check
        self.bot = bot
        self.ctx = ctx
        self.items = ['banner', 'border', 'avaborder']

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


    @discord.ui.button(label = "Banners", style = discord.ButtonStyle.red)
    async def Banners_button(self, button: discord.Button, interaction : discord.Interaction):
        await interaction.response.defer()

        stat = 'banners'
        stats = 'banners'
        lists = 'banner_list'
        name = 'banner_name'
          
        lb = await self.bot.db.fetch(f'SELECT * FROM {stats}')

            
        my_lb = self.listing(self.registered_check[0][lists])
        data = []
        

        for faction in lb:
            data.append(faction[name])
        
        pagination_view = RPaginationView()
        pagination_view.data = data
        pagination_view.lb = lb
        pagination_view.my_lb = my_lb
        pagination_view.stat = stat
        pagination_view.category = self.ctx
        pagination_view.registered_check = self.registered_check    

        await pagination_view.send(self.ctx, self.member, self.bot)
        while pagination_view.value is None:
            await asyncio.sleep(1)

        self.items[0] = pagination_view.value   

        em = discord.Embed(
                title = 'Item Catalog',
                description = '',
                colour = color
        )
        
        itemlist = ''

        em.set_footer(text=f'{itemlist}')

        if self.items[0] == 'banner':
            profile = Image.open("default.png")

            
        else:                                                    
            banner = await self.bot.db.fetch('SELECT * FROM banners WHERE banner_name = $1', self.items[0])
            banneris = banner[0]["banner_place"]
            profile = Image.open(banneris)
            itemlist += f'{self.items[0]} Banner \\'


            

        titleis = 'Player'
            

            
                        
        if self.items[1] == 'border':
            borderis = Image.open("profile1.png")
            
        else:
        
            border = await self.bot.db.fetch('SELECT * FROM borders WHERE border_name = $1', self.items[1])
            borderis = f'{border[0]["border_place"]}'
            borderis = Image.open(borderis)
            itemlist += f'{self.items[1]} Border'

        borderis = borderis.convert('RGBA')
        if self.items[2] == 'avaborder':
            avaborderis = Image.open("profile2.png")
            
        else:
        
            avaborder = await self.bot.db.fetch('SELECT * FROM avatar_borders WHERE banner_name = $1', self.items[2])
            avaborderis = f'{avaborder[0]["avatar_place"]}'
            avaborderis = Image.open(avaborderis)

            if itemlist == '':
                itemlist += f'{self.items[1]} AvaBorder'
            else:
                itemlist += f'\ {self.items[1]} AvaBorder'
            
        
        avaborderis = avaborderis.convert('RGBA')
                                                        
        player_clan_1 = 'Clan | None'
        font = ImageFont.truetype("BebasNeue-Regular.ttf", 150)
        font2 =  ImageFont.truetype("BebasNeue-Regular.ttf", 70)
        font3 =  ImageFont.truetype("BebasNeue-Regular.ttf", 50)                  

        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', self.member.id)
        
        name = f'{self.member.display_name}'
        if len(name) > 15:
            name = name[:15] + ".."

        data = BytesIO(await self.member.display_avatar.read())
        pfp = Image.open(data)
        pfp.convert('RGBA')
        pfp = pfp.resize((300,300))
        mask_im = Image.new("L", pfp.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.rounded_rectangle((0, 0, 300, 300), fill=255,width=3, radius=15)
        

        guild = self.bot.get_guild(774883579472904222)
        role = guild.get_role(798548690860113982)
        
        if (role in self.member.roles) or (self.member.id == 924352653616635966):
            
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


        design = None
        des = 0
        comrank = f"Comm | Unranked "
        rarerank = f"Rares | Unranked "

        if des == 1:
            profile.paste(design, (0,0), design) 
        profile.paste(pfp, (40,30), mask_im)
        profile.paste(borderis, (0,0), borderis)
        profile.paste(avaborderis, (0,0), avaborderis)

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
                        
        em.set_image(url="attachment://rgb_img.png")
  

        await self.ctx.edit(file = dfile ,embed = em, view = self)
        


            
    @discord.ui.button(label = "Borders", style = discord.ButtonStyle.red)
    async def Borders_button(self, button: discord.Button, interaction : discord.Interaction):
        await interaction.response.defer()

        stat = 'borders'
        stats = 'borders'
        lists = 'border_list'
        name = 'border_name'

        lb = await self.bot.db.fetch(f'SELECT * FROM {stats}')

            
        my_lb = self.listing(self.registered_check[0][lists])
        data = []
        

        for faction in lb:
            data.append(faction[name])
        
        pagination_view = RPaginationView()
        pagination_view.data = data
        pagination_view.lb = lb
        pagination_view.my_lb = my_lb
        pagination_view.stat = stat
        pagination_view.category = self.ctx
        pagination_view.registered_check = self.registered_check    

        await pagination_view.send(self.ctx,self.member,self.bot)
        while pagination_view.value is None:
            await asyncio.sleep(1)

        self.items[1] = pagination_view.value   

        em = discord.Embed(
                title = 'Item Catalog',
                description = '',
                colour = color
        )
        
        itemlist = ''

        em.set_footer(text=f'{itemlist}')

        if self.items[0] == 'banner':
            profile = Image.open("default.png")

            
        else:                                                    
            banner = await self.bot.db.fetch('SELECT * FROM banners WHERE banner_name = $1', self.items[0])
            banneris = banner[0]["banner_place"]
            profile = Image.open(banneris)
            itemlist += f'{self.items[0]} Banner \\'


            

        titleis = 'Player'
            

            
                        
        if self.items[1] == 'border':
            borderis = Image.open("profile1.png")
            
        else:
        
            border = await self.bot.db.fetch('SELECT * FROM borders WHERE border_name = $1', self.items[1])
            borderis = f'{border[0]["border_place"]}'
            borderis = Image.open(borderis)
            itemlist += f'{self.items[1]} Border'

        borderis = borderis.convert('RGBA')
        if self.items[2] == 'avaborder':
            avaborderis = Image.open("profile2.png")
            
        else:
        
            avaborder = await self.bot.db.fetch('SELECT * FROM avatar_borders WHERE banner_name = $1', self.items[2])
            avaborderis = f'{avaborder[0]["avatar_place"]}'
            avaborderis = Image.open(avaborderis)

            if itemlist == '':
                itemlist += f'{self.items[1]} AvaBorder'
            else:
                itemlist += f'\ {self.items[1]} AvaBorder'
            
        
        avaborderis = avaborderis.convert('RGBA')
                                                        
        player_clan_1 = 'Clan | None'
        font = ImageFont.truetype("BebasNeue-Regular.ttf", 150)
        font2 =  ImageFont.truetype("BebasNeue-Regular.ttf", 70)
        font3 =  ImageFont.truetype("BebasNeue-Regular.ttf", 50)                  

        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', self.member.id)
        
        name = f'{self.member.display_name}'
        if len(name) > 15:
            name = name[:15] + ".."

        data = BytesIO(await self.member.display_avatar.read())
        pfp = Image.open(data)
        pfp.convert('RGBA')
        pfp = pfp.resize((300,300))
        mask_im = Image.new("L", pfp.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.rounded_rectangle((0, 0, 300, 300), fill=255,width=3, radius=15)
        

        guild = self.bot.get_guild(774883579472904222)
        role = guild.get_role(798548690860113982)
        
        if (role in self.member.roles) or (self.member.id == 924352653616635966):
            
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


        design = None
        des = 0
        comrank = f"Comm | Unranked "
        rarerank = f"Rares | Unranked "

        if des == 1:
            profile.paste(design, (0,0), design) 
        profile.paste(pfp, (40,30), mask_im)
        profile.paste(borderis, (0,0), borderis)
        profile.paste(avaborderis, (0,0), avaborderis)

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
                        
        em.set_image(url="attachment://rgb_img.png")
  

        await self.ctx.edit(file = dfile ,embed = em, view = self)

    @discord.ui.button(label = "AvaBorders", style = discord.ButtonStyle.red)
    async def AvaBorders_button(self, button: discord.Button, interaction : discord.Interaction):

        await interaction.response.defer()

        stat = 'avaborders'
        stats = 'avatar_borders'
        lists = 'avaborder_list'
        name = 'banner_name'
          
        lb = await self.bot.db.fetch(f'SELECT * FROM {stats}')

            
        my_lb = self.listing(self.registered_check[0][lists])
        data = []
        

        for faction in lb:
            data.append(faction[name])
        
        pagination_view = RPaginationView()
        pagination_view.data = data
        pagination_view.lb = lb
        pagination_view.my_lb = my_lb
        pagination_view.stat = stat
        pagination_view.category = self.ctx
        pagination_view.registered_check = self.registered_check    

        await pagination_view.send(self.ctx, self.member, self.bot)
        while pagination_view.value is None:
            await asyncio.sleep(1)

        self.items[2] = pagination_view.value   

        em = discord.Embed(
                title = 'Item Catalog',
                description = '',
                colour = color
        )
        
        itemlist = ''

        em.set_footer(text=f'{itemlist}')

        if self.items[0] == 'banner':
            profile = Image.open("default.png")

            
        else:                                                    
            banner = await self.bot.db.fetch('SELECT * FROM banners WHERE banner_name = $1', self.items[0])
            banneris = banner[0]["banner_place"]
            profile = Image.open(banneris)
            itemlist += f'{self.items[0]} Banner \\'


            

        titleis = 'Player'
            

            
                        
        if self.items[1] == 'border':
            borderis = Image.open("profile1.png")
            
        else:
        
            border = await self.bot.db.fetch('SELECT * FROM borders WHERE border_name = $1', self.items[1])
            borderis = f'{border[0]["border_place"]}'
            borderis = Image.open(borderis)
            itemlist += f'{self.items[1]} Border'

        borderis = borderis.convert('RGBA')
        if self.items[2] == 'avaborder':
            avaborderis = Image.open("profile2.png")
            
        else:
        
            avaborder = await self.bot.db.fetch('SELECT * FROM avatar_borders WHERE banner_name = $1', self.items[2])
            avaborderis = f'{avaborder[0]["avatar_place"]}'
            avaborderis = Image.open(avaborderis)

            if itemlist == '':
                itemlist += f'{self.items[1]} AvaBorder'
            else:
                itemlist += f'\ {self.items[1]} AvaBorder'
            
        
        avaborderis = avaborderis.convert('RGBA')
                                                        
        player_clan_1 = 'Clan | None'
        font = ImageFont.truetype("BebasNeue-Regular.ttf", 150)
        font2 =  ImageFont.truetype("BebasNeue-Regular.ttf", 70)
        font3 =  ImageFont.truetype("BebasNeue-Regular.ttf", 50)                  

        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', self.member.id)
        
        name = f'{self.member.display_name}'
        if len(name) > 15:
            name = name[:15] + ".."

        data = BytesIO(await self.member.display_avatar.read())
        pfp = Image.open(data)
        pfp.convert('RGBA')
        pfp = pfp.resize((300,300))
        mask_im = Image.new("L", pfp.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.rounded_rectangle((0, 0, 300, 300), fill=255,width=3, radius=15)
        

        guild = self.bot.get_guild(774883579472904222)
        role = guild.get_role(798548690860113982)
        
        if (role in self.member.roles) or (self.member.id == 924352653616635966):
            
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


        design = None
        des = 0
        comrank = f"Comm | Unranked "
        rarerank = f"Rares | Unranked "

        if des == 1:
            profile.paste(design, (0,0), design) 
        profile.paste(pfp, (40,30), mask_im)
        profile.paste(borderis, (0,0), borderis)
        profile.paste(avaborderis, (0,0), avaborderis)

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
                        
        em.set_image(url="attachment://rgb_img.png")
  

        await self.ctx.edit(file = dfile ,embed = em, view = self)

        
    async def interaction_check(self, interaction : discord.Interaction):
        return interaction.user == self.member
                                        
    async def on_timeout(self):
        self.value = None

        for i in self.children:
            i.disabled = True

class RPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 6
    numbre : int = 0
    value = None
    member = None
    bot = None
    filtered = None

    async def send(self, ctx, member, bot):
        self.member = member
        self.bot = bot
        self.message = await ctx.edit(view=self)
        await self.update_message(self.data[:self.sep],self.category, self.lb,self.my_lb, self.registered_check, self.stat)


        


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
        
    async def create_embed(self, data,category, lb,my_lb,stat, registered_check):
        my_lb = self.my_lb
        lb = self.lb
        stat = self.stat
        registered_check = self.registered_check
        stat = stat.lower()
        if (stat == 'titles') or (stat == 'title') or (stat == 't'):
            title = 'Title Catalog'
            desc = 'Filter using `SS`,`A`,`B`,`C`,`D` or search the item'
            name = 'banner_name'
            lists = 'banner_list'
        elif (stat == 'borders') or (stat == 'border')or (stat == 'bo'):
            stats = 'borders'
            name = 'border_name'
            title = 'Select a Border'
            place = 'border_place'
            lists = 'border_list'
            desc = ''     
        elif (stat == 'avaborders') or (stat == 'avaborder')or (stat == 'a'):
            stats = 'avatar_borders'
            name = 'banner_name'
            title = "Select an AvaBorder"
            place = 'avatar_place'
            lists = 'avaborder_list'
            desc = ''
        elif (stat == 'banner') or (stat == 'banners')or (stat == 'b'):
            stats = 'banners'
            name = 'banner_name'
            title = 'Select a Banner'
            place = 'banner_place'
            lists = 'banner_list'
            desc = ''
        else:
            name = 'banner_name'
            title = 'Select a Banner'
            desc = ''
        lb_embed = discord.Embed(
            title = title,
            description = desc,
            colour = 0x2e3035
        )
        category = None
        if category == None:
            if (stat == 'titles') or (stat == 'title') or (stat == 't'):
                for i in data:
                    if lb[self.numbre]["title_place"] in my_lb:
                        F = self.listing(registered_check[0]["title_list"])
                        T = int(F.index(lb[self.numbre]["title_place"])) + 1
                        ids = lb[self.numbre]["title_place"]
                        amt = F[T]
                        lb_embed.add_field(name = f'{lb[self.numbre]["banner_name"].title()} *Owned ✅*', value = f'Title ID | **{ids}**\nAmount | x**{amt}**')

                    else:
                        ids = lb[self.numbre]["title_place"]
                        lb_embed.add_field(name = f'{lb[self.numbre]["banner_name"].title()}', value = f'Title ID | **{ids}**\nNone Owned')
                    lb_embed.set_footer(text = f'Owned:{int((len(self.listing(registered_check[0]["title_list"]))/3))} Dc:{registered_check[0]["banner_pieces"]} Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')
                    self.numbre = self.numbre + 1
            else:
                banner_names = []
                othernumbre = 0   
                num = random.randint(1,4)
                profile = Image.open(f"shop{num}.png")

                if self.filtered == None:
                    pass
                else:
                    where = ''
                    ranks = []
                    shop = ''

                    if 'ss' in  self.filtered:
                        ranks.append('SS')
                    if 's' in  self.filtered:
                        ranks.append('S')
                    if 'a' in  self.filtered:
                        ranks.append('A')
                    if 'b' in  self.filtered:
                        ranks.append('B')
                    if 'c' in  self.filtered:
                        ranks.append('C')
                    if 'd' in  self.filtered:
                        ranks.append('D')
                    
                    if ranks == []:
                        where=  ''
                        pass
                    else:
                        rank_placeholders = ', '.join(['$' + str(i + 1) for i in range(len(ranks))])
                        where = f'WHERE rank IN ({rank_placeholders})'

                    
                    if 'purchasable' in self.filtered:
                        ranknumber = len(ranks) + 1
                        if where == '':
                            shop = f'WHERE shop = ${ranknumber}'

                        else:    
                            shop = f'AND shop = ${ranknumber}'
                        ranks.append('True')
                    elif 'nonpurchasable' in self.filtered:
                        ranknumber = len(ranks) + 1
                        if where == '':
                            shop = f'WHERE shop = ${ranknumber}'

                        else:  
                            shop = f'AND shop = ${ranknumber}'
                        ranks.append('False')
                    


                    if 'price+' in self.filtered:
                        lb = await self.bot.db.fetch(f'SELECT * FROM {stats} {where} {shop} ORDER BY price ASC', *ranks) 
                    elif 'price-' in self.filtered:
                        lb = await self.bot.db.fetch(f'SELECT * FROM {stats} {where} {shop} ORDER BY price DESC', *ranks)                 
                    elif 'rarity+' in self.filtered:
                        lb = await self.bot.db.fetch(f'SELECT * FROM {stats} {where} {shop}', *ranks)
                        order = {'SS': 6, 'S': 5, 'A': 4, 'B': 3, 'C': 2, 'D': 1}
                        lb = sorted(lb, key=lambda row: order.get(row['rank'], float('inf')))

                    elif 'rarity-' in self.filtered:
                        lb = await self.bot.db.fetch(f'SELECT * FROM {stats} {where} {shop}', *ranks)
                        order = {'SS': 1, 'S': 2, 'A': 3, 'B': 4, 'C': 5, 'D': 6}
                        lb = sorted(lb, key=lambda row: order.get(row['rank'], float('inf')))

                    else:
                        lb = await self.bot.db.fetch(f'SELECT * FROM {stats} {where} {shop}', *ranks)

                    
                    

                    if 'notowned' in self.filtered:
                        my_lb = self.listing(registered_check[0][lists])
                        
                        lb = [i for i in lb if i[name] not in my_lb]
                                
                    
                    bad = []       
                    for faction in lb:
                        bad.append(faction[name])
                    
                    
                    self.data = bad
                    data = bad[:self.sep]
                    self.lb = lb


                    self.filtered = None
                    self.numbre =  0

                for i in data:
                    othernumbre += 1
                    item = Image.open(lb[self.numbre][place])
                    item = item.convert("RGBA")
                    item = item.resize((403,171))
                    xvalue = (othernumbre - 1) % 2
                    yvalue = math.ceil(othernumbre / 2) - 1
                    profile.paste(item, (111+ (xvalue*655),33 + (yvalue*241)), item)
                    rank = Image.open(f'{lb[self.numbre]["rank"].lower()}.png')
                    rank = rank.resize((80,80))
                    profile.paste(rank, (30+ (xvalue*655),80 + (yvalue*241)), rank)
                    if lb[self.numbre]["price"] == 0:
                        price = f'N/A'
                    else:
                        price = f'{lb[self.numbre]["price"]} dc'
                    font = ImageFont.truetype("BebasNeue-Regular.ttf", 40)
                    blurred = Image.new('RGBA', profile.size)
                    draw = ImageDraw.Draw(blurred)
                    draw.text((530+ (xvalue*655),190 + (yvalue*241)), text=price, fill='black', font=font)
                    blurred = blurred.filter(ImageFilter.BoxBlur(2))
                    profile.paste(blurred,blurred)
                    draw = ImageDraw.Draw(profile)
                    draw.text((530+ (xvalue*655),190 + (yvalue*241)), text=price, font = font)    
                    
                    display = lb[self.numbre][name]
                    font = ImageFont.truetype("BebasNeue-Regular.ttf", 40)
                    blurred = Image.new('RGBA', profile.size)
                    draw = ImageDraw.Draw(blurred)
                    draw.text((312+ (xvalue*655),190 + (yvalue*241)), text=display, fill='black', font=font,anchor="mm")
                    blurred = blurred.filter(ImageFilter.BoxBlur(4))
                    profile.paste(blurred,blurred)
                    draw = ImageDraw.Draw(profile)
                    draw.text((312+ (xvalue*655),190 + (yvalue*241)), text=display, font = font,anchor="mm")  
                    banner_names.append(lb[self.numbre][name].title())   
                    self.numbre += 1
          


                bytes = BytesIO()
                profile.save(bytes, format="PNG")
                bytes.seek(0)
                

                lb_embed.set_image(url=f"attachment://profile.png")
                dfile = discord.File(bytes,"profile.png")
                lb_embed.set_footer(text = f'Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')
                    


                new_options = [discord.SelectOption(label=name.title(), value=name.lower()) for name in banner_names]
                self.children[5].options = new_options
                await self.message.edit(view=self)

        else:
            categories = []
            categories_num = []
            item = []
            for i in lb:
                if i['banner_category'] in categories:
                    index = categories.index(i['banner_category'])
                    categories_num[index] += 1
                    tup = item[index]
                    tup += f', {i[name].title()}'
                    item[index] = tup
                else:
                    categories.append(i['banner_category'])
                    item.append(f'{i[name].title()}')
                    categories_num.append(1)

            categorieslist = ''
            
            for i in data:
                p = categories.index(i)
                if i == None:
                    categorieslist += f'**Misc** | {categories_num[p]}\n({item[p]})\n\n'
                else:
                    categorieslist += f'**{i.title()}** | {categories_num[p]}\n({item[p]})\n\n'
            

            lb_embed.add_field(name = f'Categories' , value =  f'{categorieslist}' )
            self.numbre = self.numbre + 1

            lb_embed.set_footer(text = f'Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')
            


        return lb_embed, dfile
    
    async def update_message(self,data,category, lb, my_lb, stat, registered_check):
        self.update_buttons()
        embed,dfile = await self.create_embed(data,category, lb, my_lb, stat, registered_check)
        
        
        if dfile == None:
            await self.category.edit(embed=embed, view=self)
        else:
            await self.category.edit(file=dfile, embed= embed, view=self)

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
        if self.current_page == int(len(self.data) / self.sep) + 1:
            from_item = self.current_page * self.sep - self.sep
            until_item = len(self.data)
        return self.data[from_item:until_item]


    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red, emoji='♦️')
    async def first_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page = 1
        self.numbre = 0

        await self.update_message(self.get_current_page_data(),self.category, self.lb, self.my_lb, self.stat, self.registered_check)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple, emoji='🔹')
    async def prev_button(self,  button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()

        delete =  int(len(self.data)) - self.sep * self.current_page
        delete = 12
        if int(len(self.data)) < self.sep * self.current_page:
            new = int(len(self.data)) - self.sep * (self.current_page -1)
            delete = new + 6
        self.current_page -= 1
        self.numbre -= delete
        await self.update_message(self.get_current_page_data(), self.category,self.lb,self.my_lb, self.stat, self.registered_check)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple, emoji='🔹')
    async def next_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data(),self.category, self.lb,self.my_lb, self.stat, self.registered_check)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red, emoji='♦️')
    async def last_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page = math.ceil(len(self.data) / self.sep)
        self.numbre = (self.sep * (self.current_page -1))
        await self.update_message(self.get_current_page_data(), self.category,self.lb,self.my_lb, self.stat, self.registered_check)

    @discord.ui.button(label="Filters",
                       style=discord.ButtonStyle.green)
    async def lddd_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()

        view = Filters(self.member)
        message = await interaction.followup.send('', ephemeral=True,view=view)
        await view.wait()
        self.filtered = view.value
        self.current_page = 1

        await message.delete()
        await self.update_message(self.get_current_page_data(), self.category,self.lb,self.my_lb, self.stat, self.registered_check)
        

    @discord.ui.select(placeholder="Select an item..", min_values=1, max_values=1,options=[
                           discord.SelectOption(label="None", value="None")])
    async def sort_dropdown(self, select: discord.ui.Select, interaction: discord.Interaction):
        await interaction.response.defer()
        self.value = select.values[0]
        self.stop()

class RDPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 6
    numbre : int = 0
    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb,self.owned,self.my_lb, self.registered_check, self.stat)

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
        
    async def create_embed(self, data,lb,owned,my_lb,stat , registered_check):
        my_lb = self.my_lb
        owned = self.owned
        lb = self.lb
        stat = self.stat
        registered_check = self.registered_check
        stat = stat.lower()
        if (stat == 'titles') or (stat == 'title') or (stat == 't'):
            title = 'Title Inventory'
        elif (stat == 'borders') or (stat == 'border')or (stat == 'bo'):
            title = 'Border Inventory'
        elif (stat == 'avaborders') or (stat == 'avaborder')or (stat == 'a'):
            title = "AvaBorder Inventory"
        elif (stat == 'banner') or (stat == 'banners')or (stat == 'b'):
            title = 'Banner Inventory'
        elif (stat == 'oddity') or (stat == 'oddities')or (stat == 'o'):
            title = 'Oddity Inventory'
        else:
            title = 'Banner Inventory'
        lb_embed = discord.Embed(
            title = title,
            description = '',
            colour = color
        )
        if (stat == 'titles') or (stat == 'title') or (stat == 't'):
            for i in data:
                if lb[self.numbre]["title_place"] in my_lb:
                    F = self.listing(registered_check[0]["title_list"])
                    T = int(F.index(lb[self.numbre]["title_place"])) + 1
                    ids = lb[self.numbre]["title_place"]
                    amt = F[T]
                    lb_embed.add_field(name = f'{lb[self.numbre]["banner_name"].title()} *Owned ✅*', value = f'Title ID | **{ids}**\nAmount | x**{amt}**')

                else:
                    ids = lb[self.numbre]["title_place"]
                    lb_embed.add_field(name = f'{lb[self.numbre]["banner_name"].title()}', value = f'Title ID | **{ids}**\nNone Owned')
                lb_embed.set_footer(text = f'Owned:{int((len(self.listing(registered_check[0]["title_list"]))/3))} Dc:{registered_check[0]["banner_pieces"]} Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')
                self.numbre = self.numbre + 1
        elif (stat == 'borders') or (stat == 'border') or (stat == 'bo'):
            for i in data:

                if lb[self.numbre]["border_name"] in my_lb:  
                    F = self.listing(registered_check[0]["border_list"])
                    T = int(F.index(lb[self.numbre]["border_name"])) + 1
                    amt = F[T]
                    lb_embed.add_field(name = f'{lb[self.numbre]["border_name"].title()} *Owned ✅*', value = f'Rank | **{lb[self.numbre]["rank"].title()}**\nAmount | x**{amt}**')
                  

                else:
                    lb_embed.add_field(name = f'{lb[self.numbre]["border_name"].title()}', value = f'Rank | **{lb[self.numbre]["rank"].title()}**\nNone Owned')
                lb_embed.set_footer(text = f'Owned:{int(len(self.listing(registered_check[0]["border_list"]))/3)} Dc:{registered_check[0]["banner_pieces"]} Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')
                self.numbre = self.numbre + 1
        elif (stat == 'avaborders') or (stat == 'avaborder') or (stat == 'a'):
            for i in data:
                if lb[self.numbre]["banner_name"] in my_lb:
                    F = self.listing(registered_check[0]["avaborder_list"])
                    T = int(F.index(lb[self.numbre]["banner_name"])) + 1
                    amt = F[T]
                    lb_embed.add_field(name = f'{lb[self.numbre]["banner_name"].title()} *Owned ✅*', value = f'Rank | **{lb[self.numbre]["rank"].title()}**\nAmount | x**{amt}**')

                else:
                    
                    lb_embed.add_field(name = f'{lb[self.numbre]["banner_name"].title()}', value = f'Rank | **{lb[self.numbre]["rank"].title()}**\nNone Owned')
                lb_embed.set_footer(text = f'Owned:{int(len(self.listing(registered_check[0]["avaborder_list"]))/3)} Dc:{registered_check[0]["banner_pieces"]} Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')
                self.numbre = self.numbre + 1
        elif (stat == 'banner') or (stat == 'banners') or (stat == 'b'):
            for i in data:
                if lb[self.numbre]["banner_name"] in my_lb:
                    F = self.listing(registered_check[0]["banner_list"])
                    T = int(F.index(lb[self.numbre]["banner_name"])) + 1
                    amt = F[T]
                    lb_embed.add_field(name = f'{lb[self.numbre]["banner_name"].title()} *Owned ✅*', value = f'Rank | **{lb[self.numbre]["rank"].title()}**\nAmount | x**{amt}**')

                else:

                    lb_embed.add_field(name = f'{lb[self.numbre]["banner_name"].title()}', value = f'Rank | **{lb[self.numbre]["rank"].title()}**\nNone Owned')
                lb_embed.set_footer(text = f'Owned:{int(len(self.listing(registered_check[0]["banner_list"]))/3)} Dc:{registered_check[0]["banner_pieces"]} Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')
                self.numbre = self.numbre + 1
            
        elif (stat == 'oddities') or (stat == 'oddity') or (stat == 'o'):
            for i in data:

                lb_embed.add_field(name = f'{lb[self.numbre]["oddities_display"].title()}', value = f'EquipID | **{lb[self.numbre]["oddities_name"]}**\nType | **{lb[self.numbre]["oddities_type"].title()}**\nDesc | {lb[self.numbre]["oddities_desc"]}')


                lb_embed.set_footer(text = f'Fc:{registered_check[0]["special"]} Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')
                self.numbre = self.numbre + 1

        return lb_embed
    
    async def update_message(self,data, lb,owned, my_lb, stat, registered_check):
        self.update_buttons()
        await self.message.edit(embed= await self.create_embed(data, lb, owned, my_lb, stat, registered_check), view=self)

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
        if self.current_page == int(len(self.data) / self.sep) + 1:
            from_item = self.current_page * self.sep - self.sep
            until_item = len(self.data)
        return self.data[from_item:until_item]


    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red, emoji='♦️')
    async def first_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page = 1
        self.numbre = 0

        await self.update_message(self.get_current_page_data(), self.lb, self.owned, self.my_lb, self.stat, self.registered_check)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple, emoji='🔹')
    async def prev_button(self,  button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()

        delete =  int(len(self.data)) - self.sep * self.current_page
        delete = 12
        if int(len(self.data)) < self.sep * self.current_page:
            new = int(len(self.data)) - self.sep * (self.current_page -1)
            delete = new + 6
        self.current_page -= 1
        self.numbre -= delete
        await self.update_message(self.get_current_page_data(), self.lb,self.owned,self.my_lb, self.stat, self.registered_check)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.blurple, emoji='🔹')
    async def next_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data(), self.lb,self.owned,self.my_lb, self.stat, self.registered_check)

    @discord.ui.button(label="",
                       style=discord.ButtonStyle.red, emoji='♦️')
    async def last_page_button(self, button: discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.current_page = math.ceil(len(self.data) / self.sep)
        self.numbre = (self.sep * (self.current_page -1))
        await self.update_message(self.get_current_page_data(), self.lb,self.owned,self.my_lb, self.stat, self.registered_check)


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
        if (stat == 'titles') or (stat == 'title') or (stat == 't'):
            stats = 'titles'
            lists = 'title_list'
            name = 'title_place'
        elif (stat == 'border') or (stat == 'borders')or (stat == 'bo'):
            stats = 'borders'
            place = 'border_place'
            lists = 'border_list'
            name = 'border_name'
            count = 'border_count'
        elif (stat == 'avaborder') or (stat == 'avaborders')or (stat == 'a'):
            stats = 'avatar_borders'
            place = 'avatar_place'
            lists = 'avaborder_list'
            name = 'banner_name'
            count = 'avaborder_count'
        elif (stat == 'banner') or (stat == 'banners')or (stat == 'b'):
            stats = 'banners'
            place = 'banner_place'
            lists = 'banner_list'
            name = 'banner_name'
            count = 'banner_count' 

        if (stat == 'titles') or (stat == 'title')or (stat == 't'):
            title = 'Title Shop'
            desc = "Filter using `S`,`A`,`B`,`C`,`D` or search the item\nEnter a range using `>number` or `<number`."
        elif (stat == 'borders') or (stat == 'border')or (stat == 'bo'):
            title = 'Border Shop'
            desc = "Filter using `S`,`A`,`B`,`C`,`D` or search the item\nEnter a range using `>number` or `<number`."     
        elif (stat == 'avaborders') or (stat == 'avaborder')or (stat == 'a'):
            title = "AvaBorder Shop"
            desc = "Filter using `S`,`A`,`B`,`C`,`D` or search the item\nEnter a range using `>number` or `<number`."
        elif (stat == 'banner') or (stat == 'banners')or (stat == 'b'):
            title = 'Banner Shop'
            desc = "Filter using `SS`,`S`,`A`,`B`,`C`,`D` or search the item\nEnter a range using `>number` or `<number`."
        else:
            title = 'Banner Shop'
            desc = "Filter using `SS`,`S`,`A`,`B`,`C`,`D` or search the item\nEnter a range using `>number` or `<number`."            
        lb_embed = discord.Embed(
            title = title,
            description = desc,
            colour = color
        )
        if (stat == 'titles') or (stat == 'title'):
      
            for i in data:
                lb_embed.add_field(name = f'{lb[self.numbre]["banner_name"].title()}', value = f'TitleID | **{lb[self.numbre]["title_place"]}**\nCost | x**{lb[self.numbre]["price"]} Dc**')
                self.numbre = self.numbre + 1

            lb_embed.set_footer(text = f'Page {self.current_page}/{math.ceil(len(self.data) / self.sep)}')
            dfile = None
            return lb_embed, dfile
        else:
            othernumbre = 0   
            num = random.randint(1,4)
            profile = Image.open(f"shop{num}.png")
            
            for i in data:
                othernumbre += 1
                item = Image.open(lb[self.numbre][place])
                item = item.convert("RGBA")
                item = item.resize((403,171))
                xvalue = (othernumbre - 1) % 2
                yvalue = math.ceil(othernumbre / 2) - 1
                profile.paste(item, (111+ (xvalue*655),33 + (yvalue*241)), item)
                rank = Image.open(f'{lb[self.numbre]["rank"].lower()}.png')
                rank = rank.resize((80,80))
                profile.paste(rank, (30+ (xvalue*655),80 + (yvalue*241)), rank)
                price = f'{lb[self.numbre]["price"]} dc'
                font = ImageFont.truetype("BebasNeue-Regular.ttf", 40)
                blurred = Image.new('RGBA', profile.size)
                draw = ImageDraw.Draw(blurred)
                draw.text((530+ (xvalue*655),190 + (yvalue*241)), text=price, fill='black', font=font)
                blurred = blurred.filter(ImageFilter.BoxBlur(2))
                profile.paste(blurred,blurred)
                draw = ImageDraw.Draw(profile)
                draw.text((530+ (xvalue*655),190 + (yvalue*241)), text=price, font = font)    
                
                display = lb[self.numbre][name]
                font = ImageFont.truetype("BebasNeue-Regular.ttf", 40)
                blurred = Image.new('RGBA', profile.size)
                draw = ImageDraw.Draw(blurred)
                draw.text((312+ (xvalue*655),190 + (yvalue*241)), text=display, fill='black', font=font,anchor="mm")
                blurred = blurred.filter(ImageFilter.BoxBlur(4))
                profile.paste(blurred,blurred)
                draw = ImageDraw.Draw(profile)
                draw.text((312+ (xvalue*655),190 + (yvalue*241)), text=display, font = font,anchor="mm")  

                self.numbre += 1


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
                       style=discord.ButtonStyle.red, emoji='♦️')
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
        stat = stat.lower()


        title = 'Limited Shop'
        desc = "Items are listed here only for a limited time.\nBuy them now or they'll be gone forever!"
        lb_embed = discord.Embed(
            title = title,
            description = desc,
            colour = color
        )

        othernumbre = 0   
        for i in data:
            othernumbre += 1
            lb_embed.add_field(name = f'{lb[self.numbre]["item_name"].title()} ', value = f'Rank | **{lb[self.numbre]["rank"].title()}**\nCost | x**{lb[self.numbre]["price"]} Dc**')
            end_time = lb[self.numbre]['delete_time']
            start_time = datetime.now()
            duration = end_time - start_time
            days, seconds = divmod(duration.total_seconds(), 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            banneris = lb[self.numbre]['item_place']
            lb_embed.set_image(url=banneris)
            lb_embed.set_footer(text = f'⏰ {int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s ㅤItem {self.current_page}/{math.ceil(len(self.data) / self.sep)}')
            self.numbre = self.numbre + 1


        return lb_embed

    async def update_message(self,data, lb, stat):
        self.update_buttons()
        try:
            banneris = lb[self.numbre]['item_place']
        except IndexError:
 
            banneris = lb[self.numbre]['item_place']         
        embed = await self.create_embed(data, lb, stat)
        await self.message.edit(view=self)
        embed.set_image(url=banneris) 

        await self.message.edit(embed= embed)

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

class MiscCommands(commands.Cog):
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

    def c_listing(self, str1):
        if str1 is not None:
            list_str = str1.split(',')

            if list_str[0] == '':
                list_str.remove(list_str[0])

            list_num = []

            for e in list_str:
                list_num.append(int(e.strip()))

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

    def f_badges(self, dict1 : dict):
            main_dict = {
                'normal gym':{'emoji':'<:normal_gym:930205494671474728>','desc':'Awarded to players who complete the Normal gym.'},
                'fire gym':{'emoji':'<:fire_gym:930205493224411218>','desc':'Awarded to players who complete the Fire gym.'},
                'water gym':{'emoji':'<:water_gym:930205495694880798>','desc':'Awarded to players who complete the Water gym.'},
                'grass gym':{'emoji':'<:grass_gym:930205495241895946>','desc':'Awarded to players who complete the Grass gym.'},
                'electric gym':{'emoji':'<:electric_gym:930205493371228200>','desc':'Awarded to players who complete the Electric gym.'},
                'ice gym':{'emoji':'<:ice_gym:930205494801494037>','desc':'Awarded to players who complete the Ice gym.'},
                'fighting gym':{'emoji':'<:fighting_gym:930205493526409306>','desc':'Awarded to players who complete the Fighting gym.'},
                'poison gym':{'emoji':'<:poison_gym:930205494839242782>','desc':'Awarded to players who complete the Poison gym.'},
                'ground gym':{'emoji':'<:ground_gym:930205494411395182>','desc':'Awarded to players who complete the Ground gym.'},
                'flying gym':{'emoji':'<:flying_gym:930205494000369665>','desc':'Awarded to players who complete the Flying gym.'},
                'psychic gym':{'emoji':'<:psychic_gym:930205495124459550>','desc':'Awarded to players who complete the Psychic gym.'},
                'bug gym':{'emoji':'<:bug_gym:930205487595675721>','desc':'Awarded to players who complete the Bug gym.'},
                'rock gym':{'emoji':'<:rock_gym:930205494574981230>','desc':'Awarded to players who complete the Rock gym.'},
                'ghost gym':{'emoji':'<:ghost_gym:930205496051380325>','desc':'Awarded to players who complete the Ghost gym.'},
                'dragon gym':{'emoji':'<:dragon_gym:930205494554030110>','desc':'Awarded to players who complete the Dragon gym.'},
                'dark gym':{'emoji':'<:dark_gym:930205487562100856>','desc':'Awarded to players who complete the Dark gym.'},
                'steel gym':{'emoji':'<:steel_gym:930205494663057478>','desc':'Awarded to players who complete the Steel gym.'},
                'fairy gym':{'emoji':'<:fairy_gym:930205493488676965>','desc':'Awarded to players who complete the Fairy gym.'},
                'clan league':{'emoji':'<:clan_league:930342197075783740>','desc':'Awarded to players who won the Clan League.'},
                'tournament 1':{'emoji':'<:tournament_1:930356319020548136>','desc':'Awarded to players for winning a Tournament.'},
                'streak':{'emoji':'<:streak:930373099801706526>','desc':'Awarded to players of a clan that gets a streak of 7 wins.'},
                'menacing':{'emoji':'<:menacing:930387483445837854>','desc':'Awarded to players who wipe an entire clan.'},
                'leaderboard':{'emoji':'<:leaderboard:930362131013070879>','desc':'Awarded to players who secure top 8 placement in ranked battles at the end of the season.'},
                'swiff':{'emoji':'<:swiff:930428662711484486>','desc':'Awarded to players who get a streak of 20 wins in Ranked battles'},
                'tournament 2':{'emoji':'<:tournament_2:930418041240555520>','desc':'Awarded to players for winning a Tournament.'},
                'elite 4':{'emoji':'<:4_:931160643468406824>','desc':'Awarded to players who defeat the Elite 4.'}
            }

            dict1 = main_dict

            return dict1

    @commands.command(name = 'shop', aliases = ['s'])
    async def shop_command(self,ctx,stat : str = None, filters :str = None,*, category : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

  
        if user_ban_list:
            await ctx.send('You are banned from the bot.')

        else:        
            if registered_check:
                if stat is None:
                    em = discord.Embed(
                        title = 'Shop',
                        description = '**d!shop [item type/limited] [filter]**\nView the shop\n[item type] banner,border,avaborder,title\n[filter] S,A,B,C,D or search the item',
                        colour = color
                    )
                    await ctx.send(embed = em)  
                else:
                    if stat == 'limited':
                        current_time = datetime.now()
                        await self.bot.db.execute(f"DELETE FROM limited WHERE delete_time <= $1", current_time)
                        lb = await self.bot.db.fetch(f'SELECT * FROM limited ORDER BY delete_time DESC')
                        if lb == []:
                            await ctx.send(f"There are no limited items on sale right now..")
                            return
                        
                        lb.reverse()
                        
                        data = []
                        for faction in lb:
                            data.append(faction['item_name'])
                        

                        pagination_view = LPaginationView()
                        pagination_view.data = data
                        pagination_view.lb = lb
                        pagination_view.stat = stat
                        pagination_view.registered_check = registered_check
                        await pagination_view.send(ctx)                                                                                                    


                    else:
                        if (stat == 'titles') or (stat == 'title')or (stat == 't'):
                            stats = 'titles'
                            name = 'title_place'
                        elif (stat == 'borders') or (stat == 'border')or (stat == 'bo'):
                            stats = 'borders'
                            name = 'border_name'
                        elif (stat == 'avaborders') or (stat == 'avaborder')or (stat == 'a'):
                            stats = 'avatar_borders'
                            name = 'banner_name'
                        elif (stat == 'banner') or (stat == 'banners')or (stat == 'b'):
                            stats = 'banners'
                            name = 'banner_name'
                        else:
                            await ctx.send("Incorrect item type. **banner/border/avaborder**")
                            return
                        shop = 'True'
                        if filters is None:
                            pass
                        else:
                            filters = filters.title()
                        
                        if filters is None:
                            
                            lb = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE shop = $1 ORDER BY price ASC', shop)
                        elif filters.startswith(">"):
                            sfilters = int(filters[1:])
                            lb = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE shop = $1 AND price >= {sfilters} ORDER BY price ASC',shop)
                        elif filters.startswith("<"):
                            sfilters = int(filters[1:])
                            lb = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE shop = $1 AND price <= {sfilters} ORDER BY price DESC',shop)                    
                        elif (filters == 'S') or (filters == 'A') or (filters == 'B') or (filters == 'C') or (filters == 'D'):
                            lb = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE rank = $1 AND shop = $2 ORDER BY price ASC',filters,shop)
                        elif (filters == 'Category') or (filters == 'Cat'):

                            if category == None:
                                await ctx.send(f"Please mention a category, `d!shop category [category]`")
                                return
                            else:
                                lb = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE banner_category = $1',category.lower())
                                if lb == []:
                                    await ctx.send(f"Category Not Found. Use `d!shop category` to search for categories`")
                                    return
                    
                        else:
                            filters = filters.lower()
                            start = f'{filters}%'
                            lb = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE shop = $1 AND {name} LIKE $2 ORDER BY price ASC',shop,start)

                        if lb == []:
                            await ctx.send(f"Your search for **{filters}** didn't return any results. Were you trying to use a filter? `SS`, `S`, `A`, `B`,`C`, `D`")
                            return
                            
                        data = []
                        

                        for faction in lb:
                            data.append(faction[name])

                        pagination_view = SPaginationView()
                        pagination_view.data = data
                        pagination_view.lb = lb
                        pagination_view.stat = stat
                        pagination_view.registered_check = registered_check

                        await pagination_view.send(ctx)
            else:
                await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'addtoshop')
    async def addtoshop_command(self,ctx, stat :str = None, *, item :str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if str(ctx.author.id) in admins_list:
                if (stat is None) or (item is None):
                    em = discord.Embed(
                        title = 'Misc',
                        description = '**Add to shop**\n\nd!addtoshop [banners/titles/avatar_borders/borders] [Banners/Title/Border/AvaBorder]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    if (stat == 'titles') or (stat == 'title')or (stat == 't'):
                        name = 'title_place'
                    elif (stat == 'borders') or (stat == 'border')or (stat == 'bo'):
                        name = 'border_name'
                    elif (stat == 'avaborders') or (stat == 'avaborder')or (stat == 'a'):
                        name = 'banner_name'
                    elif (stat == 'banners') or (stat == 'banner')or (stat == 'b'):
                        name = 'banner_name'
                    else:
                        await ctx.send("X")
                    shop = 'True'
                    await self.bot.db.execute(f'UPDATE {stat} SET shop = $1 WHERE {name} = $2', shop, item)
                    await ctx.send("Item added to the shop!")
            else:
                await ctx.send("You don't have the permission to perform this command!")

    @commands.command(name = 'addtolim')
    async def addtolimit_command(self,ctx,stat : str = None,  item_name : str = None, item_place : str = None, rank :str = None, price : int = None, time : int = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if str(ctx.author.id) in admins_list:
                if (stat is None) or (item_name is None) or (time is None):
                    em = discord.Embed(
                        title = 'Misc',
                        description = '**Add to shop**\n\nd!addtolim [type] [name] [place] [rank] [price] [time]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    if (stat == 'title') or (stat == 'titles')or (stat == 't'):
                        stats = 'titles'
                        lists = 'title_list'
                        name = 'title_place'
                        current = 'title'
                    elif (stat == 'border') or (stat == 'borders')or (stat == 'bo'):
                        stats = 'borders'
                        lists = 'border_list'
                        name = 'border_name'
                        current = 'banner_border'
                    elif (stat == 'avaborders') or (stat == 'avaborder')or (stat == 'a'):
                        stats = 'avatar_borders'
                        lists = 'avaborder_list'
                        name = 'banner_name'
                        current = 'avatar_border'
                    elif (stat == 'banner') or (stat == 'banners')or (stat == 'b'):
                        stats = 'banners'
                        lists = 'banner_list'
                        name = 'banner_name'
                        current = 'current_banner'
                    else:
                        await ctx.send("Incorrect item type. **banner/border/avaborder/title**")
                        return
                    delete_time = datetime.now() + timedelta(days=time)
                    await self.bot.db.execute('INSERT INTO limited (item_name, item_type, price, rank, delete_time, item_place) VALUES ($1, $2, $3, $4, $5, $6)', item_name.lower(), stats.lower(), price, rank.title(), delete_time, item_place)
                    await ctx.send("Item added to the Limited shop!")
            else:
                await ctx.send("You don't have the permission to perform this command!")

    @commands.command(name = 'buy')
    async def buy_command(self, ctx, stat : str = None,*, item : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        
        if registered_check:
                if (stat is None) and (item is None):
                    em = discord.Embed(
                        title = 'Misc',
                        description = '**Buy from Shop**\nd!buy [item type] [item name]\n[item type] banner,border,avaborder,title,key,oddity',
                        colour = color
                    )

                    await ctx.send(embed = em)

                elif (stat == 'keys') or (stat == 'key'):


                    if item is None:
                        item = 1
                    
                    try:
                        item = int(item)
                    except ValueError:
                        await ctx.send("Please type a numerical value.")
                        return 
                    

                    if registered_check[0]['banner_pieces'] >= item*200:
                        view = ConfirmCancel(ctx.author)
                        
                        await ctx.send (f'Are you sure you want to buy **{item}** **Key**? **-{item*200}**dc', view = view)
                        await view.wait()
                        if view.value is True:
                            registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                            if registered_check[0]["banner_pieces"] >= item*200:

                                flists = str(registered_check[0]['achievements'])
                                new_admins = ''
                                admins_list = self.listing(flists)
                                for p,admin in enumerate(admins_list):
                                    if p == 0:
                                        new_admins += str(admin)
                                    elif p == 8:
                                        if int(admin) == 6:
                                            admins_list[9] = 1
                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                            await ctx.send("**Bronze Achievement Completed! ✦ Buy 7 Keys ✦**\n*10dc rewarded & Lootbox rewarded*")
                                        elif int(admin) == 14:
                                            admins_list[9] = 2
                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                            await ctx.send("**Silver Achievement Completed! ✦✦ Buy 15 Keys ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                        elif int(admin) == 29:
                                            admins_list[9] = 3
                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                            await ctx.send("**Gold Achievement Completed! ✦✦✦ Buy 30 Keys ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                        admin = int(admin) + 1
                                        new_admins += f' {admin}'                                                      
                                    else:
                                        new_admins += f' {admin}'  

                                await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, ctx.author.id)   

                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - {item*200} WHERE player_id = $1', ctx.author.id) 
                                await self.bot.db.execute(f'UPDATE registered SET scraps = scraps + {item} WHERE player_id = $1', ctx.author.id) 
                                await ctx.send("Keys bought!")
                            else:
                                await ctx.send("You don't have enough dc to buy a key.")
                        elif view.value is False:
                            await ctx.send("Cancelled.")
                        else:
                            await ctx.send("Timed out.")
                    else:
                        await ctx.send("You don't have enough dc to buy a key.")
                elif (stat == 'oddity') or (stat == 'o'):
                    item = item.lower()
                    lbtrue = await self.bot.db.fetch(f'SELECT * FROM oddities')
                    slist = []

                    for i in range(len(lbtrue)):
                        slist.append(lbtrue[i][f'oddities_name'])
                    if item.lower() in slist:
                        isit = 'True'
                        if (ctx.author.id == 0) or (ctx.author.id == 1209502516715192332):
                            lb = await self.bot.db.fetch(f'SELECT * FROM oddities WHERE oddities_name = $1',item)
                        else:
                            lb = await self.bot.db.fetch(f'SELECT * FROM oddities WHERE oddities_name = $1 AND shop = $2',item,isit)
                        if lb == []:
                            await ctx.send("This item either doesn't exist or isn't listed in the shop")
                        else:
                            price = lb[0]["price"]
                            if registered_check[0]["special"] < price:
                                await ctx.send("You don't have enough Fabled Coins!")
                            else:
                                
                                dflists = str(registered_check[0]['oddities'])
                                listbuy = self.listing(dflists)
                                if item.lower() in listbuy:
                                    await ctx.send("You've already bought this item.")
                                    return
                                view = ConfirmCancel(ctx.author)
                                await ctx.send (f'Are you sure you want to buy **{item}**?', view = view)
                                await view.wait()
                                if view.value is True:
                                    registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                                    if registered_check[0]["special"] < price:
                                        await ctx.send("You don't have enough Fabled Coins!")
                                    else:
                                        pass
                                        flists = str(registered_check[0]['achievements'])
                                        new_admins = ''
                                        admins_list = self.listing(flists)
                                        for p,admin in enumerate(admins_list):
                                            if p == 0:
                                                new_admins += str(admin)
                                            elif p == 28:
                                                if int(admin) == 0:
                                                    admins_list[29] = 1
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                    await ctx.send("**Bronze Achievement Completed! ✦ Buy an Oddity ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                elif int(admin) == 1:
                                                    admins_list[29] = 2
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                    await ctx.send("**Silver Achievement Completed! ✦✦ Buy 2 Oddities ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                elif int(admin) == 2:
                                                    admins_list[29] = 3
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                    await ctx.send("**Gold Achievement Completed! ✦✦✦ Buy 3 Oddities ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                admin = int(admin) + 1
                                                new_admins += f' {admin}'                                                      
                                            else:
                                                new_admins += f' {admin}'  

                                        await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, ctx.author.id) 
                                        new_admins = ''  

                                        
                                        a = f'{item.lower()}'
                                        
                                        if registered_check[0]['oddities'] is None:
                                            admins_list = self.listing(dflists)
                                            new_admins = f' {a}'
                                            await self.bot.db.execute(f'UPDATE registered SET oddities = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)
                                            await self.bot.db.execute(f'UPDATE registered SET special = special - {price} WHERE player_id = $1', ctx.author.id)
                                            await ctx.send("Item bought!") 

                                        else:
                                            new_admins = str(dflists) + f' {a}'
                                            await self.bot.db.execute(f'UPDATE registered SET oddities = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            await self.bot.db.execute(f'UPDATE registered SET special = special - {price} WHERE player_id = $1', ctx.author.id)

                                            await ctx.send("Item bought!") 
                                       
                                elif view.value is False:
                                    await ctx.send('Cancelled.')
                                else:
                                    await ctx.send('Timed Out')   
                else:
                    
                    if (stat == 'titles') or (stat == 'title')or (stat == 't'):
                        stats = 'titles'
                        lists = 'title_list'
                        name = 'title_place'
                        count = 'title_count'
                    elif (stat == 'borders') or (stat == 'border')or (stat == 'bo'):
                        stats = 'borders'
                        lists = 'border_list'
                        name = 'border_name'
                        count = 'border_count'
                    elif (stat == 'avaborders') or (stat == 'avaborder')or (stat == 'a'):
                        stats = 'avatar_borders'
                        lists = 'avaborder_list'
                        name = 'banner_name'
                        count = 'avaborder_count'
                    elif (stat == 'banner') or (stat == 'banners')or (stat == 'b'):
                        stats = 'banners'
                        lists = 'banner_list'
                        name = 'banner_name'
                        count = 'banner_count'
                    else:
                        await ctx.send("Incorrect item type. **banner/border/avaborder/title/oddity**")
                        return
                    item = item.lower()
                    lbtrue = await self.bot.db.fetch(f'SELECT * FROM {stats}')
                    slist = []

                    for i in range(len(lbtrue)):
                        slist.append(lbtrue[i][f'{name}'])
                    if item.lower() in slist:
                        isit = 'True'
                        if (ctx.author.id == 0) or (ctx.author.id == 1209502516715192332):
                            lb = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE {name} = $1',item)
                        else:
                            lb = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE {name} = $1 AND shop = $2',item,isit)
                        if lb == []:
                            lb = await self.bot.db.fetch(f'SELECT * FROM limited WHERE item_name = $1 AND item_type = $2',item,stats)
                        if lb == []:
                            
                            await ctx.send("This item either doesn't exist or isn't listed in the shop")
                        else:
                            price = lb[0]["price"]
                            if registered_check[0]["banner_pieces"] < price:
                                await ctx.send("You don't have enough Dom Coins!")
                            else:
                                
                                dflists = str(registered_check[0][lists])
                                listbuy = self.listing(dflists)
                                view = ConfirmCancel(ctx.author)
                                await ctx.send (f'Are you sure you want to buy **{item}**?', view = view)
                                await view.wait()
                                if view.value is True:
                                    registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                                    if registered_check[0]["banner_pieces"] < price:
                                        await ctx.send("You don't have enough Dom Coins!")
                                    else:
                                        flists = str(registered_check[0]['achievements'])
                                        new_admins = ''
                                        admins_list = self.listing(flists)
                                        for p,admin in enumerate(admins_list):
                                            if p == 0:
                                                new_admins += str(admin)
                                            elif p == 10:
                                                if int(admin) == 9:
                                                    admins_list[11] = 1
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                    await ctx.send("**Bronze Achievement Completed! ✦ Buy 10 Items ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                elif int(admin) == 24:
                                                    admins_list[11] = 2
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                    await ctx.send("**Silver Achievement Completed! ✦✦ Buy 25 Items ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                elif int(admin) == 49:
                                                    admins_list[11] = 3
                                                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                    await ctx.send("**Gold Achievement Completed! ✦✦✦ Buy 50 Items ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                admin = int(admin) + 1
                                                new_admins += f' {admin}'                                                      
                                            else:
                                                new_admins += f' {admin}'  

                                        await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, ctx.author.id)   

                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                        s = 1
                                        if item.lower() in listbuy:
                                            new_admins = ''
                                            admins_list = self.listing(dflists)
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
                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - {price} WHERE player_id = $1', ctx.author.id)  

                                            await ctx.send("Item bought!")                                          
                                        else:
                                            new_admins = ''
                                            itemcode = await id_generator()
                                            
                                            a = f'{item.lower()}'
        
                                            b = 1
                                            c = f"{itemcode}"
                                            
                                            if registered_check[0][lists] is None:
                                                admins_list = self.listing(dflists)
                                                new_admins = f' {a}' + f' {b}' + f' {c}'
                                                await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - {price} WHERE player_id = $1', ctx.author.id)
                                                await ctx.send("Item bought!") 

                                            else:
                                                new_admins = str(dflists) + f' {a}' + f' {b}' + f' {c}'
                                                await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces - {price} WHERE player_id = $1', ctx.author.id)

                                                await ctx.send("Item bought!") 
                                       
                                elif view.value is False:
                                    await ctx.send('Cancelled.')
                                else:
                                    await ctx.send('Timed Out')    

                    else:
                        await ctx.send("Item not found.")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name ='rate')
    async def gg(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:


            datern = str(datetime.now().date())
            if datern == '2023-12-16':
                item = 'bladegif'
            elif datern == '2023-12-17':
                item = 'jinwoogif'
            elif datern == '2023-12-18':
                item = 'sharingangif'
            elif datern == '2023-12-19':
                item = 'gear5gif'
            elif datern == '2023-12-20':
                item = 'csmgif'
            elif datern == '2023-12-21':
                item = 'akazagif'
            elif datern == '2023-12-22':
                item = 'yaegif'
            elif datern == '2023-12-23':
                item = 'sukunagif'
            elif datern == '2023-12-24':
                item = 'raidengif'
            elif datern == '2023-12-25':
                item = 'aquagif'
            elif datern == '2023-12-26':
                item = 'jingliugif'
            elif datern == '2023-12-27':
                item = 'ichigogif'
            else:
                pass

            await ctx.send(f"Rate UP! for **{item.title()}** by 50%\nThis doesn't mean you have a 50% chance every lootbox rather, it means that when you get a SS banner you have a 50% chance of getting that banner.")


    @commands.command(name = 'open')
    @commands.cooldown(1, 10 , commands.BucketType.user)
    async def wish_command(self, ctx, amount : int = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        
        if registered_check:
            if amount == None:
                amount = 1
                text = f'a box'
            else:
                if amount > 10:
                    await ctx.send("You can only open up to 10 boxes")
                    return
                text = f'**{amount}** boxes'


            if (registered_check[0]['wishes'] >= amount) and (registered_check[0]['scraps'] >= amount):

                view = ConfirmCancel(ctx.author)
                
                await ctx.send(f"Are you sure you want to open {text}?", view = view)
                await view.wait()
                
                if view.value is True:
                    pass
                elif view.value is False:
                    await ctx.send("Cancelled")
                    return
                else:
                    await ctx.send("Timed out")
                    return
                
                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes - {amount} , scraps = scraps - {amount} WHERE player_id = $1', ctx.author.id)

                z = amount
                items = []
                ranks = []
                stuff = []
                while z > 0:
                    z -= 1
                    registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                    if ctx.author.id == 1209502516715192332:
                        roll = 980
                    elif registered_check[0]['gold'] == 29:
                        roll = random.randint(940,1000)
                    elif registered_check[0]['gold'] == 49:
                        roll = 980
                    else:
                        roll = random.randint(1,1000)
                        if (registered_check[0]['purple'] == 4) and (roll <= 649):
                            roll = random.randint(650,939)


                    


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

                    excluded_items = ['bronze','silver','gold','platinum','dominant','bronze2','silver2','gold2','platinum2','dominant2','clan','casual', 'siesta', 'tonikaku']

                    if (roll >= 0) and (roll < 400):
                        await self.bot.db.execute(f'UPDATE registered SET gold = gold + 1, purple = purple + 1 WHERE player_id = $1', ctx.author.id)
                        rank = 'D'
                        lbtrue = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE rank = $1 AND shop = $2', rank, shop)
                        slist = []
                        for i in range(len(lbtrue)):
                            slist.append(lbtrue[i][f'{name}'])

                        slist = [item for item in slist if item not in excluded_items]

                        item = random.choice(slist)


                    elif (roll >= 400) and (roll < 650):
                        await self.bot.db.execute(f'UPDATE registered SET gold = gold + 1, purple = purple + 1 WHERE player_id = $1', ctx.author.id)
                        rank = 'C'
                        lbtrue = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE rank = $1 AND shop = $2', rank, shop)
                        slist = []
                        for i in range(len(lbtrue)):
                            slist.append(lbtrue[i][f'{name}'])

                        slist = [item for item in slist if item not in excluded_items]

                        item = random.choice(slist)

                    
                    elif (roll >= 650) and (roll < 860):
                        await self.bot.db.execute(f'UPDATE registered SET gold = gold + 1, purple = 0 WHERE player_id = $1', ctx.author.id)
                        rank = 'B'
                        lbtrue = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE rank = $1 AND shop = $2', rank, shop)
                        slist = []
                        for i in range(len(lbtrue)):
                            slist.append(lbtrue[i][f'{name}'])

                        slist = [item for item in slist if item not in excluded_items]

                        item = random.choice(slist)

                    elif (roll >= 860) and (roll < 940):
                        await self.bot.db.execute(f'UPDATE registered SET gold = gold + 1, purple = 0 WHERE player_id = $1', ctx.author.id)
                        rank = 'A'    
                        lbtrue = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE rank = $1 AND shop = $2', rank, shop)
                        slist = []
                        for i in range(len(lbtrue)):
                            slist.append(lbtrue[i][f'{name}'])

                        slist = [item for item in slist if item not in excluded_items]

                        item = random.choice(slist)


                    elif (roll >= 940) and (roll < 970):
                        await self.bot.db.execute(f'UPDATE registered SET gold = gold + 1, purple = 0 WHERE player_id = $1', ctx.author.id)
                        rank = 'S'
                        lbtrue = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE rank = $1 AND shop = $2', rank, shop)
                        slist = []
                        for i in range(len(lbtrue)):
                            slist.append(lbtrue[i][f'{name}'])

                        slist = [item for item in slist if item not in excluded_items]

                        item = random.choice(slist)


                    elif (roll >= 970) and (roll < 1005):
                        await self.bot.db.execute(f'UPDATE registered SET gold = 0, purple = 0 WHERE player_id = $1', ctx.author.id)
                        


                        rank = 'SS'
                        types = 'Banner'
                        stats = 'banners'
                        lists = 'banner_list'
                        name = 'banner_name'
                        flists = str(registered_check[0][lists])
                        listbuy = self.listing(flists)
                        lbtrue = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE rank = $1', rank)
                        slist = []
                        for i in range(len(lbtrue)):
                            slist.append(lbtrue[i][f'{name}'])

                        slist = [item for item in slist if item not in excluded_items]

                        item = random.choice(slist)

                    items.append(item)
                    ranks.append(rank)
                    stuff.append(types)

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

             

                    flists = str(registered_check[0]['achievements'])
                    new_admins = ''
                    admins_list = self.listing(flists)
                    for p,admin in enumerate(admins_list):
                        if p == 0:
                            new_admins += str(admin)
                        elif p == 12:
                            if int(admin) == 9:
                                admins_list[13] = 1
                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                await ctx.send("**Bronze Achievement Completed! ✦ Open 10 Lootboxes ✦**\n*10dc rewarded & Lootbox rewarded*")
                            elif int(admin) == 19:
                                admins_list[13] = 2
                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                await ctx.send("**Silver Achievement Completed! ✦✦ Open 20 Lootboxes ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                            elif int(admin) == 29:
                                admins_list[13] = 3
                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                await ctx.send("**Gold Achievement Completed! ✦✦✦ Open 30 Lootboxes ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                            admin = int(admin) + 1
                            new_admins += f' {admin}'                                                      
                        else:
                            new_admins += f' {admin}'  

                    await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, ctx.author.id)   




                wish_embed_1 = discord.Embed(
                    title = f'{ctx.author.name} is opening LootBoxes!',
                    description = '',
                    colour = color
                )
                if ('SS' in ranks) or ('S' in ranks):
                    bozo = 'https://media.tenor.com/szDO6RwgxMMAAAAC/wish.gif'
                elif ('A' in ranks) or ('B' in ranks):
                    bozo = 'https://media.tenor.com/JcMSVVkgfgMAAAAC/genshin-wish.gif'
                else:
                    bozo = 'https://media.tenor.com/KGwWGVz9-XQAAAAC/genshin-impact-wish.gif'

                wish_embed_1.set_image(url=bozo)
                wish_embed_1.set_footer(text = f'Inventory updated: -{amount} LootBox -{amount} Key')


                message = await ctx.send(embed = wish_embed_1)

                tobesent = ''

                for t,i in enumerate(items):

                    if (ranks[t] == 'SS'):
                        ranked = '<:ss:1126547376719532112>'
                    elif (ranks[t]  == 'S'):
                        ranked = '<:s_:1126546706721415320>'
                    elif (ranks[t]  == 'A'):
                        ranked = '<:a:1126546710332710943>'
                    elif (ranks[t]  == 'B'):
                        ranked = '<:b:1126546712283066479>'
                    elif (ranks[t]  == 'C'):
                        ranked = '<:c:1126546716200542378>'
                    else:
                        ranked = '<:d:1126546717978919033>' 

                    tobesent += f'{ranked} **{i.title()}** **{stuff[t].upper()}**\n'

                await asyncio.sleep(6)

                wish_embed_2 = discord.Embed(
                    title = f'Items you got ✨',
                    description = f'{tobesent}',
                    colour = color
                )

                await message.reply(embed = wish_embed_2)

            else:
                await ctx.send('You do not have enough lootboxes or keys. Complete achievements to get lootboxes and buy keys from the shop!')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'inventory', aliases = ['inv'])

    async def inventory_command(self, ctx, stat : str = None):
        all_banners = await self.bot.db.fetch('SELECT * FROM banners')
        all_borders = await self.bot.db.fetch('SELECT * FROM borders')
        all_avaborders = await self.bot.db.fetch('SELECT * FROM avatar_borders')
        all_titles = await self.bot.db.fetch('SELECT * FROM titles')

        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

  
        if user_ban_list:
            await ctx.send('You are banned from the bot.')

        else:
            if registered_check:

                if stat == None:
                    inv_embed = discord.Embed(
                        title = f"{ctx.author.name}'s inventory",
                        description = '',
                        colour = color
                    )

                    
                    inv_embed.add_field(name = f'Dom Coins', value = f'{registered_check[0]["banner_pieces"]}')
                    inv_embed.add_field(name = f'Lootboxes', value = f'{registered_check[0]["wishes"]}')
                    inv_embed.add_field(name = f'Keys', value = f'{registered_check[0]["scraps"]}')



                    inv_embed.set_thumbnail(url = ctx.author.display_avatar)



                    await ctx.send(embed = inv_embed)
                else:
                    owned =''
                    if (stat == 'titles') or (stat == 'title') or (stat == 't'):
                        stats = 'titles'
                        lists = 'title_list'
                        name = 'title_place'
                    elif (stat == 'borders') or (stat == 'border') or (stat == 'bo'):
                        stats = 'borders'
                        lists = 'border_list'
                        name = 'border_name'
                    elif (stat == 'avaborders') or (stat == 'avaborder') or (stat == 'a'):
                        stats = 'avatar_borders'
                        lists = 'avaborder_list'
                        name = 'banner_name'
                    elif (stat == 'banners') or (stat == 'banner') or (stat == 'b'):
                        stats = 'banners'
                        lists = 'banner_list'
                        name = 'banner_name'
                    elif (stat == 'oddity') or (stat == 'o') or (stat == 'oddities'):
                        stats = 'oddities'
                        lists = 'oddities'
                        name = 'oddities_name'
                    else:
                        await ctx.send("Incorrect item type. **banner/border/avaborder/titles/oddity**")
                        return 

                    s = await self.bot.db.fetch(f'SELECT * FROM {stats}')
                    data = []
                    e = 0
                    for faction in s:
                        data.append(faction[name]) 
                    lb = []  
                    for i in data:
                        my_lb = self.listing(registered_check[0][lists])
                        
                        if s[e][name] in my_lb:
                            t = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE {name} = $1', s[e][name])
                            lb.append(t[0])
                        e = 1 + e
                        
           
                    if lb == []:
                        await ctx.send(f"You don't have any of these items!")
                        return
                        
                    my_lb = self.listing(registered_check[0][lists])
                    data = []
                    lb.reverse()
                    for faction in lb:
                        data.append(faction[name])
                    pagination_view = RDPaginationView()
                    pagination_view.data = data
                    pagination_view.lb = lb
                    pagination_view.my_lb = my_lb
                    pagination_view.stat = stat
                    pagination_view.registered_check = registered_check
                    pagination_view.owned = owned

                    await pagination_view.send(ctx)                    

            else:
                await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.group(name = 'kddey', invoke_without_command = True)
    async def get_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            em = discord.Embed(
                title = 'Get',
                description = 'Get items.',
                colour = color
            )

            em.add_field(name = 'd!get wish [amount]', value = 'Trade your scraps for wishes. 5 scraps = 1 wish.',inline=False)

            em.add_field(name = 'd!get banner', value = 'Trade your banner pieces for a random banner. 24 banner pieces = 1 banner.\nBanners can be viewed with the `d!banners` command.\nDuplicate banners will convert into 30 scraps.',inline=False)


            await ctx.send(embed = em)
        
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @get_command.command(name = 'afdwish')
    async def get_wish_command(self, ctx, amt : int = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if amt is None:
                em = discord.Embed(
                    title = 'Get Wish',
                    description = 'd!get wish [amt]\n\n**Trade your scraps for wishes. 5 scraps = 1 wish.**',
                    colour = discord.Colour.blue()
                )

                await ctx.send(embed = em)

            else:
                if amt == 0:
                    await ctx.send('😐😐 you really that broke?')

                else:
                    if registered_check[0]['scraps'] >= 5*amt:
                        scrap_amt = registered_check[0]['scraps'] - (5*amt)

                        wish_amt = registered_check[0]['wishes'] + amt

                        await self.bot.db.fetch('UPDATE registered SET scraps = $1 WHERE player_id = $2', scrap_amt, ctx.author.id)
                        await self.bot.db.fetch('UPDATE registered SET wishes = $1 WHERE player_id = $2', wish_amt, ctx.author.id)

                        await ctx.send(f'Converted **{5*amt} scraps** to **{amt} wishes**.')

                    else:
                        await ctx.send(f'You do not have enough scraps for {amt} wishes.')

        else:
            await ctx.send('You have not registered! Use `d!start` to register.')

    @get_command.command(name = 'adfdcbanner')
    @commands.cooldown(1, 12, commands.BucketType.user)
    async def get_banner_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if registered_check[0]['banner_pieces'] >= 24:
                banners = await self.bot.db.fetch('SELECT * FROM banners')

                banner_list = []

                for i in range(len(banners)):
                    banner_list.append(banners[i]['banner_name'])

                confirm_msg = await ctx.send(f'{ctx.author.mention} Are you sure you want to trade 24 banner pieces for a banner?')

                await confirm_msg.add_reaction('✅')
                await confirm_msg.add_reaction('❌')

                def check(reaction : discord.Reaction, user : discord.User):
                    return user.id == ctx.author.id and reaction.message.channel.id == ctx.channel.id and str(reaction.emoji) in ['\U00002705', '\U0000274C']

                try:
                    reaction_add, user = await self.bot.wait_for(
                        'reaction_add',
                        timeout = 15,
                        check = check
                    )

                except asyncio.TimeoutError:
                    await ctx.send('Timed-out. Aborted.')
                    return

                else:
                    if str(reaction_add) == '✅':
                        chosen = random.choice(banner_list)

                        my_banner_list = self.listing(registered_check[0]['banner_list'])
                        
                        if chosen not in my_banner_list:
                            await self.bot.db.execute('UPDATE registered SET banner_count = banner_count + 1 WHERE player_id = $1', ctx.author.id)

                            if registered_check[0]['banner_list'] is None:
                                await self.bot.db.execute('UPDATE registered SET banner_list = $1 WHERE player_id = $2', chosen.title(), ctx.author.id)
                                await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces - 24 WHERE player_id = $1', ctx.author.id)

                            else:
                                new_banner_list = registered_check[0]['banner_list'] + f' {chosen.title()}'

                                await self.bot.db.execute('UPDATE registered SET banner_list = $1 WHERE player_id = $2', new_banner_list, ctx.author.id)
                                await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces - 24 WHERE player_id = $1', ctx.author.id)

                            a = 0

                        else:
                            await self.bot.db.execute('UPDATE registered SET scraps = scraps + 30 WHERE player_id = $1', ctx.author.id)
                            await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces - 24 WHERE player_id = $1', ctx.author.id)

                            a = 1

                        rolling_msg = await ctx.send('Rolling the Wheel of Banners....')

                        random.shuffle(banner_list)

                        for i in range(7):
                            time.sleep(0.2)
                            await rolling_msg.edit(content = f'Rolling the Wheel of Banners.... **{banner_list[i]}**')

                        time.sleep(0.2)
                        await rolling_msg.edit(content = 'You got a ..')
                        time.sleep(0.2)
                        await rolling_msg.edit(content = 'You got a ...')
                        time.sleep(0.2)
                        await rolling_msg.edit(content = 'You got a ....')
                        time.sleep(0.5)
                        await rolling_msg.edit(content = f'You got a ✨ **{chosen}** ✨ banner!')

                        if a == 1:
                            await rolling_msg.edit(content = f'You got a ✨ **{chosen}** ✨ banner!\n\nConverted duplicate banner into 30 scraps!')

                    elif str(reaction_add) == '❌':
                        await ctx.send('Cancelled.')

            else:
                await ctx.send('You do not have enough banner pieces! You need atleast 24.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'addbanner')
    async def add_banner_command(self, ctx, price : int = None, rank : str = None, place : str = None, *, banner_name : str = None,):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if (banner_name is None) or (place is None) or (rank is None):
                em = discord.Embed(
                    title = 'Add Banner',
                    description = '**Add a new banner**\n\nd!addbanner [Price] [Rank] [File name] [Banner Name]',
                    colour = discord.Colour.blue()
                )

                await ctx.send(embed = em)
            
            else:
                if ctx.author.id in [0, 1209502516715192332]:
                    banners = await self.bot.db.fetch('SELECT * FROM banners')

                    banner_list = []

                    for i in range(len(banners)):
                        banner_list.append(banners[i]['banner_name'])

                    if banner_name in banner_list:
                        await ctx.send('That banner is already uploaded!')

                    else:
                        shop = 'False'
                        await self.bot.db.execute('INSERT INTO banners (banner_name,banner_place,rank,price,shop) VALUES ($1,$2,$3,$4,$5)',banner_name.lower(),place,rank,price,shop)

                        await ctx.send('Banner added!')

                else:
                    await ctx.send('You do not have permission to use this command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'addborder')
    async def add_border_command(self, ctx, price : int = None,  rank : str = None, place : str = None, *, banner_name : str = None,):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if (banner_name is None) or (place is None) or (rank is None):
                em = discord.Embed(
                    title = 'Add Border',
                    description = '**Add a new border**\n\nd!addborder [Price] [Rank] [File name] [Border Name]',
                    colour = discord.Colour.blue()
                )

                await ctx.send(embed = em)
            
            else:
                if ctx.author.id in [0, 1209502516715192332]:
                    banners = await self.bot.db.fetch('SELECT * FROM borders')

                    banner_list = []
                    for i in range(len(banners)):
                        banner_list.append(banners[i]['border_name'])

                    if banner_name in banner_list:
                        await ctx.send('That border is already uploaded!')

                    else:
                        shop = 'False'
                        await self.bot.db.execute('INSERT INTO borders (border_name,border_place,rank,price,shop) VALUES ($1,$2,$3,$4,$5)',banner_name.lower(),place,rank,price,shop)

                        await ctx.send('Border added!')

                else:
                    await ctx.send('You do not have permission to use this command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'addavaborder')
    async def add_avaborder_command(self, ctx,  price : int = None, rank : str = None, place : str = None, *, banner_name : str = None,):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if (banner_name is None) or (place is None) or (rank is None) or (price is None):
                em = discord.Embed(
                    title = 'Add AvaBorder',
                    description = '**Add a new Avaborder**\n\nd!addavaborder [Price] [Rank] [File name] [AvaBorder Name]',
                    colour = discord.Colour.blue()
                )

                await ctx.send(embed = em)
            
            else:
                if ctx.author.id in [0, 1209502516715192332]:
                    banners = await self.bot.db.fetch('SELECT * FROM avatar_borders')

                    banner_list = []
 
                    for i in range(len(banners)):
                        banner_list.append(banners[i]['banner_name'])

                    if banner_name in banner_list:
                        await ctx.send('That Avaborder is already uploaded!')

                    else:
                        shop = 'False'
                        await self.bot.db.execute('INSERT INTO avatar_borders (banner_name,avatar_place,rank,price,shop) VALUES ($1,$2,$3,$4,$5)',banner_name.lower(),place,rank,price,shop)

                        await ctx.send('AvaBorder added!')

                else:
                    await ctx.send('You do not have permission to use this command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'addtitle')
    async def add_title_command(self, ctx,  price : int = None, place : str = None,*, banner_name : str = None,):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if (banner_name is None)   or (price is None) or (place is None):
                em = discord.Embed(
                    title = 'Add Title',
                    description = '**Add a new Title**\n\nd!addtitle [Price] [Title ID] [Title Name',
                    colour = discord.Colour.blue()
                )

                await ctx.send(embed = em)
            
            else:
                if ctx.author.id in [0, 1209502516715192332]:
                    banners = await self.bot.db.fetch('SELECT * FROM titles')

                    banner_list = []
 
                    for i in range(len(banners)):
                        banner_list.append(banners[i]['title_place'])

                    if banner_name in banner_list:
                        await ctx.send('That title is already uploaded!')

                    else:
                        shop = 'False'
                        await self.bot.db.execute('INSERT INTO titles (banner_name,price,shop,title_place) VALUES ($1,$2,$3,$4)',banner_name.lower(),price,shop,place)

                        await ctx.send('Title added!')

                else:
                    await ctx.send('You do not have permission to use this command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'asdfcremovebanner')
    async def remove_banner_command(self, ctx, banner_name : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if banner_name is None:
                em = discord.Embed(
                    title = 'Add Banner',
                    description = '**Add a new banner**\n\nd!addbanner [banner name (must be only one name)] [imagine link]',
                    colour = discord.Embed.blue()
                )

                await ctx.send(embed = em)

            else:
                if ctx.author.id in [0]:
                    banners = await self.bot.db.fetch('SELECT * FROM banners')

                    banner_list = []

                    for i in range(len(banners)):
                        banner_list.append(banners[i]['banner_name'])

                    if banner_name.title() not in banner_list:
                        await ctx.send('That banner does not exist!')

                    else:
                        await self.bot.db.execute('DELETE FROM banners WHERE banner_name = $1', banner_name.title())

                        await self.bot.db.execute('UPDATE registered SET current_banner = NULL WHERE current_banner = $1', banner_name.title())

                        await ctx.send(f'{banner_name.title()} has been deleted.')

                else:
                    await ctx.send('You do not have permission to use this command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'catalog', aliases = ['c'])
    async def banners_command(self, ctx):
        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

  
        if user_ban_list:
            await ctx.send('You are banned from the bot.')

        else:       
            registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
 
            if registered_check == []:
                await ctx.send('You have not registered yet! Use `d!start` to register.')
                return

            em = discord.Embed(
                    title = 'Item Catalog',
                    description = '',
                    colour = color
            )
            em.set_image(url="attachment://profilenew.png")
            em.set_footer(text='Select items to try out a profile')
            
            followup = await ctx.send(file = discord.File('profilenew.png') ,embed = em)
            view = bannersembed(ctx.author, registered_check, self.bot, followup)

            await followup.edit(view = view)























            return
            categories = None
            if (stat == 'titles') or (stat == 'title') or (stat == 't'):
                stats = 'titles'
                lists = 'title_list'
                name = 'title_place'
            elif (stat == 'borders') or (stat == 'border') or (stat == 'bo'):
                stats = 'borders'
                lists = 'border_list'
                name = 'border_name'
            elif (stat == 'avaborders') or (stat == 'avaborder') or (stat == 'a'):
                stats = 'avatar_borders'
                lists = 'avaborder_list'
                name = 'banner_name'
            elif (stat == 'banners') or (stat == 'banner') or (stat == 'b'):
                stats = 'banners'
                lists = 'banner_list'
                name = 'banner_name'
                
            else:
                await ctx.send("Incorrect item type. **banner/border/avaborder/titles**")
                return 

            if filters is None:
                pass
            else:
                filters = filters.title()
                filtersd = filters.upper()
            if filters is None:
                categories = True
                lb = await self.bot.db.fetch(f'SELECT * FROM {stats}')
            elif (filtersd == 'SS') or (filtersd == 'S') or (filtersd == 'A') or (filtersd == 'B') or (filtersd == 'C') or (filtersd == 'D'):
                lb = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE rank = $1',filtersd)
            
            elif (filters == 'Category') or (filters == 'Cat'):

                if category == None:
                    await ctx.send(f"Please mention a category, `d!catalog category [category]`")
                    return
                else:
                    lb = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE banner_category = $1',category.lower())
                    if lb == []:
                        await ctx.send(f"Category Not Found. Use `d!catalog category` to search for categories`")
                        return
            
            elif (filters == 'All'):
                lb = await self.bot.db.fetch(f'SELECT * FROM {stats}')

            else:
                filters = filters.lower()
                start = f'{filters}%'
                lb = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE {name} LIKE $1',start)
            if categories == True:
                pass
            else:
                if lb == []:
                    await ctx.send(f"Your search for **{filters}** didn't return any results. Were you trying to use a filter? `SS`, `S`, `A`, `B`,`C`, `D`")
                    return
                
            my_lb = self.listing(registered_check[0][lists])
            data = []
            
            if categories == True:
                categori = []
                for i in lb:
                    if i['banner_category'] in categori:
                        pass
                    else:
                        categori.append(i['banner_category'])
                if 'new' in categori:
                    categori.remove('new')
                    categori.insert(0, 'new') 
                else:
                    pass

                data = categori
            else:
                lb.reverse()
                for faction in lb:
                    data.append(faction[name])
            
            pagination_view = RPaginationView()
            pagination_view.data = data
            pagination_view.lb = lb
            pagination_view.my_lb = my_lb
            pagination_view.stat = stat
            pagination_view.category = categories
            pagination_view.registered_check = registered_check

            await pagination_view.send(ctx)


    @commands.command(name = 'view',  aliases = ['v'])
    async def banner_command(self, ctx, stat : str = None, item : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

  
        if user_ban_list:
            await ctx.send('You are banned from the bot.')

        else:
            if registered_check:

                if (stat is None) or (item is None):
                    em = discord.Embed(
                        title = 'View Item',
                        description = '**View an item.**\n\nd!view [Item type] [Item name]\n[item type] banner,border,avaborder,title',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    stat = stat.lower()
                    if (stat == 'border') or (stat == 'borders') or (stat == 'bo'):
                        stats = 'borders'
                        place = 'border_place'
                        lists = 'border_list'
                        name = 'border_name'
                        count = 'border_count'
                    elif (stat == 'avaborder') or (stat == 'avaborders') or (stat == 'a'):
                        stats = 'avatar_borders'
                        place = 'avatar_place'
                        lists = 'avaborder_list'
                        name = 'banner_name'
                        count = 'avaborder_count'
                    elif (stat == 'banner') or (stat == 'banners') or (stat == 'b'):
                        stats = 'banners'
                        place = 'banner_place'
                        lists = 'banner_list'
                        name = 'banner_name'
                        count = 'banner_count' 
                    else:
                        await ctx.send("Incorrect item type. **banner/border/avaborder**")
                        return 
                    banners = await self.bot.db.fetch(f'SELECT * FROM {stats}')



                    banner_list =  []
                    for i in range(len(banners)):
                        banner_list.append(banners[i][name])

                    if item.lower() in banner_list:
                        chosen_banner = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE {name} = $1', item.lower())
                        if chosen_banner[0]["price"] == 0:
                            price = '**Not purchasable through the shop**'
                        else:
                            price = f'x**{chosen_banner[0]["price"]}**'
                        
                        if chosen_banner[0]["banner_category"] == None:
                            category = ''
                        else:
                            category = f'({chosen_banner[0]["banner_category"].title()})'
                        banner_embed = discord.Embed(
                            title = chosen_banner[0][name].title(),
                            description = f'Rank | **{chosen_banner[0]["rank"].upper()}**\nCost | {price}\n{category}',
                            colour = color
                        )
                        banneris = chosen_banner[0][place]

            


                        banner_embed.set_image(url=f"attachment://{banneris}")
                        view = Tryout(ctx.author) 
                        sent = await ctx.send(file = discord.File(banneris) , embed = banner_embed, view = view)
                        await view.wait()

                        if view.value == True:
                            banner = await self.bot.db.fetch('SELECT * FROM banners WHERE banner_name = $1', registered_check[0]['current_banner'])
                            if banner == []:
                                check = 'default.png'
                            else:
                                check = banner[0]["banner_place"]      
                            if  (check.endswith(('.gif') )) or (banneris.lower().endswith(('.gif'))):
                                await ctx.send("This feature is not available for Gifs.")
                            else:                                
                                if (stat == 'banner') or (stat == 'banners') or (stat == 'b'):
                                    profile = Image.open(banneris)
                                    profile.convert('RGBA')                        
                                else:
                                    if registered_check[0]['current_banner'] is None:
                                        
                                        profile = Image.open("default.png")
                                        profile.convert('RGBA')
                                        
                                    else:                                                    
                                        banner = await self.bot.db.fetch('SELECT * FROM banners WHERE banner_name = $1', registered_check[0]['current_banner'])
                                        bannerisd = banner[0]["banner_place"]
                                        profile = Image.open(bannerisd)
                                        profile.convert('RGBA')

                                titleis = 'Player'                       
                                if (stat == 'border') or (stat == 'borders') or (stat == 'bo'):
                                    borderis = Image.open(banneris)
                                else:
                                    if registered_check[0]['banner_border'] is None:
                                        
                                        borderis = Image.open("profile1.png")
                                        
                                    else:
                                    
                                        border = await self.bot.db.fetch('SELECT * FROM borders WHERE border_name = $1', registered_check[0]['banner_border'])
                                        borderis = f'{border[0]["border_place"]}'
                                        borderis = Image.open(borderis)
                                if (stat == 'avaborder') or (stat == 'avaborders') or (stat == 'a'):
                                    avaborderis = Image.open(banneris)
                                else:
                                    if registered_check[0]['avatar_border'] is None:
                                        
                                        avaborderis = Image.open("profile2.png")
                                        
                                    else:
                                    
                                        avaborder = await self.bot.db.fetch('SELECT * FROM avatar_borders WHERE banner_name = $1', registered_check[0]['avatar_border'])
                                        avaborderis = f'{avaborder[0]["avatar_place"]}'
                                        avaborderis = Image.open(avaborderis)

                                font = ImageFont.truetype("BebasNeue-Regular.ttf", 150)
                                font2 =  ImageFont.truetype("BebasNeue-Regular.ttf", 70)
                                font3 =  ImageFont.truetype("BebasNeue-Regular.ttf", 50)  
                                
                                layout = Image.open("defaultlayout.png")
                                profile.paste(layout, (0,0), layout.convert('RGBA'))                      
                                
                                profile.paste(borderis, (0,0), borderis.convert('RGBA'))
                                
                                    
                                name = f'{ctx.author.display_name}'
                                data = BytesIO(await ctx.author.display_avatar.read())
                                pfp = Image.open(data)
                                pfp.convert('RGBA')
                                pfp = pfp.resize((300,300))
                                mask_im = Image.new("L", pfp.size, 0)
                                draw = ImageDraw.Draw(mask_im)
                                draw.rounded_rectangle((0, 0, 300, 300), fill=255,width=3, radius=15)
                                profile.paste(pfp, (40,30), mask_im)
                                profile.paste(avaborderis, (0,0), avaborderis.convert('RGBA'))
                                
                                guild = self.bot.get_guild(774883579472904222)
                                role = guild.get_role(798548690860113982)
                                player_clan_1 = "Clan | None"
                                if role in ctx.author.roles:
                                    
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
                                rarerank = 'Rares | None'
                                comrank = "Comm | None"
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
                                profile.save(bytes, format="PNG")
                                bytes.seek(0)
            

                                banner_embed.set_image(url=f"attachment://profile.png")
                                await sent.edit(file = discord.File(bytes,"profile.png"),embed = banner_embed)

                    else:
                        await ctx.send('Item not found.')

            else:
                await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'set')
    async def set_banner_command(self, ctx, stat: str = None,*,banner_name : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

  
        if user_ban_list:
            await ctx.send('You are banned from the bot.')

        else:
            if registered_check:
                if (banner_name is None) or (stat is None):
                    em = discord.Embed(
                        title = 'Set Item',
                        description = 'Set your default Banner/Title/Border/AvaBorder for your profile.\n\n**d!set [item type] [item name]**\n\n[item type] banner,border,avaborder,title',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    if (stat == 'title') or (stat == 'titles') or (stat == 't'):
                        stats = 'titles'
                        lists = 'title_list'
                        name = 'title_place'
                        current = 'title'
                    elif (stat == 'border') or (stat == 'borders')or (stat == 'bo'):
                        stats = 'borders'
                        lists = 'border_list'
                        name = 'border_name'
                        current = 'banner_border'
                    elif (stat == 'avaborders') or (stat == 'avaborder')or (stat == 'a'):
                        stats = 'avatar_borders'
                        lists = 'avaborder_list'
                        name = 'banner_name'
                        current = 'avatar_border'
                    elif  (stat == 'banner') or (stat == 'banners')or (stat == 'b'):
                        stats = 'banners'
                        lists = 'banner_list'
                        name = 'banner_name'
                        current = 'current_banner'
                    elif  (stat == 'oddity') or (stat == 'o')or (stat == 'oddities'):
                        stats = 'oddities'
                        lists = 'oddities'
                        name = 'oddities_name'

                        banners = await self.bot.db.fetch(f'SELECT * FROM {stats}')
                        banner_list = []
                        for i in range(len(banners)):
                            banner_list.append(banners[i][name])
                        if banner_name.lower() == 'none':
                            oddity = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE oddities_name = $1',banner_name.lower())
                            role = guild.get_role(int(oddity[0]['oddities_place']))
                            await ctx.author.remove_roles(role) 
                            await self.bot.db.execute(f'UPDATE registered SET current_badge = NULL WHERE player_id = $1', ctx.author.id)
                            await ctx.send("Badge set to None.")
                            return

                        if banner_name.lower() in banner_list:         
                            flists = str(registered_check[0][lists])
                            my_banner_list = self.listing(flists)
                            if (banner_name.lower() in my_banner_list) or (ctx.author.id == 0):
                                oddity = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE oddities_name = $1',banner_name.lower())
                                if oddity[0]['oddities_type'] == 'badge':
                                    guild = self.bot.get_guild(774883579472904222)
                                    role = guild.get_role(int(oddity[0]['oddities_place']))
                                    if registered_check[0]['current_badge'] == None:
                                        pass
                                    else:
                                        role2 = guild.get_role(int(registered_check[0]['current_badge']))
                                        await ctx.author.remove_roles(role2) 
                                    await self.bot.db.execute(f'UPDATE registered SET current_badge = $1 WHERE player_id = $2', oddity[0]['oddities_place'], ctx.author.id)
                                    await ctx.author.add_roles(role)
                                    
                                await ctx.send(f'Set as {banner_name.title()}')

                            else:
                                await ctx.send('You do not own that item.')

                        else:
                            await ctx.send('Item not found.')
                        
                        return
                    else:
                        await ctx.send("Incorrect item type. **banner/border/avaborder/title/oddity**")
                        return 
                    banners = await self.bot.db.fetch(f'SELECT * FROM {stats}')
                    banner_list = []
                    title = await self.bot.db.fetch(f'SELECT * FROM titles WHERE title_place = $1', banner_name.lower())
                    if banner_name.lower() == 'none':
                        await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', ctx.author.id) 
                        await self.bot.db.execute(f'UPDATE registered SET {current} = NULL WHERE player_id = $1',ctx.author.id)
                        await ctx.send(f'Set as default.')
                        return


                    for i in range(len(banners)):
                        banner_list.append(banners[i][name])
                    
                    if banner_name.lower() in banner_list:         
                        flists = str(registered_check[0][lists])
                        my_banner_list = self.listing(flists)
                        if (banner_name.lower() in my_banner_list) or (ctx.author.id == 0):
                            if (stat == 'titles') or (stat == 'title') or (stat == 't'):
                                banner_name = title[0]['banner_name'] 
                            await self.bot.db.execute(f'UPDATE registered SET profile = NULL WHERE player_id = $1', ctx.author.id)                        
                            await self.bot.db.execute(f'UPDATE registered SET {current} = $1 WHERE player_id = $2', banner_name.lower(), ctx.author.id)

                            await ctx.send(f'Set as {banner_name.title()}')

                        else:
                            await ctx.send('You do not own that item.')

                    else:
                        await ctx.send('Item not found.')

            else:
                await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'refund', aliases = ['rf'])
    async def refundr_command(self, ctx, stat: str = None, banner_name :str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if (banner_name is None) or (stat is None):
                em = discord.Embed(
                    title = 'Refund',
                    description = 'Refund an item.\n\n**d!refund [item type] [item name]**\n\n[item type] banner,border,avaborder',
                    colour = color
                )

                await ctx.send(embed = em)

            else:
                if (stat == 'border') or (stat == 'borders')or (stat == 'bo'):
                    stats = 'borders'
                    lists = 'border_list'
                    name = 'border_name'
                    current = 'banner_border'
                    count = 'border_count'
                elif (stat == 'avaborders') or (stat == 'avaborder')or (stat == 'a'):
                    stats = 'avatar_borders'
                    lists = 'avaborder_list'
                    name = 'banner_name'
                    current = 'avatar_border'
                    count = 'avaborder_count'
                elif  (stat == 'banner') or (stat == 'banners')or (stat == 'b'):
                    stats = 'banners'
                    lists = 'banner_list'
                    name = 'banner_name'
                    current = 'current_banner'
                    count = 'banner_count'
                elif (stat == 'title') or (stat == 'titles')or (stat == 't'):
                    await ctx.send("Titles can't be refunded.")
                    return
                else:
                    await ctx.send("Incorrect item type. **banner/border/avaborder**")
                    return 
                
                banners = await self.bot.db.fetch(f'SELECT * FROM {stats}')
                banner_list = []
                for i in range(len(banners)):
                    banner_list.append(banners[i][name])

                if banner_name.lower() in banner_list:         
                    flists = str(registered_check[0][lists])
                    my_banner_list = self.listing(flists)
                    if banner_name.lower() in my_banner_list:
                        no = ['bronze','silver','gold','platinum','dominant','bronze2', 'silver2', 'gold2', 'platinum2', 'dominant2','casual']
                        if banner_name.lower() in no:
                            await ctx.send("You can't refund those!")
                        else:
                            bannerd = await self.bot.db.fetch(f'SELECT * FROM {stats} WHERE {name} = $1', banner_name.lower())
                            dc1 = bannerd[0]['price']
                            if dc1 == 0:
                                rank = bannerd[0]['rank']
                                if rank == 'S':
                                    dc = 750
                                elif rank == 'A':
                                    dc = 500
                                elif rank == 'B':
                                    dc = 300
                                elif rank == 'C':
                                    dc = 200
                                elif rank == 'D':
                                    dc = 100
                                elif rank == 'SS':
                                    dc = 0
                                else:
                                    await ctx.send('Unknown error')
                                    return
                            else:
                                dc = dc1
                            dc = int(dc/2)
                            view = ConfirmCancel(ctx.author)                    
                            if dc == 0:
                                                                    
                                await ctx.send(f"Are you sure you want to refund **{banner_name.title()}** for **5 Lootboxes + 5 Keys**?", view = view)
                                await view.wait()                  
                            else:                                               
                                await ctx.send(f"Are you sure you want to refund **{banner_name.title()}** for **{dc}dc**?", view = view)
                                await view.wait()

                            if view.value is True:

                                registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                                flists = str(registered_check[0][lists])
                                my_banner_list = self.listing(flists)
                                if banner_name.lower() in my_banner_list:

                                    if dc == 0:                                
                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 5, scraps = scraps + 5 WHERE player_id = $1', ctx.author.id) 
                                    else:    
                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {dc} WHERE player_id = $1', ctx.author.id) 
                                    new_admins = ''
                                    admins_list = self.listing(flists)
                                    t = 1
                                    s = 1
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
                                            if admin == banner_name.lower():
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
                                            if admin == banner_name.lower():
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
                                    await self.bot.db.execute(f'UPDATE registered SET {count} = {count} - 1 WHERE player_id = $1', ctx.author.id) 
                                    if dc == 0: 
                                        await ctx.send(f"Refunded **{banner_name.title()}** for **5 Lootboxes + 5 Keys**.")
                                    else:
                                        await ctx.send(f"Refunded **{banner_name.title()}** for **{dc}dc**.")
                                else:
                                    await ctx.send('You do not own that item.')

                            elif view.value == False:
                                await ctx.send("Cancelled.")
                            else:
                                await ctx.send("Timed out.")
                    else:
                        await ctx.send('You do not own that item.')

                else:
                    await ctx.send('Item not found.')                            

            
        else: 
            await ctx.send('You have not registered yet! Use `d!start` to register.')


    @commands.command(name = 'addcard')
    async def add_card_command(self, ctx,price : int = None, rank: str= None, url : str = None, url2 :str = None,banner_name : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if (banner_name is None) or (url is None) or(price is None) or (url2 is None):
                em = discord.Embed(
                    title = 'Add Card',
                    description = '**Add a new card**\n\nd!addcard [Price] [Rank] [File link] [File name] [Card Name]',
                    colour = color
                )

                await ctx.send(embed = em)
            
            else:
                if ctx.author.id in [0,779031315789906010,504680133169250304]:
                    banners = await self.bot.db.fetch('SELECT * FROM cards')

                    banner_list = []

                    for i in range(len(banners)):
                        banner_list.append(banners[i]['card_name'])

                    if banner_name.lower() in banner_list:
                        await ctx.send('That banner is already uploaded!')

                    else:
                        if (str(url).startswith('https://discord.com/channels/') is True) or (str(url).startswith('https://media') is True):
                            shop = 'False'
                            await self.bot.db.execute('INSERT INTO cards (card_name,card_place,rank,price,shop) VALUES ($1,$2,$3,$4,$5,$6)',banner_name.lower(),url,rank,price,shop,url2)

                            await ctx.send('Card added!')

                        else:
                            await ctx.send('Invalid link.')

                else:
                    await ctx.send('You do not have permission to use this command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')






    @commands.command(name = 'fffbadges')
    async def badges_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            badges = {}

            badges = self.f_badges(badges)

            badges_keys = list(badges.keys())

            all_badges = ''

            for i in range(0,len(badges_keys),3):
                if all_badges == '':
                    all_badges += f'{badges[badges_keys[i]]["emoji"]} - {badges_keys[i].title()} | {badges[badges_keys[i+1]]["emoji"]} - {badges_keys[i+1].title()} | {badges[badges_keys[i+2]]["emoji"]} - {badges_keys[i+2].title()}'

                else:
                    if i < len(badges):
                        all_badges += f'\n\n{badges[badges_keys[i]]["emoji"]} - {badges_keys[i].title()} '

                    if i+1 < len(badges):
                        all_badges += f'| {badges[badges_keys[i+1]]["emoji"]} - {badges_keys[i+1].title()} '

                    if i+2 < len(badges):
                        all_badges += f'| {badges[badges_keys[i+2]]["emoji"]} - {badges_keys[i+2].title()}'

            badges_embed = discord.Embed(
                title = 'Badges',
                description = all_badges,
                colour = color
            )

            await ctx.send(embed = badges_embed)

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.group(name = 'cccbadge', invoke_without_command = True)
    async def badge_command(self, ctx, *, badge_name = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if badge_name is None:
                em = discord.Embed(
                    title = 'Badge',
                    description = 'Badge command.',
                    colour = discord.Colour.blue()
                )

                em.add_field(name = 'd!badge [badge name]', value = 'View a badge and how to obtain it.')
                em.add_field(name = '\u200b', value = '\u200b')
                em.add_field(name = '\u200b', value = '\u200b')
                em.add_field(name = 'd!badge give [mention] [badge name]', value = 'Award a badge to a player.')
                em.add_field(name = '\u200b', value = '\u200b')
                em.add_field(name = '\u200b', value = '\u200b')
                em.add_field(name = 'd!badge take [mention] [badge name]', value = 'Take a badge from a player.')
                em.add_field(name = '\u200b', value = '\u200b')
                em.add_field(name = '\u200b', value = '\u200b')

                await ctx.send(embed = em)

            else:
                badges = {}

                badges = self.f_badges(badges)

                if badge_name.lower() in badges:
                    badge_em = discord.Embed(
                        title = f'{badge_name.title()} badge',
                        description = f'{badges[badge_name.lower()]["emoji"]} - {badges[badge_name.lower()]["desc"]}',
                        colour = discord.Colour.dark_orange()
                    )

                    await ctx.send(embed = badge_em)

                else:
                    await ctx.send('Badge not found.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @badge_command.command(name = 'aaagive', aliases = ['gv'])
    async def badge_give_command(self, ctx, member : discord.Member = None, *, badge_name : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if str(ctx.author.id) in admins_list:
                if (member is None) or (badge_name is None):
                    em = discord.Embed(
                        title = 'Badge Give',
                        description = '**Award a badge to a user.**\n\nd!badge give [mention] [badge name]',
                        colour = discord.Colour.blue()
                    )

                    await ctx.send(embed = em)

                else:
                    member_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                    if member_check:
                        badges = {}

                        badges = self.f_badges(badges)
                        
                        if badge_name.lower() in badges:
                            if member_check[0]['badges'] is None:
                                await self.bot.db.execute('UPDATE registered SET badges = $1 WHERE player_id = $2', badges[badge_name.lower()]["emoji"], member.id)

                                await ctx.send(f'{badges[badge_name.lower()]["emoji"]} badge has been awarded to {member.mention}')

                            else:
                                member_badges = member_check[0]['badges'].split()

                                if badges[badge_name.lower()]["emoji"] not in member_badges:
                                    new_badges = member_check[0]['badges'] + f' {badges[badge_name.lower()]["emoji"]}'

                                    await self.bot.db.execute('UPDATE registered SET badges = $1 WHERE player_id = $2', new_badges, member.id)

                                    await ctx.send(f'{badges[badge_name.lower()]["emoji"]} badge has been awarded to {member.mention}')

                                elif badge_name.lower() == 'leaderboard':
                                    new_badges = member_check[0]['badges'] + f' {badges[badge_name.lower()]["emoji"]}'

                                    await self.bot.db.execute('UPDATE registered SET badges = $1 WHERE player_id = $2', new_badges, member.id)

                                    await ctx.send(f'{badges[badge_name.lower()]["emoji"]} badge has been awarded to {member.mention}')
                                
                                else:
                                    await ctx.send('That person has already been awarded that badge.')

                        else:
                            await ctx.send('Badge not found.')
                    
                    else:
                        await ctx.send('That person has not registered yet!')

            else:
                await ctx.send('You do not have permission to use that command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @badge_command.command(name = 'tffdasake', aliases = ['tk'])
    async def badge_take_command(self, ctx, member : discord.Member = None, *, badge_name = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if str(ctx.author.id) in admins_list:
                if (member is None) or (badge_name is None):
                    em = discord.Embed(
                        title = 'Badge Take',
                        description = '**Take a badge from a user.**\n\nd!badge take [mention] [badge name]',
                        colour = discord.Colour.blue()
                    )

                    await ctx.send(embed = em)

                else:
                    member_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                    if member_check:
                        badges = {}

                        badges = self.f_badges(badges)

                        if badge_name.lower() in badges:
                            if member_check[0]['badges'] is None:
                                await ctx.send('That person does not have any badges!')
                            
                            else:
                                member_badges = member_check[0]['badges'].split()

                                if badges[badge_name.lower()]["emoji"] in member_badges:
                                    member_badges.remove(badges[badge_name.lower()]["emoji"])

                                    new_badges = ''

                                    for i in member_badges:
                                        if member_badges.index(i) == 0:
                                            new_badges += i

                                        else:
                                            new_badges += f' {i}'

                                    await self.bot.db.execute('UPDATE registered SET badges = $1 WHERE player_id = $2', new_badges, member.id)

                                    await ctx.send(f'{badges[badge_name.lower()]["emoji"]} has been taken from {member.mention}')

                                else:
                                    await ctx.send('That person has not been awarded that badge.')

                        else:
                            await ctx.send('Badge not found.')

                    else:
                        await ctx.send('That person has not registered yet!')

            else:
                await ctx.send('You do not have permission to use that command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'afvcredeem')
    async def redeem_command(self, ctx, member: discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', ctx.guild.id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if str(ctx.author.id) in admins_list:
                if member is None:
                    em = discord.Embed(
                        title = 'Redeem',
                        description = '**Redeem 40k pc for a user**\n\nd!redeem [mention] *(Admin exclusive)*',
                        colour = discord.Colour.blue()
                    )

                    await ctx.send(embed = em)

                else:
                    member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                    if member_registered:
                        if member_registered[0]['pc'] == 0:
                            await ctx.send('That person does not have enough 40k redeem items!')

                        else:
                            confirm_msg = await ctx.send(f'{member.mention} Are you sure you want to redeem 40k pc? This action is irreversible.')

                            await confirm_msg.add_reaction('✅')
                            await confirm_msg.add_reaction('❌')

                            def check(reaction : discord.Reaction, user : discord.User):
                                return user.id == member.id and reaction.message.channel.id == ctx.channel.id and str(reaction.emoji) in ['\U00002705', '\U0000274C']

                            try:
                                reaction_add, user = await self.bot.wait_for(
                                    'reaction_add',
                                    timeout = 15,
                                    check = check
                                )

                            except asyncio.TimeoutError:
                                await ctx.send('Timed-out. Aborted.')
                                return

                            else:
                                if str(reaction_add) == '✅':
                                    await self.bot.db.execute('UPDATE registered SET pc = pc - 1 WHERE player_id = $1', member.id)

                                    await ctx.send('Done. You can now trade the pc.')

                                elif str(reaction_add) == '❌':
                                    await ctx.send('Cancelled.')
                    else:
                        await ctx.send('That person has not registered yet.')

            else:
                    await ctx.send('You do not have pemission to use that command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

        
    @commands.command(name = 'giveodd')
    async def giveod_command(self, ctx, member: discord.Member = None, item : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', ctx.guild.id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if str(ctx.author.id) in admins_list:
                if member is None:
                    em = discord.Embed(
                        title = 'Give Oddity',
                        description = '**Give an oddity to a user**\n\nd!giveodd [mention] [item] *(Admin exclusive)*',
                        colour = discord.Colour.blue()
                    )

                    await ctx.send(embed = em)

                else:       
                    member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)
                    dflists = str(member_registered[0]['oddities'])
                    listbuy = self.listing(dflists)
                    if item.lower() in listbuy:
                        await ctx.send("This person already has this item.")
                        return
                    a = f'{item.lower()}'
                    
                    if member_registered[0]['oddities'] is None:
                        admins_list = self.listing(dflists)
                        new_admins = f' {a}'
                        await self.bot.db.execute(f'UPDATE registered SET oddities = $1 WHERE player_id = $2', str(new_admins), member.id)
                        await ctx.send("Item Given!") 

                    else:
                        new_admins = str(dflists) + f' {a}'
                        await self.bot.db.execute(f'UPDATE registered SET oddities = $1 WHERE player_id = $2', new_admins, member.id)

                        await ctx.send("Item Given!") 
    
    @commands.command(name = 'addodd')
    async def addodd_command(self, ctx, oddity_desc : str = None, oddity_id : str = None,oddity_place : str = None,oddity_price : int = None, oddity_type : str = None, *, oddity_display : str = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', ctx.guild.id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if str(ctx.author.id) in admins_list:
                if (oddity_price is None) or (oddity_place is None) or (oddity_id is None) or (oddity_type is None) or (oddity_display is None):
                    em = discord.Embed(
                        title = 'Add oddity',
                        description = '**Add oddity**\n\nd!addodd [oddity_desc] [oddity_id] [oddity_place] [oddity_price] [oddity_type] [oddity_display]',
                        colour = discord.Colour.blue()
                    )

                    await ctx.send(embed = em)

                else:        
                    shop = 'False'
                    if oddity_desc == 'none':
                        await self.bot.db.execute('INSERT INTO oddities (price,oddities_place,oddities_name,oddities_type,oddities_display,shop) VALUES ($1,$2,$3,$4,$5,$6)',oddity_price,oddity_place,oddity_id,oddity_type,oddity_display,shop)
                    else:
                        await self.bot.db.execute('INSERT INTO oddities (price,oddities_place,oddities_name,oddities_type,oddities_display,shop,oddities_desc) VALUES ($1,$2,$3,$4,$5,$6,$7)',oddity_price,oddity_place,oddity_id,oddity_type,oddity_display,shop,oddity_desc)

                    await ctx.send('Oddity added!')


    @commands.command(name = 'addcat')
    async def addcategory_command(self,ctx, stat :str = None, item :str = None, *, category : str = None ):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(786448967172882442)
            role2 = guild.get_role(1090438349455622204)
            role3 = guild.get_role(781452019578961921)
            if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles):
                if (stat is None) or (item is None) or (category is None):
                    em = discord.Embed(
                        title = 'Misc',
                        description = '**Add category**\n\nd!addcat [banner/avaborder/border] [item name] [category]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:

                    if (stat == 'borders') or (stat == 'border')or (stat == 'bo'):
                        name = 'border_name'
                        stat = 'borders'
                    elif (stat == 'avaborders') or (stat == 'avaborder')or (stat == 'a'):
                        name = 'banner_name'
                        stat = 'avatar_borders'
                    elif (stat == 'banners') or (stat == 'banner')or (stat == 'b'):
                        name = 'banner_name'
                        stat = 'banners'
                    else:
                        await ctx.send("X")
                        return
                    
                    banners = await self.bot.db.fetch(f'SELECT * FROM {stat}')
                    banner_list = []
                    for i in range(len(banners)):
                        banner_list.append(banners[i][name])

                    if item.lower() in banner_list:
                        await self.bot.db.execute(f'UPDATE {stat} SET banner_category = $1 WHERE {name} = $2', category.lower(), item.lower())
                        await ctx.send("Category added!")
                    else:
                        await ctx.send("This item doesn't exist!")
            else:
                await ctx.send("You don't have the permission to perform this command!")

def setup(bot):
    bot.add_cog(MiscCommands(bot))