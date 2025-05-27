import discord
from discord.ext import commands
import asyncpg
import asyncio
import random
import math
import string

color = 0x32006e

class Rules(discord.ui.View):
    current_page : int = 1
    sep : int = 1
    numbre : int = 0
    sort_option = "t"
    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb, self.stat)

    async def create_embed(self, data,lb,stat ):
        lb = self.lb    

        if self.sort_option == 't':
            title = 'Dominant Battling Rules'
            desc = "We here at Dominant want both **beginners** and the **hardcore sweats** to have fun dueling at our server. To make this possible we allow any ruleset to be followed in ranked and be counted as a duel. Just specify which ruleset you want to play with, and you're good to go. Here are the rulesets."
        elif self.sort_option == 'ourare':
            title = 'Rares OU (G8/G9)'
            desc = 'Here are the rules for the format **Rares OU (G8/G9)**'
        elif self.sort_option == 'uurare':
            title = 'Rares UU'
            desc = 'Here are the rules for the format **Rares UU**'
        elif self.sort_option == 'oucommon':
            title = 'Common OU (G8/G9)'
            desc = 'Here are the rules for the format **Common OU (G8/G9)**'
        elif self.sort_option == 'uucommon':
            title = 'Common UU'
            desc = 'Here are the rules for the format **Common UU**'
        elif self.sort_option == 'mixnmega':
            title = 'Mix and Mega'
            desc = 'Here are the rules for the format **Mix and Mega**'
        elif self.sort_option == 'mega':
            title = 'Megas'
            desc = 'Here are the rules for the format **Megas**'
        elif self.sort_option == 'cmr':
            title = 'CMR'
            desc = 'Here are the rules for the format **CMR**'

        em = discord.Embed(
        title = title,
        description = desc,
        colour = color
        )


        if self.sort_option == 't':
            em.add_field(name='Rares', value='**•** OU (G8/G9)\n**•** UU',inline=False)
            em.add_field(name='Common', value='**•** OU (G8/G9)\n**•** UU',inline=False)
            em.add_field(name='Other Formats', value='**•** Mix and Mega\n**•** Megas\n**•** CMR ',inline=False)

        elif self.sort_option == 'ourare':
            em.add_field(name="Ruleset", value="• Skips on misses with moves which have a minimum of 70 acc (Rares)\n• Redo on crucial miss\n• Redo on crucial freeze/crucial paralysis\n• No 151+ moves\n• No duplicates", inline=False)
            em.add_field(name="Pokemons banned", value="None", inline=False)
            em.add_field(name="Moves Banned", value="• The following Gen 8 moves are banned: Eternabeam, V-Create, and Dragon Ascent\n• No heals (dream eater type moves are ok)\n• No venom drench", inline=False)

        elif self.sort_option == 'uurare':
            em.add_field(name="Ruleset", value="• Skips on misses with moves which have a minimum of 70 acc (Rares)\n• Redo on crucial miss\n• Redo on crucial freeze/crucial paralysis\n• No 151+ moves\n• No duplicates", inline=False)
            em.add_field(name="Pokemons banned", value="Mega Rayquaza, Koraidon, Miraidon, Magearna, Primal Groudon, Primal Kyogre, Yveltal, Mega Metagross, Mega Salamence, Arceus, Marshadaow, Zacian, Eternatus Banned, Mega Mew2.\n\nYou can use megas, paradox, slaking, and regular Ray, Kyo, Grou, Mew2, and unbanned rares.", inline=False)
            em.add_field(name="Moves Banned", value="• No venom drench\n• The following Gen 8 moves are banned: Eternabeam, V-Create, and Dragon Ascent\n• No heals (dream eater type moves are ok)", inline=False)

        elif self.sort_option == 'oucommon':
            em.add_field(name="Ruleset", value="• Skips on misses with moves which have a minimum of 75 acc (Commons)\n• Redo on crucial miss\n• Redo on crucial freeze/crucial paralysis\n• No 151+ moves\n• No duplicates", inline=False)
            em.add_field(name="Pokemons banned", value="• Slaking, Iron Hands, Flutter Mane, Slither Wing, Great Tusk, Iron Moth, Walking Wake, Iron Leaves are banned (commons)", inline=False)
            em.add_field(name="Moves Banned", value="• No venom drench\n• No heals (dream eater type moves are ok)", inline=False)


        elif self.sort_option == 'uucommon':
            em.add_field(name="Ruleset", value="• Skips on misses with moves which have a minimum of 90 acc (Commons)\n• Redo on crucial miss\n• Redo on crucial freeze/crucial paralysis\n• No 141+ moves\n• No duplicates", inline=False)
            em.add_field(name="Pokemons banned", value="• Metagross, Primarina, Golisopod, Garchomp, Braviary, Salamence, Staraptor, Slaking, Dragapult, Dragonite, Kommo-o, Falinks, Infernape, Haxorus, Sneasler, Ursaluna, Grimmsnarl, Hawlucha\n• All Paradox Pokemon Banned Besides: Brute Bonnet, Iron Thorns, and Sandy Shocks", inline=False)
            em.add_field(name="Moves Banned", value="• No heals (dream eater type moves are ok)\n• No venom drench\n• No superpower", inline=False)


        elif self.sort_option == 'mixnmega':
            em.add_field(name="Ruleset", value="• Skips on misses with moves which have a minimum of 70 acc\n• Redo on crucial miss\n• Redo on crucial freeze/crucial paralysis\n• No 151+ moves\n• No duplicates\n• You Will be allowed to use Only One Paradox Pokemon (Gen 9), Commons, Rares, and Mega per Team.", inline=False)
            em.add_field(name="Pokemons banned", value="Assume all forms of a Pokemon are banned unless specified (ex. no form of Groudon, Kyogre, Rayquaza, Mewtwo can be added to a duel, for instance).\n\nRares Banned: Rayquaza, Kyogre, Groudon, Reshiram, Zekrom, Dialga, Palkia, Arceus, Giratina, Yveltal, Marshadow, Xerneas, Mega-Diancie, Miraidon, Koraidon, Zacian, Zamazenta, Mewtwo, Lugia, Ho-oh, Attack Deoxys, Lunala, Solgaleo, Complete Zygarde, Regigigas, Magearna, Eternatus.\n\nMegas Banned: Mega Metagross, Mega Salamence.\n\nComs Banned: Slaking\n\nMega Latios/as will count as a Mega Evolution, Walking Wake and Iron Leaves count as Paradox Pokemon.", inline=False)
            em.add_field(name="Moves Banned", value="• No venom drench\n• The following Gen 8 moves are banned: Eternabeam, V-Create, and Dragon Ascent\n• No heals (dream eater type moves are ok)", inline=False)

        elif self.sort_option == 'mega':
            em.add_field(name="Ruleset", value="• Skips on misses with moves which have a minimum of 75 acc\n• Redo on crucial miss\n• Redo on crucial freeze/crucial paralysis\n• No 151+ moves\n• Only mega evolutions\n• No duplicates", inline=False)
            em.add_field(name="Pokemons banned", value="None", inline=False)
            em.add_field(name="Moves Banned", value="• No venom drench\n• The following Gen 8 moves are banned: Eternabeam, V-Create, and Dragon Ascent\n• No heals (dream eater type moves are ok)", inline=False)

        elif self.sort_option == 'cmr':
            em.add_field(name="Ruleset", value="• Skips on misses with moves which have a minimum of 70 acc (Rares)\n• Redo on crucial miss\n• Redo on crucial freeze/crucial paralysis\n• No 151+ moves\n• No duplicates\n• One common, one mega, one rare, paradox in one team", inline=False)
            em.add_field(name="Pokemons banned", value="None", inline=False)
            em.add_field(name="Moves Banned", value="• No venom drench\n• The following Gen 8 moves are banned: Eternabeam, V-Create, and Dragon Ascent\n• No heals (dream eater type moves are ok)", inline=False)

        self.change = 'no'
        em.set_footer(text=f'Made by Dominant Battling Staff')
        return em

    async def update_message(self,data, lb, stat):
        await self.message.edit(embed= await self.create_embed(data, lb, stat), view=self)

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

    @discord.ui.select(placeholder="Pick format to info...", min_values=1, max_values=1,
                       options=[
                           discord.SelectOption(label="Rares OU", value="ourare"),
                           discord.SelectOption(label="Rares UU", value="uurare"),
                           discord.SelectOption(label="Commons OU", value="oucommon"),
                           discord.SelectOption(label="Commons UU", value="uucommon"),
                           discord.SelectOption(label="Mix and Mega", value="mixnmega"),
                           discord.SelectOption(label="Megas", value="mega"),
                           discord.SelectOption(label="CMR", value="cmr"),
                       ])

    async def sort_dropdown(self, select: discord.ui.Select, interaction: discord.Interaction):
        await interaction.response.defer()
        self.sort_option = select.values[0]
        self.change = 'yes'
        self.current_page = 1
        await self.update_message(self.get_current_page_data(), self.lb, self.stat)

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
                            await ctx.send(f"Completed Daily Quest | {strs[int(admins_list[0])]}\n Awarded **25dc** to <@{author_id}>")
                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1', author_id) 
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
        if check1[0]['quests'] == None:
            pass
        else:
            flists = str(check1[0]['quests'])
            new_admins = ''
            admins_list = listing(flists)
            strs = ['Complete 5 casual duel', 'Win 3 casual duel','Complete 5 ranked duel', 'Win 3 ranked duel','Complete 5 ranked with commons' , 'complete 5 ranked with rares','Trade 3 times with another user in Dom Bot']

            for p,admin in enumerate(admins_list):
        
                if p == 0:
                    new_admins += str(admin)
                elif p == 1:

                    if int(admins_list[0]) in m:   
                        if admin == admins_list[2]:
                            pass
                        elif int(admin) == (int(admins_list[2])-1):
                            await ctx.send(f"Completed Daily Quest | {strs[int(admins_list[0])]}\n Awarded **25dc** to <@{member_id}>")
                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1', member_id) 
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

class WPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 8
    numbre : int = 0
    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb, self.stat)

    async def create_embed(self, data,lb,stat ):
        lb = self.lb
        stat = self.stat
        if stat.lower() == 'rare':
            desc = "Points"
            gamble = 'Weekly Rare Leaderbaord'
        elif stat.lower() == 'common':
            desc = "Points"
            gamble = 'Weekly Common Leaderbaord'
        elif stat.lower() == 'gamble':
            desc = "Net"
            gamble = 'Weekly Gamble Leaderbaord'
        else:
            desc = "Points"
            gamble = 'Weekly Rare Leaderbaord'   

        scoreStr = ''        
        lb_embed = discord.Embed(
            title = gamble,
            description = f'Top Players for each leaderboard get rewarded dc',
            colour = color
        )
        for i in data:
            
            if stat.lower() == 'rare':
                crudescore3 = lb[self.numbre]['weekly']
                if crudescore3 > 0:
                    crudescore3 = f'{"{:,}".format(crudescore3)}'
                else:
                    crudescore3 = f'{"{:,}".format(crudescore3)}'
            elif stat.lower() == 'common':
                crudescore3 = lb[self.numbre]['weekly']
                if crudescore3 > 0:
                    crudescore3 = f'{"{:,}".format(crudescore3)}'
                else:
                    crudescore3 = f'{"{:,}".format(crudescore3)}'
            elif stat.lower() == 'gamble':
                crudescore3 = lb[self.numbre]['weekly']
                if crudescore3 > 0:
                    crudescore3 = f'+{"{:,}".format(crudescore3)}pc'
                else:
                    crudescore3 = f'{"{:,}".format(crudescore3)}pc'

            scoreStr = f"**{desc} 》 **{crudescore3}"
            
            lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
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



class DPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 8
    numbre : int = 0
    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb, self.stat)

    async def create_embed(self, data,lb,stat ):
        lb = self.lb
        stat = self.stat
        if stat.lower() == 'rare':
            desc = "Points"
            gamble = 'Daily Rare Leaderbaord'
        elif stat.lower() == 'common':
            desc = "Points"
            gamble = 'Daily Common Leaderbaord'
        elif stat.lower() == 'gamble':
            desc = "Net"
            gamble = 'Daily Gamble Leaderbaord'
        else:
            desc = "Points"
            gamble = 'Daily Rare Leaderbaord'   

        scoreStr = ''        
        lb_embed = discord.Embed(
            title = gamble,
            description = f'Top Players for each leaderboard get rewarded Lootboxes',
            colour = color
        )
        for i in data:
            
            if stat.lower() == 'rare':
                crudescore3 = lb[self.numbre]['daily']
                if crudescore3 > 0:
                    crudescore3 = f'{"{:,}".format(crudescore3)}'
                else:
                    crudescore3 = f'{"{:,}".format(crudescore3)}'
            elif stat.lower() == 'common':
                crudescore3 = lb[self.numbre]['daily']
                if crudescore3 > 0:
                    crudescore3 = f'{"{:,}".format(crudescore3)}'
                else:
                    crudescore3 = f'{"{:,}".format(crudescore3)}'
            elif stat.lower() == 'gamble':
                crudescore3 = lb[self.numbre]['daily']
                if crudescore3 > 0:
                    crudescore3 = f'+{"{:,}".format(crudescore3)}pc'
                else:
                    crudescore3 = f'{"{:,}".format(crudescore3)}pc'

            scoreStr = f"**{desc} 》 **{crudescore3}"
            
            lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
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
        try:
            await interaction.response.edit_message(view=self)
        except discord.errors.NotFound as e:
            pass
            
            
    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.red, emoji = "❌" )
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

async def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class RPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 8
    numbre : int = 0
    sort_option = "global"
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
            title = 'Rare Ranked Leaderboard',
            description = f'Click the buttons to change pages.',
            colour = color
        )
        if self.change == 'no':
            pass
        else:
            self.numbre = 0
        


        if self.sort_option == 'global':      
            lb = await stat.db.fetch('SELECT * FROM rank_system WHERE matches_played >= 0 ORDER BY points DESC')
            for i in data:
                scoreStr = f"**Rank 》 **{lb[self.numbre]['player_rank']}\n**Points 》 **{lb[self.numbre]['points']}"
                lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1
            self.change = 'no'
        elif self.sort_option == 'wins':      
            lb = await stat.db.fetch('SELECT * FROM rank_system WHERE matches_played >= 0 ORDER BY wins DESC')
            for i in data:
                winrate = round(lb[self.numbre]['wins'] / lb[self.numbre]['matches_played'] * 100, 2) if lb[self.numbre]['matches_played'] > 0 else 0
                scoreStr = f"**Wins 》 **{lb[self.numbre]['wins']}\n**Winrate 》 **{winrate}%"
                lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1      

            self.change = 'no'         

        elif self.sort_option == 'streak':      
            lb = await stat.db.fetch('SELECT * FROM rank_system WHERE matches_played >= 0 ORDER BY streak DESC')
            for i in data:
                scoreStr = f"**Streak 》 **{lb[self.numbre]['streak']}\n**Matches 》 **{lb[self.numbre]['matches_played']}"
                lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1 

            self.change = 'no'              

        elif self.sort_option == 'matches':      
            lb = await stat.db.fetch('SELECT * FROM rank_system WHERE matches_played >= 0 ORDER BY matches_played DESC')
            for i in data:
                scoreStr = f"**Matches 》 **{lb[self.numbre]['matches_played']}\n**Wins 》 **{lb[self.numbre]['wins']}"
                lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1  

            self.change = 'no'

        elif self.sort_option == 'rank':      
            lb = await stat.db.fetch(f'SELECT * FROM rank_system WHERE matches_played >= 0 AND rank_value = $1 ORDER BY points DESC', stats)
            data = data[:len(lb)]
            for i in data:
                scoreStr = f"**Rank 》 **{lb[self.numbre]['player_rank']}\n**Points 》 **{lb[self.numbre]['points']}"
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
                           discord.SelectOption(label="Global Rank", value="global"),
                           discord.SelectOption(label="Global Wins", value="wins"),
                           discord.SelectOption(label="Global Matches", value="matches"),
                           discord.SelectOption(label="Global Streaks", value="streak"),
                           discord.SelectOption(label="Local Rank", value="rank"),

                       ])

    async def sort_dropdown(self, select: discord.ui.Select, interaction: discord.Interaction):
        await interaction.response.defer()
        self.sort_option = select.values[0]
        self.change = 'yes'
        self.current_page = 1
        await self.update_message(self.get_current_page_data(), self.lb, self.stat,self.stats)

class CAPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 8
    numbre : int = 0
    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep], self.lb, self.stat)

    async def create_embed(self, data,lb,stat ):
        lb = self.lb
        stat = self.stat
        if stat is None:
            desc = 'Points'
        elif stat.lower() == 'matches':
            desc = 'Matches'
        else:
            desc = f'{stat.title()}'
        scoreStr = ''        
        lb_embed = discord.Embed(
            title = 'Casual Leaderboard',
            description = f'Order by \n`d!calb [wins,matches,points,streaks]`',
            colour = color
        )
        for i in data:
            
            if stat is None:
                crudescore3 = lb[self.numbre]['points']
            elif stat.lower() == 'matches':
                crudescore3 = lb[self.numbre]['matches_played']
            else:
                crudescore3 = lb[self.numbre][f'{stat.lower()}']   

            scoreStr = f"**{desc} 》 **{crudescore3}"
            
            lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
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

class CPaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 8
    numbre : int = 0
    sort_option = "global"
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
            title = 'Common Ranked Leaderboard',
            description = f'Click the buttons to change pages.',
            colour = color
        )
        if self.change == 'no':
            pass
        else:
            self.numbre = 0

        if self.sort_option == 'global':      
            lb = await stat.db.fetch('SELECT * FROM common_system WHERE matches_played >= 0 ORDER BY points DESC')
            for i in data:
                scoreStr = f"**Rank 》 **{lb[self.numbre]['player_rank']}\n**Points 》 **{lb[self.numbre]['points']}"
                lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1
        elif self.sort_option == 'wins':      
            lb = await stat.db.fetch('SELECT * FROM common_system WHERE matches_played >= 0 ORDER BY wins DESC')
            
            for i in data:
                winrate = round(lb[self.numbre]['wins'] / lb[self.numbre]['matches_played'] * 100, 2) if lb[self.numbre]['matches_played'] > 0 else 0
                scoreStr = f"**Wins 》 **{lb[self.numbre]['wins']}\n**Winrate 》 **{winrate}%"
                lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1               

        elif self.sort_option == 'streak':      
            lb = await stat.db.fetch('SELECT * FROM common_system WHERE matches_played >= 0 ORDER BY streak DESC')
            for i in data:
                scoreStr = f"**Streak 》 **{lb[self.numbre]['streak']}\n**Matches 》 **{lb[self.numbre]['matches_played']}"
                lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1               

        elif self.sort_option == 'matches':      
            lb = await stat.db.fetch('SELECT * FROM common_system WHERE matches_played >= 0 ORDER BY matches_played DESC')
            for i in data:
                scoreStr = f"**Matches 》 **{lb[self.numbre]['matches_played']}\n**Wins 》 **{lb[self.numbre]['wins']}"
                lb_embed.add_field(name = f"{self.numbre+1}# {lb[self.numbre]['player_name']} ", value = f'{scoreStr}', inline=False)
                self.numbre = self.numbre + 1               
        elif self.sort_option == 'rank':      
            lb = await stat.db.fetch(f'SELECT * FROM common_system WHERE matches_played >= 0 AND rank_value = $1 ORDER BY points DESC', stats)
            for i in data:
                scoreStr = f"**Rank 》 **{lb[self.numbre]['player_rank']}\n**Points 》 **{lb[self.numbre]['points']}"
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
                           discord.SelectOption(label="Global Rank", value="global"),
                           discord.SelectOption(label="Global Wins", value="wins"),
                           discord.SelectOption(label="Global Matches", value="matches"),
                           discord.SelectOption(label="Global Streaks", value="streak"),
                           discord.SelectOption(label="Local Rank", value="rank"),

                       ])

    async def sort_dropdown(self, select: discord.ui.Select, interaction: discord.Interaction):
        await interaction.response.defer()
        self.sort_option = select.values[0]
        self.change = 'yes'
        self.current_page = 1
        await self.update_message(self.get_current_page_data(), self.lb, self.stat,self.stats)

    
