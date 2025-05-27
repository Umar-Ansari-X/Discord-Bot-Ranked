import discord
import asyncpg
from discord.ext import commands, tasks
import json
import asyncio
from pymongo import MongoClient
import os
from PIL import Image
import re
from datetime import datetime, timedelta


intents = discord.Intents.all()

async def get_prefix(bot, message):
    list = ["V.", "v.",f"<@{client.application_id}>", f"<@{client.application_id}>" ]
    return commands.when_mentioned_or(*list)(bot, message)

client = commands.Bot(command_prefix = get_prefix, case_insensitive = True, intents = intents)

client.remove_command('help')

cluster = MongoClient("####")
database = cluster['discord']
collection = database["faction"]
faction = database["wars"]

os.chdir(r"C:\Users\Hi\Documents\codes\dominant_bot\bot_files\database")

async def create_db_pool():
    client.db = await asyncpg.create_pool(dsn='####', max_size=5, min_size=1
    )

@client.event
async def on_ready():

    ranked_players = await client.db.fetch('SELECT player_id FROM rank_system')
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, 
                                                                name = f'{len(ranked_players)} players play Ranked Battles'))
    daily_update_task.start()
    print('Bot is ready!')

@tasks.loop(hours=1)
async def daily_update_task():
    guild_id = 774883579472904222
    record = await client.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

    timer = record[0]['timer']

    if timer is None or timer + timedelta(hours=24) <= datetime.utcnow():
        await update_daily()
        await client.db.execute('UPDATE server_constants SET timer = $1', datetime.utcnow())

async def update_daily():

    stut = 'rank_system'
    lb = await client.db.fetch('SELECT * FROM rank_system WHERE matches_played >= 0 ORDER BY daily DESC LIMIT 3')

    player = [row['player_id'] for row in lb]
    playerstr = ''

    for t,v in enumerate(player):
        if t == 0:
            dc = 2
        elif t == 1:
            dc = 1
        elif t == 2:
            dc = 1

        await client.db.execute(f'UPDATE registered SET wishes = wishes + {dc} WHERE player_id = $1', player[t])
                                                                                                                                                                                                        
        playerstr += f'<@{v}> Won **{dc} Lootbox**\n'


    await client.db.execute(f'UPDATE {stut} SET daily = 0')
    channel = client.get_channel()

    await channel.send(f'Daily Rare leaderboard rewards are here! Here are the results..\n{playerstr}')    

    stut = 'common_system'
    lb = await client.db.fetch('SELECT * FROM common_system WHERE matches_played >= 0 ORDER BY daily DESC LIMIT 3')


    player = [row['player_id'] for row in lb]
    playerstr = ''

    for t,v in enumerate(player):
        if t == 0:
            dc = 2
        elif t == 1:
            dc = 1
        elif t == 2:
            dc = 1


        await client.db.execute(f'UPDATE registered SET wishes = wishes + {dc} WHERE player_id = $1', player[t])
                                                                                                                                                                                                        
        playerstr += f'<@{v}> Won **{dc} Lootbox**\n'


    await client.db.execute(f'UPDATE {stut} SET daily = 0')
    channel = client.get_channel()

    await channel.send(f'Daily Common leaderboard rewards are here! Here are the results..\n{playerstr}')    


@client.command(name = 'ping')
async def ping_command(ctx):
    await ctx.send(f'Pong! **{int(client.latency * 1000)}ms**')

@client.event
async def on_guild_join(guild):
    guild_id = guild.id

    server = await client.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

    if server:
        return

    else:
        await client.db.execute('INSERT INTO server_constants (guild_id, admins, tourney_status, ranked_enable) VALUES ($1, $2, 0, 0)', guild_id, str(939848059314130984))

        return

@client.event
async def on_member_remove(member):
    registered = await client.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

    if registered:
        clan_name = registered[0]['clan_1']
        if clan_name is not None:  
            collection.update_one({"_id": str(clan_name.title())}, {"$pull": {"members": member.id}})

            await client.db.execute('UPDATE registered SET clan_1 = NULL, current_banner = NULL, title = NULL, banner_border = NULL, avatar_border = NULL WHERE player_id = $1', member.id)
        
        return

    else:
        return

@client.command(name = "amogus")
async def amogus(ctx):
    with open("datas.json", "r") as f:
        data = json.load(f)

    ranked_players = await client.db.fetch("SELECT * FROM rank_system")

    for i in ranked_players:
   
        playerID = str(i["player_id"])

        data[playerID] = {}
        data[playerID]["rank"] = i["player_rank"]
        data[playerID]["rankValue"] = i["rank_value"]
        data[playerID]["points"] = i["points"]
        data[playerID]["wins"] = i["wins"]
        data[playerID]["matches"] = i["matches_played"]
        data[playerID]["streak"] = i["streak"]
        data[playerID]["floor"] = i["rank_floor"]
        data[playerID]["opponent"] = None
 

    with open("datas.json", "w") as f:
        json.dump(data, f, indent = 2)

    await ctx.send("no")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = '**Still on cooldown**, please try again in {:.2f}s'.format(error.retry_after)

        await ctx.send(msg)

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

class ConfirmCancel(discord.ui.View):
    def __init__(self, member : discord.Member):
        super().__init__(timeout = 60)

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

