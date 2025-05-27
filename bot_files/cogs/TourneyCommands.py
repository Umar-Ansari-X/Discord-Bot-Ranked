import asyncio
import discord
import random
from discord.ext import commands
from datetime import timedelta, timezone
import datetime
import time
from pymongo import MongoClient
import asyncio
import string
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import math

color = 0x32006e

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

class pingbutton(discord.ui.View):
    def __init__(self, member : discord.Member,status : str, bot):
        super().__init__(timeout = 15)

        self.value = None
        self.member = member
        self.bot = bot
        self.status = status
        
        if status == 'yes':
            self.children[1].label = 'Turn Off Pings'
            self.children[1].emoji = '🔇'
            self.children[1].style = discord.ButtonStyle.red
        else:
            self.children[1].label = 'Turn On Pings'
            self.children[1].emoji = '🔉'
            self.children[1].style = discord.ButtonStyle.green


    @discord.ui.button(label = "Ping Opponents", style = discord.ButtonStyle.blurple, emoji = "🔔" )
    async def confirm_button(self, button: discord.Button, interaction : discord.Interaction):
        self.value = True
        self.stop()
                
        for i in self.children:
            i.disabled = True

        await interaction.response.edit_message(view = self)

    @discord.ui.button(label = "Pings", style = discord.ButtonStyle.green, emoji = "🔔" )
    async def disab_button(self, button: discord.Button, interaction : discord.Interaction):
        if self.status == 'yes':

            pingy = 'no'
            await self.bot.db.execute(f'UPDATE registered SET ping = $1 WHERE player_id = $2',pingy, self.member.id)
            text = 'Turned OFF Pings for Wars 🔇'
        else:
            pingy = 'yes'
            await self.bot.db.execute(f'UPDATE registered SET ping = $1 WHERE player_id = $2',pingy, self.member.id)
            text = 'Turned ON Pings for Wars 🔉'
        

        self.value = False
        self.stop()
                
        for i in self.children:
            i.disabled = True
        
        await interaction.response.edit_message(view=self)   

        await interaction.followup.send(content=text, ephemeral=True)
            

    async def interaction_check(self, interaction : discord.Interaction):
        return interaction.user == self.member
                                        
    async def on_timeout(self):
        self.value = None

        for i in self.children:
            i.disabled = True

class Wars(discord.ui.View):
    def __init__(self, member : discord.Member, choices : str):
        super().__init__(timeout = 15)

        self.value = None
        self.member = member
        self.choices = choices

        new_options = []
        for i in choices:
            new_options.append(discord.SelectOption(label=i[1].title(), value=i[0].lower()))
            self.children[0].options = new_options         

    @discord.ui.select(placeholder="Pick a War", min_values=1, max_values=1,options=[discord.SelectOption(label="None", value="None")])
    async def sort_dropdown(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.value = select.values[0]

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

class Career(discord.ui.View):
    current_page : int = 1
    sep : int = 3
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
        
        em = discord.Embed(
        title = f"Powerups",
        description = f"Click the buttons to change pages.",
        colour = color
        )

        for i in data:
            if i == 'bridger':
                em.add_field(name='Bridger ⛩️', value="**• Uses:** 9\n**• Cooldown:** 1 match\n**• Description:** Bridger becomes available when your clan is trailing by 10 points or more. When activated, if your clan loses a match, the enemy clan gains the usual 1 point. However, if your clan wins the match, you earn 3 points, allowing you to make a comeback and close the gap with the leading clan. OFFENSIVE",inline=False)

            elif i == 'jeopardy':
                em.add_field(name='Jeopardy ⚔️', value="**• Uses:** 7\n**• Cooldown:** 1 match\n**• Description:** Jeopardy when activated, you have the option to either gain 2 points or remove 2 points from your clan's score. If your clan wins, you gain 2 points, but if you lose, you lose 2 points. OFFENSIVE",inline=False)
            elif i == 'battle':
                em.add_field(name='Battle cry 🗣️', value="**• Uses:** 5\n**• Cooldown:** 1 match\n**• Description:** If your clan lost the most recent match, you can buy this powerup.. your next match if you win will gain 2 points for the clan. OFFENSIVE",inline=False)

            elif i == 'immunity':
                em.add_field(name='Immunity 🛡️', value="**• Uses:** 5\n**• Cooldown:** 3 matches\n**• Description:** Immunity is a strategic powerup that provides your clan with a shield. When activated, if your clan loses the match, it reduces the amount of points gained by the enemy clan by 3. DEFENSIVE",inline=False)

            elif i == 'breakthrough':
                em.add_field(name='Breakthrough ⚡', value="**• Uses:** 1\n**• Cooldown:** 3 matches\n**• Description:** When activated, Breakthrough allows your clan to retaliate when your opponent uses a powerup. If your clan wins and if the opponent clan used a defensive powerup, you get 4 points. If you lose, then you can't use powerups such as Immunity and Reflection shield. Can only be used when the leading clan is less than halfway to the goal. OFFENSIVE",inline=False)

            elif i == 'counterstrike':
                em.add_field(name='Counterstrike 🛩️', value="**• Uses:** 1\n**• Cooldown:** 3 matches\n**• Description:** When activated, Counterstrike allows your clan to retaliate when your opponent uses a powerup. If your clan loses and if the opponent clan used an offensive powerup, you get 4 points. If the opponent used a defensive powerup, you can't use powerups such as Jeopardy and Battle cry. Can only be used when the leading clan is less than halfway to the goal. DEFENSIVE",inline=False)

            elif i == 'strategic':
                em.add_field(name='Strategic Retreat :flag_white:', value="**• Uses:** 3\n**• Cooldown:** 5 matches\n**• Description:** When activated, forfeit the match and lose 1 point, but now you have destroyed any powerup activated in the next match. DEFENSIVE",inline=False)

            elif i == 'reflection':
                em.add_field(name='Reflection Shield 🌟', value="**• Uses:** 2\n**• Cooldown:** 4 matches\n**• Description:** When activated, reflect any powerup used by the opponent back onto them. If the opponent uses a powerup, you steal the opponent's powerup.. this could mean negative effects as well. DEFENSIVE",inline=False)

            elif i == 'mimicry':
                em.add_field(name='Mimicry 👥', value="**• Uses:** 2\n**• Cooldown:** 7 matches\n**• Description:** When activated, copy the powerup activated by the opponent in the match. This powerup can copy ANY powerup, meaning if you're on cooldown for a powerup, this will overwrite that cooldown and activate it for you. DEFENSIVE",inline=False)

            elif i == 'sacrifice':
                em.add_field(name='Sacrifice 🕊️', value="**• Uses:** 1\n**• Cooldown:** 10 matches\n**• Description:** When activated, Sacrifice allows you to intentionally lose the battle, and you won't lose a point. But if you lose more than 1 point because of the opponent, it enables Retribution for the next match. DEFENSIVE",inline=False)

            elif i == 'retribution':
                em.add_field(name='Retribution <:abyss:1096728826702213231>', value="**• Cooldown:** Activates after Sacrifice\n**• Description:** Allows your clan to win 5 points if the clan wins the match. OFFENSIVE",inline=False)


        em.set_footer(text=f'Note: All powerups still take one match to activate. ')
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

        delete = 6
        if int(len(self.data)) < self.sep * self.current_page:
            new = int(len(self.data)) - self.sep * (self.current_page -1)
            delete = new + 3
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
            strs = [ 'Complete 5 casual duel', 'Win 3 casual duel','Complete 5 ranked duels', 'Win 3 ranked duel','Complete 5 ranked with commons' , 'Complete 5 ranked with rares','Trade 3 times with another user in Dom Bot']
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
            strs = [ 'Complete 5 casual duel', 'Win 3 casual duel','Complete 5 ranked duel', 'Win 3 ranked duel','Complete 5 ranked with commons' , 'complete 5 ranked with rares','Trade 3 times with another user in Dom Bot']

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
    
def date_diff_in_seconds(dt2, dt1):
  timedelta = dt1 - dt2
  return timedelta.days * 24 * 3600 + timedelta.seconds

def dhms_from_seconds(seconds):
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	return (days, hours, minutes, seconds)

async def warwin(self,ctx, warid):
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
        "enemymembers": 1,
        "enemyplayerscore": 1,
        'wartype': 1,
        'allyplayerscored': 1,
        'enemyplayerscored' : 1,
        'powerups' : 1
    })
    enemyscored = war_data['enemyplayerscored']
    allyscored = war_data['allyplayerscored']
    faction_name = war_data['teamone']
    efaction_name = war_data['teamtwo']
    winscore = war_data['winscore']
    allyffscore = war_data['allyscore']
    enemyffscore = war_data['enemyscore']
    allymembers = war_data['allymembers']
    allyscore = war_data['allyplayerscore']
    enemymembers = war_data['enemymembers']
    enemyscore = war_data['enemyplayerscore']
    formats = war_data['wartype']
    powerups = war_data['powerups']
    if self.faction.count_documents({"_id": warid, "wartype": 'br' }, limit = 1):
        allycheck = list(self.faction.find( {"_id": warid}, {"_id": 0, "teamone": 1}))
        faction_name = allycheck[0]['teamone']
        enemycheck = list(self.faction.find( {"_id": warid}, {"_id": 0, "teamtwo": 1}))
        efaction_name = enemycheck[0]['teamtwo']
        allyfscore = list(self.faction.find( {"_id": warid}, {"_id": 0, "allyscore": 1}))
        enemyfscore = list(self.faction.find( {"_id": warid}, {"_id": 0, "enemyscore": 1}))
        allyffscore = int(allyfscore[0]['allyscore'])
        enemyffscore = int(enemyfscore[0]['enemyscore'])            
        war_score = list(self.faction.find({"_id": warid}))
        allymembers = None
        for faction in war_score:
            allymembers = faction["allymembers"]
        allyscore = None
        for faction in war_score:
            allyscore = faction["allyplayerscore"]
        enemymembers = None
        for faction in war_score:
            enemymembers = faction["enemymembers"]
        enemyscore = None
        for faction in war_score:
            enemyscore = faction["enemyplayerscore"]
        enemyscored = None
        for faction in war_score:
            enemyscored = faction["enemyplayerscored"]
        allyscored = None
        for faction in war_score:
            allyscored = faction["allyplayerscored"]
        ally_score = list(zip(allymembers,allyscore,allyscored))
        allyStr = ""
        for i in ally_score:
            scorelist = list(i)
            crudescore1 = int(scorelist[0])
            crudescore2 = str(scorelist[1])
            crudescore3 = str(scorelist[2])
            allyStr += f'<@{crudescore1}> Won `{crudescore2}` / Lost `{int(crudescore3)-int(crudescore2)}`\n'
        enemy_score = list(zip(enemymembers,enemyscore,enemyscored))
        enemyStr = ""
        for i in enemy_score:
            scorelist = list(i)
            crudescore1 = int(scorelist[0])
            crudescore2 = str(scorelist[1])
            crudescore3 = str(scorelist[2])
            enemyStr += f'<@{crudescore1}> Won  `{crudescore2}` / Lost `{int(crudescore3)-int(crudescore2)}`\n'
        allymember = list(self.faction.find( {"_id": warid}, {"_id": 0, "allymembers": 1}))
        allymemberStr = ''
        for i in allymember[0]['allymembers']:
                member  = await self.bot.fetch_user(i)
                allymemberStr += f"`{member.name}` "
        
        oppmembers = list(self.faction.find( {"_id": warid}, {"_id": 0, "enemymembers": 1}))
        oppmemberStr = ""
        for i in oppmembers[0]['enemymembers']:
                member  = await self.bot.fetch_user(i)
                oppmemberStr += f"`{member.name}` "

        if allyffscore == enemyffscore:
            winning = "Nobody"

        if allyffscore > enemyffscore:
            winning = faction_name
            winning_scores = allyscore
            winning_total = allyscored
            losing_total = enemyscored
            losing_scores = enemyscore
            winning_team = allymembers
            losing_team = enemymembers
            losing = efaction_name
            winsore = allyffscore - enemyffscore
        
        if allyffscore < enemyffscore:
            winning = efaction_name
            winning_scores = enemyscore
            winning_team = enemymembers
            losing_team = allymembers
            winning_total = enemyscored
            losing_total = allyscored
            losing_scores = allyscore
            losing = faction_name
            winsore = enemyffscore - allyffscore
        
        allypingStr = ""
        for i in allymember[0]['allymembers']:
                member  = await self.bot.fetch_user(i)
                allypingStr += f"{member.mention} "
        opppingStr = ""
        for i in oppmembers[0]['enemymembers']:
                member  = await self.bot.fetch_user(i)
                opppingStr += f"{member.mention} "

        embed_channel = self.bot.get_channel(807513833554968576)

      

        mvp_scores = [(win * 2) - ((total_matches-win) * 1.5) for win, total_matches in zip(winning_scores, winning_total)]

        mvp_index = mvp_scores.index(max(mvp_scores))
        mvp = winning_team[mvp_index]

        score = f'{allyffscore}-{enemyffscore}'


        for i in winning_team:
            war_check = await self.bot.db.fetch('SELECT * FROM wars WHERE player_id = $1', i)
            res_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', i)
            if (res_check[0]['blade'] == None)  or (res_check[0]['blade'] != warid):
                await self.bot.db.execute(f'UPDATE wars SET warswon = warswon + 1 WHERE player_id = $1', i)
            else:
                indexof = winning_team.index(i)
                newwin = winning_scores[indexof]
                newlost = winning_total[indexof] - winning_scores[indexof]
                streakd = war_check[0]['streak']
                oldpoints = war_check[0]['points']
                rank_value = war_check[0]['rank_value']
                if rank_value == 0:
                    oldrank = 'Bronze'
                elif rank_value == 1:
                    oldrank = 'Silver'
                elif rank_value == 2:
                    oldrank = 'Gold'
                elif rank_value == 3:
                    oldrank = 'Platinum'
                elif rank_value == 4:
                    oldrank = 'Dominant'
                if mvp == i:
                    mvpd = 100
                else:
                    mvpd = 0
                streakup = (streakd * 0.1) + 1
                if streakup > 2:
                    streakup = 2

    
                pointsrec = ((((newwin * 30) - (newlost * 25) + (winsore*2))* streakup) + mvpd) 
                pointsrec = int(pointsrec)

                if pointsrec > 750:
                    pointsrec = 750
                elif pointsrec < 200:
                    pointsrec = 200
                newpoints = oldpoints + pointsrec
                if newpoints < 0:
                    pointsrec = 0
                    newpoints = 0

                if 1250 > newpoints >= 0:
                    rank = 'Bronze'
                elif 3000 > newpoints >= 1250:
                    rank = 'Silver'
                elif 5000 > newpoints >= 3000:
                    rank = 'Gold'
                elif 8000 > newpoints >= 5000 :
                    rank = 'Platinum'
                else:
                    rank = 'Dominant'
                
                if oldrank == rank:
                    pass
                else:
                    if rank == 'Bronze':
                        newrank = 0
                    elif rank == 'Silver':
                        newrank = 1
                    elif rank == 'Gold':
                        newrank = 2
                    elif rank == 'Platinum':
                        newrank = 3
                    elif rank == 'Dominant':
                        newrank = 4
                    await self.bot.db.execute('UPDATE wars SET rank_value = $1 WHERE player_id = $2', newrank, i)
                await self.bot.db.execute(f'UPDATE wars SET points = points + {pointsrec}, streak = streak + 1, warswon = warswon + 1 WHERE player_id = $1', i)
                await self.bot.db.execute(f'UPDATE registered SET blade = NULL WHERE player_id = $1', i)
                await embed_channel.send(f"**Blade** :crossed_swords: <@{i}> Earned **+{pointsrec}**.")

        for i in losing_team:
            war_check = await self.bot.db.fetch('SELECT * FROM wars WHERE player_id = $1', i)
            res_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', i)
            if (res_check[0]['blade'] == None)  or (res_check[0]['blade'] != warid):
                await self.bot.db.execute(f'UPDATE wars SET warslost = warslost + 1 WHERE player_id = $1', i)
            else:
                indexof = losing_team.index(i)
                newwin = losing_scores[indexof]
                newtotal = losing_total[indexof]
                newlost = losing_total[indexof] - losing_scores[indexof]
                streakd = war_check[0]['streak']
                oldpoints = war_check[0]['points']
                rank_value = war_check[0]['rank_value']
                if rank_value == 0:
                    oldrank = 'Bronze'
                elif rank_value == 1:
                    oldrank = 'Silver'
                elif rank_value == 2:
                    oldrank = 'Gold'
                elif rank_value == 3:
                    oldrank = 'Platinum'
                elif rank_value == 4:
                    oldrank = 'Dominant'

                pointsrec = ((newwin * 26) - (newlost * 30) - (winsore*2) - ((50 - newtotal)*10))
                pointsrec = int(pointsrec)

                if pointsrec < -750:
                    pointsrec = -750
                elif pointsrec > -200:
                    pointsrec = -200
                
                newpoints = oldpoints + pointsrec
                txt = ''
                if newpoints < 0:
                    newpoints = 0
                    pointsrec = 0
                    txt = "Already at **0**"
                if 1250 > newpoints >= 0:
                    rank = 'Bronze'
                elif 3000 > newpoints >= 1250:
                    rank = 'Silver'
                elif 5000 > newpoints >= 3000:
                    rank = 'Gold'
                elif 8000 > newpoints >= 5000 :
                    rank = 'Platinum'
                else:
                    rank = 'Dominant'
                if oldrank == rank:
                    pass
                else:
                    if rank == 'Bronze':
                        newrank = 0
                    elif rank == 'Silver':
                        newrank = 1
                    elif rank == 'Gold':
                        newrank = 2
                    elif rank == 'Platinum':
                        newrank = 3
                    elif rank == 'Dominant':
                        newrank = 4

                    await self.bot.db.execute('UPDATE wars SET rank_value = $1 WHERE player_id = $2', newrank, i)


                await self.bot.db.execute(f'UPDATE wars SET points = points + {pointsrec}, streak = 0, warslost = warslost + 1 WHERE player_id = $1', i)
                await self.bot.db.execute(f'UPDATE registered SET blade = NULL WHERE player_id = $1', i)
                await embed_channel.send(f"**Blade** :crossed_swords: <@{i}> Lost **{pointsrec}**. {txt}")

        self.collection.update_one({"_id":str(winning.title())}, {"$addToSet": {"career": f":green_circle: **Won** against `{str(losing.title())}` with score `{score}` on *{datetime.datetime.now().date()}*\n《**MVP**》<@{mvp}>"}})
        self.collection.update_one({"_id":str(losing.title())}, {"$addToSet": {"career": f":red_circle: **Lost** against `{str(winning.title())}` with score `{score}` on *{datetime.datetime.now().date()}*\n《**MVP**》<@{mvp}>"}})
    
        clans1 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(winning.title()))
        clans2 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(losing.title()))

        ready = 'False'
        await self.bot.db.execute('UPDATE clans SET ready_for_war = $1 WHERE clan_name = $2', ready, str(winning.title()))
        await self.bot.db.execute('UPDATE clans SET ready_for_war = $1 WHERE clan_name = $2', ready, str(losing.title()))
        await self.bot.db.execute('UPDATE clans SET warmembers = NULL WHERE clan_name = $1', str(winning.title()))
        await self.bot.db.execute('UPDATE clans SET warmembers = NULL WHERE clan_name = $1', str(losing.title()))

        ccstr = ''
        dominate = 0
        teamdiff = 75
        bonus = 1.5
        close = 0
        

        flag = False
        for p, i in enumerate(winning_scores):
            if (i >= winning_total[p]/2) and (winning_total[p] != 0):
                pass
            else:
                teamdiff = 0
                flag = True
                break
        
        if flag == False:
            ccstr += f'+75 TEAM DIFF\n'
        
        
        if winsore >= 30:
            dominate = 50
            ccstr += f'+50 DOMINATION\n'

        if winsore < 6:
            close = 25
            ccstr += f'+25 BREATHTAKING\n'


        flag = False
        for i in winning_total:
            if i >= 5:
                pass
            else:
                bonus = 1
                flag = True
                break

        if flag == False:
            ccstr += f'x1.5 IN IT TOGETHER\n'
        

        await self.bot.db.execute('UPDATE clans SET comeback = $1 WHERE clan_name = $2', str(losing.title()), str(winning.title()))
        await self.bot.db.execute('UPDATE clans SET comeback = $1 WHERE clan_name = $2',  str(winning.title()),  str(losing.title()))        
        
        
        streakrn = clans1[0]['streak']
        winpfp = clans1[0]['avatar']
        
        if streakrn > 10:
            streakrn = 10
        streaks = (streakrn/10)+1
        ccstr += f'x{streaks} STREAK BONUS\n'
        win_score = (sum(winning_scores)*2) + (sum(winning_total))
        ccstr = f'+{round(win_score)} WIN&MATCHES BONUS\n' + ccstr
        if (powerups != 'no') and (powerups != '10101'):
            ccstr += f'+250 POWERUPS'
            power = 250
        else:
            power = 0

        neutral_coins = ((bonus * (win_score) + teamdiff + dominate + close ) * (streaks)) + power
        enemy_coins = (sum(losing_total)*0.25) +  (sum(losing_scores)) + power
        neutral_coins = round(neutral_coins)
        enemy_coins = round(enemy_coins)

        await self.bot.db.execute(f'UPDATE clans SET cc = cc + {neutral_coins} WHERE clan_name = $1', str(winning.title()))
        await self.bot.db.execute(f'UPDATE clans SET cc = cc + {enemy_coins} WHERE clan_name = $1', str(losing.title()))
        
        war = 'war'
        await self.bot.db.execute('UPDATE registered SET clan_2 = NULL WHERE clan_1 = $1 AND clan_2 = $2', str(winning.title()), war)
        await self.bot.db.execute('UPDATE registered SET clan_2 = NULL WHERE clan_1 = $1 AND clan_2 = $2', str(losing.title()), war)

        ccstr += f'\n**Total: {neutral_coins} cc**'





        member_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', mvp)
        flists = str(member_check[0]['achievements'])
        new_admins = ''
        admins_list = listing(flists)


 

        clan1embed = discord.Embed(
        title = f"{allyffscore} / {sum(allyscored)}",
        description = f'',
        colour = 0x4c0843
        )        
        if faction_name == winning:
            textstr = allyStr
            coinstr = ccstr
            name = faction_name
            clan = clans1
        else:
            textstr = allyStr
            if (powerups != 'no') and (powerups != '10101'):
                coinstr = f'+250 Powerups\n**Total: {enemy_coins} cc**'
            else:
                coinstr = f'**Total: {enemy_coins} cc**'
            name = faction_name
            clan = clans2           
            

        avatar = clan[0]['avatar']
        if avatar is None:
            pfp = 'clandefault.png'
        else:
            pfp = avatar
        clan1embed.add_field(name = f'Players', value = textstr, inline=False)
        clan1embed.add_field(name = f'Earnings', value = coinstr, inline=False)
        clan1embed.set_thumbnail(url=f"attachment://{pfp}")
        clan1embed.set_author(name = name)

        await embed_channel.send(f'{opppingStr} {allypingStr}',file = discord.File(pfp), embed = clan1embed ) 

        

        clan1embed = discord.Embed(
        title = f"{enemyffscore} / {sum(enemyscored)}",
        description = f'',
        colour = 0x8f0d3a
        )        
        if efaction_name == winning:
            textstr = enemyStr
            coinstr = ccstr
            name = efaction_name
            clan = clans1
        else:
            textstr = enemyStr
            if (powerups != 'no') and (powerups != '10101'):
                coinstr = f'+250 Powerups\n**Total: {enemy_coins} cc**'
            else:
                coinstr = f'**Total: {enemy_coins} cc**'
                
            name = efaction_name
            clan = clans2           
            

        avatar = clan[0]['avatar']
        if avatar is None:
            pfp = 'clandefault.png'
        else:
            pfp = avatar
        clan1embed.add_field(name = f'Players', value = textstr, inline=False)
        clan1embed.add_field(name = f'Earnings', value = coinstr, inline=False)
        clan1embed.set_thumbnail(url=f"attachment://{pfp}")
        clan1embed.set_author(name = name)

        await embed_channel.send(file = discord.File(pfp), embed = clan1embed ) 

        actualtime = "Ended"
        embedScore = discord.Embed(
        title = f"🏆 {winning} Won!",
        description = f'**MVP** was <@{mvp}>\n**{winning}** won by **{winsore} wins.**',
        colour = 0xf5144f
        )
        pfp = 'win.png'
        embedScore.set_footer(text = f'{actualtime}')
        passs = Image.open(pfp)
        if winpfp == None:
            realpfp = Image.open('clandefault.png')
            
        else:
            realpfp = Image.open(winpfp)

        realpfp = realpfp.resize((300,300))
        passs.paste(realpfp, (490,103), realpfp.convert('RGBA'))
        bytes = BytesIO()
        passs.save(bytes, format="PNG")
        bytes.seek(0)
        dfile = discord.File(bytes, filename= "rgb_img.png")    
        embedScore.set_image(url=f"attachment://rgb_img.png")

        for p,admin in enumerate(admins_list):
            if p == 0:
                new_admins += str(admin)
            elif p == 34:
                if int(admin) == 0:
                    admins_list[35] = 1
                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  mvp)
                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  mvp)
                    await ctx.send("**Bronze Achievement Completed! ✦ Get MVP in a war ✦**\n*10dc rewarded & Lootbox rewarded*")
                elif int(admin) == 2:
                    admins_list[35] = 2
                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  mvp)
                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  mvp)
                    await ctx.send("**Silver Achievement Completed! ✦✦ Get 3 MVPs ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                elif int(admin) == 9:
                    admins_list[35] = 3
                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  mvp)
                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  mvp)
                    await ctx.send("**Gold Achievement Completed! ✦✦✦ Get 10 MVPs ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                admin = int(admin) + 1
                new_admins += f' {admin}'                                                       
            else:
                new_admins += f' {admin}'  
        await self.bot.db.execute(f'UPDATE registered SET achievements = $1, mvps = mvps + 1 WHERE player_id = $2', new_admins, mvp) 
        await self.bot.db.execute(f'UPDATE wars SET mvps = mvps + 1 WHERE player_id = $1', mvp) 
        await self.bot.db.execute('UPDATE clans SET streak = streak + 1, played = played + 1, points = points + 1 WHERE clan_name = $1', str(winning.title()))
        await self.bot.db.execute('UPDATE clans SET played = played + 1, streak = 0 WHERE clan_name = $1', str(losing.title()))
        await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1', mvp)

        await embed_channel.send(file = dfile, embed = embedScore ) 

        self.faction.delete_one({"_id": warid})


    elif self.faction.count_documents({"_id": warid, "wartype": 'koth' }, limit = 1):  

        allycheck = list(self.faction.find( {"_id": warid}, {"_id": 0, "teamone": 1}))
        faction_name = allycheck[0]['teamone']
        enemycheck = list(self.faction.find( {"_id": warid}, {"_id": 0, "teamtwo": 1}))
        efaction_name = enemycheck[0]['teamtwo']
        allyfscore = list(self.faction.find( {"_id": warid}, {"_id": 0, "allyscore": 1}))
        enemyfscore = list(self.faction.find( {"_id": warid}, {"_id": 0, "enemyscore": 1}))
        allyffscore = int(allyfscore[0]['allyscore'])
        enemyffscore = int(enemyfscore[0]['enemyscore'])            
        war_score = list(self.faction.find({"_id": warid}))
        allymembers = None
        for faction in war_score:
            allymembers = faction["allymembers"]
        allyscore = None
        for faction in war_score:
            allyscore = faction["allyplayerscore"]
        enemymembers = None
        for faction in war_score:
            enemymembers = faction["enemymembers"]
        enemyscore = None
        for faction in war_score:
            enemyscore = faction["enemyplayerscore"]
        enemyscored = None
        for faction in war_score:
            enemyscored = faction["enemyplayerscored"]
        allyscored = None
        for faction in war_score:
            allyscored = faction["allyplayerscored"]


        ally_score = list(zip(allymembers,allyscore,enemymembers,enemyscore,allyscored,enemyscored))
        allymembers = []
        allymembers2 = []
        allyscore = []
        allyscore2 = []
        enemymembers = []
        enemymembers2 = []
        enemyscore = []
        enemyscore2 = []
        allyscored2 = []
        enemyscored2 =[]
        for i in ally_score:
            scorelist = list(i)
            if enemyffscore > 0:
                crudescore1 = int(scorelist[0])
                allyzunit = f'~~<@{crudescore1}>~~'
                allymembers2.append(allyzunit)
                crudescore2 = str(scorelist[1])
                st = str(scorelist[4])
                allyscored2.append(st)
                allyscore2.append(crudescore2)
                enemyffscore -= 1

            else:
                crudescore1 = int(scorelist[0])
                allyunit = f'<@{crudescore1}>'
                allymembers.append(allyunit)
                crudescore2 = str(scorelist[1])
                st = str(scorelist[4])
                allyscored2.append(st)
                allyscore.append(crudescore2)                      
            
            if allyffscore >0:
                crudescore3 = int(scorelist[2])
                enemyzunit = f'~~<@{crudescore3}>~~'
                enemymembers2.append(enemyzunit)
                crudescore4 = str(scorelist[3])
                st = str(scorelist[5])
                enemyscored2.append(st)
                enemyscore2.append(crudescore4)
                allyffscore -= 1 
            else:
                crudescore3 = int(scorelist[2])
                enemyunit = f'<@{crudescore3}>'                                
                enemymembers.append(enemyunit)
                crudescore4 = str(scorelist[3])
                st = str(scorelist[5])
                enemyscored2.append(st)
                enemyscore.append(crudescore4)
        allymembers.extend(allymembers2)    
        allyscore.extend(allyscore2)
        enemymembers.extend(enemymembers2)
        enemyscore.extend(enemyscore2)
        allyscored.extend(allyscored2)
        enemyscored.extend(enemyscored2)
        ally_score = list(zip(allymembers,allyscore,enemymembers,enemyscore,allyscored,enemyscored))

        allyStr = ''
        enemyStr = ''
        for i in ally_score:
            scorelist = list(i)
            crudescore1 = str(scorelist[0])
            crudescore2 = int(scorelist[1])
            crudescore3 = str(scorelist[2])
            crudescore4 = int(scorelist[3])
            crudescore5 = int(scorelist[4])
            crudescore6 = int(scorelist[5])
    
            allyStr += f'{crudescore1} Won `{crudescore2}`/ Lose `{crudescore5}`\n'
            enemyStr += f'{crudescore3} Won `{crudescore4}`/ Lose `{crudescore6}`\n'


        allymember = list(self.faction.find( {"_id": warid}, {"_id": 0, "allymembers": 1}))
        allymemberStr = ''
        for i in allymember[0]['allymembers']:
                member  = await self.bot.fetch_user(i)
                allymemberStr += f"`{member.name}` "
        
        oppmembers = list(self.faction.find( {"_id": warid}, {"_id": 0, "enemymembers": 1}))
        oppmemberStr = ""
        for i in oppmembers[0]['enemymembers']:
                member  = await self.bot.fetch_user(i)
                oppmemberStr += f"`{member.name}` "

        allyffscore = int(allyfscore[0]['allyscore'])
        enemyffscore = int(enemyfscore[0]['enemyscore'])    


        
        war_score = list(self.faction.find({"_id": warid}))
        allymembers = None
        for faction in war_score:
            allymembers = faction["allymembers"]
        allyscore = None
        for faction in war_score:
            allyscore = faction["allyplayerscore"]
        enemymembers = None
        for faction in war_score:
            enemymembers = faction["enemymembers"]
        enemyscore = None
        for faction in war_score:
            enemyscore = faction["enemyplayerscore"]
        enemyscored = None
        for faction in war_score:
            enemyscored = faction["enemyplayerscored"]
        allyscored = None
        for faction in war_score:
            allyscored = faction["allyplayerscored"]

        if allyffscore == enemyffscore:
            winning = "Nobody"

        if allyffscore > enemyffscore:
            winning = faction_name
            winning_scores = allyscore
            winning_total = allyscored
            losing_total = enemyscored
            losing_scores = enemyscore
            winning_team = allymembers
            losing = efaction_name
            winsore = allyffscore - enemyffscore
        
        if allyffscore < enemyffscore:
            winning = efaction_name
            winning_scores = enemyscore
            winning_team = enemymembers
            winning_total = enemyscored
            losing_total = allyscored
            losing_scores = allyscore
            losing = faction_name
            winsore = enemyffscore - allyffscore
        
        allypingStr = ""
        for i in allymember[0]['allymembers']:
                member  = await self.bot.fetch_user(i)
                allypingStr += f"{member.mention} "
        opppingStr = ""
        for i in oppmembers[0]['enemymembers']:
                member  = await self.bot.fetch_user(i)
                opppingStr += f"{member.mention} "

        embed_channel = self.bot.get_channel(807513833554968576)

      

        max_score  = max(winning_scores)
        max_index = winning_scores.index(max_score)
        mvp = winning_team[max_index]
        score = f'{allyffscore}-{enemyffscore}'


        clans1 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(winning.title()))
        clans2 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(losing.title()))



        ccstr = ''
        dominate = 0
        comeback = 0
        teamdiff = 100
        bonus = 50
        close = 0


        
        flag = False
        for p, i in enumerate(winning_scores):
            if i >= 1:
                pass
            else:
                teamdiff = 0
                flag = True
                break
        
        
        if flag == False:
            ccstr += f'+100 TEAM DIFF\n'
        
        if winsore >= 4:
            dominate = 50
            ccstr += f'+50 DOMINATION\n'

        if winsore < 2:
            close = 25
            ccstr += f'+25 BREATHTAKING\n'

        if clans1[0]['comeback'] == None:
            pass
        else:
            if clans1[0]['comeback'] == 'Lose':
                comeback = 30
                ccstr += f'+30 COMEBACK\n'
        flag = False
        for i in winning_total:
            if i >= 3:
                pass
            else:
                bonus = 0
                flag = True
                break
        if flag == False:
            ccstr += f'+50 IRON WALL\n'
        
        comeback1 = 'Win'
        comeback2 = 'Lose'
    
        
        
        streakrn = clans1[0]['streak']
        winpfp = clans1[0]['avatar']
        
        if streakrn > 10:
            streakrn = 10
        streaks = (streakrn/10)+1
        ccstr += f'x{streaks} STREAK BONUS\n'
        win_score = (sum(winning_scores)*10) + (sum(winning_total)*5)
        ccstr = f'+{round(win_score)} WIN&MATCHES BONUS\n' + ccstr
        neutral_coins = (bonus + (win_score) + teamdiff + dominate +comeback + close ) * (streaks)
        enemy_coins = (sum(losing_total)*2.5) +  (sum(losing_scores)*5)
        neutral_coins = round(neutral_coins)
        enemy_coins = round(enemy_coins)



        ccstr += f'\n**Total: {neutral_coins} cc**'





        member_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', mvp)
        flists = str(member_check[0]['achievements'])
        new_admins = ''
        admins_list = listing(flists)

 

        clan1embed = discord.Embed(
        title = f"{allyffscore} / {sum(allyscored)}",
        description = f'',
        colour = 0x4c0843
        )        
        if faction_name == winning:
            textstr = allyStr
            coinstr = ccstr
            name = faction_name
            clan = clans1
        else:
            textstr = allyStr
            coinstr = f'**Total: {enemy_coins} cc**'
            name = faction_name
            clan = clans2           
            

        avatar = clan[0]['avatar']
        if avatar is None:
            pfp = 'clandefault.png'
        else:
            pfp = avatar
        clan1embed.add_field(name = f'Players', value = textstr, inline=False)
        clan1embed.add_field(name = f'Earnings', value = coinstr, inline=False)
        clan1embed.set_thumbnail(url=f"attachment://{pfp}")
        clan1embed.set_author(name = name)

        await embed_channel.send(f'{opppingStr} {allypingStr}',file = discord.File(pfp), embed = clan1embed ) 


        clan1embed = discord.Embed(
        title = f"{enemyffscore} / {sum(enemyscored)}",
        description = f'',
        colour = 0x8f0d3a
        )        
        if efaction_name == winning:
            textstr = enemyStr
            coinstr = ccstr
            name = efaction_name
            clan = clans1
        else:
            textstr = enemyStr
            coinstr = f'**Total: {enemy_coins} cc**'
            name = efaction_name
            clan = clans2           
            

        avatar = clan[0]['avatar']
        if avatar is None:
            pfp = 'clandefault.png'
        else:
            pfp = avatar
        clan1embed.add_field(name = f'Players', value = textstr, inline=False)
        clan1embed.add_field(name = f'Earnings', value = coinstr, inline=False)
        clan1embed.set_thumbnail(url=f"attachment://{pfp}")
        clan1embed.set_author(name = name)

        await embed_channel.send(file = discord.File(pfp), embed = clan1embed ) 

        actualtime = "Ended"
        embedScore = discord.Embed(
        title = f"🏆 {winning} Won!",
        description = f'**MVP** was <@{mvp}>\n**{winning}** won by **{winsore} wins.**',
        colour = 0xf5144f
        )
        pfp = 'win.png'
        embedScore.set_footer(text = f'{actualtime}')
        passs = Image.open(pfp)
        if winpfp == None:
            realpfp = Image.open('clandefault.png')
            
        else:
            realpfp = Image.open(winpfp)

        realpfp = realpfp.resize((300,300))
        passs.paste(realpfp, (490,103), realpfp.convert('RGBA'))
        bytes = BytesIO()
        passs.save(bytes, format="PNG")
        bytes.seek(0)
        dfile = discord.File(bytes, filename= "rgb_img.png")    
        embedScore.set_image(url=f"attachment://rgb_img.png")

        for p,admin in enumerate(admins_list):
            if p == 0:
                new_admins += str(admin)
            elif p == 34:
                if int(admin) == 0:
                    admins_list[35] = 1
                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  mvp)
                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  mvp)
                    await ctx.send("**Bronze Achievement Completed! ✦ Get MVP in a war ✦**\n*10dc rewarded & Lootbox rewarded*")
                elif int(admin) == 2:
                    admins_list[35] = 2
                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  mvp)
                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  mvp)
                    await ctx.send("**Silver Achievement Completed! ✦✦ Get 3 MVPs ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                elif int(admin) == 9:
                    admins_list[35] = 3
                    await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  mvp)
                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  mvp)
                    await ctx.send("**Gold Achievement Completed! ✦✦✦ Get 10 MVPs ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                admin = int(admin) + 1
                new_admins += f' {admin}'                                                       
            else:
                new_admins += f' {admin}'  

        self.collection.update_one({"_id":str(winning.title())}, {"$addToSet": {"career": f":green_circle: **Won** against `{str(losing.title())}` with score `{score}` on *{datetime.datetime.now().date()}*\n《**MVP**》<@{mvp}>"}})
        self.collection.update_one({"_id":str(losing.title())}, {"$addToSet": {"career": f":red_circle: **Lost** against `{str(winning.title())}` with score `{score}` on *{datetime.datetime.now().date()}*\n《**MVP**》<@{mvp}>"}})
        await self.bot.db.execute(f'UPDATE clans SET cc = cc + {neutral_coins} WHERE clan_name = $1', str(winning.title()))
        await self.bot.db.execute(f'UPDATE clans SET cc = cc + {enemy_coins} WHERE clan_name = $1', str(losing.title()))
        await self.bot.db.execute('UPDATE clans SET comeback = $1 WHERE clan_name = $2', comeback1,str(winning.title()))
        await self.bot.db.execute('UPDATE clans SET comeback = $1 WHERE clan_name = $2',comeback2,  str(losing.title()))    
        await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, mvp) 
        await self.bot.db.execute('UPDATE clans SET streak = streak + 1, played = played + 1, points = points + 1, event = event + 1, event_played = event_played + 1 WHERE clan_name = $1', str(winning.title()))
        await self.bot.db.execute('UPDATE clans SET played = played + 1, streak = 0, event_played = event_played + 1 WHERE clan_name = $1', str(losing.title()))
        await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1', mvp)

        await embed_channel.send(file = dfile, embed = embedScore ) 
        self.faction.delete_one({"_id": warid})  