class RankCommands(commands.Cog):
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

    bronze1_value = 1
    bronze2_value = 1
    bronze3_value = 1

    silver1_value = 2
    silver2_value = 2
    silver3_value = 2

    gold1_value = 3
    gold2_value = 3
    gold3_value = 3
    
    platinum1_value = 4
    platinum2_value = 4
    platinum3_value = 4

    dominant_value = 5

    @commands.group(name = 'ranked', aliases = ['rank', 'r'], invoke_without_command = True)
    async def ranked_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            em1 = discord.Embed(
                title = 'Ranked',
                description = 'Commands related to ranked battles: *(Page 1/2)*',
                colour = color
            )


            em1.add_field(name = 'd!rareleaderboard/rlb [order by (optional)]', value = 'View the top players in ranked battles. \n[Order by] wins,matches,points,streaks',inline=False)

            em1.add_field(name = 'd!comleaderboard/clb [order by (optional)]', value = 'View the top players in ranked battles. \n[Order by] wins,matches,points,streaks',inline=False)

            em1.add_field(name = 'd!ranked info/i', value = 'Learn about rank battles.',inline=False)

            em1.add_field(name = 'd!ranked rules/rule', value = 'View rules for ranked.',inline=False)



            em2 = discord.Embed(
                title = 'Ranked [Aliases: rank, r]',
                description = 'Commands related to ranked battles: *(Page 2/2)*',
                colour = color
            )
            em2.add_field(name = 'd!ranked enable/en [channel]', value = 'Enable ranked battles.*(Admin exclusive)*',inline=False)

            em2.add_field(name = 'd!ranked disable/dis', value = 'Disable ranked battles.*(Admin exclusive)*',inline=False)

            em2.add_field(name = 'd!ranked ban [mention]', value = 'Ban a player from ranked battles.*(Admin exclusive)*',inline=False)

            em2.add_field(name = 'd!ranked unban [mention]', value = 'Unban a player from ranked battles.*(Admin exclusive)*',inline=False)

            em2.add_field(name = 'd!ranked givep/givepoints|gp [points][mention]', value = 'Give a certain amount of points to a player. *(Owner exclusive)*',inline=False)

            em2.add_field(name = 'd!ranked takep/takepoints|tp [points][mention]', value = 'Take a certain amount of points from a player. *(Owner exclusive)*',inline=False)

            
            embeds = [em1, em2]

            current_page = 0

            ranked_msg = await ctx.send(embed = em1)

            await ranked_msg.add_reaction('\U000025C0')
            await ranked_msg.add_reaction('\U000025B6')

            def check(reaction : discord.Reaction, user : discord.User):
                return user.id == ctx.author.id and reaction.message.channel.id == ctx.channel.id and str(reaction.emoji) in ['\U000025C0', '\U000025B6']

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
                    if str(reaction_add) in ['\U000025C0', '\U000025B6']:
                        if current_page == 0:
                            current_page = 1

                            await ranked_msg.edit(embed = embeds[current_page])

                        elif current_page == 1:
                            current_page = 0

                            await ranked_msg.edit(embed = embeds[current_page])
        
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @ranked_command.command(name = 'enable', aliases = ['en'])
    async def ranked_enable_command(self, ctx, channel : discord.TextChannel = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)
            admins = server[0]['admins']
            admins_list = self.listing(admins)
            if str(ctx.author.id) in admins_list:
                if channel is None:
                    em = discord.Embed(
                        title = 'Ranked',
                        description = '**Enable ranked battles.**\n\nd!ranked enable [channel]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    await self.bot.db.execute('UPDATE server_constants SET ranked_enable = $1, ranked_channel = $2 WHERE guild_id = $3', 1, channel.id, guild_id)

                    await ctx.send(f'Ranked battles are now enabled and matches will be logged in {channel.mention}.')

            else:
                await ctx.send('You do not have permission to use that command.')

        else:
            await ctx.send('You do have not registered yet! Use `d!start` to register.')

    @ranked_command.command(name = 'disable', aliases = ['dis'])
    async def ranked_disable_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            (server[0]['admins'])

            admins = server[0]['admins']

            admins_list = self.listing(admins)
            
            (admins_list)

            if str(ctx.author.id) in admins_list:
                await self.bot.db.execute('UPDATE server_constants SET ranked_enable = 0, ranked_channel = NULL WHERE guild_id = $1', guild_id)

                await ctx.send('Ranked battles have now been disabled.')

            else:
                await ctx.send('You do not have permission to use that command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @ranked_command.command(name = 'ban')
    async def ranked_ban_command(self, ctx, member : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        
        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if str(ctx.author.id) in admins_list:
                if member is None:
                    em = discord.Embed(
                        title = 'Ranked',
                        description = '**Ban a player from ranked battles.**\n\nd!ranked ban [mention]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                    if member_registered:
                        member_id = member.id

                        ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', member_id)

                        if ban_list:
                            await ctx.send('That person is already banned from ranked battles.')

                        else:
                            await self.bot.db.execute('INSERT INTO bans (rank_bans) VALUES ($1)',member_id)

                            await ctx.send(f'**{member.name}** has been banned from ranked battles.')

                    else:
                        await ctx.send('That person has not registered yet! Use `d!start` to register.')

            else:
                await ctx.send('You do not have permission to use that command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @ranked_command.command(name = 'unban')
    async def ranked_unban_command(self, ctx, member : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        
        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if str(ctx.author.id) in admins_list:
                if member is None:
                    em = discord.Embed(
                        title = 'Ranked',
                        description = '**Unban a player from ranked battles.**\n\nd!ranked unban [mention]',
                        colour = color
                    )

                    await ctx.send(embed = em)

                else:
                    member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                    if member_registered:
                        member_id = member.id

                        ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', member_id)

                        if not ban_list:
                            await ctx.send('That person is not banned from ranked battles!')

                        else:
                            await self.bot.db.execute('DELETE FROM bans WHERE rank_bans = $1', member_id)

                            await ctx.send(f'**{member.name}** has been unbanned from ranked battles.')

                    else:
                        await ctx.send('That person has not registered yet! Use `d!start` to register.')

            else:
                await ctx.send('You do not have permission to use that command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')


    @commands.command(name = 'ccccccimage', aliases = ['img'])
    async def paginate(self, ctx):
        data = [1,2,3,4,5,6,7]
        felix = [0,9,6]
        pagination_view = RPaginationView()
        pagination_view.data = data, felix
        await pagination_view.send(ctx)

    @commands.command(name = 'rareleaderboard', aliases = ['rlb'])
    async def rleaderboard_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
   
        if registered_check:
            rank = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', ctx.author.id)
            playerrank = rank[0]['rank_value']
            lb = await self.bot.db.fetch(f'SELECT * FROM rank_system WHERE matches_played >= 0 ORDER BY points DESC')
            data = []
            for faction in lb:
                data.append(faction['player_name'])
            stat = self.bot
            stats = playerrank
            pagination_view = RPaginationView()
            pagination_view.data = data
            pagination_view.lb = lb
            pagination_view.stat = stat
            pagination_view.stats = stats
            await pagination_view.send(ctx)

                

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'comleaderboard', aliases = ['clb'])
    async def cleaderboard_command(self, ctx, stat = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
       
        if registered_check:

            rank = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', ctx.author.id)
            playerrank = rank[0]['rank_value']
 
            lb = await self.bot.db.fetch(f'SELECT * FROM common_system WHERE matches_played >= 0 ORDER BY points DESC')

            data = []
            for faction in lb:
                data.append(faction['player_name'])

            stat = self.bot
            stats = playerrank
    
            pagination_view = CPaginationView()
            pagination_view.data = data
            pagination_view.lb = lb
            pagination_view.stat = stat
            pagination_view.stats = stats
            await pagination_view.send(ctx)

                

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @ranked_command.command(name = 'info', aliases = ['i'])
    async def ranked_info_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            ranked_info_embed = discord.Embed(
                title = 'Ranked',
                description = "Welcome to Ranked Battles!\nRanked battles are a new way to battle in Poketwo with players at your level. There are 5 ranks: Bronze, Silver, Gold, Platinum, Dominant. Each of the first 4 ranks have 3 subranks labelled Bronze I, Bronze Il and so on. \nYou lose the same amount of points your opponent gains and you cannot go below O points.\nUse d!log rare or d!log com to log your battles for a rare or common duel respectively and d!r1b or d!clb to view the top players.\nPlayers will recieve awards for particular achievements such as #1 on the leaderboard.\nGiven below is the points distribution for the ranks:",
                colour = color
            )

            ranked_info_embed.add_field(name = 'Bronze I', value = '0 - 83 points')
            ranked_info_embed.add_field(name = 'Bronze II', value = '83 - 167 points')
            ranked_info_embed.add_field(name = 'Bronze III', value = '167 - 250 points')
            ranked_info_embed.add_field(name = 'Silver I', value = '250 - 333 points')
            ranked_info_embed.add_field(name = 'Silver II', value = '333 - 416 points')
            ranked_info_embed.add_field(name = 'Silver III', value = '416 - 500 points')
            ranked_info_embed.add_field(name = 'Gold I', value = '500 - 583 points')
            ranked_info_embed.add_field(name = 'Gold II', value = '583 - 667 points')
            ranked_info_embed.add_field(name = 'Gold III', value = '667 - 750 points')
            ranked_info_embed.add_field(name = 'Platinum I', value = '750 - 833 points')
            ranked_info_embed.add_field(name = 'Platinum II', value = '833 - 916 points')
            ranked_info_embed.add_field(name = 'Platinum III', value = '916 - 1250 points')
            ranked_info_embed.add_field(name = 'Dominant', value = '1250+ points')

            await ctx.send(embed = ranked_info_embed)

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @commands.command(name = 'rules', aliases = ['rule'])
    async def ranked_rule_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:

            data = ['t','ourare', 'uurare', 'oucommon', 'uucommon', 'mixnmega', 'mega', 'cmr']

            
            stat = None
            lb = None
            stats = None

            pagination_view = Rules()
            pagination_view.data = data
            pagination_view.lb = lb
            pagination_view.stat = stat
            pagination_view.stats = stats
            await pagination_view.send(ctx)

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @ranked_command.command(name = 'givecp', aliases = ['givecpoints', 'gcp'])
    async def ranked_give_cpoints_command(self, ctx, points : int = None, member : discord.Member = None):
        guild_id = ctx.guild.id

        server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

        admins = server[0]['admins']

        admins_list = self.listing(admins)
        if str(ctx.author.id) in admins_list:
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

            if (points is None) or (member is None):
                em = discord.Embed(
                    title = 'Givepoints',
                    description = '**Give points to a player without altering their matches played and wins.**\n\nd!ranked givep [points] [mention]',
                    colour = color
                ) 

                await ctx.send(embed = em)

            else:
                member_id = int(member.id)

                player = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', member_id)

                if not player:
                    await ctx.send('That person is not registered in the database!')

                else:
                    player_previous_points = player[0]['points']
                    
                    if int(points) <= 0:
                        await ctx.send('Invalid number.')

                    else:
                        await self.bot.db.execute('UPDATE common_system SET points = $1 WHERE player_id = $2', int(player_previous_points) + int(points), member_id)

                        player_updated = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', member_id)

                        player_points = player_updated[0]['points']

                        if (int(player_points) >= 0) and (int(player_points) <= 83):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze1, bronze_value, member_id)

                        elif (int(player_points) >= 84) and (int(player_points) <= 167):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze2, bronze_value, member_id)

                        elif (int(player_points) >= 168) and (int(player_points) <= 250):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze3, bronze_value, member_id)

                        elif (int(player_points) >= 251) and (int(player_points) <= 333):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver1, silver_value, member_id)

                        elif (int(player_points) >= 334) and (int(player_points) <= 416):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver2, silver_value, member_id)

                        elif (int(player_points) >= 417) and (int(player_points) <= 500):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver3, silver_value, member_id)

                        elif (int(player_points) >= 501) and (int(player_points) <= 583):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold1, gold_value, member_id)

                        elif (int(player_points) >= 584) and (int(player_points) <= 667):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold2, gold_value, member_id)

                        elif (int(player_points) >= 668) and (int(player_points) <= 750):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold3, gold_value, member_id)

                        elif (int(player_points) >= 751) and (int(player_points) <= 833):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum1, platinum_value, member_id)

                        elif (int(player_points) >= 834) and (int(player_points) <= 916):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum2, platinum_value, member_id)

                        elif (int(player_points) >= 917) and (int(player_points) <= 1249):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum3, platinum_value, member_id)

                        elif int(player_points) >= 1250:
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', dominant, dominant_value, member_id)

                        await ctx.send(f'Gave {points} points to {member.name}.')

        else:
            await ctx.send('You do not have permission to use that command.')

    @ranked_command.command(name = 'takecp', aliases = ['takecpoints', 'tcp'])
    async def ranked_take_cpoints_command(self, ctx, points : int = None, member : discord.Member = None):
        guild_id = ctx.guild.id

        server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

        admins = server[0]['admins']

        admins_list = self.listing(admins)
        if str(ctx.author.id) in admins_list:
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

            if (points is None) or (member is None):
                em = discord.Embed(
                    title = 'Takepoints',
                    description = '**Take points from a player without altering their matches played.**\n\nd!ranked takecp [points] [mention]',
                    colour = color
                )

                await ctx.send(embed = em)

            else:
                member_id = int(member.id)

                player = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', member_id)

                if not player:
                    await ctx.send('That person is not registered in the database!')

                else:
                    player_previous_points = player[0]['points']

                    if (player_previous_points < points) or (points <= 0):
                        await ctx.send('Invalid number.')

                    else: 
                        await self.bot.db.execute('UPDATE common_system SET points = $1 WHERE player_id = $2', int(player_previous_points) - int(points), member_id)

                        player_updated = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', member_id)

                        player_points = player_updated[0]['points']

                        if (int(player_points) >= 0) and (int(player_points) <= 83):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze1, bronze_value, member_id)

                        elif (int(player_points) >= 84) and (int(player_points) <= 167):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze2, bronze_value, member_id)

                        elif (int(player_points) >= 168) and (int(player_points) <= 250):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze3, bronze_value, member_id)

                        elif (int(player_points) >= 251) and (int(player_points) <= 333):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver1, silver_value, member_id)

                        elif (int(player_points) >= 334) and (int(player_points) <= 416):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver2, silver_value, member_id)

                        elif (int(player_points) >= 417) and (int(player_points) <= 500):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver3, silver_value, member_id)

                        elif (int(player_points) >= 501) and (int(player_points) <= 583):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold1, gold_value, member_id)

                        elif (int(player_points) >= 584) and (int(player_points) <= 667):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold2, gold_value, member_id)

                        elif (int(player_points) >= 668) and (int(player_points) <= 750):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold3, gold_value, member_id)

                        elif (int(player_points) >= 751) and (int(player_points) <= 833):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum1, platinum_value, member_id)

                        elif (int(player_points) >= 834) and (int(player_points) <= 916):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum2, platinum_value, member_id)

                        elif (int(player_points) >= 917) and (int(player_points) <= 1249):
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum3, platinum_value, member_id)

                        elif int(player_points) >= 1250:
                            await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', dominant, dominant_value, member_id)

                        await ctx.send(f'Took {points} points from {member.name}.')
        
        else:
            await ctx.send('You do not have permission to use that command.')
    @ranked_command.command(name = 'givep', aliases = ['givepoints', 'gp'])
    async def ranked_give_points_command(self, ctx, points : int = None, member : discord.Member = None):
        guild_id = ctx.guild.id

        server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

        admins = server[0]['admins']

        admins_list = self.listing(admins)
        if str(ctx.author.id) in admins_list:
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

            if (points is None) or (member is None):
                em = discord.Embed(
                    title = 'Givepoints',
                    description = '**Give points to a player without altering their matches played and wins.**\n\nd!ranked givep [points] [mention]',
                    colour = color
                ) 

                await ctx.send(embed = em)

            else:
                member_id = int(member.id)

                player = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', member_id)

                if not player:
                    await ctx.send('That person is not registered in the database!')

                else:
                    player_previous_points = player[0]['points']
                    
                    if int(points) <= 0:
                        await ctx.send('Invalid number.')

                    else:
                        await self.bot.db.execute('UPDATE rank_system SET points = $1 WHERE player_id = $2', int(player_previous_points) + int(points), member_id)

                        player_updated = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', member_id)

                        player_points = player_updated[0]['points']

                        if (int(player_points) >= 0) and (int(player_points) <= 83):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze1, bronze_value, member_id)

                        elif (int(player_points) >= 84) and (int(player_points) <= 167):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze2, bronze_value, member_id)

                        elif (int(player_points) >= 168) and (int(player_points) <= 250):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze3, bronze_value, member_id)

                        elif (int(player_points) >= 251) and (int(player_points) <= 333):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver1, silver_value, member_id)

                        elif (int(player_points) >= 334) and (int(player_points) <= 416):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver2, silver_value, member_id)

                        elif (int(player_points) >= 417) and (int(player_points) <= 500):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver3, silver_value, member_id)

                        elif (int(player_points) >= 501) and (int(player_points) <= 583):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold1, gold_value, member_id)

                        elif (int(player_points) >= 584) and (int(player_points) <= 667):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold2, gold_value, member_id)

                        elif (int(player_points) >= 668) and (int(player_points) <= 750):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold3, gold_value, member_id)

                        elif (int(player_points) >= 751) and (int(player_points) <= 833):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum1, platinum_value, member_id)

                        elif (int(player_points) >= 834) and (int(player_points) <= 916):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum2, platinum_value, member_id)

                        elif (int(player_points) >= 917) and (int(player_points) <= 1249):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum3, platinum_value, member_id)

                        elif int(player_points) >= 1250:
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', dominant, dominant_value, member_id)

                        await ctx.send(f'Gave {points} points to {member.name}.')

        else:
            await ctx.send('You do not have permission to use that command.')

    @ranked_command.command(name = 'takep', aliases = ['takepoints', 'tp'])
    async def ranked_take_points_command(self, ctx, points : int = None, member : discord.Member = None):
        guild_id = ctx.guild.id

        server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

        admins = server[0]['admins']

        admins_list = self.listing(admins)
        if str(ctx.author.id) in admins_list:
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

            if (points is None) or (member is None):
                em = discord.Embed(
                    title = 'Takepoints',
                    description = '**Take points from a player without altering their matches played.**\n\nd!ranked takep [points] [mention]',
                    colour = color
                )

                await ctx.send(embed = em)

            else:
                member_id = int(member.id)

                player = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', member_id)

                if not player:
                    await ctx.send('That person is not registered in the database!')

                else:
                    player_previous_points = player[0]['points']

                    if (player_previous_points < points) or (points <= 0):
                        await ctx.send('Invalid number.')

                    else: 
                        await self.bot.db.execute('UPDATE rank_system SET points = $1 WHERE player_id = $2', int(player_previous_points) - int(points), member_id)

                        player_updated = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', member_id)

                        player_points = player_updated[0]['points']

                        if (int(player_points) >= 0) and (int(player_points) <= 83):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze1, bronze_value, member_id)

                        elif (int(player_points) >= 84) and (int(player_points) <= 167):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze2, bronze_value, member_id)

                        elif (int(player_points) >= 168) and (int(player_points) <= 250):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze3, bronze_value, member_id)

                        elif (int(player_points) >= 251) and (int(player_points) <= 333):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver1, silver_value, member_id)

                        elif (int(player_points) >= 334) and (int(player_points) <= 416):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver2, silver_value, member_id)

                        elif (int(player_points) >= 417) and (int(player_points) <= 500):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver3, silver_value, member_id)

                        elif (int(player_points) >= 501) and (int(player_points) <= 583):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold1, gold_value, member_id)

                        elif (int(player_points) >= 584) and (int(player_points) <= 667):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold2, gold_value, member_id)

                        elif (int(player_points) >= 668) and (int(player_points) <= 750):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold3, gold_value, member_id)

                        elif (int(player_points) >= 751) and (int(player_points) <= 833):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum1, platinum_value, member_id)

                        elif (int(player_points) >= 834) and (int(player_points) <= 916):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum2, platinum_value, member_id)

                        elif (int(player_points) >= 917) and (int(player_points) <= 1249):
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum3, platinum_value, member_id)

                        elif int(player_points) >= 1250:
                            await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', dominant, dominant_value, member_id)

                        await ctx.send(f'Took {points} points from {member.name}.')
        
        else:
            await ctx.send('You do not have permission to use that command.')

    @ranked_command.command(name = 'rdafcadeset')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ranked_reset_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            if ctx.author.id in [0]:
                confirm_msg = await ctx.send('Are you sure you want to reset the season?\n\n**This action will revert all ranked data and is not reversible!**')

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
                        positions = await self.bot.db.fetch('SELECT player_id FROM rank_system WHERE matches_played > 9 ORDER BY points DESC')

                        emoji = '<:leaderboard:930362131013070879>'

                        for i in range(8):
                            player_badges = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', positions[i]['player_id'])

                            if player_badges[0]['badges'] is None:
                                await self.bot.db.execute('UPDATE registered SET badges = $1 WHERE player_id = $2', emoji, positions[i]['player_id'])

                            else:
                                new_badges = player_badges[0]['badges'] + f' {emoji}'

                                await self.bot.db.execute('UPDATE registered SET badges = $1 WHERE player_id = $2', new_badges, positions[i]['player_id'])
                        
                        bronze1 = 'Bronze II'

                        await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = 1, points = 150, wins = 0, matches_played = 0', bronze1)

                        await ctx.send('The season has been reset and Leaderboard badges have been given!')

                    elif str(reaction_add) == '❌':
                        await ctx.send('Cancelled.')

            else:
                await ctx.send('You do not have permission to use this command.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')



    @commands.command(name = 'weekly', aliases = ['w'])
    async def weedskly_command(self, ctx, stat = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if (stat == "r") or (stat == "rares"):
            stat = 'rare'  
        elif (stat == "c") or (stat == "commons"):
            stat = 'common'    
        if registered_check:
            stats = {
                'rare' : 'SELECT * FROM rank_system WHERE matches_played >= 0 AND weekly <> 0 ORDER BY weekly DESC',
                'common' : 'SELECT * FROM common_system WHERE matches_played >= 0 AND weekly <> 0 ORDER BY weekly DESC',
                'gamble' : 'SELECT * FROM gamble WHERE player_name IS NOT NULL AND played >= 0 ORDER BY weekly DESC',
            }
            if stat is None:
                
                em = discord.Embed(
                    title = 'Weekly Leaderboard',
                    description = '**d!weekly [leaderboard]**\n\nSee the weekly leaderboard for Common/Rare/Gamble.',
                    colour = color
                )

                await ctx.send(embed = em)

            elif stat.lower() not in stats:
                em = discord.Embed(
                    title = 'Weekly Leaderboard',
                    description = '**d!weekly [leaderboard]**\n\nSee the weekly leaderboard for Common/Rare/Gamble.',
                    colour = color
                )

                await ctx.send(embed = em)

            elif (stat.lower() in stats):
                lb = await self.bot.db.fetch(stats[stat.lower()])

                data = []
                for faction in lb:
                    data.append(faction['player_name'])
      
                pagination_view = WPaginationView()
                pagination_view.data = data
                pagination_view.lb = lb
                pagination_view.stat = stat
                pagination_view.stats = stats
                await pagination_view.send(ctx)
                

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')


    @commands.command(name = 'daily', aliases = ['d'])
    async def weedafkly_command(self, ctx, stat = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if (stat == "r") or (stat == "rares"):
            stat = 'rare'  
        elif (stat == "c") or (stat == "commons"):
            stat = 'common'   
   
        if registered_check:
            stats = {
                'rare' : 'SELECT * FROM rank_system WHERE matches_played >= 0 AND daily <> 0 ORDER BY daily DESC',
                'common' : 'SELECT * FROM common_system WHERE matches_played >= 0 AND daily <> 0 ORDER BY daily DESC',
                'gamble' : 'SELECT * FROM gamble WHERE player_name IS NOT NULL AND played >= 0 ORDER BY daily DESC',
            }
            if stat is None:
                
                em = discord.Embed(
                    title = 'Daily Leaderboard',
                    description = '**d!daily [leaderboard]**\n\nSee the daily leaderboard for Common/Rare.',
                    colour = color
                )

                await ctx.send(embed = em)

            elif stat.lower() not in stats:
                em = discord.Embed(
                    title = 'Daily Leaderboard',
                    description = '**d!daily [leaderboard]**\n\nSee the daily leaderboard for Common/Rare.',
                    colour = color
                )

                await ctx.send(embed = em)

            elif (stat.lower() in stats):
                lb = await self.bot.db.fetch(stats[stat.lower()])

                data = []
                for faction in lb:
                    data.append(faction['player_name'])
      
                pagination_view = DPaginationView()
                pagination_view.data = data
                pagination_view.lb = lb
                pagination_view.stat = stat
                pagination_view.stats = stats
                await pagination_view.send(ctx)
                

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')





def setup(bot):
    bot.add_cog(RankCommands(bot))