@client.listen()
async def on_message(ctx):

    return

    alliesList = ctx.mentions

    if (nospaces.startswith("<@716390085896962058>trade")) or (nospaces.startswith("<@716390085896962058>t")):
        if  len(alliesList) == 2:

            profile = await client.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)
            channel = client.get_channel(ctx.channel.id)
            if profile:
                profile2 = await client.db.fetch('SELECT * FROM gamble WHERE player_id = $1', ctx.author.id)

                if ctx.author.nick == None:

                    if ctx.author.global_name == None:
                        name = ctx.author.name
                    else:
                        name = ctx.author.global_name
                else:
                    name = ctx.author.nick
                
                if profile2[0]['player_name'] == name:
                    pass
                else:
                    await client.db.execute(f'UPDATE gamble SET player_name = $1 WHERE player_id = $2', name, ctx.author.id)      
                        
            else:
                await channel.send(f"Please do `d!start` {ctx.author.mention} and send the trade again or this trade wont be recorded for either user.")
            
            

            member = alliesList[1]
            gamba = await client.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)
            if gamba:
                gamba2 = await client.db.fetch('SELECT * FROM gamble WHERE player_id = $1', member.id)

                if member.nick == None:
                    if member.global_name == None:
                        name2 = member.name
                    else:
                        name2 = member.global_name
                else:
                    name2 = member.nick

                if gamba2[0]['player_name'] == name2:
                    pass
                else:
                    await client.db.execute(f'UPDATE gamble SET player_name = $1 WHERE player_id = $2', name2, member.id)       
            else:
                await channel.send(f"Please do `d!start` {member.mention} and send the trade again or this trade wont be recorded for either user.")                    
                
        else:
            pass

    else:
        pass


    if ctx.author.id == 716390085896962058:
        if isinstance(ctx.embeds, list) and len(ctx.embeds) > 0:
            
            embed = ctx.embeds[0]

            titles = embed.title
            value_partsd = titles.split('\n')
            if value_partsd[0].split()[0] == "✅":

                fields = embed.fields
                
                if len(fields) > 0:
                    
                    channel = client.get_channel(ctx.channel.id)
                    
                    first_field = fields[0]
                    
                    vb = first_field.name
        
                    value_partsds = vb.replace("🟢 ", "")                       
                    nameone = value_partsds
                
                    
                    
                    registered_check = await client.db.fetch('SELECT * FROM gamble WHERE player_name = $1', nameone)

                    onevalue_parts = first_field.value.split('\n')
                    noneis = onevalue_parts[0]

                    second_field = fields[1]
                    secondvalue_parts = second_field.value.split('\n')
                    noneisto = secondvalue_parts[0]

                    vb = second_field.name
                    
                    value_partsds = vb.replace("🟢 ", "")                        
                    nametwo = value_partsds
                    
                    member_check = await client.db.fetch('SELECT * FROM gamble WHERE player_name = $1', nametwo)
                    if member_check:
                        pass
                    else:
                        await channel.send(f"Please update your registered name, use `d!update` to update your name. **{nametwo}**")
                        return
                    if registered_check:
                        pass
                    else:
                        await channel.send(f"Please update your registered name, use `d!update` to update your name. **{nameone}**")
                        return
                    
                    if ((noneis == 'None') and (noneisto == 'None')) or ((noneis != 'None') and (noneisto != 'None')):
                        await channel.send("Trades for other purposes are not allowed here except gambling, make sure that only one user is adding an item.")
                        return
                    elif noneis == "None":
                        onecoins = 0
                        cancel1 = 'yes'
                        cancel2 = 'no'
                    elif noneisto == "None":
                        secondcoins = 0
                        cancel1 = 'no'
                        cancel2 = 'yes'

                    onevalue_parts = first_field.value.split('\n')
                    
                    onecoins = 0
                    if cancel1 == 'yes':
                        pass
                        
                    else:
            
                        for i in onevalue_parts:
                            if i.split()[1] == 'Pokécoins':
                                onecoins = i.split()[0]
                                onecoins = int(onecoins.replace(",", ""))

                            elif i.split()[1] == 'redeems':
                                secondcoins +=  (40000*int(i.split()[0]))


                            else:
                                text = i
                                percentage = float(text[-6:-1])
                                
                                word = text[text.find('**') + 2:text.rfind('**')]

                                starter = word.split()[0]

                                rares=    [
                                        "Mew", "Celebi", "Jirachi", "Deoxys", "Phione", "Manaphy", "Darkrai", "Shaymin", "Arceus",
                                        "Victini", "Keldeo", "Meloetta", "Genesect", "Diancie", "Hoopa", "Volcanion", "Magearna",
                                        "Marshadow", "Zeraora", "Meltan", "Melmetal", "Articuno", "Zapdos", "Moltres", "Mewtwo",
                                        "Raikou", "Entei", "Suicune", "Lugia", "Ho-Oh", "Regirock", "Regice", "Registeel", "Latias",
                                        "Latios", "Kyogre", "Groudon", "Rayquaza", "Uxie", "Mesprit", "Azelf", "Dialga", "Palkia",
                                        "Heatran", "Regigigas", "Giratina", "Cresselia", "Cobalion", "Terrakion", "Virizion",
                                        "Tornadus", "Thundurus", "Reshiram", "Zekrom", "Landorus", "Kyurem", "Xerneas", "Yveltal",
                                        "Zygarde", "Type:", "Silvally", "Tapu",
                                        "Cosmog", "Cosmoem", "Solgaleo", "Lunala", "Necrozma", "Nihilego", "Buzzwole", "Pheromosa",
                                        "Xurkitree", "Celesteela", "Kartana", "Guzzlord", "Poipole", "Naganadel", "Stakataka",
                                        "Blacephalon", "Zacian", "Zamazenta", "Eternatus", "Kubfu", "Urshifu", "Regieleki",
                                        "Regidrago", "Glastrier", "Spectrier", "Calyrex", "Enamorus", "Miraidon", "Koraidon", "Chien-pao", "Chi-yu", "Wo-chien", "Ting-lu"
                                    ]
                            
                                if starter == "✨":
                                    shiny = word.split()[1]
                                    if shiny == 'Alolan':
                                        poke = word.split()[2]
                                        if poke == 'Vulpix':
                                            if 9 >= percentage >= 0:
                                                onecoins += 100000000
                                            elif 80 >= percentage >9:
                                                onecoins += 12000000
                                            elif 90 >= percentage > 80:
                                                onecoins += 40000000
                                            elif 100 >= percentage > 90:
                                                onecoins += 100000000
                                            else:
                                                await channel.send("error")    
                                        elif poke == 'Ninetales':
                                            if 9 >= percentage >= 0:
                                                onecoins += 100000000
                                            elif 80 >= percentage >9:
                                                onecoins += 9000000
                                            elif 90 >= percentage > 80:
                                                onecoins += 30000000
                                            elif 100 >= percentage > 90:
                                                onecoins += 100000000
                                            else:
                                                await channel.send("error")                                                                                                                                            
                                        else:
                                            if 9 >= percentage >= 0:
                                                onecoins += 100000000
                                            elif 80 >= percentage >9:
                                                onecoins += 500000
                                            elif 90 >= percentage > 80:
                                                onecoins += 7000000
                                            elif 100 >= percentage > 90:
                                                onecoins += 100000000
                                            else:
                                                await channel.send("error")

                                    elif shiny == 'Galarian':
                                        poke = word.split()[2]
                                        if (poke == 'Articuno') or (poke == 'Moltres') or (poke == 'Zapdos'):
                                            if 9 >= percentage >= 0:
                                                onecoins += 100000000
                                            elif 80 >= percentage >9:
                                                onecoins += 10000000
                                            elif 90 >= percentage > 80:
                                                onecoins += 40000000
                                            elif 100 >= percentage > 90:
                                                onecoins += 100000000
                                            else:
                                                await channel.send("error")    
                                        elif poke == 'Ponyta':
                                            if 9 >= percentage >= 0:
                                                onecoins += 100000000
                                            elif 80 >= percentage >9:
                                                onecoins += 6000000
                                            elif 90 >= percentage > 80:
                                                onecoins += 30000000
                                            elif 100 >= percentage > 90:
                                                onecoins += 100000000
                                            else:
                                                await channel.send("error")                                        
                                        else:                                               
                                            if 9 >= percentage >= 0:
                                                onecoins += 100000000
                                            elif 80 >= percentage >9:
                                                onecoins += 1500000
                                            elif 90 >= percentage > 80:
                                                onecoins += 7000000
                                            elif 100 >= percentage > 90:
                                                onecoins += 100000000
                                            else:
                                                await channel.send("error")      

                                    elif shiny == 'Hisuian':

                                        if 9 >= percentage >= 0:
                                            onecoins += 100000000
                                        elif 80 >= percentage >9:
                                            onecoins += 1500000
                                        elif 90 >= percentage > 80:
                                            onecoins += 7000000
                                        elif 100 >= percentage > 90:
                                            onecoins += 100000000
                                        else:
                                            await channel.send("error")     

                                    elif (shiny in rares) or (starter == 'Primal'):

                                        if 9 >= percentage >= 0:
                                            onecoins += 100000000
                                        elif 80 >= percentage >9:
                                            onecoins += 5000000
                                        elif 90 >= percentage > 80:
                                            onecoins += 40000000
                                        elif 100 >= percentage > 90:
                                            onecoins += 100000000
                                        else:
                                            await channel.send("error") 
                                
                                    else:

                                        if 9 >= percentage >= 0:
                                            onecoins += 8000000
                                        elif 80 >= percentage >9:
                                            onecoins += 50000
                                        elif 90 >= percentage > 80:
                                            onecoins += 1000000
                                        elif 100 >= percentage > 90:
                                            onecoins += 8000000
                                        else:
                                            await channel.send("error") 


                                elif starter == 'Alolan':
                                    if 9 >= percentage >= 0:
                                        onecoins += 250000
                                    elif 80 >= percentage >9:
                                        onecoins += 800
                                    elif 90 >= percentage > 80:
                                        onecoins += 8000
                                    elif 100 >= percentage > 90:
                                        onecoins += 250000
                                    else:
                                        await channel.send("error")

                                elif starter == 'Galarian':
                                    if 9 >= percentage >= 0:
                                        onecoins += 500000
                                    elif 80 >= percentage >9:
                                        onecoins += 150
                                    elif 90 >= percentage > 80:
                                        onecoins += 15000
                                    elif 100 >= percentage > 90:
                                        onecoins += 500000
                                    else:
                                        await channel.send("error")      

                                elif starter == 'Hisuian':

                                    if 9 >= percentage >= 0:
                                        onecoins += 600000
                                    elif 80 >= percentage >9:
                                        onecoins += 300
                                    elif 90 >= percentage > 80:
                                        onecoins += 15000
                                    elif 100 >= percentage > 90:
                                        onecoins += 600000
                                    else:
                                        await channel.send("error")     

                                elif (starter in rares) or (starter == 'Primal'):

                                    if 9 >= percentage >= 0:
                                        onecoins += 350000
                                    elif 80 >= percentage >9:
                                        onecoins += 1000
                                    elif 90 >= percentage > 80:
                                        onecoins += 15000
                                    elif 100 >= percentage > 90:
                                        onecoins += 450000
                                    else:
                                        await channel.send("error") 
                                
                                else:

                                    if 9 >= percentage >= 0:
                                        onecoins += 10000
                                    elif 80 >= percentage >9:
                                        onecoins += 2
                                    elif 90 >= percentage > 80:
                                        onecoins += 10
                                    elif 100 >= percentage > 90:
                                        onecoins += 20000
                                    else:
                                        await channel.send("error") 



                
                    secondvalue_parts = second_field.value.split('\n')
                    secondcoins = 0
                    if cancel2 == 'yes':
                        pass
                    else:
                
                        for i in secondvalue_parts:
                            if i.split()[1] == 'Pokécoins':
                                secondcoins = i.split()[0]
                                secondcoins = int(secondcoins.replace(",", ""))

                            elif i.split()[1] == 'redeems':
                                secondcoins +=  (40000*int(i.split()[0]))

                            else:

                                text = i
                                percentage = float(text[-6:-1])
                                word = text[text.find('**') + 2:text.rfind('**')]

                                starter = word.split()[0]

                                rares=    [
                                        "Mew", "Celebi", "Jirachi", "Deoxys", "Phione", "Manaphy", "Darkrai", "Shaymin", "Arceus",
                                        "Victini", "Keldeo", "Meloetta", "Genesect", "Diancie", "Hoopa", "Volcanion", "Magearna",
                                        "Marshadow", "Zeraora", "Meltan", "Melmetal", "Articuno", "Zapdos", "Moltres", "Mewtwo",
                                        "Raikou", "Entei", "Suicune", "Lugia", "Ho-Oh", "Regirock", "Regice", "Registeel", "Latias",
                                        "Latios", "Kyogre", "Groudon", "Rayquaza", "Uxie", "Mesprit", "Azelf", "Dialga", "Palkia",
                                        "Heatran", "Regigigas", "Giratina", "Cresselia", "Cobalion", "Terrakion", "Virizion",
                                        "Tornadus", "Thundurus", "Reshiram", "Zekrom", "Landorus", "Kyurem", "Xerneas", "Yveltal",
                                        "Zygarde", "Type:", "Silvally", "Tapu",
                                        "Cosmog", "Cosmoem", "Solgaleo", "Lunala", "Necrozma", "Nihilego", "Buzzwole", "Pheromosa",
                                        "Xurkitree", "Celesteela", "Kartana", "Guzzlord", "Poipole", "Naganadel", "Stakataka",
                                        "Blacephalon", "Zacian", "Zamazenta", "Eternatus", "Kubfu", "Urshifu", "Regieleki",
                                        "Regidrago", "Glastrier", "Spectrier", "Calyrex", "Enamorus", "Miraidon", "Koraidon", "Chien-pao", "Chi-yu", "Wo-chien", "Ting-lu"

                                    ]
                                
                                if starter == "✨":
                                    shiny = word.split()[1]
                                    if shiny == 'Alolan':
                                        poke = word.split()[2]
                                        if poke == 'Vulpix':
                                            if 9 >= percentage >= 0:
                                                secondcoins += 100000000
                                            elif 80 >= percentage >9:
                                                secondcoins += 12000000
                                            elif 90 >= percentage > 80:
                                                secondcoins += 40000000
                                            elif 100 >= percentage > 90:
                                                secondcoins += 100000000
                                            else:
                                                await channel.send("error")    
                                        elif poke == 'Ninetales':
                                            if 9 >= percentage >= 0:
                                                secondcoins += 100000000
                                            elif 80 >= percentage >9:
                                                secondcoins += 9000000
                                            elif 90 >= percentage > 80:
                                                secondcoins += 30000000
                                            elif 100 >= percentage > 90:
                                                secondcoins += 100000000
                                            else:
                                                await channel.send("error")                                                                                                                                            
                                        else:
                                            if 9 >= percentage >= 0:
                                                secondcoins += 100000000
                                            elif 80 >= percentage >9:
                                                secondcoins += 500000
                                            elif 90 >= percentage > 80:
                                                secondcoins += 7000000
                                            elif 100 >= percentage > 90:
                                                secondcoins += 100000000
                                            else:
                                                await channel.send("error")

                                    elif shiny == 'Galarian':
                                        poke = word.split()[2]
                                        if (poke == 'Articuno') or (poke == 'Moltres') or (poke == 'Zapdos'):
                                            if 9 >= percentage >= 0:
                                                secondcoins += 100000000
                                            elif 80 >= percentage >9:
                                                secondcoins += 10000000
                                            elif 90 >= percentage > 80:
                                                secondcoins += 40000000
                                            elif 100 >= percentage > 90:
                                                secondcoins += 100000000
                                            else:
                                                await channel.send("error")    
                                        elif poke == 'Ponyta':
                                            if 9 >= percentage >= 0:
                                                secondcoins += 100000000
                                            elif 80 >= percentage >9:
                                                secondcoins += 6000000
                                            elif 90 >= percentage > 80:
                                                secondcoins += 30000000
                                            elif 100 >= percentage > 90:
                                                secondcoins += 100000000
                                            else:
                                                await channel.send("error")                                        
                                        else:                                               
                                            if 9 >= percentage >= 0:
                                                secondcoins += 100000000
                                            elif 80 >= percentage >9:
                                                secondcoins += 1500000
                                            elif 90 >= percentage > 80:
                                                secondcoins += 7000000
                                            elif 100 >= percentage > 90:
                                                secondcoins += 100000000
                                            else:
                                                await channel.send("error")      

                                    elif shiny == 'Hisuian':

                                        if 9 >= percentage >= 0:
                                            secondcoins += 100000000
                                        elif 80 >= percentage >9:
                                            secondcoins += 1500000
                                        elif 90 >= percentage > 80:
                                            secondcoins += 7000000
                                        elif 100 >= percentage > 90:
                                            secondcoins += 100000000
                                        else:
                                            await channel.send("error")     

                                    elif (shiny in rares) or (starter == 'Primal'):

                                        if 9 >= percentage >= 0:
                                            secondcoins += 100000000
                                        elif 80 >= percentage >9:
                                            secondcoins += 5000000
                                        elif 90 >= percentage > 80:
                                            secondcoins += 40000000
                                        elif 100 >= percentage > 90:
                                            secondcoins += 100000000
                                        else:
                                            await channel.send("error") 
                                
                                    else:

                                        if 9 >= percentage >= 0:
                                            secondcoins += 8000000
                                        elif 80 >= percentage >9:
                                            secondcoins += 50000
                                        elif 90 >= percentage > 80:
                                            secondcoins += 1000000
                                        elif 100 >= percentage > 90:
                                            secondcoins += 8000000
                                        else:
                                            await channel.send("error") 


                                elif starter == 'Alolan':
                                    if 9 >= percentage >= 0:
                                        secondcoins += 250000
                                    elif 80 >= percentage >9:
                                        secondcoins += 800
                                    elif 90 >= percentage > 80:
                                        secondcoins += 8000
                                    elif 100 >= percentage > 90:
                                        secondcoins += 250000
                                    else:
                                        await channel.send("error")

                                elif starter == 'Galarian':
                                    if 9 >= percentage >= 0:
                                        secondcoins += 500000
                                    elif 80 >= percentage >9:
                                        secondcoins += 150
                                    elif 90 >= percentage > 80:
                                        secondcoins += 15000
                                    elif 100 >= percentage > 90:
                                        secondcoins += 500000
                                    else:
                                        await channel.send("error")      

                                elif starter == 'Hisuian':

                                    if 9 >= percentage >= 0:
                                        secondcoins += 600000
                                    elif 80 >= percentage >9:
                                        secondcoins += 300
                                    elif 90 >= percentage > 80:
                                        secondcoins += 15000
                                    elif 100 >= percentage > 90:
                                        secondcoins += 600000
                                    else:
                                        await channel.send("error")     

                                elif (starter in rares) or (starter == 'Primal'):

                                    if 9 >= percentage >= 0:
                                        secondcoins += 350000
                                    elif 80 >= percentage >9:
                                        secondcoins += 1000
                                    elif 90 >= percentage > 80:
                                        secondcoins += 15000
                                    elif 100 >= percentage > 90:
                                        secondcoins += 450000
                                    else:
                                        await channel.send("error") 
                                
                                else:

                                    if 9 >= percentage >= 0:
                                        secondcoins += 10000
                                    elif 80 >= percentage >9:
                                        secondcoins += 2
                                    elif 90 >= percentage > 80:
                                        secondcoins += 10
                                    elif 100 >= percentage > 90:
                                        secondcoins += 20000
                                    else:
                                        await channel.send("error") 







                    if onecoins < secondcoins:
                        
                        check = await client.db.fetch('SELECT * FROM registered WHERE player_id = $1', registered_check[0]['player_id'])
                        mcheck = await client.db.fetch('SELECT * FROM registered WHERE player_id = $1', member_check[0]['player_id'])

                        flists = str(check[0]['achievements'])
                        new_admins = ''
                        admins_list = listing(flists)
                        
                        for p,admin in enumerate(admins_list):
                            if p == 0:
                                new_admins += str(admin)                        
                            elif p == 22:
                                if int(admin) == 249:
                                    admins_list[23] = 1
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await channel.send("**Bronze Achievement Completed! ✦ Play 250 Gambles ✦**\n*10dc rewarded & Lootbox rewarded*")
                                elif int(admin) == 499:
                                    admins_list[23] = 2
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await channel.send("**Silver Achievement Completed! ✦✦ Play 500 Gambles ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                elif int(admin) == 999:
                                    admins_list[23] = 3
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await channel.send("**Gold Achievement Completed! ✦✦✦ Play 1000 Gambles ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                admin = int(admin) + 1
                                new_admins +=  f' {admin}'
                            elif p == 20:
                                if int(admin) == 99:
                                    admins_list[21] = 1
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await channel.send("**Bronze Achievement Completed! ✦ Win 100 Gambles ✦**\n*10dc rewarded & Lootbox rewarded*")
                                elif int(admin) == 249:
                                    admins_list[21] = 2
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await channel.send("**Silver Achievement Completed! ✦✦ Win 250 Gambles ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                elif int(admin) == 499:
                                    admins_list[21] = 3
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await channel.send("**Gold Achievement Completed! ✦✦✦ Win 500 Gambles ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                admin = int(admin) + 1
                                new_admins +=  f' {admin}'

                            elif p == 24:
                                if int(admin) < registered_check[0]['streak']:
                                    if int(admin) == 9:
                                        admins_list[25] = 1
                                        await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   registered_check[0]['player_id'])
                                        await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',   registered_check[0]['player_id'])
                                        await channel.send("**Bronze Achievement Completed! ✦ Get a Gamble Streak of 10 ✦**\n*10dc rewarded & Lootbox rewarded*")
                                    elif int(admin) == 14:
                                        admins_list[25] = 2
                                        await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   registered_check[0]['player_id'])
                                        await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',   registered_check[0]['player_id'])
                                        await channel.send("**Silver Achievement Completed! ✦✦ Get a Gamble Streak of 15 ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                    elif int(admin) == 24:
                                        admins_list[25] = 3
                                        await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   registered_check[0]['player_id'])
                                        await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',   registered_check[0]['player_id'])
                                        await channel.send("**Gold Achievement Completed! ✦✦✦ Get a Gamble Streak of 25 ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")  
                                    admin = registered_check[0]['streak']
                                    new_admins +=  f' {admin}'
                                else:
                                    new_admins +=  f' {admin}'                                                           
                            else:
                                new_admins += f' {admin}'  
                        
                        await client.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins,  registered_check[0]['player_id'])    

                        flists = str(mcheck[0]['achievements'])
                        new_admins = ''
                        admins_list =listing(flists)
                        for p,admin in enumerate(admins_list):
                    
                            if p == 0:
                                new_admins += str(admin)                        
                            elif p == 22:
                                if int(admin) == 249:
                                    admins_list[23] = 1
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1', member_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  member_check[0]['player_id'])
                                    await channel.send("**Bronze Achievement Completed! ✦ Play 250 Gambles ✦**\n*10dc rewarded & Lootbox rewarded*")
                                elif int(admin) == 499:
                                    admins_list[23] = 2
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await channel.send("**Silver Achievement Completed! ✦✦ Play 500 Gambles ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                elif int(admin) == 999:
                                    admins_list[23] = 3
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await channel.send("**Gold Achievement Completed! ✦✦✦ Play 1000 Gambles ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                admin = int(admin) + 1
                                new_admins += f' {admin}'                                                       
                            else:
                                new_admins += f' {admin}'  

                        await client.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins,  member_check[0]['player_id'])   

                        if 100000 > secondcoins >= 1:
                            dc = 2
                        elif 400000 > secondcoins >= 100000:
                            dc = 2
                        elif 900000 > secondcoins >= 400000:
                            dc = 2
                        elif 1500000 > secondcoins >= 900000:
                            dc = 3
                        elif 2200000 > secondcoins >= 1500000:
                            dc = 3
                        elif 3000000 > secondcoins >= 2200000:
                            dc = 4
                        elif 3000000 <= secondcoins:
                            dc = 4

                        highest = registered_check[0]['highest']
                        if secondcoins > highest:
                            final = secondcoins
                        
                        elif onecoins > highest:
                            final = onecoins
                        else:
                            final = highest

                        highest1 = member_check[0]['highest']
                        if onecoins > highest:
                            final1 = onecoins
                        elif secondcoins > highest:
                            final1 = secondcoins
                        else:
                            final1 = highest1

                        author = await client.fetch_user(member_check[0]['player_id'])
                        person = await client.fetch_user(registered_check[0]['player_id'])
                        view = ConfirmCancel(author)

                        await channel.send(f"Accept this Gamble Log? {author.mention}\n**{person.name}** **Won {'{:,}'.format(secondcoins)}pc** and **{author.name}** **Won {'{:,}'.format(onecoins)}pc**",view=view)
                        await view.wait()
                        if view.value == True:
                            if member_check[0]['with_player'] == None:
                                testname = 'None'
                            else:
                                testname = member_check[0]['with_player']

                            if member_check[0]['next_player'] == None:
                                timetest = 'None'
                            else:
                                timetest = member_check[0]['next_player']
                            
                            flag = False
                            current_time = datetime.now()
                            if nameone == testname:
                                if timetest >= current_time:
                                    flag = False
                                else:
                                    flag = True
                            else:
                                flag = True

                            if (secondcoins >= 30000) and (flag == True):
                                next_time = datetime.now() + timedelta(minutes=3)
                                await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {dc} WHERE player_id = $1',  registered_check[0]['player_id'])
                                await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 1 WHERE player_id = $1',  member_check[0]['player_id'])
                                await client.db.execute(f'UPDATE gamble SET played = played + 1, won = won + 1,  streak = streak + 1, highest = $1, total = total + {secondcoins}, weekly = weekly + {secondcoins}, with_player = $2, next_player = $3 WHERE player_name = $4', final,nametwo,next_time, nameone)
                                await client.db.execute(f'UPDATE gamble SET streak = 0, played = played + 1, net = net + {secondcoins},highest = $1, weekly = weekly - {secondcoins}, with_player = $2, next_player = $3 WHERE player_name = $4', final1,nameone,next_time, nametwo)        
                                await channel.send(f"Trade logged! **<@{registered_check[0]['player_id']}> Won {'{:,}'.format(secondcoins)}pc** and **<@{member_check[0]['player_id']}> Won {'{:,}'.format(onecoins)}pc**\n*pc calculated is an approx*\n\n**{nameone}** got **{dc}**dc & **{nametwo}** got **1**dc")
                            else:
                                next_time = datetime.now() + timedelta(minutes=3)
                                await client.db.execute(f'UPDATE gamble SET played = played + 1, won = won + 1,  streak = streak + 1, highest = $1, total = total + {secondcoins}, weekly = weekly + {secondcoins}, with_player = $2, next_player = $3 WHERE player_name = $4', final,nametwo,next_time, nameone)
                                await client.db.execute(f'UPDATE gamble SET streak = 0, played = played + 1, net = net + {secondcoins},highest = $1, weekly = weekly - {secondcoins}, with_player = $2, next_player = $3 WHERE player_name = $4', final1,nameone,next_time, nametwo)        
                                await channel.send(f"Trade logged! **<@{registered_check[0]['player_id']}> Won {'{:,}'.format(secondcoins)}pc** and **<@{member_check[0]['player_id']}> Won {'{:,}'.format(onecoins)}pc**\n*pc calculated is an approx*")                                

                        elif view.value == False:
                            await channel.send("Cancelled")
                        else:
                            await channel.send("Timed Out.")

                    else:

                        mcheck = await client.db.fetch('SELECT * FROM registered WHERE player_id = $1', registered_check[0]['player_id'])
                        check = await client.db.fetch('SELECT * FROM registered WHERE player_id = $1', member_check[0]['player_id'])

                        flists = str(check[0]['achievements'])
                        new_admins = ''
                        admins_list = listing(flists)
                        
                        for p,admin in enumerate(admins_list):
                            if p == 0:
                                new_admins += str(admin)                        
                            elif p == 22:
                                if int(admin) == 249:
                                    admins_list[23] = 1
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await channel.send("**Bronze Achievement Completed! ✦ Play 250 Gambles ✦**\n*10dc rewarded & Lootbox rewarded*")
                                elif int(admin) == 499:
                                    admins_list[23] = 2
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await channel.send("**Silver Achievement Completed! ✦✦ Play 500 Gambles ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                elif int(admin) == 999:
                                    admins_list[23] = 3
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await channel.send("**Gold Achievement Completed! ✦✦✦ Play 1000 Gambles ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                admin = int(admin) + 1
                                new_admins +=  f' {admin}'
                            elif p == 20:
                                if int(admin) == 99:
                                    admins_list[21] = 1
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await channel.send("**Bronze Achievement Completed! ✦ Win 100 Gambles ✦**\n*10dc rewarded & Lootbox rewarded*")
                                elif int(admin) == 249:
                                    admins_list[21] = 2
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await channel.send("**Silver Achievement Completed! ✦✦ Win 250 Gambles ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                elif int(admin) == 499:
                                    admins_list[21] = 3
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',   member_check[0]['player_id'])
                                    await channel.send("**Gold Achievement Completed! ✦✦✦ Win 500 Gambles ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                admin = int(admin) + 1
                                new_admins +=  f' {admin}'

                            elif p == 24:
                                if int(admin) < member_check[0]['streak']:
                                    if int(admin) == 9:
                                        admins_list[25] = 1
                                        await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   member_check[0]['player_id'])
                                        await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',   member_check[0]['player_id'])
                                        await channel.send("**Bronze Achievement Completed! ✦ Get a Gamble Streak of 10 ✦**\n*10dc rewarded & Lootbox rewarded*")
                                    elif int(admin) == 14:
                                        admins_list[25] = 2
                                        await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   member_check[0]['player_id'])
                                        await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',   member_check[0]['player_id'])
                                        await channel.send("**Silver Achievement Completed! ✦✦ Get a Gamble Streak of 15 ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                    elif int(admin) == 24:
                                        admins_list[25] = 3
                                        await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   member_check[0]['player_id'])
                                        await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',   member_check[0]['player_id'])
                                        await channel.send("**Gold Achievement Completed! ✦✦✦ Get a Gamble Streak of 25 ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")  
                                    admin = member_check[0]['streak']
                                    new_admins +=  f' {admin}'
                                else:
                                    new_admins +=  f' {admin}'                                                           
                            else:
                                new_admins += f' {admin}'  
                        
                        await client.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins,  member_check[0]['player_id'])    

                        flists = str(mcheck[0]['achievements'])
                        new_admins = ''
                        admins_list =listing(flists)
                        for p,admin in enumerate(admins_list):
                    
                            if p == 0:
                                new_admins += str(admin)                        
                            elif p == 22:
                                if int(admin) == 249:
                                    admins_list[23] = 1
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1', registered_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 10 WHERE player_id = $1',  registered_check[0]['player_id'])
                                    await channel.send("**Bronze Achievement Completed! ✦ Play 250 Gambles ✦**\n*10dc rewarded & Lootbox rewarded*")
                                elif int(admin) == 499:
                                    admins_list[23] = 2
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 25 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await channel.send("**Silver Achievement Completed! ✦✦ Play 500 Gambles ✦✦**\n*25dc rewarded & Lootbox rewarded*")
                                elif int(admin) == 999:
                                    admins_list[23] = 3
                                    await client.db.execute(f'UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 50 WHERE player_id = $1',   registered_check[0]['player_id'])
                                    await channel.send("**Gold Achievement Completed! ✦✦✦ Play 1000 Gambles ✦✦✦**\n*50dc rewarded & Lootbox rewarded*")

                                admin = int(admin) + 1
                                new_admins += f' {admin}'                                                       
                            else:
                                new_admins += f' {admin}'  

                        await client.db.execute(f'UPDATE registered SET achievements = $1 WHERE player_id = $2', new_admins,  registered_check[0]['player_id'])   



                        if 100000 > onecoins >= 1:
                            dc = 1
                        elif 400000 > onecoins >= 100000:
                            dc = 1
                        elif 900000 > onecoins >= 400000:
                            dc = 2
                        elif 1500000 > onecoins >= 900000:
                            dc = 2
                        elif 2200000 > onecoins >= 1500000:
                            dc = 3
                        elif 3000000 > onecoins >= 2200000:
                            dc = 3
                        elif 3000000 <= onecoins:
                            dc = 4

                        

                        highest = member_check[0]['highest']
                        if onecoins > highest:
                            final = onecoins
                        elif secondcoins > highest:
                            final = secondcoins
                        else:
                            final = highest

                        highest1 = registered_check[0]['highest']
                        if onecoins > highest:
                            final1 = onecoins
                        elif secondcoins > highest:
                            final1 = secondcoins
                        else:
                            final1 = highest1

                        author = await client.fetch_user(member_check[0]['player_id'])
                        person = await client.fetch_user(registered_check[0]['player_id'])
                        view = ConfirmCancel(person)

                        await channel.send(f"Accept this Gamble Log? {person.mention}\n**{person.name}** **Won {'{:,}'.format(secondcoins)}pc** and **{author.name}** **Won {'{:,}'.format(onecoins)}pc**",view=view)
                        await view.wait()
                        if view.value == True:

                            if member_check[0]['with_player'] == None:
                                testname = 'None'
                            else:
                                testname = member_check[0]['with_player']

                            if member_check[0]['next_player'] == None:
                                timetest = 'None'
                            else:
                                timetest = member_check[0]['next_player']

                            flag = False
                            current_time = datetime.now()
                            if nameone == testname:
                                if timetest >= current_time:
                                    flag = False
                                else:
                                    flag = True
                            else:
                                flag = True

                            if (onecoins >= 30000) and (flag  == True):
                                
                                next_time = datetime.now() + timedelta(minutes=3)
                                await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + {dc} WHERE player_id = $1',  member_check[0]['player_id'])
                                await client.db.execute(f'UPDATE registered SET banner_pieces = banner_pieces + 1 WHERE player_id = $1',  registered_check[0]['player_id'])
                                await client.db.execute(f'UPDATE gamble SET played = played + 1, won = won + 1, streak = streak + 1, highest = $1, total = total + {onecoins}, weekly = weekly + {onecoins}, with_player = $2, next_player = $3 WHERE player_name = $4',final,nameone,next_time, nametwo)
                                await client.db.execute(f'UPDATE gamble SET streak = 0, played = played + 1,highest = $1,   net = net + {onecoins}, weekly = weekly - {onecoins}, with_player = $2,  next_player = $3 WHERE player_name = $4', final1,nametwo,next_time,nameone)
                                await channel.send(f"Trade logged! **<@{registered_check[0]['player_id']}>** **Won {'{:,}'.format(secondcoins)}pc** and **<@{member_check[0]['player_id']}>** **Won {'{:,}'.format(onecoins)}pc**\n*pc calculated is an approx*\n\n**{nameone}** got **1**dc & **{nametwo}** got **{dc}**dc")
                            else:
                                next_time = datetime.now() + timedelta(minutes=3)
                                await client.db.execute(f'UPDATE gamble SET played = played + 1, won = won + 1, streak = streak + 1, highest = $1, total = total + {onecoins}, weekly = weekly + {onecoins}, with_player = $2, next_player = $3 WHERE player_name = $4',final,nameone,next_time, nametwo)
                                await client.db.execute(f'UPDATE gamble SET streak = 0, played = played + 1,highest = $1,   net = net + {onecoins}, weekly = weekly - {onecoins}, with_player = $2, next_player = $3 WHERE player_name = $4', final1,nametwo,next_time, nameone)
                                await channel.send(f"Trade logged! **<@{registered_check[0]['player_id']}>** **Won {'{:,}'.format(secondcoins)}pc** and **<@{member_check[0]['player_id']}>** **Won {'{:,}'.format(onecoins)}pc**\n*pc calculated is an approx*")                                

                        elif view.value == False:
                            await channel.send("Cancelled")
                        
                        else:
                            await channel.send("Timed Out.")


                else:
                    await channel.send('You have not registered yet! Use `d!start` to register.')
                    
                        

extensions = ['cogs.TourneyCommands', 'cogs.RankCommands', 'cogs.ClanCommands', 
                'cogs.HelpCommands', 'cogs.MiscCommands','cogs.AdminCommands',
                'cogs.RegisteredCommands','cogs.RadCommands', 'cogs.TradeCommands','cogs.SpawnCommands']

if __name__ == '__main__':
    for ext in extensions: 
        client.load_extension(ext)
client.loop.run_until_complete(create_db_pool())
client.run("####")