async def warcheck(self, ctx, warid, allyffscore, enemyffscore):
    scorecheck = list(self.faction.find({"_id": warid }, {"_id": 0, "winscore": 1}))
    score = scorecheck[0]['winscore']
    timecheck = list(self.faction.find({"_id": warid }, {"_id": 0, "time": 1}))
    expiration = timecheck[0]['time']
    
    allyscore = list(self.faction.find({"_id": warid }, {"_id": 0, "allyscore": 1}))
    allyffscore = allyscore[0]['allyscore']
    enemyscore = list(self.faction.find({"_id": warid }, {"_id": 0, "enemyscore": 1}))
    enemyffscore = enemyscore[0]['enemyscore']
    
    t = datetime.datetime.now(timezone.utc)
    timenow = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
    


    if allyffscore >= score:
        await warwin(self,ctx, warid)
    elif enemyffscore >= score:
        await warwin(self,ctx, warid)
    elif timenow >= expiration:
        await warwin(self,ctx, warid)
    else:
        return



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

class TourneyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = MongoClient("####")
        database = self.cluster['discord']
        self.collection = database["faction"]
        self.faction = database["wars"]

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

    @commands.command(name = 'warstart')
    async def war_commdfafdaand(self,ctx,mode : str = None, duration : int = None, winscore : int = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if registered_check:
            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(786448967172882442)
            role2 = guild.get_role(1090438349455622204)
            role3 = guild.get_role(781452019578961921)
            if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles):
                if (mode == None) or (duration == None) or (winscore == None) :
                    em = discord.Embed(
                        title = "Help 🛠️",
                        description = '**d!war [Mode] [Duration: in days max 7 days][If its a BR: Winscore] **',
                        colour = color
                    )
                    await ctx.send(embed = em)
                
                else:


                    if duration > 7:
                        await ctx.send("Max 7 days")
                    elif winscore >150:
                        await ctx.send("Max 150 wins")
                    else:
                        await ctx.message.delete()
                        one = await ctx.send(f"{ctx.author.mention} Please specify the **1st** Clan name.")
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
                                if (mode.lower() == 'br') or (mode.lower() =='koth'):
                                    three =await ctx.send(f"{ctx.author.mention} Please mention the ally members of **{clan_1}**. *Make sure you ask them before adding them here*")
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

                                        if len(alliesList) > 15:
                                            await ctx.send("Too many members.. *(Max 15)*")
                                        elif len(alliesList) < 3:
                                            await ctx.send("Add more members.. *(Min 3)*")                            
                                        else:
                                            await three.delete()
                                            await allies.delete()
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
                                                if len(enemiesList) > 15:
                                                    await ctx.send("Too many members.. *(Max 15)*")
                                                elif len(enemiesList) < 3:
                                                    await ctx.send("Add more members.. *(Min 3)*")
                                                else:
                                                    clans1 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(clan_1.title()))
                                                    clans2 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', str(clan_2.title()))
                                                    if not clans1:
                                                        await ctx.send(f'{str(clan_1.title())} is not a registered clan.')
                                                    elif not clans2:
                                                        await ctx.send(f'{str(clan_2.title())} is not a registered clan.')
                                                    else:
                                                        await four.delete()
                                                        await enemies.delete() 
                                                        faction_name = str(clan_1.title())
                                                        factionMembers = list(self.collection.find( {"_id": faction_name}, {"_id": 0, "members": 1}))
                                                        faction_members = []
                                                        for i in factionMembers[0]['members']:
                                                            faction_members.append(i)
                                                        check = all(item in faction_members for item in alliesList)
                                                        if check is True:
                                                            test1 = await ctx.send(f"**{clan_1.title()}'s** team's members are all from the same Clan..")
                                                            for item in alliesList:
                                                                checkk = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', item)
                                                                warcheck = checkk[0]['clan_2']
                                                                if warcheck == None:
                                                                    wardd = 'war'
                                                                    await self.bot.db.execute(f'UPDATE registered SET clan_2 = $1 WHERE player_id = $2', wardd, item)
                                                                else:
                                                                    pass



                                                            efaction_name = str(clan_2.title())
                                                            efactionMembers = list(self.collection.find( {"_id": efaction_name}, {"_id": 0, "members": 1}))
                                                            efaction_members = []
                                                            for i in efactionMembers[0]['members']:
                                                                efaction_members.append(i)
                                                            check = all(item in efaction_members for item in enemiesList)
                                                            if check is True:
                                                                test2 = await ctx.send(f"**{clan_2.title()}'s** team's members are all also from the same Clan.. ")

                                                                for item in enemiesList:
                                                                    checkk = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', item)
                                                                    warcheck = checkk[0]['clan_2']
                                                                    if warcheck == None:
                                                                        wardd = 'war'
                                                                        await self.bot.db.execute(f'UPDATE registered SET clan_2 = $1 WHERE player_id = $2', wardd, item)
                                                                    else:
                                                                        pass


                                                                enemyitems = len(enemiesList)
                                                                enemyscore = [0] * enemyitems
                                                                enemyscored = [0] * enemyitems
                                                                
                                                                allyitems = len(alliesList)
                                                                allyscore = [0] * allyitems
                                                                allyscored = [0] * allyitems
                                                                to = datetime.datetime.now(timezone.utc)
                                                                timenewe = int(time.mktime(to.timetuple()) + to.microsecond / 1E6)
                                                                self.collection.update_one({"_id":faction_name}, {"$set": {"time": timenewe}})
                                                                self.collection.update_one({"_id":efaction_name}, {"$set": {"time": timenewe}})
                                                                if mode.lower() == 'br':
                                                                    view = ConfirmCancel(ctx.author)
                                                                    message = await ctx.send(f'{ctx.author.mention} Are you sure? This will be a **BR** first to reach **{winscore}** wins between **{clan_1}** and **{clan_2}**', view = view)
                                                                    
                                                                    await view.wait()

                                                                    if view.value is True: 
                                                                    
                                                                        await test1.delete()
                                                                        await test2.delete()    
                                                                        await message.delete()   
                                                                        view = ConfirmCancel(ctx.author)
                                                                        dex = await ctx.send(f'{ctx.author.mention} Enable powerups? Powerups increase the cc amount earned by both clans.', view = view)
                                                                        
                                                                        await view.wait()

                                                                        if view.value is True: 
                                                                            powerups = '10101'
                                                                        elif view.value is False:
                                                                            powerups = 'no'
                                                                        else:
                                                                            powerups = 'no'                                                                          

                                                                        await dex.delete()                                                   
                                                                        time_change = datetime.timedelta(days=duration)
                                                                        t = datetime.datetime.now(timezone.utc) + time_change
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
                                                                        self.faction.insert_one({"_id": warid, "allyscore": 0, "enemyscore" : 0, "allymembers": alliesList, "enemymembers": enemiesList,"allymembersname": alliesListname, "enemymembersname": enemiesListname, "allyplayerscored": allyscored, "enemyplayerscored": enemyscored,"allyplayerscore": allyscore, "enemyplayerscore": enemyscore, "winscore" : winscore, "time" : timenew,"teamone": faction_name, "teamtwo":efaction_name,  "faction": True, "wartype": 'br',"history": history,"powerups": powerups, "1powerup": power, "2powerup" : power })
                                                                        allymemberStr = ""
                                                                        for i in alliesList:
                                                                                allymemberStr += f"<@{i}> "
                                                                        oppmemberStr = ""
                                                                        for i in enemiesList:
                                                                                oppmemberStr += f"<@{i}> "
                                                                        war = discord.Embed(
                                                                        title = f"⚔️ {faction_name} VS {efaction_name} First to get {winscore} wins",
                                                                        description = f'To log wins do d!log [Opponent]\nd!viewwar **{warid}** to view this war.',
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
                                                                elif mode.lower() == 'koth':
                                                                    view = ConfirmCancel(ctx.author)
                                                                    message = await ctx.send(f'{ctx.author.mention} Are you sure? This will be a **Koth** between **{clan_1}** and **{clan_2}**', view = view)
                                                                    
                                                                    await view.wait()

                                                                    if view.value is True:   
                                                                        await test1.delete()
                                                                        await test2.delete()    
                                                                        await message.delete()                                                          
                                                                        time_change = datetime.timedelta(days=duration)
                                                                        t = datetime.datetime.now(timezone.utc) + time_change
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
                                                                        self.faction.insert_one({"_id": warid, "allyscore": 0, "enemyscore" : 0, "allymembers": alliesList, "enemymembers": enemiesList,"allymembersname": alliesListname, "enemymembersname": enemiesListname, "allyplayerscored": allyscored, "enemyplayerscored": enemyscored, "allyplayerscore": allyscore, "enemyplayerscore": enemyscore, "winscore" : winscore, "time" : timenew,"teamone": faction_name, "teamtwo":efaction_name,  "faction": True, "wartype": 'koth' ,"history": history })
                                                                        allymemberStr = ""
                                                                        for i in alliesList:
                                                                                allymemberStr += f"<@{i}> "
                                                                        oppmemberStr = ""
                                                                        for i in enemiesList:
                                                                                oppmemberStr += f"<@{i}> "
                                                                        war = discord.Embed(
                                                                        title = f"⚔️ {faction_name} VS {efaction_name} First to get {winscore} wins",
                                                                        description = f'To log wins do d!log [Opponent]\nd!viewwar **{warid}** to view this war.',
                                                                        colour = color
                                                                        )
                                                                        war.add_field(name = f'{faction_name}', value = allymemberStr, inline=False)
                                                                        war.add_field(name = f'{efaction_name}', value = oppmemberStr, inline=False)
                                                                        war.add_field(name = 'Scoreboard: ', value = "Log your wins and they'll show up here.", inline=False)
                                                                        war.set_footer(text = f'Ends in {duration} Day(s).')
                                                                        await ctx.send(embed = war)
                                                                    elif view.value is False:
                                                                        await ctx.send("Cancelled.")
                                                                    else:
                                                                        await ctx.send("Timed out.")      

                                                                else:
                                                                    await ctx.send("Incorrect war type. War types currently available: **br**")
                                                            else:
                                                                await ctx.send(f"Not all members are from the same clan. Try again if this is a mistake.")
                                                                return

                                                        else:
                                                            await ctx.send(f"Not all members are from the same clan. Try again if this is a mistake.")
                                                            return
                                            
                                        
                                else:
                                    await ctx.send("Incorrect mode.")
            else:
                await ctx.send('You do not have permission to use that command.')               
        else:
            await ctx.send("You haven't registered yet! do `d!start` to register.")

    @commands.command(name='powerup', aliases = ['powerups'], )
    async def log_pow_command(self,ctx,warid =None, powbuy : str = None):
        if (warid == None) or (powbuy == None):


            data = ['bridger','jeopardy', 'battle', 'immunity', 'breakthrough', 'counterstrike', 'strategic', 'reflection', 'mimicry', 'sacrifice', 'retribution']

            
            stat = None
            lb = None
            stats = None

            pagination_view = Career()
            pagination_view.data = data
            pagination_view.lb = lb
            pagination_view.stat = stat
            pagination_view.stats = stats
            await pagination_view.send(ctx)

        else:
            player = ctx.author

            registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', player.id)
            if registered_check:
                registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
                clan_name = registered_check[0]['clan_1']
                if clan_name:
                    cland = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', clan_name.title())
                else:
                    await ctx.send("You're not in a clan!")
                    return
                
                if self.faction.count_documents({"_id": warid}, limit = 1):
                    if powbuy == 'immunity':
                        price = 60
                        no = 'a'

                    elif powbuy == 'jeopardy':
                        price = 35
                        no = 'b'

                    elif powbuy == 'bridger':
                        price = 50
                        no = '3'
                    else:
                        return
                    if cland[0]['dc'] < price:
                        message = await ctx.send(f"Your clan doesn't have enough Dc.. it costs **{price}**Dc. Give your clan Dc by using the command `d!clan give [dc]`")
                        await message.delete(delay=3)
                        await ctx.message.delete() 
                        return
                    war_data = self.faction.find_one({"_id": warid}, {
                        "_id": 0,
                        'powerups':1,
                        "allyscore": 1,
                        "enemyscore": 1
                    })
                    powers = war_data['powerups']
                    allyscore = war_data['allyscore']
                    enemyscore = war_data['enemyscore']
                    if powers == 'no':
                        await ctx.send("Powerups disabled.")
                        return
                    
                    view = ConfirmCancel(ctx.author)
                    sed = await ctx.send(f'{ctx.author.mention} Buy {powbuy} for **{price}dc**?', view = view)
                    await view.wait()

                    if view.value is True: 
                        await sed.delete() 
                        flag = False
                        if self.faction.count_documents({"_id": warid, "allymembers": player.id}, limit = 1):
                            clan = 1
                            flag = True
                            if powbuy == 'bridger':
                                if (enemyscore - allyscore) > 9:
                                    pass
                                else:
                                    message = await ctx.send("You can only buy this powerup when there is a difference of 10 or more points.")
                                    await message.delete(delay=2) 
                                    await ctx.message.delete()
                                    return
                            elif powbuy == 'jeopardy':
                                if allyscore < 2:
                                    message = await ctx.send("You can only buy this powerup when your clan has atleast 2 points.")       
                                    await message.delete(delay=2) 
                                    await ctx.message.delete()
                                    return             
                        if flag == False:
                            if self.faction.count_documents({"_id": warid, "enemymembers": player.id,}, limit = 1):
                                clan = 2
                                if powbuy == 'bridger':
                                    if (allyscore - enemyscore) > 9:
                                        pass
                                    else:
                                        message = await ctx.send("You can only buy this powerup when there is a difference of 10 or more points.")
                                        await message.delete(delay=2) 
                                        await ctx.message.delete()
                                        return  
                                elif powbuy == 'jeopardy':
                                    if enemyscore < 2:
                                        message = await ctx.send("You can only buy this powerup when your clan has atleast 2 points.")    
                                        await message.delete(delay=2)   
                                        await ctx.message.delete() 
                                        return             
                            else:
                                clan = 0

                        if clan == 0:
                            await ctx.send(f"You are not in the war.")
                            return
                        elif clan == 1:
                            if powers[1] == '4':
                                if powbuy == 'immunity':
                                    message = await ctx.send("Immunity cooldown.. you have to buy another powerup before buying immunity again.")
                                    await message.delete(delay=2)
                                    await ctx.message.delete()
                                    return
                            elif powers[1] != '0':
                                message = await ctx.send("The clan already has a powerup enabled.")
                                await message.delete(delay=2) 
                                await ctx.message.delete()
                                return
                            pow2 = powers[3]
                            powers = f'1{no}1{pow2}'
                            powers = str(powers)
                            self.faction.update_one({"_id":warid}, {"$set": {"powerups": powers}})
                            await self.bot.db.execute(f'UPDATE clans SET dc = dc - {price} WHERE clan_name = $1', clan_name.title()) 
                            message = await ctx.send("Powerup bought!")
                            await message.delete(delay=2) 
                            await ctx.message.delete()
                        elif clan == 2:
                            if powers[3] == '4':
                                if powbuy == 'immunity':
                                    message = await ctx.send("Immunity cooldown.. you have to buy another powerup before buying immunity again.")
                                    await message.delete(delay=2) 
                                    await ctx.message.delete()
                                    return
                            elif powers[3] != '0':
                                message = await ctx.send("The clan already has a powerup enabled.")
                                await message.delete(delay=2) 
                                await ctx.message.delete()
                                return
                            pow1 = powers[1]
                            powers = f'1{pow1}1{no}'
                            powers = str(powers)
                            self.faction.update_one({"_id":warid}, {"$set": {"powerups": powers}})
                            await self.bot.db.execute(f'UPDATE clans SET dc = dc - {price} WHERE clan_name = $1', clan_name.title()) 
                            message = await ctx.send("Powerup bought!")
                            await message.delete(delay=2) 
                            await ctx.message.delete()
                        else:
                            await ctx.send("Error")
                            return

                        
                    elif view.value is False:
                        await sed.delete() 
                        await ctx.send("Cancelled.")
                    else:
                        await ctx.send("Timed out.")

                else:
                    await ctx.send(f"Incorrect War ID.")
            else:
                await ctx.send("You haven't registered yet! do `d!start` to register.")

    @commands.command(name ="viewwar", aliases = ['vv'], )
    async def view_dfadfwar_command(self, ctx,*, warid = None):
        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

  
        if user_ban_list:
            await ctx.send('You are banned from the bot.')

        else:

            registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
            if registered_check:    

                if warid == None:
                    warids = self.faction.find({})
                    warid_list = [doc["_id"] for doc in warids]
                    truelist = []
                    for i in warid_list:
                        war_dataed = self.faction.find_one({"_id": i}, {
                            "teamone": 1,
                            "teamtwo": 1,
                        })
                        faction_name = war_dataed['teamone']
                        efaction_name = war_dataed['teamtwo']

                        title = f'{faction_name} VS {efaction_name}'
                        truelist.append((i,title))

                    view = Wars(ctx.author, truelist)
                    await ctx.reply(view = view)
                    await view.wait()

                    if view.value is None:
                        await ctx.send("Timed Out.")
                        return
                    else:
                        warid = view.value.upper()

                else:
                    pass

                

                if self.faction.count_documents({"_id": warid }, limit = 1):
                    load = await ctx.send("**Generating embed.**")
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

                    clan1 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', faction_name)
                    if clan1[0]['avatar'] is None:
                        pfp = Image.open("clandefault.png")
                        pfp.convert('RGBA')
                    else:
                        pfp = Image.open(clan1[0]['avatar'])
                        pfp.convert('RGBA')
                    pfp = pfp.resize((300,300))
                    profile.paste(pfp, (210,50),pfp.convert('RGBA'))

                    clan2 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', efaction_name)
                    if clan2[0]['avatar'] is None:
                        pfp = Image.open("clandefault.png")
                        pfp.convert('RGBA')
                    else:
                        pfp = Image.open(clan2[0]['avatar'])
                        pfp.convert('RGBA')
                    pfp = pfp.resize((300,300))
                    profile.paste(pfp, (930,50),pfp.convert('RGBA'))

                    font = ImageFont.truetype("Pacifico-Regular.ttf", 80)

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
                    dfile = discord.File(bytes, filename= "rgb_img.png")     


                    if formats == 'br':
                        ally_score = list(zip(allymembers,allyscore,allyscored))
                        allyStr = ""
                        ok = 0
                        allypings = []
                        for i in ally_score:
                            
                            scorelist = list(i)
                            crudescore1 = int(scorelist[0])
                            crudescore2 = str(scorelist[1])
                            crudescore3 = str(scorelist[2])

                            allypings.append(crudescore1)
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
                        enemypings = []
                        for i in enemy_score:
                            scorelist = list(i)
                            crudescore1 = int(scorelist[0])
                            crudescore2 = str(scorelist[1])
                            crudescore3 = str(scorelist[2])
                            enemypings.append(crudescore1)

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

                        fduration = list(self.faction.find( {"_id": warid}, {"_id": 0, "time": 1}))
                        duration = fduration[0]['time']
                        
                        date1 = datetime.datetime.fromtimestamp(duration)
                        t = datetime.datetime.now(timezone.utc)
                        timenew = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
                        date2 = datetime.datetime.fromtimestamp(timenew)
                        
                        actualtime = "%dd %dh %dm %ds" % dhms_from_seconds(date_diff_in_seconds(date2, date1))
                        embedScore = discord.Embed(
                        title = f"{faction_name} VS {efaction_name} (First to {winscore})",
                        description = f'To log wins do d!log [Opponent]\n\u200b',
                        colour = color
                        )
                        embedScore.add_field(name = 'ＳＣＯＲＥＢＯＡＲＤ', value = f"", inline=False)
                        embedScore.add_field(name = f'{faction_name} {allyffscore}', value = allyStr)
                        embedScore.add_field(name = f'{efaction_name} {enemyffscore}', value = enemyStr)
                        embedScore.add_field(name = f'History', value= logstr, inline=False)
                        if (powerups == None) or (powerups == 'no'):
                            powerups = '❌ Disabled'
                        else:
                            powerups = '📡 Enabled'


                        embedScore.add_field(name = f'Powerups: {powerups}', value= '', inline=False)
                        embedScore.set_footer(text = f'Ends in {actualtime}')
                        embedScore.set_image(url=f"attachment://rgb_img.png")

                        player = ctx.author.id

                        flag = True
           
                        if self.faction.count_documents({"_id": warid, "allymembers": player}, limit = 1):
                            toping = enemypings
                            clan11 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', efaction_name)
                        
                        elif self.faction.count_documents({"_id": warid, "enemymembers": player}, limit = 1):
                            toping = allypings
                            clan11 = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1', faction_name)
                        
                        else:
                            flag = False

                        if flag:

                            ping = registered_check[0]['ping']

                            view = pingbutton(ctx.author, ping, self.bot)

                            await load.edit("",file = discord.File(bytes,"rgb_img.png"),embed = embedScore, view = view)

                            await view.wait()

                            if view.value is True:
                                timenow = datetime.datetime.now(timezone.utc)
                                timenow_naive = timenow.replace(tzinfo=None)
                                if (clan11[0]['pingtime'] == None) or (clan11[0]['pingtime'] <= timenow_naive):
                                    midnight = datetime.datetime.now(timezone.utc) + datetime.timedelta(hours=1)
                                    midnight_naive = midnight.replace(tzinfo=None)
                                    await self.bot.db.execute(f'UPDATE clans SET pingtime = $1 WHERE clan_name = $2',midnight_naive, clan11[0]['clan_name'])

                                    pinged = ''

                                    for i in toping:
                                        check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', i)
                                        pingvalue = check[0]['ping']

                                        if pingvalue == 'yes':
                                            pinged += f'<@{i}>\n'
                                        else:
                                            member  = await self.bot.fetch_user(i)
                                            pinged += f'**{member.name}** 🔇 Do Not Disturb\n'

                                    await load.reply(f"{ctx.author.mention} is pinging all enemy opponents!\n\n{pinged}")
                                else:
                                    time_difference = clan11[0]['pingtime'] - timenow_naive
                                    formatted_time = format_time_difference(time_difference)
                                    await ctx.send(f"There is still time left before you can ping them again! **{formatted_time} Left**")
       
                            else:
                                pass

                        else:
                            await load.edit("",file = discord.File(bytes,"rgb_img.png"),embed = embedScore)












                    elif formats == 'koth':

                        ally_score = list(zip(allymembers,allyscore,enemymembers,enemyscore,allyscored,enemyscored))
                        Str = ""
                        allymembers = []
                        allymembers2 = []
                        allyscore = []
                        allyscore2 = []
                        enemymembers = []
                        enemymembers2 = []
                        enemyscore = []
                        enemyscore2 = []
                        allyscored2 = []
                        enemyscored2 =[]
                        for i in ally_score:
                            scorelist = list(i)
                            if enemyffscore > 0:
                                crudescore1 = int(scorelist[0])
                                allyzunit = f'~~<@{crudescore1}>~~'
                                allymembers2.append(allyzunit)
                                crudescore2 = str(scorelist[1])
                                st = str(scorelist[4])
                                allyscored2.append(st)
                                allyscore2.append(crudescore2)
                                enemyffscore -= 1

                            else:
                                crudescore1 = int(scorelist[0])
                                allyunit = f'<@{crudescore1}>'
                                allymembers.append(allyunit)
                                crudescore2 = str(scorelist[1])
                                st = str(scorelist[4])
                                allyscored2.append(st)
                                allyscore.append(crudescore2)                      
                            
                            if allyffscore >0:
                                crudescore3 = int(scorelist[2])
                                enemyzunit = f'~~<@{crudescore3}>~~'
                                enemymembers2.append(enemyzunit)
                                crudescore4 = str(scorelist[3])
                                st = str(scorelist[5])
                                enemyscored2.append(st)
                                enemyscore2.append(crudescore4)
                                allyffscore -= 1 
                            else:
                                crudescore3 = int(scorelist[2])
                                enemyunit = f'<@{crudescore3}>'                                
                                enemymembers.append(enemyunit)
                                crudescore4 = str(scorelist[3])
                                st = str(scorelist[5])
                                enemyscored2.append(st)
                                enemyscore.append(crudescore4)
                        allymembers.extend(allymembers2)    
                        allyscore.extend(allyscore2)
                        enemymembers.extend(enemymembers2)
                        enemyscore.extend(enemyscore2)
                        allyscored.extend(allyscored2)
                        enemyscored.extend(enemyscored2)
                        ally_score = list(zip(allymembers,allyscore,enemymembers,enemyscore,allyscored,enemyscored))
                                
                        for i in ally_score:
                            scorelist = list(i)
                            crudescore1 = str(scorelist[0])
                            crudescore2 = int(scorelist[1])
                            crudescore3 = str(scorelist[2])
                            crudescore4 = int(scorelist[3])
                            crudescore5 = int(scorelist[4])
                            crudescore6 = int(scorelist[5])
                            if ally_score.index(i) == 0:
                                Str += f'`{crudescore2}`/`{crudescore5}` {crudescore1}  :crossed_swords:  {crudescore3} `{crudescore4}`/`{crudescore6}`\n'
                            else:
                                Str += f'`{crudescore2}`/`{crudescore5}` {crudescore1}      {crudescore3} `{crudescore4}`/`{crudescore6}`\n'
                        await load.edit("**Generating embed..**")
                        logstr = ''
                        for i in logstrs:
                            logstr += f'{i}\n'


                        fduration = list(self.faction.find( {"_id": warid}, {"_id": 0, "time": 1}))
                        duration = fduration[0]['time']
                        
                        date1 = datetime.datetime.fromtimestamp(duration)
                        t = datetime.datetime.now(timezone.utc)
                        timenew = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
                        date2 = datetime.datetime.fromtimestamp(timenew)
                        
                        actualtime = "%dd %dh %dm %ds" % dhms_from_seconds(date_diff_in_seconds(date2, date1))
                        embedScore = discord.Embed(
                        title = f"{faction_name} VS {efaction_name}",
                        description = f'To log wins do d!wlog **{warid}** [Opponent]\n\u200b',
                        colour = color
                        )
                        embedScore.add_field(name = 'ＳＣＯＲＥＢＯＡＲＤ', value = f"", inline=False)
                        embedScore.add_field(name = f'{faction_name}     {efaction_name}', value = Str)
                        embedScore.add_field(name = f'Past logs', value= logstr,inline=False)
                        embedScore.set_footer(text = f'Ends in {actualtime}')
                        embedScore.set_image(url=f"attachment://rgb_img.png")
                        await load.edit("",file = discord.File(bytes,"rgb_img.png"),embed = embedScore)
                        enemyffscore = war_data['enemyscore']
                        allyffscore = war_data['allyscore']

                else:
                    await ctx.send("Incorrect War ID.")
            else:
                await ctx.send("You haven't registered yet! do `d!start` to register.")

          

    @commands.command(name='swap')
    async def order_command(self,ctx,warid =None, opponent1 : discord.Member = None, replace2 : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        if registered_check:
            
            guild = self.bot.get_guild(774883579472904222)
            role = guild.get_role(786448967172882442)
            role2 = guild.get_role(1090438349455622204)
            if (role in ctx.author.roles) or (role2 in ctx.author.roles):
                if (warid == None) or (opponent1 == None) or (replace2 == None) :
                    em = discord.Embed(
                        title = "Help 🛠️",
                        description = '**d!swap warid [playerahead] [playerbehind]**',
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
                            "enemymembers": 1,
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
                        enemymembers = war_data['enemymembers']
                        enemyscore = war_data['enemyplayerscore']
                        formats = war_data['wartype']


                        if self.faction.count_documents({"_id": warid, "enemymembers": opponent1.id,}, limit = 1):

                            actualenemy = []
                            for i in enemymembers:
                                actualenemy.append(i)
                            indexenemy = actualenemy.index(opponent1.id)
                            actualenemy = war_data["enemymembers"]
                            actualenemy[indexenemy] = replace2.id

                            index2enemy = actualenemy.index(replace2.id)
                            actualenemy[index2enemy] = opponent1.id


                            self.faction.update_one({"_id":warid}, {"$set": {"enemymembers": actualenemy}})
                            await ctx.send("Swapped!")
                        else:

                            actualenemy = []
                            for i in allymembers:
                                actualenemy.append(i)
                            indexenemy = actualenemy.index(opponent1.id)
                            actualenemy = war_data["allymembers"]
                            actualenemy[indexenemy] = replace2.id
                            
                            index2enemy = actualenemy.index(replace2.id)
                            actualenemy[index2enemy]


                            self.faction.update_one({"_id":warid}, {"$set": {"allymembers": actualenemy}})      
                            await ctx.send("Swapped!")                      

                    else:                       
                        await ctx.send(f"Incorrect War ID.")
            else:
                await ctx.send("Admins only.")
        else:
            await ctx.send("Register first.")              
    




    @commands.command(name='addwins')
    async def addwins_command(self,ctx, warid = None, number :int = None, clanname : str = None):
        guild = self.bot.get_guild(774883579472904222)
        role = guild.get_role(786448967172882442)
        role2 = guild.get_role(1090438349455622204)
        role3 = guild.get_role(781452019578961921)
        if (role in ctx.author.roles) or (role2 in ctx.author.roles) or (role3 in ctx.author.roles):
            if (warid == None) or (number == None) or (clanname == None):
                em = discord.Embed(
                    title = "Help 🛠️",
                    description = '**d!addwins [War ID] [no.]**',
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
                            if clanname is None:
                                pass
                            else:
                                clanname = clanname.replace("’", "'")
                            allycheck = list(self.faction.find( {"_id": warid}, {"_id": 0, "teamone": 1}))
                            faction_name = allycheck[0]['teamone']
                            enemycheck = list(self.faction.find( {"_id": warid}, {"_id": 0, "teamtwo": 1}))
                            efaction_name = enemycheck[0]['teamtwo']    
                            if clanname == faction_name:                                
                                self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": {number}}})
                                await ctx.send(f"{number} War wins added to {clanname}")
                            elif clanname == efaction_name:
                                self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": {number}}})
                                await ctx.send(f"{number} War wins added to {clanname}")
                            else:
                                await ctx.send("Incorrect clan name.")

                            
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


    @commands.command(name='wars')
    async def warsss(self,ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

            if user_ban_list:
                await ctx.send('You are banned from the bot.')
                return
            
            faction_score = list(self.faction.aggregate([{"$sort" : {"time" : -1}}]))
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
            title = f"Current ongoing wars",
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
                crudescore6 = int(scorelist[5])
            
                
                date1 = datetime.datetime.fromtimestamp(crudescore6)
                t = datetime.datetime.now(timezone.utc)
                timenew = int(time.mktime(t.timetuple()) + t.microsecond / 1E6)
                date2 = datetime.datetime.fromtimestamp(timenew)   
                actualtime = "%dd %dh %dm %ds" % dhms_from_seconds(date_diff_in_seconds(date2, date1))  

                wars.add_field(name = f'`{serial}#` {crudescore1} {crudescore2} {crudescore4} :crossed_swords:  {crudescore3} {crudescore5}', value = f'Ends in {actualtime}', inline=False)
                serial += 1
            await ctx.send(embed = wars)
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')






    @commands.group(name = 'log', aliases = ['l'], invoke_without_command = True)
    async def log_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            em1 = discord.Embed(
                title = 'Ranked',
                description = 'Commands related to logging battles:',
                colour = color
            )

            em1.add_field(name = 'd!log rare [mention] [score]', value = 'Log a rare ranked battles match.',inline=False)

            em1.add_field(name = 'd!log com [mention] [score]', value = 'Log a common ranked battles match.',inline=False)

            em1.add_field(name = 'd!log casual [mention] [score]', value = 'Log a casual battles match.',inline=False)

            em1.add_field(name = 'd!log war [mention]', value = 'Log a clan war match.',inline=False)

            em1.add_field(name = 'd!log blade [mention]', value = 'Log a clan war match (ONLY FOR BLADES).',inline=False)


            await ctx.send(embed = em1)
        
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')


    @log_command.command(name = 'rare')
    async def rare_log_command(self, ctx, member : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        score = '1'
        if registered_check:
            if (member is None) or (score is None):
                em = discord.Embed(
                    title = 'Rank Log',
                    description = '**Log your ranked battles.**\n\nd!log rare [mention] [score]',
                    colour = color
                )

                await ctx.send(embed = em)
            
            else:
                member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                if member_registered:
                    author_id = ctx.author.id

                    member_id = member.id

                    guild_id = ctx.guild.id

                    users = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', author_id)

                    players = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', member_id)

                    if (users) and (players):
                        winner = int(users[0]['points'])
                        loser = int(players[0]['points'])
                        if winner > loser:
                            diff = int(winner - loser)
                            points = 10 - 10*(diff/1000)
                            points = math.ceil(points)
                            if points < 2:
                                points = 2
                            wpoints = math.ceil(points)
                        else:
                            diff = int(loser - winner)
                            points = 10 + 10*(diff/1000)
                            points = math.ceil(points)
                            if points > 15:
                                points = 15
                            wpoints = math.ceil(points)

                        if winner > loser:
                            diff = int(winner - loser)
                            coins = 3 - 3*(diff/1000)
                            coins = math.ceil(coins)
                            if coins < 2:
                                coins = 2
                        else:
                            diff = int(loser - winner)
                            coins = 4 + 4*(diff/1000)
                            coins = math.ceil(coins)
                            if coins > 7:
                                coins = 7  
                    

                        ranked = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

                        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', author_id)

                        player_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', member_id)

                        user_rank = int(users[0]['rank_value'])

                        player_rank = int(players[0]['rank_value'])

                        ranked_enable = ranked[0]['ranked_enable']

                        ranked_channel = ranked[0]['ranked_channel']

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

                        if ranked_enable == 1:
                            if (not user_ban_list) and (not player_ban_list):
                                if ctx.author.id != member.id:
                                    channelist = [867504450498723850,1089940839960170567, 1089940862500352031,1150446880719900764, 1048286966707396658]
                                    if ctx.channel.id not in channelist:
                                        await ctx.send("This command can only be used in the Ranked Battling channels which are <#867504450498723850> <#1089940839960170567> <#1089940862500352031>")
                                        return
                                    if (users[0]["matches_played"] >= 10) and (players[0]["matches_played"] >= 10):
                                        await ctx.send(f'**Remember that only the winner must send the log request. For this log** {ctx.author.name} **will be considered as the winner.**')
                                        view = ConfirmCancel(member)
                                        await ctx.send(f'{member.mention} click the ✅ if you agree to the score and the winner or click the ❌ to cancel.', view = view)
                                        
                                        await view.wait()

                                        if view.value is True:

                                            a = [2,3,5]
                                            m = [2,5]               
                                            await quests(self,ctx, a, author_id, m,member_id)

                                            ranked_battle_embed = discord.Embed(
                                                title = 'Ranked Battles',
                                                description = f'{ctx.message.author.mention} beat {member.mention} in {ctx.message.channel.mention}\n Score: {score}',
                                                colour = color
                                            )

                                            ranking_channel = self.bot.get_channel(ranked_channel)

                                            await ranking_channel.send(embed = ranked_battle_embed)
                                            if  (users[0]['matches_played'] < 10) or (players[0]['matches_played'] < 10):
                                                pass
                                            else:
                                                await ctx.reply(f'{ctx.author.name} won **+{wpoints}** points and {member.name} lost **-{points}** points.', mention_author = False)

                                            #Updating score of both players depending on ranked or unranked

                                            await self.bot.db.execute(f'UPDATE rank_system SET weekly = weekly + {wpoints}, daily = daily + {wpoints} WHERE player_id = $1', author_id)
                                            await self.bot.db.execute(f'UPDATE rank_system SET weekly = weekly - {points}, daily = daily - {points} WHERE player_id = $1', member_id)                                                    

                                            if (users[0]['matches_played'] >= 10) and (players[0]['matches_played'] >= 10):

                                                await self.bot.db.execute(f'UPDATE rank_system SET matches_played = matches_played + 1, points = points + {wpoints}, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute(f'UPDATE rank_system SET matches_played = matches_played + 1, points = points - {points} WHERE player_id = $1', member_id)



                                            elif (users[0]['matches_played'] < 10) and (players[0]['matches_played'] >= 10):
                                            
                                                await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 9 WHERE player_id = $1', member_id)

                                            elif (users[0]['matches_played'] >= 10) and (players[0]['matches_played'] < 10):

                                                await self.bot.db.execute(f'UPDATE rank_system SET matches_played = matches_played + 1, points = points + {wpoints}, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute(f'UPDATE rank_system SET matches_played = matches_played + 1, points = points - {points} WHERE player_id = $1', member_id)

                                            elif (users[0]['matches_played'] < 10) and (players[0]['matches_played'] < 10):

                                                await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', member_id)

                                            #Setting streak
                                            await self.bot.db.execute('UPDATE rank_system SET streak = streak + 1 WHERE player_id = $1', author_id)
                                            await self.bot.db.execute('UPDATE rank_system SET streak = 0 WHERE player_id = $1', member_id)

                                            #Preventing score from being negative

                                            users_updated = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', author_id)
                                            players_updated = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', member_id)

                                            user_points = int(users_updated[0]['points'])
                                            player_points = int(players_updated[0]['points'])

                                            if int(user_points) < 0:
                                                await self.bot.db.execute('UPDATE rank_system SET points = 0 WHERE player_id = $1', author_id)

                                            if int(player_points) < 0:
                                                await self.bot.db.execute('UPDATE rank_system SET points = 0 WHERE player_id = $1', member_id)

                                            #Awarding Achieve for ctx
                                            flists = str(registered_check[0]['achievements'])
                                            new_admins = ''
                                            admins_list = self.listing(flists)
                                            
                                            for p,admin in enumerate(admins_list):
                                        
                                                if p == 0:
                                                    if int(admin) == 249:
                                                        admins_list[1] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Play 250 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 499:
                                                        admins_list[1] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Play 500 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 999:
                                                        admins_list[1] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Play 1000 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + 1
                                                    new_admins += str(admin)
                                                elif p == 2:
                                                    if int(admin) == 99:
                                                        admins_list[3] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Win 100 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 299:
                                                        admins_list[3] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Win 300 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 699:
                                                        admins_list[3] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Win 700 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + 1
                                                    new_admins +=  f' {admin}'
                                                elif p == 4:
                                                    if (int(admin) > 999) and (int(admins_list[5]) == 0):
                                                        admins_list[5] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Get 1000 Points ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif (int(admin) > 2499) and (int(admins_list[5]) == 1):
                                                        admins_list[5] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Get 2500 Points ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif (int(admin) > 4999) and (int(admins_list[5]) == 2):
                                                        admins_list[5] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Get 5000 Points ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + points
                                                    new_admins += f' {admin}'
                                                elif p == 6:
                                                    if int(admin) < users_updated[0]['streak']:
                                                        if int(admin) == 9:
                                                            admins_list[7] = 1
                                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                            await ctx.send("**Bronze Achievement Completed! ✦ Get a Streak of 10 ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                        elif int(admin) == 14:
                                                            admins_list[7] = 2
                                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                            await ctx.send("**Silver Achievement Completed! ✦✦ Get a Streak of 15 ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                        elif int(admin) == 24:
                                                            admins_list[7] = 3
                                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                            await ctx.send("**Gold Achievement Completed! ✦✦✦ Get a Streak of 25 ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")  
                                                        admin = users_updated[0]['streak']
                                                        new_admins +=  f' {admin}' 
                                                    else:
                                                        new_admins +=  f' {admin}'                                                        
                                                else:
                                                    new_admins += f' {admin}'  
                                            
                                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, ctx.author.id)                                          

                                            #Awarding Achieve for member
                                            flists = str(member_registered[0]['achievements'])
                                            new_admins = ''
                                            admins_list = self.listing(flists)
                                            for p,admin in enumerate(admins_list):
                                        
                                                if p == 0:
                                                    if int(admin) == 249:
                                                        admins_list[1] = 1
                                                        
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  member.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Play 250 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 499:
                                                        admins_list[1] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  member.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Play 500 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 999:
                                                        admins_list[1] = 3
                                                        
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  member.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Play 1000 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + 1
                                                    new_admins += str(admin)                                                       
                                                else:
                                                    new_admins += f' {admin}'  

                                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, member.id)   
                                            
                                            if players_updated[0]['streak'] < 0:
                                                await self.bot.db.execute('UPDATE rank_system SET streak = 0 WHERE player_id = $1', member_id)
                
                                            #Awarding borders/avaborder
                                            stat = ['banners','borders', 'avaborders']
                                            g = 0
                                            d = 0
                                            if users_updated[0]['points'] >= 0:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        count = 'title_count'
                                                        s = ''
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'bronze2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'bronze2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'bronze2'
                                                        count = 'banner_count'
                                                        
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await ctx.send("Awarded **Bronze2** Banner, Border, AvaBorder!")
                                                        g = g + 1
                                                        brewards = ['bronze2', 'bronze2', 'bronze2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"

                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            
                                            g = 0
                                            d = 0
                                            if users_updated[0]['points'] >= 250:
                                                for i in stat:
                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'silver2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'silver2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'silver2'
                                                        count = 'banner_count'

                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await ctx.send("Awarded **Silver2** Banner, Border, AvaBorder!")
                                                        g = g + 1
                                                        brewards = ['silver2', 'silver2', 'silver2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            g = 0
                                            d = 0                                                                
                                            if users_updated[0]['points'] >= 500:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'gold2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'gold2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'gold2'
                                                        count = 'banner_count'
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1', ctx.author.id)
                                                            await ctx.send("Awarded **10**dc and **Gold2** Banner, Border, AvaBorder!")
                                                        g = g + 1
                                                        brewards = ['gold2', 'gold2', 'gold2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            g = 0
                                            d = 0                                                               
                                            if users_updated[0]['points'] >= 750:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'platinum2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'platinum2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'platinum2'
                                                        count = 'banner_count'
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1', ctx.author.id)
                                                            await ctx.send("Awarded **25**dc and **Platinum** Banner, Border, AvaBorder!")
                                                        g = g + 1
                                                        brewards = ['platinum2', 'platinum2', 'platinum2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            g = 0
                                            d = 0
                                            if users_updated[0]['points'] >= 1250:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'dominant2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'dominant2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'dominant2'
                                                        count = 'banner_count'
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1', ctx.author.id)
                                                            await ctx.send("Awarded **50**dc and **Dominant** Banner, Border, AvaBorder!")
                                                        g = g + 1
                                                        brewards = ['dominant2', 'dominant2', 'dominant2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)

                                                        


                                            #Updating rank of winner

                                            if (int(user_points) >= 0) and (int(user_points) <= 83):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze1, bronze_value, author_id)

                                            elif (int(user_points) >= 84) and (int(user_points) <= 167):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze2, bronze_value, author_id)

                                            elif (int(user_points) >= 168) and (int(user_points) <= 250):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze3, bronze_value, author_id)

                                            elif (int(user_points) >= 251) and (int(user_points) <= 333):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver1, silver_value, author_id)

                                            elif (int(user_points) >= 334) and (int(user_points) <= 416):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver2, silver_value, author_id)

                                            elif (int(user_points) >= 417) and (int(user_points) <= 500):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver3, silver_value, author_id)

                                            elif (int(user_points) >= 501) and (int(user_points) <= 583):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold1, gold_value, author_id)

                                            elif (int(user_points) >= 584) and (int(user_points) <= 667):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold2, gold_value, author_id)

                                            elif (int(user_points) >= 668) and (int(user_points) <= 750):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold3, gold_value, author_id)

                                            elif (int(user_points) >= 751) and (int(user_points) <= 833):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum1, platinum_value, author_id)

                                            elif (int(user_points) >= 834) and (int(user_points) <= 916):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum2, platinum_value, author_id)

                                            elif (int(user_points) >= 917) and (int(user_points) <= 1249):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum3, platinum_value, author_id)

                                            elif int(user_points) >= 1250:
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', dominant, dominant_value, author_id)

                                            #Updating rank of loser

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

                                            #Giving wishes to 100+ points
                                        
                                            (users_updated[0]['streak'])
                                            if users_updated[0]['streak'] > 2:
                                                wishes = math.ceil((users_updated[0]['streak']/2)) - 1
                                                coins = wishes + coins
                                                winter = round(coins*0.5)
                                                coins = winter + coins

                                                if coins > 10:
                                                    coins = 10
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {coins} WHERE player_id = $1',  ctx.author.id)
                                                await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces + 1 WHERE player_id = $1', member.id)
                                                
                                                await ctx.send(f"Coins rewarded **+{coins}** to {ctx.author.name} | Coins rewarded **+1** to {member.name}\n**WINTER FEST +{winter}**")

                                            else:
                                                winter = round(coins*0.5)
                                                coins = winter + coins

                                                await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces + 1 WHERE player_id = $1', member.id)
                                                
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {coins} WHERE player_id = $1', ctx.author.id)
                                                await ctx.send(f"Coins rewarded **+{coins}** to {ctx.author.name} | Coins rewarded **+1** to {member.name}\n**WINTER FEST +{winter}**")
                                        elif view.value is False:
                                            await ctx.send('Cancelled.')
                                        else:
                                            await ctx.send('Timed Out')    

                                
                                             
                                    elif (users[0]["matches_played"] < 10) or (players[0]["matches_played"] < 10):
                                    
                                        await ctx.send(f'**Remember that only the winner must send the log request. For this log** {ctx.author.name} **will be considered as the winner.**')
                                        view = ConfirmCancel(member)
                                        await ctx.send(f'{member.mention} click the ✅ if you agree to the score and the winner or click the ❌ to cancel.', view = view)
                                        
                                        await view.wait()

                                        if view.value is True:
                                            a = [2,3,5]
                                            m = [2,5]               
                                            await quests(self,ctx, a, author_id, m,member_id)

                                            ranked_battle_embed = discord.Embed(
                                                title = 'Ranked Battles',
                                                description = f'{ctx.message.author.mention} beat {member.mention} in {ctx.message.channel.mention}\n Score: {score}',
                                                colour = color
                                            )

                                            ranking_channel = self.bot.get_channel(ranked_channel)

                                            await ranking_channel.send(embed = ranked_battle_embed)
                                            await ctx.reply('Logged succesfully.', mention_author = False)

                                            if  (users[0]['matches_played'] < 10) or (players[0]['matches_played'] < 10):
                                                pass
                                            else:
                                                await ctx.reply(f'{ctx.author.name} won **+{wpoints}** points and {member.name} lost **-{points}** points.', mention_author = False)                                                    

                                            #Updating score of both players depending on ranked or unranked
                                            await self.bot.db.execute(f'UPDATE rank_system SET weekly = weekly + {wpoints}, daily = daily + {wpoints} WHERE player_id = $1', author_id)
                                            await self.bot.db.execute(f'UPDATE rank_system SET weekly = weekly - {points}, daily = daily - {points} WHERE player_id = $1', member_id)
                                            if (users[0]['matches_played'] >= 10) and (players[0]['matches_played'] >= 10):

                                                await self.bot.db.execute(f'UPDATE rank_system SET matches_played = matches_played + 1, points = points + {wpoints}, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute(f'UPDATE rank_system SET matches_played = matches_played + 1, points = points - {points} WHERE player_id = $1', member_id)
                                                    

                                            elif (users[0]['matches_played'] < 10) and (players[0]['matches_played'] >= 10):

                                                await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 8 WHERE player_id = $1', member_id)

                                            elif (users[0]['matches_played'] >= 10) and (players[0]['matches_played'] < 10):

                                                await self.bot.db.execute(f'UPDATE rank_system SET matches_played = matches_played + 1, points = points + {wpoints}, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute(f'UPDATE rank_system SET matches_played = matches_played + 1, points = points - {points} WHERE player_id = $1', member_id)

                                            elif (users[0]['matches_played'] < 10) and (players[0]['matches_played'] < 10):

                                                await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', member_id)

                                            #Setting streak
                                            await self.bot.db.execute('UPDATE rank_system SET streak = streak + 1 WHERE player_id = $1', author_id)
                                            await self.bot.db.execute('UPDATE rank_system SET streak = 0 WHERE player_id = $1', member_id)

                                            #Preventing score from being negative

                                            users_updated = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', author_id)
                                            players_updated = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', member_id)

                                            user_points = int(users_updated[0]['points'])
                                            player_points = int(players_updated[0]['points'])

                                            if int(user_points) < 0:
                                                await self.bot.db.execute('UPDATE rank_system SET points = 0 WHERE player_id = $1', author_id)

                                            if int(player_points) < 0:
                                                await self.bot.db.execute('UPDATE rank_system SET points = 0 WHERE player_id = $1', member_id)

                                            #Awarding Achieve for ctx
                                            flists = str(registered_check[0]['achievements'])
                                            new_admins = ''
                                            admins_list = self.listing(flists)
                                           
                                            for p,admin in enumerate(admins_list):
                                        
                                                if p == 0:
                                                    if int(admin) == 249:
                                                        admins_list[1] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Play 250 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 499:
                                                        admins_list[1] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Play 500 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 999:
                                                        admins_list[1] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Play 1000 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + 1
                                                    new_admins += str(admin)
                                                elif p == 2:
                                                    if int(admin) == 99:
                                                        admins_list[3] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Win 100 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 299:
                                                        admins_list[3] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Win 300 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 699:
                                                        admins_list[3] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Win 700 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + 1
                                                    new_admins +=  f' {admin}'
                                                elif p == 4:
                                                    if (int(admin) > 999) and (int(admins_list[5]) == 0):
                                                        admins_list[5] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Get 1000 Points ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif (int(admin) > 2499) and (int(admins_list[5]) == 1):
                                                        admins_list[5] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Get 2500 Points ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif (int(admin) > 4999) and (int(admins_list[5]) == 2):
                                                        admins_list[5] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Get 5000 Points ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + points
                                                    new_admins += f' {admin}'
                                                elif p == 6:
                                                    if int(admin) < users_updated[0]['streak']:
                                                        if int(admin) == 9:
                                                            admins_list[7] = 1
                                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                            await ctx.send("**Bronze Achievement Completed! ✦ Get a Streak of 10 ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                        elif int(admin) == 14:
                                                            admins_list[7] = 2
                                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                            await ctx.send("**Silver Achievement Completed! ✦✦ Get a Streak of 15 ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                        elif int(admin) == 24:
                                                            admins_list[7] = 3
                                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                            await ctx.send("**Gold Achievement Completed! ✦✦✦ Get a Streak of 25 ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")  
                                                        admin = users_updated[0]['streak']
                                                        new_admins +=  f' {admin}' 
                                                    else:
                                                        new_admins +=  f' {admin}'                                                          
                                                else:
                                                    new_admins += f' {admin}'  
                                            
                                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, ctx.author.id)                                          

                                            #Awarding Achieve for member
                                            flists = str(member_registered[0]['achievements'])
                                            new_admins = ''
                                            admins_list = self.listing(flists)
                                            for p,admin in enumerate(admins_list):
                                        
                                                if p == 0:
                                                    if int(admin) == 249:
                                                        admins_list[1] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  member.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Play 250 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 499:
                                                        admins_list[1] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  member.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Play 500 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 999:
                                                        admins_list[1] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  member.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Play 1000 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + 1
                                                    new_admins += str(admin)                                                       
                                                else:
                                                    new_admins += f' {admin}'  

                                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, member.id)   
                                            
                                            if players_updated[0]['streak'] < 0:
                                                await self.bot.db.execute('UPDATE rank_system SET streak = 0 WHERE player_id = $1', member_id)

                                            #Awarding borders/avaborder
                                            stat = ['banners','borders', 'avaborders']
                                            g = 0
                                            d = 0
                                            if users_updated[0]['points'] >= 0:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        count = 'title_count'
                                                        s = ''
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'bronze2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'bronze2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'bronze2'
                                                        count = 'banner_count'
                                                        
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await ctx.send("Awarded **Bronze2** Banner, Border, AvaBorder!")
                                                            
                                                        g = g + 1
                                                        brewards = ['bronze2', 'bronze2', 'bronze2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            g = 0
                                            d = 0
                                            if users_updated[0]['points'] >= 250:
                                                for i in stat:
                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'silver2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'silver2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'silver2'
                                                        count = 'banner_count'

                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await ctx.send("Awarded **Silver2** Banner, Border, AvaBorder!")
                                                            
                                                        g = g + 1
                                                        brewards = ['silver2', 'silver2', 'silver2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            g = 0
                                            d = 0                                                                    
                                            if users_updated[0]['points'] >= 500:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'gold2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'gold2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'gold2'
                                                        count = 'banner_count'
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1', ctx.author.id)
                                                            await ctx.send("Awarded **10**dc and **Gold2** Banner, Border, AvaBorder!")                                                                
                                                        g = g + 1
                                                        brewards = ['gold2', 'gold2', 'gold2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            g = 0
                                            d = 0                                                                    
                                            if users_updated[0]['points'] >= 750:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'platinum2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'platinum2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'platinum2'
                                                        count = 'banner_count'
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1', ctx.author.id)
                                                            await ctx.send("Awarded **25**dc and **Platinum2** Banner, Border, AvaBorder!")                                                                
                                                        g = g + 1
                                                        brewards = ['platinum2', 'platinum2', 'platinum2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            g = 0
                                            d = 0
                                            if users_updated[0]['points'] >= 1250:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'dominant2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'dominant2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'dominant2'
                                                        count = 'banner_count'
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1', ctx.author.id)
                                                            await ctx.send("Awarded **50**dc and **Dominant2** Banner, Border, AvaBorder!")                                                                
                                                        g = g + 1
                                                        brewards = ['dominant2', 'dominant2', 'dominant2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)


                                                    

                                                                                                            
                                            #Updating rank of winner

                                            if (int(user_points) >= 0) and (int(user_points) <= 83):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze1, bronze_value, author_id)

                                            elif (int(user_points) >= 84) and (int(user_points) <= 167):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze2, bronze_value, author_id)

                                            elif (int(user_points) >= 168) and (int(user_points) <= 250):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze3, bronze_value, author_id)

                                            elif (int(user_points) >= 251) and (int(user_points) <= 333):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver1, silver_value, author_id)

                                            elif (int(user_points) >= 334) and (int(user_points) <= 416):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver2, silver_value, author_id)

                                            elif (int(user_points) >= 417) and (int(user_points) <= 500):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver3, silver_value, author_id)

                                            elif (int(user_points) >= 501) and (int(user_points) <= 583):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold1, gold_value, author_id)

                                            elif (int(user_points) >= 584) and (int(user_points) <= 667):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold2, gold_value, author_id)

                                            elif (int(user_points) >= 668) and (int(user_points) <= 750):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold3, gold_value, author_id)

                                            elif (int(user_points) >= 751) and (int(user_points) <= 833):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum1, platinum_value, author_id)

                                            elif (int(user_points) >= 834) and (int(user_points) <= 916):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum2, platinum_value, author_id)

                                            elif (int(user_points) >= 917) and (int(user_points) <= 1249):
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum3, platinum_value, author_id)

                                            elif int(user_points) >= 1250:
                                                await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', dominant, dominant_value, author_id)

                                            #Updating rank of loser

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

                                            #Giving coins
                                            (users_updated[0]['streak'])
                                            if users_updated[0]['streak'] > 2:
                                                wishes = math.ceil((users_updated[0]['streak']/2)) - 1
                                            
                                                coins = wishes + coins
                                                winter = round(coins*0.5)
                                                coins = winter + coins

                                                if coins > 10:
                                                    coins = 10

                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {coins} WHERE player_id = $1',  ctx.author.id)
                                                await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces + 1 WHERE player_id = $1', member.id)
                                                
                                                await ctx.send(f"Coins rewarded **+{coins}** to {ctx.author.name} | Coins rewarded **+1** to {member.name}\n**WINTER FEST +{winter}**")

                                            else:

                                                winter = round(coins*0.5)
                                                coins = winter + coins
                                                await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces + 1 WHERE player_id = $1', member.id)
                                                
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {coins} WHERE player_id = $1', ctx.author.id)
                                                await ctx.send(f"Coins rewarded **+{coins}** to {ctx.author.name} | Coins rewarded **+1** to {member.name}\n**WINTER FEST +{winter}**")
                                        elif view.value is False:
                                            await ctx.send('Cancelled.')
                                        else:
                                            await ctx.send('Timed Out')    
                                    else:
                                        await ctx.send('Unkown error.')

                                elif ctx.author.id == member.id:
                                    await ctx.send('You cannot log with yourself!')

                            elif not user_ban_list and player_ban_list:
                                await ctx.send('That person is banned from ranked battles!')

                            elif user_ban_list and not player_ban_list:
                                await ctx.send('You are banned from ranked battles.')

                            elif user_ban_list and player_ban_list:
                                await ctx.send('Both of you are banned from ranked battles.')

                        elif ranked_enable == 0:
                            await ctx.send('Ranked battles are currently not enabled.')

                    else:
                        await ctx.send('One of you have not registered yet!')

                else:
                    await ctx.send('That person has not registered yet! Use `d!start` to register.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')


    @log_command.command(name = 'com')
    async def com_log_command(self, ctx, member : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        score = '1'
        if registered_check:
            if (member is None) or (score is None):
                em = discord.Embed(
                    title = 'Rank Log',
                    description = '**Log your ranked battles.**\n\nd!log com [mention] [score]',
                    colour = color
                )

                await ctx.send(embed = em)
            
            else:
                member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                if member_registered:
                    author_id = ctx.author.id

                    member_id = member.id

                    guild_id = ctx.guild.id

                    users = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', author_id)

                    players = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', member_id)

                    if (users) and (players):
                        winner = int(users[0]['points'])
                        loser = int(players[0]['points'])
                        if winner > loser:
                            diff = int(winner - loser)
                            points = 10 - 10*(diff/1000)
                            points = math.ceil(points)
                            if points < 2:
                                points = 2
                            wpoints = math.ceil(points)
                        else:
                            diff = int(loser - winner)
                            points = 10 + 10*(diff/1000)
                            points = math.ceil(points)
                            if points > 15:
                                points = 15
                            wpoints = math.ceil(points)

                        if winner > loser:
                            diff = int(winner - loser)
                            coins = 4 - 4*(diff/1000)
                            coins = math.ceil(coins)
                            if coins < 2:
                                coins = 2
                        else:
                            diff = int(loser - winner)
                            coins = 4 + 4*(diff/1000)
                            coins = math.ceil(coins)
                            if coins > 7:
                                coins = 7  
                        ranked = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

                        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', author_id)

                        player_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', member_id)

                        user_rank = int(users[0]['rank_value'])

                        player_rank = int(players[0]['rank_value'])

                        ranked_enable = ranked[0]['ranked_enable']

                        ranked_channel = ranked[0]['ranked_channel']

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

                        if ranked_enable == 1:
                            if (not user_ban_list) and (not player_ban_list):
                                if ctx.author.id != member.id:
                                    channelist = [867504450498723850,1089940839960170567, 1089940862500352031, 1150446880719900764, 1048286966707396658]
                                    if ctx.channel.id not in channelist:
                                        await ctx.send("This command can only be used in the Ranked Battling channels which are <#867504450498723850> <#1089940839960170567> <#1089940862500352031>")
                                        return                                    
                                    if (users[0]["matches_played"] >= 10) and (players[0]["matches_played"] >= 10):
                                        await ctx.send(f'**Remember that only the winner must send the log request. For this log** {ctx.author.name} **will be considered as the winner.**')
                                        view = ConfirmCancel(member)
                                        await ctx.send(f'{member.mention} click the ✅ if you agree to the score and the winner or click the ❌ to cancel.', view = view)
                                        
                                        await view.wait()

                                        if view.value is True:
                                            a = [2,3,4]
                                            m = [2,4]               
                                            await quests(self,ctx, a, author_id, m,member_id)

                                            ranked_battle_embed = discord.Embed(
                                                title = 'Ranked Battles',
                                                description = f'{ctx.message.author.mention} beat {member.mention} in {ctx.message.channel.mention}\n Score: {score}',
                                                colour = color
                                            )

                                            ranking_channel = self.bot.get_channel(ranked_channel)

                                            await ranking_channel.send(embed = ranked_battle_embed)
                                            if  (users[0]['matches_played'] < 10) or (players[0]['matches_played'] < 10):
                                                pass
                                            else:
                                                await ctx.reply(f'{ctx.author.name} won **+{wpoints}** points and {member.name} lost **-{points}** points.', mention_author = False)

                                            #Updating score of both players depending on ranked or unranked

                                            await self.bot.db.execute(f'UPDATE common_system SET weekly = weekly + {wpoints}, daily = daily + {wpoints} WHERE player_id = $1', author_id)
                                            await self.bot.db.execute(f'UPDATE common_system SET weekly = weekly - {points}, daily = daily - {points} WHERE player_id = $1', member_id)                                                    

                                            if (users[0]['matches_played'] >= 10) and (players[0]['matches_played'] >= 10):

                                                await self.bot.db.execute(f'UPDATE common_system SET matches_played = matches_played + 1, points = points + {wpoints}, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute(f'UPDATE common_system SET matches_played = matches_played + 1, points = points - {points} WHERE player_id = $1', member_id)

                                            elif (users[0]['matches_played'] < 10) and (players[0]['matches_played'] >= 10):

                                                await self.bot.db.execute('UPDATE common_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute('UPDATE common_system SET matches_played = matches_played + 1, points = points - 9 WHERE player_id = $1', member_id)

                                            elif (users[0]['matches_played'] >= 10) and (players[0]['matches_played'] < 10):
                                                                            


                                                await self.bot.db.execute(f'UPDATE common_system SET matches_played = matches_played + 1, points = points + {wpoints}, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute(f'UPDATE common_system SET matches_played = matches_played + 1, points = points - {points} WHERE player_id = $1', member_id)

                                            elif (users[0]['matches_played'] < 10) and (players[0]['matches_played'] < 10):

                                                await self.bot.db.execute('UPDATE common_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute('UPDATE common_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', member_id)

                                            #Setting streak
                                            await self.bot.db.execute('UPDATE common_system SET streak = streak + 1 WHERE player_id = $1', author_id)
                                            await self.bot.db.execute('UPDATE common_system SET streak = 0 WHERE player_id = $1', member_id)

                                            #Preventing score from being negative

                                            users_updated = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', author_id)
                                            players_updated = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', member_id)

                                            user_points = int(users_updated[0]['points'])
                                            player_points = int(players_updated[0]['points'])

                                            if int(user_points) < 0:
                                                await self.bot.db.execute('UPDATE common_system SET points = 0 WHERE player_id = $1', author_id)

                                            if int(player_points) < 0:
                                                await self.bot.db.execute('UPDATE common_system SET points = 0 WHERE player_id = $1', member_id)

                                            #Awarding Achieve for ctx
                                            flists = str(registered_check[0]['achievements'])
                                            new_admins = ''
                                            admins_list = self.listing(flists)

                                            
                                            for p,admin in enumerate(admins_list):
                                        
                                                if p == 0:
                                                    if int(admin) == 249:
                                                        admins_list[1] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Play 250 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 499:
                                                        admins_list[1] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Play 500 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 999:
                                                        admins_list[1] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Play 1000 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + 1
                                                    new_admins += str(admin)
                                                elif p == 2:
                                                    if int(admin) == 99:
                                                        admins_list[3] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Win 100 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 299:
                                                        admins_list[3] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Win 300 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 699:
                                                        admins_list[3] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Win 700 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + 1
                                                    new_admins +=  f' {admin}'
                                                elif p == 4:
                                                    if (int(admin) > 999) and (int(admins_list[5]) == 0):
                                                        admins_list[5] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Get 1000 Points ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif (int(admin) > 2499) and (int(admins_list[5]) == 1):
                                                        admins_list[5] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Get 2500 Points ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif (int(admin) > 4999) and (int(admins_list[5]) == 2):
                                                        admins_list[5] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Get 5000 Points ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + points
                                                    new_admins += f' {admin}'
                                                elif p == 6:
                                                    if int(admin) < users_updated[0]['streak']:
                                                        if int(admin) == 9:
                                                            admins_list[7] = 1
                                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                            await ctx.send("**Bronze Achievement Completed! ✦ Get a Streak of 10 ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                        elif int(admin) == 14:
                                                            admins_list[7] = 2
                                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                            await ctx.send("**Silver Achievement Completed! ✦✦ Get a Streak of 15 ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                        elif int(admin) == 24:
                                                            admins_list[7] = 3
                                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                            await ctx.send("**Gold Achievement Completed! ✦✦✦ Get a Streak of 25 ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")  
                                                        admin = users_updated[0]['streak']
                                                        new_admins +=  f' {admin}'
                                                    else:
                                                        new_admins +=  f' {admin}'                                                           
                                                else:
                                                    new_admins += f' {admin}'  
                                            
                                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, ctx.author.id)                                          

                                            #Awarding Achieve for member
                                            flists = str(member_registered[0]['achievements'])
                                            new_admins = ''
                                            admins_list = self.listing(flists)
                                            for p,admin in enumerate(admins_list):
                                        
                                                if p == 0:
                                                    if int(admin) == 249:
                                                        admins_list[1] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  member.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Play 250 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 499:
                                                        admins_list[1] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  member.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Play 500 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 999:
                                                        admins_list[1] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  member.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Play 1000 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + 1
                                                    new_admins += str(admin)                                                       
                                                else:
                                                    new_admins += f' {admin}'  

                                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, member.id)   
                                            
                                            if players_updated[0]['streak'] < 0:
                                                await self.bot.db.execute('UPDATE common_system SET streak = 0 WHERE player_id = $1', member_id)
                
                


                                            #Awarding borders/avaborder
                                            stat = ['banners','borders', 'avaborders']
                                            g = 0
                                            d = 0
                                            if users_updated[0]['points'] >= 0:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        count = 'title_count'
                                                        s = ''
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'bronze2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'bronze2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'bronze2'
                                                        count = 'banner_count'
                                                        
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await ctx.send(f"{ctx.author.mention} ✨ Awarded **Bronze2** Banner, Border, AvaBorder!")                                                              
                                                        g = g + 1
                                                        brewards = ['bronze2', 'bronze2', 'bronze2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            
                                            g = 0
                                            d = 0
                                            if users_updated[0]['points'] >= 250:
                                                for i in stat:
                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'silver2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'silver2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'silver2'
                                                        count = 'banner_count'

                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await ctx.send(f"{ctx.author.mention} ✨ Awarded **Silver2** Banner, Border, AvaBorder!")
                                                        g = g + 1
                                                        brewards = ['silver2', 'silver2', 'silver2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            g = 0
                                            d = 0                                                                
                                            if users_updated[0]['points'] >= 500:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'gold2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'gold2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'gold2'
                                                        count = 'banner_count'
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1', ctx.author.id)
                                                            await ctx.send(f"{ctx.author.mention} ✨ Awarded **10**dc and **Gold** Banner, Border, AvaBorder!")
                                                        g = g + 1
                                                        brewards = ['gold2', 'gold2', 'gold2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            g = 0
                                            d = 0                                                               
                                            if users_updated[0]['points'] >= 750:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'platinum2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'platinum2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'platinum2'
                                                        count = 'banner_count'
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1', ctx.author.id)
                                                            await ctx.send(f"{ctx.author.mention} ✨ Awarded **25**Dc and **Platinum** Banner, Border, AvaBorder!")
                                                        g = g + 1
                                                        brewards = ['platinum2', 'platinum2', 'platinum2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            g = 0
                                            d = 0
                                            if users_updated[0]['points'] >= 1250:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'dominant2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'dominant2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'dominant2'
                                                        count = 'banner_count'
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1', ctx.author.id)
                                                            await ctx.send(f"{ctx.author.mention} ✨ Awarded **50**dc and **Dominant2** Banner, Border, AvaBorder!")
                                                        g = g + 1
                                                        brewards = ['dominant2', 'dominant2', 'dominant2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)

                                                        


                                            #Updating rank of winner

                                            if (int(user_points) >= 0) and (int(user_points) <= 83):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze1, bronze_value, author_id)

                                            elif (int(user_points) >= 84) and (int(user_points) <= 167):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze2, bronze_value, author_id)

                                            elif (int(user_points) >= 168) and (int(user_points) <= 250):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze3, bronze_value, author_id)

                                            elif (int(user_points) >= 251) and (int(user_points) <= 333):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver1, silver_value, author_id)

                                            elif (int(user_points) >= 334) and (int(user_points) <= 416):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver2, silver_value, author_id)

                                            elif (int(user_points) >= 417) and (int(user_points) <= 500):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver3, silver_value, author_id)

                                            elif (int(user_points) >= 501) and (int(user_points) <= 583):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold1, gold_value, author_id)

                                            elif (int(user_points) >= 584) and (int(user_points) <= 667):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold2, gold_value, author_id)

                                            elif (int(user_points) >= 668) and (int(user_points) <= 750):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold3, gold_value, author_id)

                                            elif (int(user_points) >= 751) and (int(user_points) <= 833):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum1, platinum_value, author_id)

                                            elif (int(user_points) >= 834) and (int(user_points) <= 916):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum2, platinum_value, author_id)

                                            elif (int(user_points) >= 917) and (int(user_points) <= 1249):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum3, platinum_value, author_id)

                                            elif int(user_points) >= 1250:
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', dominant, dominant_value, author_id)

                                            #Updating rank of loser

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

                                            #Giving wishes to 100+ points
                                        
                                            (users_updated[0]['streak'])
                                            if users_updated[0]['streak'] > 2:
                                                wishes = math.ceil((users_updated[0]['streak']/2)) - 1
                                                coins = wishes + coins

                                                winter = round(coins*0.5)
                                                coins = winter + coins

                                                if coins > 10:
                                                    coins = 10

                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {coins} WHERE player_id = $1',  ctx.author.id)
                                                await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces + 1 WHERE player_id = $1', member.id)
                                                
                                                await ctx.send(f"Coins rewarded **+{coins}** to {ctx.author.name} | Coins rewarded **+1** to {member.name}\n**WINTER FEST +{winter}**")

                                            else:

                                                winter = round(coins*0.5)
                                                coins = winter + coins

                                                await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces + 1 WHERE player_id = $1', member.id)
                                                
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {coins} WHERE player_id = $1', ctx.author.id)
                                                await ctx.send(f"Coins rewarded **+{coins}** to {ctx.author.name} | Coins rewarded **+1** to {member.name}\n**WINTER FEST +{winter}**")
                                        elif view.value is False:
                                            await ctx.send('Cancelled.')
                                        else:
                                            await ctx.send('Timed Out')    

                                
                                             
                                    elif (users[0]["matches_played"] < 10) or (players[0]["matches_played"] < 10):
                                    
                                        await ctx.send(f'**Remember that only the winner must send the log request. For this log** {ctx.author.name} **will be considered as the winner.**')
                                        view = ConfirmCancel(member)
                                        await ctx.send(f'{member.mention} click the ✅ if you agree to the score and the winner or click the ❌ to cancel.', view = view)
                                        
                                        await view.wait()

                                        if view.value is True:
                                            a = [2,3,4]
                                            m = [2,4]               
                                            await quests(self,ctx, a, author_id, m,member_id)

                                            ranked_battle_embed = discord.Embed(
                                                title = 'Ranked Battles',
                                                description = f'{ctx.message.author.mention} beat {member.mention} in {ctx.message.channel.mention}\n Score: {score}',
                                                colour = color
                                            )

                                            ranking_channel = self.bot.get_channel(ranked_channel)

                                            await ranking_channel.send(embed = ranked_battle_embed)
                                            await ctx.reply('Logged succesfully.', mention_author = False)

                                            if  (users[0]['matches_played'] < 10) or (players[0]['matches_played'] < 10):
                                                pass
                                            else:
                                                await ctx.reply(f'{ctx.author.name} won **+{wpoints}** points and {member.name} lost **-{points}** points.', mention_author = False)                                                    

                                            #Updating score of both players depending on ranked or unranked

                                            await self.bot.db.execute(f'UPDATE common_system SET weekly = weekly + {wpoints}, daily = daily + {wpoints} WHERE player_id = $1', author_id)
                                            await self.bot.db.execute(f'UPDATE common_system SET weekly = weekly - {points}, daily = daily - {points} WHERE player_id = $1', member_id) 

                                            if (users[0]['matches_played'] >= 10) and (players[0]['matches_played'] >= 10):

                                                await self.bot.db.execute(f'UPDATE common_system SET matches_played = matches_played + 1, points = points + {wpoints}, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute(f'UPDATE common_system SET matches_played = matches_played + 1, points = points - {points} WHERE player_id = $1', member_id)

                                            elif (users[0]['matches_played'] < 10) and (players[0]['matches_played'] >= 10):

                                                await self.bot.db.execute('UPDATE common_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute('UPDATE common_system SET matches_played = matches_played + 1, points = points - 8 WHERE player_id = $1', member_id)

                                            elif (users[0]['matches_played'] >= 10) and (players[0]['matches_played'] < 10):

                                                await self.bot.db.execute(f'UPDATE common_system SET matches_played = matches_played + 1, points = points + {wpoints}, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute(f'UPDATE common_system SET matches_played = matches_played + 1, points = points - {points} WHERE player_id = $1', member_id)

                                            elif (users[0]['matches_played'] < 10) and (players[0]['matches_played'] < 10):

                                                await self.bot.db.execute('UPDATE common_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', author_id)
                                                await self.bot.db.execute('UPDATE common_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', member_id)

                                            #Setting streak
                                            await self.bot.db.execute('UPDATE common_system SET streak = streak + 1 WHERE player_id = $1', author_id)
                                            await self.bot.db.execute('UPDATE common_system SET streak = 0 WHERE player_id = $1', member_id)

                                            #Preventing score from being negative

                                            users_updated = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', author_id)
                                            players_updated = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', member_id)

                                            user_points = int(users_updated[0]['points'])
                                            player_points = int(players_updated[0]['points'])

                                            if int(user_points) < 0:
                                                await self.bot.db.execute('UPDATE common_system SET points = 0 WHERE player_id = $1', author_id)

                                            if int(player_points) < 0:
                                                await self.bot.db.execute('UPDATE common_system SET points = 0 WHERE player_id = $1', member_id)
                                            #Awarding Achieve for ctx
                                            flists = str(registered_check[0]['achievements'])
                                            new_admins = ''
                                            admins_list = self.listing(flists)
                                            
                                            for p,admin in enumerate(admins_list):
                                        
                                                if p == 0:
                                                    if int(admin) == 249:
                                                        admins_list[1] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Play 250 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 499:
                                                        admins_list[1] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Play 500 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 999:
                                                        admins_list[1] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Play 1000 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + 1
                                                    new_admins += str(admin)
                                                elif p == 2:
                                                    if int(admin) == 99:
                                                        admins_list[3] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Win 100 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 299:
                                                        admins_list[3] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Win 300 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 699:
                                                        admins_list[3] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Win 700 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + 1
                                                    new_admins +=  f' {admin}'
                                                elif p == 4:
                                                    if (int(admin) > 999) and (int(admins_list[5]) == 0):
                                                        admins_list[5] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Get 1000 Points ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif (int(admin) > 2499) and (int(admins_list[5]) == 1):
                                                        admins_list[5] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Get 2500 Points ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif (int(admin) > 4999) and (int(admins_list[5]) == 2):
                                                        admins_list[5] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Get 5000 Points ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + points
                                                    new_admins += f' {admin}'
                                                elif p == 6:
                                                    if int(admin) < users_updated[0]['streak']:
                                                        if int(admin) == 9:
                                                            admins_list[7] = 1
                                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                            await ctx.send("**Bronze Achievement Completed! ✦ Get a Streak of 10 ✦**\n*10dc rewarded*")
                                                        elif int(admin) == 14:
                                                            admins_list[7] = 2
                                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                            await ctx.send("**Silver Achievement Completed! ✦✦ Get a Streak of 15 ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                        elif int(admin) == 24:
                                                            admins_list[7] = 3
                                                            await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                            await ctx.send("**Gold Achievement Completed! ✦✦✦ Get a Streak of 25 ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")  
                                                        admin = users_updated[0]['streak']
                                                        new_admins +=  f' {admin}'  
                                                    else:
                                                        new_admins +=  f' {admin}'                                                         
                                                else:
                                                    new_admins += f' {admin}'  
                                            
                                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, ctx.author.id)                                          

                                            #Awarding Achieve for member
                                            flists = str(member_registered[0]['achievements'])
                                            new_admins = ''
                                            admins_list = self.listing(flists)
                                            for p,admin in enumerate(admins_list):
                                        
                                                if p == 0:
                                                    if int(admin) == 249:
                                                        admins_list[1] = 1
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  member.id)
                                                        await ctx.send("**Bronze Achievement Completed! ✦ Play 250 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 499:
                                                        admins_list[1] = 2
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  member.id)
                                                        await ctx.send("**Silver Achievement Completed! ✦✦ Play 500 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                                    elif int(admin) == 999:
                                                        admins_list[1] = 3
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  member.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Play 1000 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + 1
                                                    new_admins += str(admin)                                                       
                                                else:
                                                    new_admins += f' {admin}'  

                                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, member.id)   
                                            
                                            if players_updated[0]['streak'] < 0:
                                                await self.bot.db.execute('UPDATE common_system SET streak = 0 WHERE player_id = $1', member_id)
     
                                            #Awarding borders/avaborder 
                                            stat = ['banners','borders', 'avaborders']
                                            g = 0
                                            d = 0
                                            if users_updated[0]['points'] >= 0:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        count = 'title_count'
                                                        s = ''
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'bronze2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'bronze2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'bronze2'
                                                        count = 'banner_count'
                                                        
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await ctx.send(f"{ctx.author.mention} ✨ Awarded **Bronze2** Banner, Border, AvaBorder!")
                                                        g = g + 1
                                                        brewards = ['bronze2', 'bronze2', 'bronze2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            g = 0
                                            d = 0
                                            if users_updated[0]['points'] >= 250:
                                                for i in stat:
                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'silver2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'silver2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'silver2'
                                                        count = 'banner_count'

                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await ctx.send(f"{ctx.author.mention} ✨ Awarded **Silver2** Banner, Border, AvaBorder!")
                                                        g = g + 1
                                                        brewards = ['silver2', 'silver2', 'silver2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            g = 0
                                            d = 0                                                                    
                                            if users_updated[0]['points'] >= 500:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'gold2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'gold2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'gold2'
                                                        count = 'banner_count'
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1', ctx.author.id)
                                                            await ctx.send(f"{ctx.author.mention} ✨ Awarded **10**dc and **Gold2** Banner, Border, AvaBorder!")
                                                        g = g + 1
                                                        brewards = ['gold2', 'gold2', 'gold2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            g = 0
                                            d = 0                                                                    
                                            if users_updated[0]['points'] >= 750:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'platinum2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'platinum2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'platinum2'
                                                        count = 'banner_count'
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1', ctx.author.id)
                                                            await ctx.send(f"{ctx.author.mention} ✨ Awarded **25**dc and **Platinum2** Banner, Border, AvaBorder!")
                                                        g = g + 1
                                                        brewards = ['platinum2', 'platinum2', 'platinum2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            g = 0
                                            d = 0
                                            if users_updated[0]['points'] >= 1250:
                                                for i in stat:

                                                    if i == 'title':
                                                        lists = 'title_list'
                                                        s = ''
                                                        count = 'title_count'
                                                    elif i == 'borders':
                                                        lists = 'border_list'
                                                        s = 'dominant2'
                                                        count = 'border_count'
                                                    elif i == 'avaborders':
                                                        lists = 'avaborder_list'
                                                        s = 'dominant2'
                                                        count = 'avaborder_count'
                                                    else:
                                                        lists = 'banner_list'
                                                        s = 'dominant2'
                                                        count = 'banner_count'
                                                    checks = str(registered_check[0][lists])
                                                    check_list = self.listing(registered_check[0][lists])
                                                    
                                                    if s in check_list:
                                                        pass
                                                    else:
                                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                                        if g == 0:
                                                            await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1', ctx.author.id)
                                                            await ctx.send(f"{ctx.author.mention} ✨ Awarded **50**dc and **Dominant2** Banner, Border, AvaBorder! ")
                                                        g = g + 1
                                                        brewards = ['dominant2', 'dominant2', 'dominant2']
                                                        
                                                        itemcode = await id_generator()
                                                        a = f'{brewards[d].lower()}'
                                                        d = d + 1
                                                        b = 1
                                                        c = f"{itemcode}"
                                        
                                                        if registered_check[0][lists] is None:
                                                            new_admins = f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                                        else:
                                                            new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                            await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)


                                                    

                                                                                                            
                                            #Updating rank of winner

                                            if (int(user_points) >= 0) and (int(user_points) <= 83):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze1, bronze_value, author_id)

                                            elif (int(user_points) >= 84) and (int(user_points) <= 167):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze2, bronze_value, author_id)

                                            elif (int(user_points) >= 168) and (int(user_points) <= 250):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze3, bronze_value, author_id)

                                            elif (int(user_points) >= 251) and (int(user_points) <= 333):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver1, silver_value, author_id)

                                            elif (int(user_points) >= 334) and (int(user_points) <= 416):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver2, silver_value, author_id)

                                            elif (int(user_points) >= 417) and (int(user_points) <= 500):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver3, silver_value, author_id)

                                            elif (int(user_points) >= 501) and (int(user_points) <= 583):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold1, gold_value, author_id)

                                            elif (int(user_points) >= 584) and (int(user_points) <= 667):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold2, gold_value, author_id)

                                            elif (int(user_points) >= 668) and (int(user_points) <= 750):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold3, gold_value, author_id)

                                            elif (int(user_points) >= 751) and (int(user_points) <= 833):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum1, platinum_value, author_id)

                                            elif (int(user_points) >= 834) and (int(user_points) <= 916):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum2, platinum_value, author_id)

                                            elif (int(user_points) >= 917) and (int(user_points) <= 1249):
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum3, platinum_value, author_id)

                                            elif int(user_points) >= 1250:
                                                await self.bot.db.execute('UPDATE common_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', dominant, dominant_value, author_id)

                                            #Updating rank of loser

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

                                            #Giving coins
                                            (users_updated[0]['streak'])
                                            if users_updated[0]['streak'] > 2:
                                                wishes = math.ceil((users_updated[0]['streak']/2)) - 1
                                            
                                                coins = wishes + coins

                                                winter = round(coins*0.5)
                                                coins = winter + coins

                                                if coins > 10:
                                                    coins = 10

                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {coins} WHERE player_id = $1',  ctx.author.id)
                                                await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces + 1 WHERE player_id = $1', member.id)
                                                
                                                await ctx.send(f"Coins rewarded **+{coins}** to {ctx.author.name} | Coins rewarded **+1** to {member.name}\n**WINTER FEST +{winter}**")

                                            else:
                                                winter = round(coins*0.5)
                                                coins = winter + coins

                                                await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces + 1 WHERE player_id = $1', member.id)
                                                
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {coins} WHERE player_id = $1', ctx.author.id)
                                                await ctx.send(f"Coins rewarded **+{coins}** to {ctx.author.name} | Coins rewarded **+1** to {member.name}\n**WINTER FEST +{winter}**")
                                        elif view.value is False:
                                            await ctx.send('Cancelled.')
                                        else:
                                            await ctx.send('Timed Out')    
                                    else:
                                        await ctx.send('Unkown error.')

                                elif ctx.author.id == member.id:
                                    await ctx.send('You cannot log with yourself!')

                            elif not user_ban_list and player_ban_list:
                                await ctx.send('That person is banned from ranked battles!')

                            elif user_ban_list and not player_ban_list:
                                await ctx.send('You are banned from ranked battles.')

                            elif user_ban_list and player_ban_list:
                                await ctx.send('Both of you are banned from ranked battles.')

                        elif ranked_enable == 0:
                            await ctx.send('Ranked battles are currently not enabled.')

                    else:
                        await ctx.send('One of you have not registered yet!')

                else:
                    await ctx.send('That person has not registered yet! Use `d!start` to register.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @log_command.command(name = 'casuaffadfadl',  aliases = ['cafdafad'])
    async def casual_log_command(self, ctx, member : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        score = '1'
        if registered_check:
            if (member is None) or (score is None):
                em = discord.Embed(
                    title = 'Casual Log',
                    description = '**Log your Casual battles.**\n\nd!log casual [mention] [score]',
                    colour = color
                )

                await ctx.send(embed = em)
            
            else:
                member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                if member_registered:

                    users = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', ctx.author.id)
                    players = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1',  member.id)

                    if (users) and (players):

 
                        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

                        player_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', member.id)


                        if (not user_ban_list) and (not player_ban_list):
                            if ctx.author.id != member.id:
                                channelist = [1113505799755538533]
                                if ctx.channel.id not in channelist:
                                    await ctx.send("This command can only be used in the Casual Battling channel which is <#1113505799755538533>")
                                    return                                
                                view = ConfirmCancel(member)
                                await ctx.send(f'{member.mention} click the ✅ if you agree to the score and the winner or click the ❌ to cancel.\n*Remember that only the winner must send the log request. For this log** {ctx.author.name} **will be considered as the winner.*', view = view)
                                
                                await view.wait()

                                if view.value is True:

                                    flists = str(registered_check[0]['achievements'])
                                    new_admins = ''
                                    admins_list = self.listing(flists)
                                    
                                    for p,admin in enumerate(admins_list):
                                
                                        if p == 0:
                                            if int(admin) == 249:
                                                admins_list[1] = 1
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                await ctx.send("**Bronze Achievement Completed! ✦ Play 250 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                            elif int(admin) == 499:
                                                admins_list[1] = 2
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                await ctx.send("**Silver Achievement Completed! ✦✦ Play 500 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                            elif int(admin) == 999:
                                                admins_list[1] = 3
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                await ctx.send("**Gold Achievement Completed! ✦✦✦ Play 1000 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                            admin = int(admin) + 1
                                            new_admins += str(admin)
                                        elif p == 2:
                                            if int(admin) == 99:
                                                admins_list[3] = 1
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                await ctx.send("**Bronze Achievement Completed! ✦ Win 100 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                            elif int(admin) == 299:
                                                admins_list[3] = 2
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                await ctx.send("**Silver Achievement Completed! ✦✦ Win 300 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                            elif int(admin) == 699:
                                                admins_list[3] = 3
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                await ctx.send("**Gold Achievement Completed! ✦✦✦ Win 700 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                            admin = int(admin) + 1
                                            new_admins +=  f' {admin}'
                                        elif p == 14:
                                            if int(admin) == 99:
                                                admins_list[15] = 1
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  ctx.author.id)
                                                await ctx.send("**Bronze Achievement Completed! ✦ Play 100 Casual Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                            elif int(admin) == 249:
                                                admins_list[15] = 2
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  ctx.author.id)
                                                await ctx.send("**Silver Achievement Completed! ✦✦ Play 250 Casual Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                            elif int(admin) == 499:
                                                admins_list[15] = 3
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  ctx.author.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  ctx.author.id)
                                                await ctx.send("**Gold Achievement Completed! ✦✦✦ Play 500 Casual Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                            admin = int(admin) + 1
                                            new_admins += f' {admin}'                              
                                        else:
                                            new_admins += f' {admin}'  
                                    
                                    await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, ctx.author.id)                                          

                                    #Awarding Achieve for member
                                    flists = str(member_registered[0]['achievements'])
                                    new_admins = ''
                                    admins_list = self.listing(flists)
                                    for p,admin in enumerate(admins_list):
                                
                                        if p == 0:
                                            if int(admin) == 249:
                                                admins_list[1] = 1
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  member.id)
                                                await ctx.send("**Bronze Achievement Completed! ✦ Play 250 Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                            elif int(admin) == 499:
                                                admins_list[1] = 2
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  member.id)
                                                await ctx.send("**Silver Achievement Completed! ✦✦ Play 500 Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                            elif int(admin) == 999:
                                                admins_list[1] = 3
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  member.id)
                                                await ctx.send("**Gold Achievement Completed! ✦✦✦ Play 1000 Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                            admin = int(admin) + 1
                                            new_admins += str(admin)        
                                        elif p == 14:
                                            if int(admin) == 99:
                                                admins_list[15] = 1
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  member.id)
                                                await ctx.send("**Bronze Achievement Completed! ✦ Play 100 Casual Matches ✦**\n*10dc rewarded & Lootbox rewarded*")
                                            elif int(admin) == 249:
                                                admins_list[15] = 2
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',  member.id)
                                                await ctx.send("**Silver Achievement Completed! ✦✦ Play 250 Casual Matches ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                            elif int(admin) == 499:
                                                admins_list[15] = 3
                                                await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  member.id)
                                                await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  member.id)
                                                await ctx.send("**Gold Achievement Completed! ✦✦✦ Play 500 Casual Matches ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                            admin = int(admin) + 1
                                            new_admins += f' {admin}'                                                  
                                        else:
                                            new_admins += f' {admin}'  

                                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, member.id)   
                                    new_admins = ''
                                    check = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', ctx.author.id)
                                    if check[0]['matches_played'] > 29:
                                        
                                        lists = 'banner_list'
                                        s = 'casual'
                                        count = 'banner_count'
                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', ctx.author.id)
                                        checks = str(registered_check[0][lists])
                                        check_list = self.listing(registered_check[0][lists])
                                        
                                        if s in check_list:
                                            pass
                                        else:                                        
                                            itemcode = await id_generator()
                                            a = f'casual'
                                            b = 1
                                            c = f"{itemcode}"
                            
                                            if registered_check[0][lists] is None:
                                                new_admins = f' {a}' + f' {b}' + f' {c}'
                                                await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), ctx.author.id)


                                            else:
                                                new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, ctx.author.id)
                                            
                                            await ctx.send(f"{ctx.author.mention} ✨ Awarded **Casual Banner**!")
                                    mcheck = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', member.id)
                                    new_admins = ''
                                    if mcheck[0]['matches_played'] > 29:
                                        
                                        lists = 'banner_list'
                                        s = 'casual'
                                        count = 'banner_count'
                                        await self.bot.db.execute(f'UPDATE registered SET {count} = {count} + 1 WHERE player_id = $1', member.id)
                                        checks = str(member_registered[0][lists])
                                        check_list = self.listing(member_registered[0][lists])
                                        
                                        if s in check_list:
                                            pass
                                        else:                                        
                                            itemcode = await id_generator()
                                            a = f'casual'
                                            b = 1
                                            c = f"{itemcode}"
                            
                                            if member_registered[0][lists] is None:
                                                new_admins = f' {a}' + f' {b}' + f' {c}'
                                                await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', str(new_admins), member.id)


                                            else:
                                                new_admins = checks + f' {a}' + f' {b}' + f' {c}'
                                                await self.bot.db.execute(f'UPDATE registered SET {lists} = $1 WHERE player_id = $2', new_admins, member.id)
                                            
                                            await ctx.send(f"{member.mention} ✨ Awarded **Casual Banner**!")

                                    author_id = ctx.author.id 
                                    member_id = member.id 
                                    a = [0,1]
                                    m = [0]               
                                    await quests(self,ctx, a, author_id, m,member_id)

                                    ranked_battle_embed = discord.Embed(
                                        title = 'Casual Battles',
                                        description = f'{ctx.message.author.mention} beat {member.mention} in {ctx.message.channel.mention}\n Score: {score}',
                                        colour = color
                                    )

                                    ranking_channel = self.bot.get_channel(1091745597301723156)

                                    await ranking_channel.send(embed = ranked_battle_embed)


                                    await ctx.reply(f'{ctx.author.name} won **+10** points and {member.name} lost **-10** points.', mention_author = False)

                                    #Updating score of both players depending on ranked or unranked
                                    await self.bot.db.execute(f'UPDATE casual SET matches_played = matches_played + 1, points = points + 10, wins = wins + 1 WHERE player_id = $1', ctx.author.id)
                                    await self.bot.db.execute(f'UPDATE casual SET matches_played = matches_played + 1, points = points - 10 WHERE player_id = $1', member.id)

                                    #Setting streak
                                    await self.bot.db.execute('UPDATE casual SET streak = streak + 1 WHERE player_id = $1', ctx.author.id)
                                    await self.bot.db.execute('UPDATE casual SET streak = 0 WHERE player_id = $1', member.id)

                                    #Preventing score from being negative

                                    users_updated = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', ctx.author.id)
                                    players_updated = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', member.id)

                                    user_points = int(users_updated[0]['points'])
                                    player_points = int(players_updated[0]['points'])

                                    if int(user_points) < 0:
                                        await self.bot.db.execute('UPDATE casual SET points = 0 WHERE player_id = $1', ctx.author.id)

                                    if int(player_points) < 0:
                                        await self.bot.db.execute('UPDATE casual SET points = 0 WHERE player_id = $1', member.id)

                                    
                                    if players_updated[0]['streak'] < 0:
                                        await self.bot.db.execute('UPDATE casual SET streak = 0 WHERE player_id = $1', member.id)
        
    
                                    await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 2 WHERE player_id = $1',  ctx.author.id)
                                    await self.bot.db.execute('UPDATE registered SET banner_pieces = banner_pieces + 1 WHERE player_id = $1', member.id)
                                    
                                    await ctx.send(f"Coins rewarded **+2** to {ctx.author.name} | Coins rewarded **+1** to {member.name} ")


                                elif view.value is False:
                                    await ctx.send('Cancelled.')
                                else:
                                    await ctx.send('Timed Out')    
                        

                            elif ctx.author.id == member.id:
                                await ctx.send('You cannot log with yourself!')

                        elif not user_ban_list and player_ban_list:
                            await ctx.send('That person is banned from ranked battles!')

                        elif user_ban_list and not player_ban_list:
                            await ctx.send('You are banned from ranked battles.')

                        elif user_ban_list and player_ban_list:
                            await ctx.send('Both of you are banned from ranked battles.')

                    else:
                        await ctx.send('One of you have not registered yet!')

                else:
                    await ctx.send('That person has not registered yet! Use `d!start` to register.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')  
            

    @log_command.command(name='war')
    async def log_fafdadction_command(self,ctx, opponent : discord.Member = None, user : discord.Member = None ):
        if (opponent == None):
            em = discord.Embed(
                title = "War",
                description = 'Log a war duel.\n\n**d!log war [Opponent]**',
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

                if g == 'yes':
                    checky = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', player.id)
                else:
                    checky = registered_check
                clan_name = checky[0]['clan_1']


                if clan_name:
                    clan = await self.bot.db.fetch('SELECT * FROM clans WHERE clan_name = $1',clan_name)
                    warid = clan[0]['ready_for_war']
                    if (warid == 'False') or (warid == 'True'):

                        await ctx.send("Either your clan is not in a war or the war hasn't started yet.")
                        return

                    if (checky[0]['clan_2'] == 'war'):
                        pass

                    else:
                        await ctx.send("Your clan is in a war but you're not in that war.")
                        return
                    

                else:
            
                    await ctx.send("You're not in a clan nor are you a Blade.")
                    return







                winner = player.id
                loser = opponent.id

                if self.faction.count_documents({"_id": warid}, limit = 1):
                    if self.faction.count_documents({"_id": warid, "allymembers": opponent.id, "enemymembers": player.id}, limit = 1):
                        winner = opponent.id
                        loser = player.id
                    
                    if self.faction.count_documents({"_id": warid, "allymembers": winner,}, limit = 1):
                        if self.faction.count_documents({"_id": warid, "enemymembers": loser}, limit = 1):
                            if g == 'yes':
                                view = ConfirmCancel(ctx.author)
                                await ctx.send(f"Are you sure? **{player.name}** will be the **WINNER** and {opponent.name} will be the **LOSER**.", view=view)
                                await view.wait()
                            else:
                                view = ConfirmCancel(opponent)
                                await ctx.send (f'{opponent.mention} Do you accept the log request? **{player}** Will be the winner.', view = view)
                                await view.wait()
                            if view.value == True:
                                war_data = self.faction.find_one({"_id": warid})
                                formats = war_data["wartype"]
                                powerups = war_data["powerups"]

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
                                        self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscored": enemyscored}})         
                                                                       
                                        allyscore = war_data["allyplayerscore"]
                                        allyscore[indexally] += 1
                                        allyscored = war_data["allyplayerscored"]
                                        allyscored[indexally] += 1
                                        self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscored": allyscored}})
                                        self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscore": allyscore}})
                                        enemyffscore = war_data["enemyscore"]
                                        if powerups == 'no':
                                            history = None


                                            allyffscore = war_data["allyscore"] + 1
                                            self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": 1}})
                                        else:
                                            history = None

                                            #Mimicry and reflector
                                            #winner
                                            if powerups[1] == '9':

                                                pow2 = powerups[3]
                                                powerups = f'1{pow2}1{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})

                                                if pow2 == '1':
                                                    powerused = 'Bridger'
                                                elif pow2 == '2':
                                                    powerused = 'Jeopardy'
                                                elif pow2 == '3':
                                                    powerused = 'Battle cry'
                                                elif pow2 == '4':
                                                    powerused = 'Immunity'
                                                elif pow2 == '5':
                                                    powerused = 'Breakthrough'
                                                elif pow2 == '6':
                                                    powerused = 'Counterstrike'
                                                elif pow2 == '7':
                                                    powerused = 'Strategic Retreat'
                                                elif pow2 == '8':
                                                    powerused = 'Reflection Shield'
                                                elif pow2 == '9':
                                                    powerused = 'Mimicry'
                                                elif pow2 == 'x':
                                                    powerused = 'Sacrifice'
                                                elif pow2 == 'z':
                                                    powerused = 'Retribution'

                                                await ctx.send(f"👥 **Mimicry** 👥 was used.. copied **{powerused}**")
                                                history = None
                                            elif powerups[1] == '8':

                                                pow2 = powerups[3]
                                                pow1 = powerups[1]
                                                powerups = f'1{pow2}1{pow1}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})

                                                if pow2 == '1':
                                                    powerused = 'Bridger'
                                                elif pow2 == '2':
                                                    powerused = 'Jeopardy'
                                                elif pow2 == '3':
                                                    powerused = 'Battle cry'
                                                elif pow2 == '4':
                                                    powerused = 'Immunity'
                                                elif pow2 == '5':
                                                    powerused = 'Breakthrough'
                                                elif pow2 == '6':
                                                    powerused = 'Counterstrike'
                                                elif pow2 == '7':
                                                    powerused = 'Strategic Retreat'
                                                elif pow2 == '8':
                                                    powerused = 'Reflection Shield'
                                                elif pow2 == '9':
                                                    powerused = 'Mimicry'
                                                elif pow2 == 'x':
                                                    powerused = 'Sacrifice'
                                                elif pow2 == 'z':
                                                    powerused = 'Retribution'

                                                await ctx.send(f"🌟 **Reflection Shield** 🌟 was used.. exchanged powerups, {faction_name} now has **{powerused}**")
                                                history = None








                                            if powerups[1] == '6':

                                                pow2 = powerups[3]
                                                powerups = f'101{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})

                                                await ctx.send(f"🛩️  **Counterstike** 🛩️ expired.. Score is **{allyffscore}** for **{faction_name}**")
                                                history = None                                            
                                            if powerups[1] == '5':

                                                pow2 = powerups[3]
                                                powerups = f'101{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                if (pow2 == '4') or (pow2 == '5') or (pow2 == '6') or (pow2 == '7') or (pow2 == '9') or (pow2 == 'x'):
                                                    await ctx.send(f"⚡ **Breakthrough** ⚡ {faction_name} got **4** Points.")
                                                else:
                                                    await ctx.send(f"⚡ **Breakthrough** ⚡ expired.. Score is **{allyffscore}** for **{faction_name}**")
                                                history = None                                             


                                            if powerups[3] == '1':
                                                if powerups[1] == '1':
                                                    powerups = f'1414'
                                                else:
                                                    powerups = f'1014'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                allyffscore = war_data["allyscore"]
                                                await ctx.send(f"🛡️ **Immunity** 🛡️ points weren't given to the winner's team. Score is **{allyffscore}** for **{faction_name}**")
                                                history = f'🛡️ **Immunity** 🛡️ **Protected {efaction_name}**' 


                                            elif powerups[1] == '1':

                                                pow2 = powerups[3]
                                                powerups = f'141{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": 1}})
                                                allyffscore = war_data["allyscore"] + 1
                                                await ctx.send(f"🛡️ **Immunity** 🛡️ expired.. Score is **{allyffscore}** for **{faction_name}**")
                                                history = None
                                            elif powerups[1] == '2':
                                                pow2 = powerups[3]
                                                powerups = f'101{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})   
                                                allyffscore = war_data["allyscore"] + 2
                                                self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": 2}})                                         
                                                await ctx.send(f"⚔️ **Jeopardy** ⚔️ Double points were given to the winner's team. Score is **{allyffscore}** for **{faction_name}**")
                                                history = f'⚔️ **Jeopardy** ⚔️ **{faction_name} Got 2 Points**' 
                                            elif powerups[1] == '3':
                                                pow2 = powerups[3]
                                                powerups = f'101{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})   
                                                allyffscore = war_data["allyscore"] + 3
                                                self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": 3}})                                         
                                                await ctx.send(f"⛩️ **Bridger** ⛩️ Triple points were given to the winner's team. Score is **{allyffscore}** for **{faction_name}**")  
                                                history = f'⛩️ **Bridger** ⛩️ **{faction_name} Got 3 Points**' 
                                            else:


                                                allyffscore = war_data["allyscore"] + 1
                                                self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": 1}})     
                                            
                    
                                            if powerups[3] == '2':
                                                pow1 = powerups[1]
                                                powerups = f'1{pow1}10'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": -2}})   
                                                enemyffscore = war_data["enemyscore"] - 2

                                                allyffscore = war_data["allyscore"]- 1
                                                self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": -1}})

                                                await ctx.send(f"⚔️ **Jeopardy** ⚔️ 2 points were deducted from the loser's team. Score is **{enemyffscore}** for **{efaction_name}**")  
                                                history = f'⚔️ **Jeopardy** ⚔️ **{efaction_name} Lost 2 Points**' 
                                            elif powerups[3] == '3':
                                                pow1 = powerups[1]
                                                powerups = f'1{pow1}10'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})


                                                await ctx.send(f"⛩️ **Bridger** ⛩️ expired... Score is **{enemyffscore}** for **{efaction_name}**")  
                                                history = None                                            


                                            pow1 = powerups[1]
                                            pow2 = powerups[3]
                                            
                                            if powerups[1] == 'a':
                                                powerups = f'111{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                pow1 = '1'
                                                try:
                                                    await player.send("🛡️ Immunity is now active for the next match.")
                                                except Exception as e:
                                                    pass
                                                
                                            elif powerups[1] == 'b':
                                                powerups = f'121{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                pow1 = '2'
                                                try:
                                                    await player.send("⚔️ Jeopardy is now active for the next match.")
                                                except Exception as e:
                                                    pass
                                            elif powerups[1] == 'c':
                                                powerups = f'131{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                pow1 = '3'
                                                try:
                                                    await player.send("⛩️ Bridger is now active for the next match.")
                                                except Exception as e:
                                                    pass

                                            if powerups[3] == 'a':
                                                powerups = f'1{pow1}11'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                try:
                                                    await opponent.send("🛡️ Immunity is now active for the next match.")
                                                except Exception as e:
                                                    pass
                                            elif powerups[3] == 'b':
                                                powerups = f'1{pow1}12'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                try:
                                                    await opponent.send("⚔️ Jeopardy is now active for the next match.")
                                                except Exception as e:
                                                    pass
                                            elif powerups[3] == 'c':
                                                powerups = f'1{pow1}13'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                try:
                                                    await opponent.send("⛩️ Bridger is now active for the next match.")
                                                except Exception as e:
                                                    pass                                          
                                        
                                        
                                        await ctx.send(f"{player.mention} Won. Updated war scores")

                                        ranked_battle_embed = discord.Embed(
                                            title = f'{faction_name} {allyffscore} VS {efaction_name} {enemyffscore} {warid}',
                                            description = f'{ctx.message.author.mention} beat {opponent.mention} in {ctx.message.channel.mention}\n**Message Link** {ctx.message.jump_url}',
                                            colour = color
                                        )

                                        ranking_channel = self.bot.get_channel(1093609140921843802)

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

                                        war_check = await self.bot.db.fetch('SELECT * FROM wars WHERE player_id  = $1', player.id)
                                        await self.bot.db.execute(f"UPDATE wars SET wins = wins + 1 WHERE player_id = $1", player.id)    
                                        
                                        await self.bot.db.execute(f'UPDATE wars SET loses = loses + 1 WHERE player_id = $1', opponent.id) 


                                        await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, player.id)                                              
                                        if winner == player.id:
                                            self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                            self.faction.update_one({"_id": warid}, {"$push": {"history": f'🟢 **Won** `{player.name}` ⚔️ 🔴 **Lost** `{opponent.name}`'}})
                                            if history != None:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": history}})                                                
                                            
                                        elif loser == player.id:
                                            self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                            self.faction.update_one({"_id": warid}, {"$push": {"history": f'🔴 **Lost** `{opponent.name}` ⚔️ 🟢 **Won** `{player.name}`'}})
                                            if history != None:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": history}})                                            
                                        await warcheck(self,ctx, warid, allyffscore, enemyffscore)
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
                                        self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscored": enemyscored}})
                                        self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscore": enemyscore}})

                                        allymembers = war_data["allymembers"]
                                        actualally = []
                                        for i in allymembers:
                                            actualally.append(i)
                                        indexallyd = actualally.index(winner)
                                        allyscored = war_data["allyplayerscored"]
                                        allyscored[indexallyd] += 1
                                        self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscored": allyscored}})    
                                        allyffscore = war_data["allyscore"]
                                        if powerups == 'no':
                                            history = None

                                            enemyffscore = war_data["enemyscore"] + 1
                                            self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": 1}})
                                        else:
                                            history = None
                                            if powerups[1] == '1':
                                                if powerups[3] == '1':
                                                    powerups = f'1414'
                                                else:
                                                    powerups = f'1410'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                enemyffscore = war_data["enemyscore"]
                                                await ctx.send(f"🛡️ **Immunity** 🛡️ points weren't given to the winner's team. Score is **{enemyffscore}** for **{efaction_name}**")
                                                history = f'🛡️ **Immunity** 🛡️ **Protected {faction_name}**' 

                                            elif powerups[3] == '1':

                                                pow1 = powerups[1]
                                                powerups = f'1{pow1}14'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": 1}})
                                                enemyffscore = war_data["enemyscore"] + 1
                                                await ctx.send("🛡️ **Immunity** 🛡️ expired..")
                                                history = None
                                            elif powerups[3] == '2':
                                                pow1 = powerups[1]
                                                powerups = f'1{pow1}10'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})   
                                                enemyffscore = war_data["enemyscore"] + 2
                                                self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": 2}})                                         
                                                await ctx.send(f"⚔️ **Jeopardy** ⚔️ Double points were given to the winner's team. Score is **{enemyffscore}** for **{efaction_name}**")
                                                history = f'⚔️ **Jeopardy** ⚔️ **{efaction_name} Got 2 Points**' 
                                            elif powerups[3] == '3':
                                                pow1 = powerups[1]
                                                powerups = f'1{pow1}10'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})   
                                                enemyffscore = war_data["enemyscore"] + 3
                                                self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": 3}})                                         
                                                await ctx.send(f"⛩️ **Bridger** ⛩️ Triple points were given to the winner's team. Score is **{enemyffscore}** for **{efaction_name}**")  
                                                history = f'⛩️ **Bridger** ⛩️ **{efaction_name} Got 3 Points**' 
                                            else:
                                                
                                                enemyffscore = war_data["enemyscore"] + 1
                                                self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": 1}})   
                                                

                                            
                                            if powerups[1] == '2':
                                                pow2 = powerups[3]
                                                powerups = f'101{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": -2}})   
                                                allyffscore = war_data["allyscore"] - 2

                                                enemyffscore = war_data["enemyscore"]- 1
                                                self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": -1}})

                                                await ctx.send(f"⚔️ **Jeopardy** ⚔️ 2 points were deducted from the loser's team. Score is **{allyffscore}** for **{faction_name}**") 
                                                history = f'⚔️ **Jeopardy** ⚔️ **{faction_name} Lost 2 Points**'      

                                            pow1 = powerups[1]
                                            pow2 = powerups[3]

                                            if powerups[1] == 'a':
                                                powerups = f'111{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                pow1 = '1'
                                                try:
                                                    await opponent.send("🛡️ Immunity is now active for the next match.")
                                                except Exception as e:
                                                    pass      
                                            elif powerups[1] == 'b':
                                                powerups = f'121{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                pow1 = '2'
                                                try:
                                                    await opponent.send("⚔️ Jeopardy is now active for the next match.")
                                                except Exception as e:
                                                    pass                                                  
                                            elif powerups[1] == 'c':
                                                powerups = f'131{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                pow1 = '3'
                                                try:
                                                    await opponent.send("⛩️ Bridger is now active for the next match.")
                                                except Exception as e:
                                                    pass      
                                                
                                            if powerups[3] == 'a':
                                                powerups = f'1{pow1}11'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                try:
                                                    await player.send("🛡️ Immunity is now active for the next match.")
                                                except Exception as e:
                                                    pass      
                                            elif powerups[3] == 'b':
                                                powerups = f'1{pow1}12'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                try:
                                                    await player.send("⚔️ Jeopardy is now active for the next match.")
                                                except Exception as e:
                                                    pass 
                                            elif powerups[3] == 'c':
                                                powerups = f'1{pow1}13'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                try:
                                                    await player.send("⛩️ Bridger is now active for the next match.")
                                                except Exception as e:
                                                    pass   

                                        await ctx.send(f"{player.mention} Won. Updated war scores")

                                        faction_name = war_data['teamone']
                                        efaction_name = war_data['teamtwo']

                                        ranked_battle_embed = discord.Embed(
                                            title = f'{faction_name} {allyffscore} VS {efaction_name} {enemyffscore} {warid}',
                                            description = f'{player.mention} beat {opponent.mention} in {ctx.message.channel.mention}\n**Message Link** {ctx.message.jump_url}',
                                            colour = color
                                        )

                                        ranking_channel = self.bot.get_channel(1093609140921843802)

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
                                            self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                            self.faction.update_one({"_id": warid}, {"$push": {"history": f'🟢 **Won** `{player.name}` ⚔️ 🔴 **Lost** `{opponent.name}`'}})
                                            if history != None:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": history}})                                               
                                        elif loser == player.id:
                                            self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                            self.faction.update_one({"_id": warid}, {"$push": {"history": f'🔴 **Lost** `{opponent.name}` ⚔️ 🟢 **Won** `{player.name}`'}})
                                            if history != None:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": history}})            

                                        await warcheck(self,ctx, warid, allyffscore, enemyffscore)

                                elif  formats == 'koth':   
                                    if winner == player.id:
                                        allyffscore = war_data['allyscore']
                                        enemyffscore = war_data['enemyscore']
                                        allymembers = war_data['allymembers']
                                        allyscore = war_data['allyplayerscore']
                                        enemymembers = war_data['enemymembers']
                                        enemyscore = war_data['enemyplayerscore']
                                        ally_score = list(zip(allymembers,allyscore,enemymembers,enemyscore))
                                        allymembers = []
                                        allymembers2 = []
                                        allyscore = []
                                        allyscore2 = []
                                        enemymembers = []
                                        enemymembers2 = []
                                        enemyscore = []
                                        enemyscore2 = []
                                        for i in ally_score:
                                            scorelist = list(i)
                                            if enemyffscore >0:
                                                crudescore1 = int(scorelist[0])
                                                allyzunit = f'~~<@{crudescore1}>~~'
                                                allymembers2.append(allyzunit)
                                                crudescore2 = str(scorelist[1])
                                                allyscore2.append(crudescore2)
                                                enemyffscore -= 1

                                            else:
                                                crudescore1 = int(scorelist[0])
                                                allyunit = f'<@{crudescore1}>'
                                                allymembers.append(allyunit)
                                                crudescore2 = str(scorelist[1])
                                                allyscore.append(crudescore2)                      
                                            
                                            if allyffscore >0:
                                                crudescore3 = int(scorelist[2])
                                                enemyzunit = f'~~<@{crudescore3}>~~'
                                                enemymembers2.append(enemyzunit)
                                                crudescore4 = str(scorelist[3])
                                                enemyscore2.append(crudescore4)
                                                allyffscore -= 1 
                                            else:
                                                crudescore3 = int(scorelist[2])
                                                enemyunit = f'<@{crudescore3}>'                                
                                                enemymembers.append(enemyunit)
                                                crudescore4 = str(scorelist[3])
                                                enemyscore.append(crudescore4)
                                        allymembers.extend(allymembers2)    
                                        allyscore.extend(allyscore2)
                                        enemymembers.extend(enemymembers2)
                                        enemyscore.extend(enemyscore2)
                                        if (allymembers[0] == f'<@{player.id}>') and (enemymembers[0] == f'<@{opponent.id}>'):        

                                            allymembers = war_data["allymembers"]
                                            actualally = []
                                            for i in allymembers:
                                                actualally.append(i)
                                            indexally = actualally.index(winner)
                                            allyscore = war_data["allyplayerscore"]
                                            allyscore[indexally] += 1
                                            allyscored = war_data["allyplayerscored"]
                                            allyscored[indexally] += 1

                                            enemymembers = war_data["enemymembers"]
                                            actualenemy = []
                                            for i in enemymembers:
                                                actualenemy.append(i)
                                            indexallyd = actualenemy.index(loser)
                                            enemyscored = war_data["enemyplayerscored"]
                                            enemyscored[indexallyd] += 1
                                            self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscored": enemyscored}})    

                                            self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscored": allyscored}})
                                            self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscore": allyscore}})
                                            self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": 1}})
                                            allyffscore = war_data["allyscore"] + 1
                                            enemyffscore = war_data["enemyscore"]
                                            await ctx.send(f"{player.mention} Won. Updated war scores")
                                            faction_name = war_data['teamone']
                                            efaction_name = war_data['teamtwo']
                                            allyffscore = war_data['allyscore']+ 1
                                            denemyffscore = war_data['enemyscore']

                                            ranked_battle_embed = discord.Embed(
                                                title = f'{faction_name} {allyffscore} VS {efaction_name} {denemyffscore} {warid}',
                                                description = f'{player.mention} beat {opponent.mention} in {ctx.message.channel.mention}\n**Message Link** {ctx.message.jump_url}',
                                                colour = color
                                            )

                                            ranking_channel = self.bot.get_channel(1093609140921843802)

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

                                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, player.id)                                              
                                            if winner == player.id:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": f'🟢 **Won** `{player.name}` ⚔️ 🔴 **Lost** `{opponent.name}`'}})
                                                
                                            elif loser == player.id:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": f'🔴 **Lost** `{opponent.name}` ⚔️ 🟢 **Won** `{player.name}`'}})
                                                
                                            await warcheck(self,ctx, warid, allyffscore, enemyffscore)
                                        else:
                                            await ctx.send("Either you or you opponent isn't supposed to battle.")
                                    else:
                                        allyffscore = war_data['allyscore']
                                        enemyffscore = war_data['enemyscore']
                                        allymembers = war_data['allymembers']
                                        allyscore = war_data['allyplayerscore']
                                        enemymembers = war_data['enemymembers']
                                        enemyscore = war_data['enemyplayerscore']
                                        ally_score = list(zip(allymembers,allyscore,enemymembers,enemyscore))

                                        allymembers = []
                                        allymembers2 = []
                                        allyscore = []
                                        allyscore2 = []
                                        enemymembers = []
                                        enemymembers2 = []
                                        enemyscore = []
                                        enemyscore2 = []
                                        for i in ally_score:
                                            scorelist = list(i)
                                            if enemyffscore >0:
                                                crudescore1 = int(scorelist[0])
                                                allyzunit = f'~~<@{crudescore1}>~~'
                                                allymembers2.append(allyzunit)
                                                crudescore2 = str(scorelist[1])
                                                allyscore2.append(crudescore2)
                                                enemyffscore -= 1

                                            else:
                                                crudescore1 = int(scorelist[0])
                                                allyunit = f'<@{crudescore1}>'
                                                allymembers.append(allyunit)
                                                crudescore2 = str(scorelist[1])
                                                allyscore.append(crudescore2)                      
                                            
                                            if allyffscore >0:
                                                crudescore3 = int(scorelist[2])
                                                enemyzunit = f'~~<@{crudescore3}>~~'
                                                enemymembers2.append(enemyzunit)
                                                crudescore4 = str(scorelist[3])
                                                enemyscore2.append(crudescore4)
                                                allyffscore -= 1 
                                            else:
                                                crudescore3 = int(scorelist[2])
                                                enemyunit = f'<@{crudescore3}>'                                
                                                enemymembers.append(enemyunit)
                                                crudescore4 = str(scorelist[3])
                                                enemyscore.append(crudescore4)
                                        allymembers.extend(allymembers2)    
                                        allyscore.extend(allyscore2)
                                        enemymembers.extend(enemymembers2)
                                        enemyscore.extend(enemyscore2)
                                        if (allymembers[0] == f'<@{opponent.id}>') and (enemymembers[0] ==  f'<@{player.id}>'):        

                                            enemymembers = war_data["enemymembers"]
                                            actualenemy = []
                                            for i in enemymembers:
                                                actualenemy.append(i)
                                            indexenemy = actualenemy.index(loser)
                                            enemyscore = war_data["enemyplayerscore"]
                                            enemyscore[indexenemy] += 1
                                            enemyscored = war_data["enemyplayerscored"]
                                            enemyscored[indexenemy] += 1
                                            self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscored": enemyscored}})
                                            self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscore": enemyscore}})
                                            self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": 1}})


                                            allymembers = war_data["allymembers"]
                                            actualally = []
                                            for i in allymembers:
                                                actualally.append(i)
                                            indexallyd = actualally.index(winner)
                                            allyscored = war_data["allyplayerscored"]
                                            allyscored[indexallyd] += 1
                                            self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscored": allyscored}})    
                                        

                                            allyffscore = war_data["allyscore"]
                                            enemyffscore = war_data["enemyscore"] + 1
                                            await ctx.send(f"{player.mention} Won. Updated war scores")
                                            faction_name = war_data['teamone']
                                            efaction_name = war_data['teamtwo']
                                            allyffscore = war_data['allyscore'] 
                                            denemyffscore = war_data['enemyscore']+ 1

                                            ranked_battle_embed = discord.Embed(
                                                title = f'{faction_name} {allyffscore} VS {efaction_name} {denemyffscore} {warid}',
                                                description = f'{player.author.mention} beat {opponent.mention} in {ctx.message.channel.mention}\n**Message Link** {ctx.message.jump_url}',
                                                colour = color
                                            )

                                            ranking_channel = self.bot.get_channel(1093609140921843802)

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
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  player.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  player.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Win 500 Clan Duels ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + 1
                                                    new_admins += f' {admin}'                                                       
                                                else:
                                                    new_admins += f' {admin}'  

                                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, player.id)                                              
                                            if winner == player.id:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": f'🟢 **Won** `{player.name}` ⚔️ 🔴 **Lost** `{opponent.name}`'}})
                                                
                                            elif loser == player.id:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": f'🔴 **Lost** `{opponent.name}` ⚔️ 🟢 **Won** `{player.name}`'}})
                                    
                                            await warcheck(self,ctx, warid, allyffscore, enemyffscore)            
                                        else:
                                            await ctx.send("Its not you're opponent's turn yet!")                                    

                
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


    @log_command.command(name='blade')
    async def log_favvvfdadction_command(self,ctx, opponent : discord.Member = None, user : discord.Member = None ):
        if (opponent == None):
            em = discord.Embed(
                title = "War",
                description = 'Log a blade duel.\n\n**d!log blade [Opponent]**',
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

                if g == 'yes':
                    checky = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', player.id)
                else:
                    checky = registered_check
                    

                warid = checky[0]['blade']

                if warid:
                    pass
                else:
                    await ctx.send("You're not a blade in any war!")
                    return
 

                winner = player.id
                loser = opponent.id

                if self.faction.count_documents({"_id": warid}, limit = 1):
                    if self.faction.count_documents({"_id": warid, "allymembers": opponent.id, "enemymembers": player.id}, limit = 1):
                        winner = opponent.id
                        loser = player.id
                    
                    if self.faction.count_documents({"_id": warid, "allymembers": winner,}, limit = 1):
                        if self.faction.count_documents({"_id": warid, "enemymembers": loser}, limit = 1):
                            if g == 'yes':
                                view = ConfirmCancel(ctx.author)
                                await ctx.send(f"Are you sure? **{player.name}** will be the **WINNER** and {opponent.name} will be the **LOSER**.", view=view)
                                await view.wait()
                            else:
                                view = ConfirmCancel(opponent)
                                await ctx.send (f'{opponent.mention} Do you accept the log request? **{player}** Will be the winner.', view = view)
                                await view.wait()
                            if view.value == True:
                                war_data = self.faction.find_one({"_id": warid})
                                formats = war_data["wartype"]
                                powerups = war_data["powerups"]

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
                                        self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscored": enemyscored}})         
                                                                       
                                        allyscore = war_data["allyplayerscore"]
                                        allyscore[indexally] += 1
                                        allyscored = war_data["allyplayerscored"]
                                        allyscored[indexally] += 1
                                        self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscored": allyscored}})
                                        self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscore": allyscore}})
                                        enemyffscore = war_data["enemyscore"]
                                        if powerups == 'no':
                                            history = None


                                            allyffscore = war_data["allyscore"] + 1
                                            self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": 1}})
                                        else:
                                            history = None

                                            #Mimicry and reflector
                                            #winner
                                            if powerups[1] == '9':

                                                pow2 = powerups[3]
                                                powerups = f'1{pow2}1{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})

                                                if pow2 == '1':
                                                    powerused = 'Bridger'
                                                elif pow2 == '2':
                                                    powerused = 'Jeopardy'
                                                elif pow2 == '3':
                                                    powerused = 'Battle cry'
                                                elif pow2 == '4':
                                                    powerused = 'Immunity'
                                                elif pow2 == '5':
                                                    powerused = 'Breakthrough'
                                                elif pow2 == '6':
                                                    powerused = 'Counterstrike'
                                                elif pow2 == '7':
                                                    powerused = 'Strategic Retreat'
                                                elif pow2 == '8':
                                                    powerused = 'Reflection Shield'
                                                elif pow2 == '9':
                                                    powerused = 'Mimicry'
                                                elif pow2 == 'x':
                                                    powerused = 'Sacrifice'
                                                elif pow2 == 'z':
                                                    powerused = 'Retribution'

                                                await ctx.send(f"👥 **Mimicry** 👥 was used.. copied **{powerused}**")
                                                history = None
                                            elif powerups[1] == '8':

                                                pow2 = powerups[3]
                                                pow1 = powerups[1]
                                                powerups = f'1{pow2}1{pow1}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})

                                                if pow2 == '1':
                                                    powerused = 'Bridger'
                                                elif pow2 == '2':
                                                    powerused = 'Jeopardy'
                                                elif pow2 == '3':
                                                    powerused = 'Battle cry'
                                                elif pow2 == '4':
                                                    powerused = 'Immunity'
                                                elif pow2 == '5':
                                                    powerused = 'Breakthrough'
                                                elif pow2 == '6':
                                                    powerused = 'Counterstrike'
                                                elif pow2 == '7':
                                                    powerused = 'Strategic Retreat'
                                                elif pow2 == '8':
                                                    powerused = 'Reflection Shield'
                                                elif pow2 == '9':
                                                    powerused = 'Mimicry'
                                                elif pow2 == 'x':
                                                    powerused = 'Sacrifice'
                                                elif pow2 == 'z':
                                                    powerused = 'Retribution'

                                                await ctx.send(f"🌟 **Reflection Shield** 🌟 was used.. exchanged powerups, {faction_name} now has **{powerused}**")
                                                history = None








                                            if powerups[1] == '6':

                                                pow2 = powerups[3]
                                                powerups = f'101{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})

                                                await ctx.send(f"🛩️  **Counterstike** 🛩️ expired.. Score is **{allyffscore}** for **{faction_name}**")
                                                history = None                                            
                                            if powerups[1] == '5':

                                                pow2 = powerups[3]
                                                powerups = f'101{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                if (pow2 == '4') or (pow2 == '5') or (pow2 == '6') or (pow2 == '7') or (pow2 == '9') or (pow2 == 'x'):
                                                    await ctx.send(f"⚡ **Breakthrough** ⚡ {faction_name} got **4** Points.")
                                                else:
                                                    await ctx.send(f"⚡ **Breakthrough** ⚡ expired.. Score is **{allyffscore}** for **{faction_name}**")
                                                history = None                                             


                                            if powerups[3] == '1':
                                                if powerups[1] == '1':
                                                    powerups = f'1414'
                                                else:
                                                    powerups = f'1014'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                allyffscore = war_data["allyscore"]
                                                await ctx.send(f"🛡️ **Immunity** 🛡️ points weren't given to the winner's team. Score is **{allyffscore}** for **{faction_name}**")
                                                history = f'🛡️ **Immunity** 🛡️ **Protected {efaction_name}**' 


                                            elif powerups[1] == '1':

                                                pow2 = powerups[3]
                                                powerups = f'141{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": 1}})
                                                allyffscore = war_data["allyscore"] + 1
                                                await ctx.send(f"🛡️ **Immunity** 🛡️ expired.. Score is **{allyffscore}** for **{faction_name}**")
                                                history = None
                                            elif powerups[1] == '2':
                                                pow2 = powerups[3]
                                                powerups = f'101{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})   
                                                allyffscore = war_data["allyscore"] + 2
                                                self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": 2}})                                         
                                                await ctx.send(f"⚔️ **Jeopardy** ⚔️ Double points were given to the winner's team. Score is **{allyffscore}** for **{faction_name}**")
                                                history = f'⚔️ **Jeopardy** ⚔️ **{faction_name} Got 2 Points**' 
                                            elif powerups[1] == '3':
                                                pow2 = powerups[3]
                                                powerups = f'101{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})   
                                                allyffscore = war_data["allyscore"] + 3
                                                self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": 3}})                                         
                                                await ctx.send(f"⛩️ **Bridger** ⛩️ Triple points were given to the winner's team. Score is **{allyffscore}** for **{faction_name}**")  
                                                history = f'⛩️ **Bridger** ⛩️ **{faction_name} Got 3 Points**' 
                                            else:


                                                allyffscore = war_data["allyscore"] + 1
                                                self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": 1}})     
                                            
                    
                                            if powerups[3] == '2':
                                                pow1 = powerups[1]
                                                powerups = f'1{pow1}10'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": -2}})   
                                                enemyffscore = war_data["enemyscore"] - 2

                                                allyffscore = war_data["allyscore"]- 1
                                                self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": -1}})

                                                await ctx.send(f"⚔️ **Jeopardy** ⚔️ 2 points were deducted from the loser's team. Score is **{enemyffscore}** for **{efaction_name}**")  
                                                history = f'⚔️ **Jeopardy** ⚔️ **{efaction_name} Lost 2 Points**' 
                                            elif powerups[3] == '3':
                                                pow1 = powerups[1]
                                                powerups = f'1{pow1}10'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})


                                                await ctx.send(f"⛩️ **Bridger** ⛩️ expired... Score is **{enemyffscore}** for **{efaction_name}**")  
                                                history = None                                            


                                            pow1 = powerups[1]
                                            pow2 = powerups[3]
                                            
                                            if powerups[1] == 'a':
                                                powerups = f'111{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                pow1 = '1'
                                                try:
                                                    await player.send("🛡️ Immunity is now active for the next match.")
                                                except Exception as e:
                                                    pass
                                                
                                            elif powerups[1] == 'b':
                                                powerups = f'121{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                pow1 = '2'
                                                try:
                                                    await player.send("⚔️ Jeopardy is now active for the next match.")
                                                except Exception as e:
                                                    pass
                                            elif powerups[1] == 'c':
                                                powerups = f'131{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                pow1 = '3'
                                                try:
                                                    await player.send("⛩️ Bridger is now active for the next match.")
                                                except Exception as e:
                                                    pass

                                            if powerups[3] == 'a':
                                                powerups = f'1{pow1}11'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                try:
                                                    await opponent.send("🛡️ Immunity is now active for the next match.")
                                                except Exception as e:
                                                    pass
                                            elif powerups[3] == 'b':
                                                powerups = f'1{pow1}12'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                try:
                                                    await opponent.send("⚔️ Jeopardy is now active for the next match.")
                                                except Exception as e:
                                                    pass
                                            elif powerups[3] == 'c':
                                                powerups = f'1{pow1}13'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                try:
                                                    await opponent.send("⛩️ Bridger is now active for the next match.")
                                                except Exception as e:
                                                    pass                                          
                                        
                                        
                                        await ctx.send(f"{player.mention} Won. Updated war scores")

                                        ranked_battle_embed = discord.Embed(
                                            title = f'{faction_name} {allyffscore} VS {efaction_name} {enemyffscore} {warid}',
                                            description = f'{ctx.message.author.mention} beat {opponent.mention} in {ctx.message.channel.mention}\n**Message Link** {ctx.message.jump_url}',
                                            colour = color
                                        )

                                        ranking_channel = self.bot.get_channel(1093609140921843802)

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

                                        war_check = await self.bot.db.fetch('SELECT * FROM wars WHERE player_id  = $1', player.id)
                                        await self.bot.db.execute(f"UPDATE wars SET wins = wins + 1 WHERE player_id = $1", player.id)    
                                        
                                        await self.bot.db.execute(f'UPDATE wars SET loses = loses + 1 WHERE player_id = $1', opponent.id) 


                                        await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, player.id)                                              
                                        if winner == player.id:
                                            self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                            self.faction.update_one({"_id": warid}, {"$push": {"history": f'🟢 **Won** `{player.name}` ⚔️ 🔴 **Lost** `{opponent.name}`'}})
                                            if history != None:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": history}})                                                
                                            
                                        elif loser == player.id:
                                            self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                            self.faction.update_one({"_id": warid}, {"$push": {"history": f'🔴 **Lost** `{opponent.name}` ⚔️ 🟢 **Won** `{player.name}`'}})
                                            if history != None:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": history}})                                            
                                        await warcheck(self,ctx, warid, allyffscore, enemyffscore)
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
                                        self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscored": enemyscored}})
                                        self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscore": enemyscore}})

                                        allymembers = war_data["allymembers"]
                                        actualally = []
                                        for i in allymembers:
                                            actualally.append(i)
                                        indexallyd = actualally.index(winner)
                                        allyscored = war_data["allyplayerscored"]
                                        allyscored[indexallyd] += 1
                                        self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscored": allyscored}})    
                                        allyffscore = war_data["allyscore"]
                                        if powerups == 'no':
                                            history = None

                                            enemyffscore = war_data["enemyscore"] + 1
                                            self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": 1}})
                                        else:
                                            history = None
                                            if powerups[1] == '1':
                                                if powerups[3] == '1':
                                                    powerups = f'1414'
                                                else:
                                                    powerups = f'1410'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                enemyffscore = war_data["enemyscore"]
                                                await ctx.send(f"🛡️ **Immunity** 🛡️ points weren't given to the winner's team. Score is **{enemyffscore}** for **{efaction_name}**")
                                                history = f'🛡️ **Immunity** 🛡️ **Protected {faction_name}**' 

                                            elif powerups[3] == '1':

                                                pow1 = powerups[1]
                                                powerups = f'1{pow1}14'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": 1}})
                                                enemyffscore = war_data["enemyscore"] + 1
                                                await ctx.send("🛡️ **Immunity** 🛡️ expired..")
                                                history = None
                                            elif powerups[3] == '2':
                                                pow1 = powerups[1]
                                                powerups = f'1{pow1}10'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})   
                                                enemyffscore = war_data["enemyscore"] + 2
                                                self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": 2}})                                         
                                                await ctx.send(f"⚔️ **Jeopardy** ⚔️ Double points were given to the winner's team. Score is **{enemyffscore}** for **{efaction_name}**")
                                                history = f'⚔️ **Jeopardy** ⚔️ **{efaction_name} Got 2 Points**' 
                                            elif powerups[3] == '3':
                                                pow1 = powerups[1]
                                                powerups = f'1{pow1}10'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})   
                                                enemyffscore = war_data["enemyscore"] + 3
                                                self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": 3}})                                         
                                                await ctx.send(f"⛩️ **Bridger** ⛩️ Triple points were given to the winner's team. Score is **{enemyffscore}** for **{efaction_name}**")  
                                                history = f'⛩️ **Bridger** ⛩️ **{efaction_name} Got 3 Points**' 
                                            else:
                                                
                                                enemyffscore = war_data["enemyscore"] + 1
                                                self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": 1}})   
                                                

                                            
                                            if powerups[1] == '2':
                                                pow2 = powerups[3]
                                                powerups = f'101{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": -2}})   
                                                allyffscore = war_data["allyscore"] - 2

                                                enemyffscore = war_data["enemyscore"]- 1
                                                self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": -1}})

                                                await ctx.send(f"⚔️ **Jeopardy** ⚔️ 2 points were deducted from the loser's team. Score is **{allyffscore}** for **{faction_name}**") 
                                                history = f'⚔️ **Jeopardy** ⚔️ **{faction_name} Lost 2 Points**'      

                                            pow1 = powerups[1]
                                            pow2 = powerups[3]

                                            if powerups[1] == 'a':
                                                powerups = f'111{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                pow1 = '1'
                                                try:
                                                    await opponent.send("🛡️ Immunity is now active for the next match.")
                                                except Exception as e:
                                                    pass      
                                            elif powerups[1] == 'b':
                                                powerups = f'121{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                pow1 = '2'
                                                try:
                                                    await opponent.send("⚔️ Jeopardy is now active for the next match.")
                                                except Exception as e:
                                                    pass                                                  
                                            elif powerups[1] == 'c':
                                                powerups = f'131{pow2}'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                pow1 = '3'
                                                try:
                                                    await opponent.send("⛩️ Bridger is now active for the next match.")
                                                except Exception as e:
                                                    pass      
                                                
                                            if powerups[3] == 'a':
                                                powerups = f'1{pow1}11'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                try:
                                                    await player.send("🛡️ Immunity is now active for the next match.")
                                                except Exception as e:
                                                    pass      
                                            elif powerups[3] == 'b':
                                                powerups = f'1{pow1}12'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                try:
                                                    await player.send("⚔️ Jeopardy is now active for the next match.")
                                                except Exception as e:
                                                    pass 
                                            elif powerups[3] == 'c':
                                                powerups = f'1{pow1}13'
                                                self.faction.update_one({"_id":warid}, {"$set": {"powerups": powerups}})
                                                try:
                                                    await player.send("⛩️ Bridger is now active for the next match.")
                                                except Exception as e:
                                                    pass   

                                        await ctx.send(f"{player.mention} Won. Updated war scores")

                                        faction_name = war_data['teamone']
                                        efaction_name = war_data['teamtwo']

                                        ranked_battle_embed = discord.Embed(
                                            title = f'{faction_name} {allyffscore} VS {efaction_name} {enemyffscore} {warid}',
                                            description = f'{player.mention} beat {opponent.mention} in {ctx.message.channel.mention}\n**Message Link** {ctx.message.jump_url}',
                                            colour = color
                                        )

                                        ranking_channel = self.bot.get_channel(1093609140921843802)

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
                                            self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                            self.faction.update_one({"_id": warid}, {"$push": {"history": f'🟢 **Won** `{player.name}` ⚔️ 🔴 **Lost** `{opponent.name}`'}})
                                            if history != None:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": history}})                                               
                                        elif loser == player.id:
                                            self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                            self.faction.update_one({"_id": warid}, {"$push": {"history": f'🔴 **Lost** `{opponent.name}` ⚔️ 🟢 **Won** `{player.name}`'}})
                                            if history != None:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": history}})            

                                        await warcheck(self,ctx, warid, allyffscore, enemyffscore)

                                elif  formats == 'koth':   
                                    if winner == player.id:
                                        allyffscore = war_data['allyscore']
                                        enemyffscore = war_data['enemyscore']
                                        allymembers = war_data['allymembers']
                                        allyscore = war_data['allyplayerscore']
                                        enemymembers = war_data['enemymembers']
                                        enemyscore = war_data['enemyplayerscore']
                                        ally_score = list(zip(allymembers,allyscore,enemymembers,enemyscore))
                                        allymembers = []
                                        allymembers2 = []
                                        allyscore = []
                                        allyscore2 = []
                                        enemymembers = []
                                        enemymembers2 = []
                                        enemyscore = []
                                        enemyscore2 = []
                                        for i in ally_score:
                                            scorelist = list(i)
                                            if enemyffscore >0:
                                                crudescore1 = int(scorelist[0])
                                                allyzunit = f'~~<@{crudescore1}>~~'
                                                allymembers2.append(allyzunit)
                                                crudescore2 = str(scorelist[1])
                                                allyscore2.append(crudescore2)
                                                enemyffscore -= 1

                                            else:
                                                crudescore1 = int(scorelist[0])
                                                allyunit = f'<@{crudescore1}>'
                                                allymembers.append(allyunit)
                                                crudescore2 = str(scorelist[1])
                                                allyscore.append(crudescore2)                      
                                            
                                            if allyffscore >0:
                                                crudescore3 = int(scorelist[2])
                                                enemyzunit = f'~~<@{crudescore3}>~~'
                                                enemymembers2.append(enemyzunit)
                                                crudescore4 = str(scorelist[3])
                                                enemyscore2.append(crudescore4)
                                                allyffscore -= 1 
                                            else:
                                                crudescore3 = int(scorelist[2])
                                                enemyunit = f'<@{crudescore3}>'                                
                                                enemymembers.append(enemyunit)
                                                crudescore4 = str(scorelist[3])
                                                enemyscore.append(crudescore4)
                                        allymembers.extend(allymembers2)    
                                        allyscore.extend(allyscore2)
                                        enemymembers.extend(enemymembers2)
                                        enemyscore.extend(enemyscore2)
                                        if (allymembers[0] == f'<@{player.id}>') and (enemymembers[0] == f'<@{opponent.id}>'):        

                                            allymembers = war_data["allymembers"]
                                            actualally = []
                                            for i in allymembers:
                                                actualally.append(i)
                                            indexally = actualally.index(winner)
                                            allyscore = war_data["allyplayerscore"]
                                            allyscore[indexally] += 1
                                            allyscored = war_data["allyplayerscored"]
                                            allyscored[indexally] += 1

                                            enemymembers = war_data["enemymembers"]
                                            actualenemy = []
                                            for i in enemymembers:
                                                actualenemy.append(i)
                                            indexallyd = actualenemy.index(loser)
                                            enemyscored = war_data["enemyplayerscored"]
                                            enemyscored[indexallyd] += 1
                                            self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscored": enemyscored}})    

                                            self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscored": allyscored}})
                                            self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscore": allyscore}})
                                            self.faction.update_one({"_id":warid}, {"$inc": {"allyscore": 1}})
                                            allyffscore = war_data["allyscore"] + 1
                                            enemyffscore = war_data["enemyscore"]
                                            await ctx.send(f"{player.mention} Won. Updated war scores")
                                            faction_name = war_data['teamone']
                                            efaction_name = war_data['teamtwo']
                                            allyffscore = war_data['allyscore']+ 1
                                            denemyffscore = war_data['enemyscore']

                                            ranked_battle_embed = discord.Embed(
                                                title = f'{faction_name} {allyffscore} VS {efaction_name} {denemyffscore} {warid}',
                                                description = f'{player.mention} beat {opponent.mention} in {ctx.message.channel.mention}\n**Message Link** {ctx.message.jump_url}',
                                                colour = color
                                            )

                                            ranking_channel = self.bot.get_channel(1093609140921843802)

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

                                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, player.id)                                              
                                            if winner == player.id:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": f'🟢 **Won** `{player.name}` ⚔️ 🔴 **Lost** `{opponent.name}`'}})
                                                
                                            elif loser == player.id:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": f'🔴 **Lost** `{opponent.name}` ⚔️ 🟢 **Won** `{player.name}`'}})
                                                
                                            await warcheck(self,ctx, warid, allyffscore, enemyffscore)
                                        else:
                                            await ctx.send("Either you or you opponent isn't supposed to battle.")
                                    else:
                                        allyffscore = war_data['allyscore']
                                        enemyffscore = war_data['enemyscore']
                                        allymembers = war_data['allymembers']
                                        allyscore = war_data['allyplayerscore']
                                        enemymembers = war_data['enemymembers']
                                        enemyscore = war_data['enemyplayerscore']
                                        ally_score = list(zip(allymembers,allyscore,enemymembers,enemyscore))

                                        allymembers = []
                                        allymembers2 = []
                                        allyscore = []
                                        allyscore2 = []
                                        enemymembers = []
                                        enemymembers2 = []
                                        enemyscore = []
                                        enemyscore2 = []
                                        for i in ally_score:
                                            scorelist = list(i)
                                            if enemyffscore >0:
                                                crudescore1 = int(scorelist[0])
                                                allyzunit = f'~~<@{crudescore1}>~~'
                                                allymembers2.append(allyzunit)
                                                crudescore2 = str(scorelist[1])
                                                allyscore2.append(crudescore2)
                                                enemyffscore -= 1

                                            else:
                                                crudescore1 = int(scorelist[0])
                                                allyunit = f'<@{crudescore1}>'
                                                allymembers.append(allyunit)
                                                crudescore2 = str(scorelist[1])
                                                allyscore.append(crudescore2)                      
                                            
                                            if allyffscore >0:
                                                crudescore3 = int(scorelist[2])
                                                enemyzunit = f'~~<@{crudescore3}>~~'
                                                enemymembers2.append(enemyzunit)
                                                crudescore4 = str(scorelist[3])
                                                enemyscore2.append(crudescore4)
                                                allyffscore -= 1 
                                            else:
                                                crudescore3 = int(scorelist[2])
                                                enemyunit = f'<@{crudescore3}>'                                
                                                enemymembers.append(enemyunit)
                                                crudescore4 = str(scorelist[3])
                                                enemyscore.append(crudescore4)
                                        allymembers.extend(allymembers2)    
                                        allyscore.extend(allyscore2)
                                        enemymembers.extend(enemymembers2)
                                        enemyscore.extend(enemyscore2)
                                        if (allymembers[0] == f'<@{opponent.id}>') and (enemymembers[0] ==  f'<@{player.id}>'):        

                                            enemymembers = war_data["enemymembers"]
                                            actualenemy = []
                                            for i in enemymembers:
                                                actualenemy.append(i)
                                            indexenemy = actualenemy.index(loser)
                                            enemyscore = war_data["enemyplayerscore"]
                                            enemyscore[indexenemy] += 1
                                            enemyscored = war_data["enemyplayerscored"]
                                            enemyscored[indexenemy] += 1
                                            self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscored": enemyscored}})
                                            self.faction.update_one({"_id":warid}, {"$set": {"enemyplayerscore": enemyscore}})
                                            self.faction.update_one({"_id":warid}, {"$inc": {"enemyscore": 1}})


                                            allymembers = war_data["allymembers"]
                                            actualally = []
                                            for i in allymembers:
                                                actualally.append(i)
                                            indexallyd = actualally.index(winner)
                                            allyscored = war_data["allyplayerscored"]
                                            allyscored[indexallyd] += 1
                                            self.faction.update_one({"_id":warid}, {"$set": {"allyplayerscored": allyscored}})    
                                        

                                            allyffscore = war_data["allyscore"]
                                            enemyffscore = war_data["enemyscore"] + 1
                                            await ctx.send(f"{player.mention} Won. Updated war scores")
                                            faction_name = war_data['teamone']
                                            efaction_name = war_data['teamtwo']
                                            allyffscore = war_data['allyscore'] 
                                            denemyffscore = war_data['enemyscore']+ 1

                                            ranked_battle_embed = discord.Embed(
                                                title = f'{faction_name} {allyffscore} VS {efaction_name} {denemyffscore} {warid}',
                                                description = f'{player.author.mention} beat {opponent.mention} in {ctx.message.channel.mention}\n**Message Link** {ctx.message.jump_url}',
                                                colour = color
                                            )

                                            ranking_channel = self.bot.get_channel(1093609140921843802)

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
                                                        await self.bot.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',  player.id)
                                                        await self.bot.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',  player.id)
                                                        await ctx.send("**Gold Achievement Completed! ✦✦✦ Win 500 Clan Duels ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                                    admin = int(admin) + 1
                                                    new_admins += f' {admin}'                                                       
                                                else:
                                                    new_admins += f' {admin}'  

                                            await self.bot.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins, player.id)                                              
                                            if winner == player.id:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": f'🟢 **Won** `{player.name}` ⚔️ 🔴 **Lost** `{opponent.name}`'}})
                                                
                                            elif loser == player.id:
                                                self.faction.update_one({"_id": warid, "history": {"$size": 5}}, {"$pop": {"history": -1}})
                                                self.faction.update_one({"_id": warid}, {"$push": {"history": f'🔴 **Lost** `{opponent.name}` ⚔️ 🟢 **Won** `{player.name}`'}})
                                    
                                            await warcheck(self,ctx, warid, allyffscore, enemyffscore)            
                                        else:
                                            await ctx.send("Its not you're opponent's turn yet!")                                    

                
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


    @commands.command(name = 'track')
    async def track_log_command(self, ctx, member : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
        
        if registered_check:
            if (member is None):
                em = discord.Embed(
                    title = 'Track Pokemons',
                    description = '**Initialize a PokeTwo Duel using Dom bot to avoid any mishaps**\n\nd!track [mention]',
                    colour = color
                )

                await ctx.send(embed = em)
            
            else:
                member_registered = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                if member_registered:

                    users = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1', ctx.author.id)
                    players = await self.bot.db.fetch('SELECT * FROM casual WHERE player_id = $1',  member.id)

                    if (users) and (players):

 
                        user_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', ctx.author.id)

                        player_ban_list = await self.bot.db.fetch('SELECT rank_bans FROM bans WHERE rank_bans = $1', member.id)


                        if (not user_ban_list) and (not player_ban_list):
                            if ctx.author.id != member.id:

                                await ctx.author.send('Please use the following command,\n\n`d!poke [poke1 name] [poke1 iv] [poke1 mint] [poke2 name] [poke2 iv] [poke2 mint] [poke3 name] [poke3 iv] [poke3 mint]`')
                                await member.send('Please use the following command,\n\n`d!poke [poke1 name] [poke1 iv] [poke1 mint] [poke2 name] [poke2 iv] [poke2 mint] [poke3 name] [poke3 iv] [poke3 mint]`')
                                
                                poke1 = f'{ctx.message.channel.id} {member.id}'
                                poke2 = f'{ctx.message.channel.id} {ctx.author.id}'
                                await self.bot.db.execute(f'UPDATE registered SET duel = $1 WHERE player_id = $2',poke1,  ctx.author.id)
                                await self.bot.db.execute(f'UPDATE registered SET duel = $1 WHERE player_id = $2',poke2,  member.id)

                                await ctx.send(f"Check your DMs and enter the pokemons. {ctx.author.mention} {member.mention}")                                
 
                        

                            elif ctx.author.id == member.id:
                                await ctx.send('You cannot initialize a duel with yourself!')

                        elif not user_ban_list and player_ban_list:
                            await ctx.send('That person is banned from Dom Bot!')

                        elif user_ban_list and not player_ban_list:
                            await ctx.send('You are banned from Dom bot!.')

                        elif user_ban_list and player_ban_list:
                            await ctx.send('Both of you are banned from Dom bot!.')

                    else:
                        await ctx.send('One of you have not registered yet!')

                else:
                    await ctx.send('That person has not registered yet! Use `d!start` to register.')

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')  

    @commands.command(name = 'poke',  aliases = ['pokes', 'pokemon'])
    async def poke_command(self, ctx, *, poke):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:  

            duel = registered_check[0]['duel'] 
            if duel == None:
                await ctx.send("You need to first initialize a duel, `d!track @mention`")
                return
            listform = duel.split(' ')
            if len(listform) >2:
                duel = f'{listform[0]} {listform[1]}'
            duelenemy = listform[1]
            duelchannel = listform[0]
            duel += poke
            await self.bot.db.execute(f'UPDATE registered SET duel = $1 WHERE player_id = $2',duel,  ctx.author.id)


            
        else:
            await ctx.send("You haven't registered yet! Please do `d!start` do register.")

def setup(bot):
    bot.add_cog(TourneyCommands(bot))