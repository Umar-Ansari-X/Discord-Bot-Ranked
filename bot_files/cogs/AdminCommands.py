import discord
from discord.ext import commands
import asyncio
import asyncpg
import math

color = 0x32006e

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name = 'admin', invoke_without_command = True)
    async def admin_command(self, ctx):
        if ctx.author.id in [0]:
            em = discord.Embed(
                title = 'Admin',
                description = 'Admin commands:',
                colour = discord.Colour.blue()
            )

            em.add_field(name = 'd!admins', value = 'Displays the current admins for the bot.')
            em.add_field(name = 'd!admin add', value = 'Add new admins for the bot.')
            em.add_field(name = 'd!admin remove', value = 'Remove an existing admin for the bot.')

            await ctx.send(embed = em)

        else:
            await ctx.send("You can't use this command.")

    def listing(self, str1):
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

    def modulus(self, num : int):
        if num is not None:
            if num >= 0:
                modulus_num = num

            elif num < 0:
                modulus_num = num*-1

            return modulus_num

    @admin_command.command(name = 'add', aliases = ['a'])
    async def admin_add_command(self, ctx, member : discord.Member = None):
        if ctx.author.id in [0]:
            if member is None:
                em = discord.Embed(
                    title = 'Admin',
                    description = '**Add a new admin for the bot.**\n\nd!admin add [mention]',
                    colour = discord.Colour.blue()
                )

                await ctx.send(embed = em)

            else:
                guild_id = ctx.guild.id

                member_id = member.id

                server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)
                
                admins = str(server[0]['admins'])
                
                admins_list = self.listing(admins)
                
                if int(member_id) in admins_list:
                    await ctx.send('That person is already an admin!')
                
                else:
                    if server[0]['admins'] is None:
                        
                        await self.bot.db.execute('UPDATE server_constants SET admins = $1 WHERE guild_id = $2', str(member_id), guild_id)

                        await ctx.send(f'{member.mention} has been added as an admin for the bot.')

                    else:
                        new_admins = str(admins) + f' {member_id}'

                        await self.bot.db.execute('UPDATE server_constants SET admins = $1 WHERE guild_id = $2', new_admins, guild_id)

                        await ctx.send(f'{member.mention} has been added as an admin for the bot.')

        else:
            await ctx.send("You can't use this command.")
    @admin_command.command(name = 'remove', aliases = ['r'])
    async def admin_remove_command(self, ctx, member : discord.Member = None):
        if ctx.author.id in [0]:
            if member is None:
                em = discord.Embed(
                    title = 'Admin',
                    description = '**Remove an existing admin for the bot.**\n\nd!admin remove [mention]',
                    colour = discord.Colour.light_grey()
                )

                await ctx.send(embed = em)

            else:
                guild_id = ctx.guild.id

                member_id = member.id

                server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)
                
                admins = str(server[0]['admins'])

                admins_list = self.listing(admins)

                if int(member_id) in admins_list:
                    admins_list.remove(int(member_id))

                    new_admins = ''

                    for admin in admins_list:
                        if admins_list.index(admin) == 0:
                            new_admins += str(admin)

                        else:
                            new_admins += f' {admin}'

                    await self.bot.db.execute('UPDATE server_constants SET admins = $1 WHERE guild_id = $2', new_admins, guild_id)

                    await ctx.send(f'{member.mention} has been removed as an admin of the bot.')

                else:
                    await ctx.send('That person is not an admin!')

        else:
            await ctx.send("You can't use this command.")                
    @commands.command(name = 'admins')
    async def admins_command(self, ctx):
        if ctx.author.id in [0]:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = str(server[0]['admins'])

            admins_list = self.listing(admins)

            admins_str = ''

            for id in admins_list:
                if admins_str == '':
                    admins_str += f'<@{id}>'

                else:
                    admins_str += f', <@{id}>'

            admins_embed = discord.Embed(
                title = 'Current admins of the bot.',
                description = admins_str,
                colour = discord.Colour.dark_magenta()
            )

            await ctx.send(embed = admins_embed)

        else:
            await ctx.send('You do not have permission to use that command.')

    @admin_command.command(name = 'ddsadranklog', aliases = ['rcvbdxlog'])
    async def admin_rank_log_command(self, ctx, winner : discord.Member = None, loser : discord.Member = None, *, score = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = server[0]['admins']

            admins_list = self.listing(admins)

            if int(ctx.author.id) in admins_list:
                if (winner is None) or (loser is None) or (score is None):
                    em = discord.Embed(
                        title = 'Admin',
                        description = '**Log a ranked match.**\n\nd!admin ranklog|rlog [winner mention] [loser mention]',
                        colour = discord.Colour.blue()
                    )

                    await ctx.send(embed = em)

                else:
                    winner_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', winner.id)

                    loser_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', loser.id)

                    if (winner_check) and (loser_check):
                        winner_id = winner.id

                        loser_id = loser.id

                        winner_details = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', winner_id)

                        loser_details = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', loser_id)

                        ranked = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

                        winner_ban_list = await self.bot.db.fetch('SELECT * rank_bans FROM bans WHERE rank_bans = $1', winner_id)

                        loser_ban_list = await self.bot.db.fetch('SELECT * rank_bans FROM bans WHERE rank_bans = $1', loser_id)

                        winner_rank = int(winner_details[0]['rank_value'])

                        loser_rank = int(loser_details[0]['rank_value'])

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
                            if (not winner_ban_list) and (not loser_ban_list):
                                if winner_details and loser_details:
                                    if (self.modulus(winner_rank - loser_rank) <= 1) or (self.modulus(loser_rank - winner_rank) <= 1):
                                        await ctx.send(f'**Remember that the winner is supposed to be mentioned first. For this log** {winner.name} **will be considered as the winner.**')
                                        rank_log_msg = await ctx.send(f'{ctx.author.mention} click the ✅ to confirm the winner and loser or click the ❌ to cancel.')

                                        await rank_log_msg.add_reaction('✅')
                                        await rank_log_msg.add_reaction('❌')

                                        def check(reaction : discord.Reaction, user : discord.User):
                                            return user.id == ctx.author.id and reaction.message.channel.id == ctx.channel.id and str(reaction.emoji) in ['✅', '❌']

                                        try:
                                            reaction_add, user = await self.bot.wait_for(
                                                'reaction_add',
                                                timeout = 10,
                                                check = check
                                            )

                                        except asyncio.TimeoutError:
                                            await ctx.send('Timed-out. Aborted.')
                                            return

                                        else:
                                            if str(reaction_add) == '✅':
                                                ranked_battle_embed = discord.Embed(
                                                    title = 'Ranked Battles',
                                                    description = f'{winner.mention} beat {loser.mention} in {ctx.message.channel.mention}\nScore: {score}'
                                                )

                                                ranked_battle_embed.set_footer(text = 'This was logged by an Admin.')

                                                ranking_channel = self.bot.get_channel(ranked_channel)

                                                await ranking_channel.send(embed = ranked_battle_embed)
                                                await ctx.send('Logged succesfully.')

                                                #Updating both players scores
                                                if (winner_details[0]['matches_played'] >= 10) and (loser_details[0]['matches_played'] >= 10):
                                                    if winner_rank - loser_rank == 1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 9, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 9 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == 0:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 10, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 10 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == -1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 11, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 11 WHERE player_id = $1', loser_id)

                                                elif (winner_details[0]['matches_played'] < 10) and (loser_details[0]['matches_played'] >= 10):
                                                    if winner_rank - loser_rank == 1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 9 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == 0:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 10 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == -1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 11 WHERE player_id = $1', loser_id)

                                                elif (winner_details[0]['matches_played'] >= 10) and (loser_details[0]['matches_played'] < 10):
                                                    if winner_rank - loser_rank == 1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 9, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == 0:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 10, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == -1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 11, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', loser_id)

                                                elif (winner_details[0]['matches_played'] < 10) and (loser_details[0]['matches_played'] < 10):
                                                    if winner_rank - loser_rank == 1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == 0:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == -1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', loser_id)

                                                #Setting streak
                                                await self.bot.db.execute('UPDATE rank_system SET streak = streak + 1 WHERE player_id = $1', winner_id)
                                                await self.bot.db.execute('UPDATE rank_system SET streak = 0 WHERE player_id = $1', loser_id)

                                                #Preventing scores from being negative

                                                winner_details_updated = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', winner_id)
                                                loser_details_updated = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', loser_id)

                                                winner_points = int(winner_details_updated[0]['points'])
                                                loser_points = int(loser_details_updated[0]['points'])

                                                if int(winner_points) < 0:
                                                    await self.bot.db.execute('UPDATE rank_system SET points = 0 WHERE player_id = $1', winner_id)

                                                if int(loser_points) < 0:
                                                    await self.bot.db.execute('UPDATE rank_system SET points = 0 WHERE player_id = $1', loser_id)

                                                #Awarding streak
                                                if winner_details_updated[0]['streak'] >= 20:
                                                    emoji = '<:swiff:930428662711484486>'

                                                    if winner_check[0]['badges'] is None:
                                                        await self.bot.db.execute('UPDATE registered SET badges = $1 WHERE player_id = $2', emoji, winner_id)

                                                    else:
                                                        if emoji not in winner_check[0]['badges'].split():
                                                            new_badges = winner_check[0]['badges'] + f' {emoji}'

                                                            await self.bot.db.execute('UPDATE registered SET badges = $1 WHERE player_id = $2', new_badges, winner_id)

                                                        else:
                                                            pass

                                                if loser_details_updated[0]['streak'] < 0:
                                                    await self.bot.db.execute('UPDATE rank_system SET streak = 0 WHERE player_id = $1', loser_id)
                                                                
                                                #Updating rank of winner

                                                if (int(winner_points) >= 0) and (int(winner_points) <= 83):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze1, bronze_value, winner_id)

                                                elif (int(winner_points) >= 84) and (int(winner_points) <= 167):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze2, bronze_value, winner_id)

                                                elif (int(winner_points) >= 168) and (int(winner_points) <= 250):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze3, bronze_value, winner_id)

                                                elif (int(winner_points) >= 251) and (int(winner_points) <= 333):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver1, silver_value, winner_id)

                                                elif (int(winner_points) >= 334) and (int(winner_points) <= 416):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver2, silver_value, winner_id)

                                                elif (int(winner_points) >= 417) and (int(winner_points) <= 500):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver3, silver_value, winner_id)

                                                elif (int(winner_points) >= 501) and (int(winner_points) <= 583):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold1, gold_value, winner_id)

                                                elif (int(winner_points) >= 584) and (int(winner_points) <= 667):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold2, gold_value, winner_id)

                                                elif (int(winner_points) >= 668) and (int(winner_points) <= 750):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold3, gold_value, winner_id)

                                                elif (int(winner_points) >= 751) and (int(winner_points) <= 833):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum1, platinum_value, winner_id)

                                                elif (int(winner_points) >= 834) and (int(winner_points) <= 916):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum2, platinum_value, winner_id)

                                                elif (int(winner_points) >= 917) and (int(winner_points) <= 1249):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum3, platinum_value, winner_id)

                                                elif int(winner_points) >= 1250:
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', dominant, dominant_value, winner_id)

                                                #Updating rank of loser

                                                if (int(loser_points) >= 0) and (int(loser_points) <= 83):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze1, bronze_value, loser_id)

                                                elif (int(loser_points) >= 84) and (int(loser_points) <= 167):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze2, bronze_value, loser_id)

                                                elif (int(loser_points) >= 168) and (int(loser_points) <= 250):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze3, bronze_value, loser_id)

                                                elif (int(loser_points) >= 251) and (int(loser_points) <= 333):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver1, silver_value, loser_id)

                                                elif (int(loser_points) >= 334) and (int(loser_points) <= 416):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver2, silver_value, loser_id)

                                                elif (int(loser_points) >= 417) and (int(loser_points) <= 500):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver3, silver_value, loser_id)

                                                elif (int(loser_points) >= 501) and (int(loser_points) <= 583):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold1, gold_value, loser_id)

                                                elif (int(loser_points) >= 584) and (int(loser_points) <= 667):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold2, gold_value, loser_id)

                                                elif (int(loser_points) >= 668) and (int(loser_points) <= 750):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold3, gold_value, loser_id)

                                                elif (int(loser_points) >= 751) and (int(loser_points) <= 833):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum1, platinum_value, loser_id)

                                                elif (int(loser_points) >= 834) and (int(loser_points) <= 916):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum2, platinum_value, loser_id)

                                                elif (int(loser_points) >= 917) and (int(loser_points) <= 1249):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum3, platinum_value, loser_id)

                                                elif int(loser_points) >= 1250:
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', dominant, dominant_value, loser_id)

                                                #Giving wishes to 100+ points
                                                if winner_points >= 100:
                                                    if winner_details_updated[0]['streak'] > 2:
                                                        wishes = registered_check[0]['wishes'] + math.ceil((winner_details_updated[0]['streak']/2)) - 1
                                                        await self.bot.db.execute('UPDATE registered SET wishes = $1 WHERE player_id = $2', wishes, winner.id)

                                                    else:
                                                        await self.bot.db.execute('UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1', winner.id)

                                            elif str(reaction_add) == '❌':
                                                await ctx.send('Cancelled.')

                                    elif (winner_details[0]['matches_played'] < 10) or (loser_details[0]['matches_played'] < 10):
                                        await ctx.send(f'**Remember that the winner is supposed to be mentioned first. For this log** {winner.name} **will be considered as the winner.**')
                                        rank_log_msg = await ctx.send(f'{ctx.author.mention} click the ✅ to confirm the winner and loser or ❌ to cancel.')

                                        await rank_log_msg.add_reaction('✅')
                                        await rank_log_msg.add_reaction('❌')

                                        def check(reaction : discord.Reaction, user : discord.User):
                                            return user.id == ctx.author.id and reaction.message.channel.id == ctx.channel.id and str(reaction.emoji) in ['✅', '❌']

                                        try:
                                            reaction_add, user = await self.bot.wait_for(
                                                'reaction_add',
                                                timeout = 10,
                                                check = check
                                            )

                                        except asyncio.TimeoutError:
                                            await ctx.send('Timed-out. Aborted.')
                                            return

                                        else:
                                            if str(reaction_add) == '✅':
                                                ranked_battle_embed = discord.Embed(
                                                    title = 'Ranked Battles',
                                                    description = f'{winner.mention} beat {loser.mention} in {ctx.message.channel.mention}\nScore: {score.content}'
                                                )

                                                ranked_battle_embed.set_footer(text = 'This was logged by an Admin.')

                                                ranking_channel = self.bot.get_channel(ranked_channel)

                                                await ranking_channel.send(embed = ranked_battle_embed)
                                                await ctx.send('Logged succesfully.')

                                                #Updating both players scores
                                                if (winner_details[0]['matches_played'] >= 10) and (loser_details[0]['matches_played'] >= 10):
                                                    if winner_rank - loser_rank == 1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 9, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 9 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == 0:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 10, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 10 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == -1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 11, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 11 WHERE player_id = $1', loser_id)

                                                elif (winner_details[0]['matches_played'] < 10) and (loser_details[0]['matches_played'] >= 10):
                                                    if winner_rank - loser_rank == 1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 9 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == 0:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 10 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == -1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 11 WHERE player_id = $1', loser_id)

                                                    else:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 8 WHERE player_id = $1', loser_id)

                                                elif (winner_details[0]['matches_played'] >= 10) and (loser_details[0]['matches_played'] < 10):
                                                    if winner_rank - loser_rank == 1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 9, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == 0:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 10, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == -1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 11, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', loser_id)

                                                    else:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 8 WHERE player_id = $1', loser_id)

                                                elif (winner_details[0]['matches_played'] < 10) and (loser_details[0]['matches_played'] < 10):
                                                    if winner_rank - loser_rank == 1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == 0:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', loser_id)

                                                    elif winner_rank - loser_rank == -1:
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points + 30, wins = wins + 1 WHERE player_id = $1', winner_id)
                                                        await self.bot.db.execute('UPDATE rank_system SET matches_played = matches_played + 1, points = points - 5 WHERE player_id = $1', loser_id)

                                                #Setting streak
                                                await self.bot.db.execute('UPDATE rank_system SET streak = streak + 1 WHERE player_id = $1', winner_id)
                                                await self.bot.db.execute('UPDATE rank_system SET streak = 0 WHERE player_id = $1', loser_id)

                                                #Preventing scores from being negative

                                                winner_details_updated = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', winner_id)
                                                loser_details_updated = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', loser_id)

                                                winner_points = int(winner_details_updated[0]['points'])
                                                loser_points = int(loser_details_updated[0]['points'])

                                                if int(winner_points) < 0:
                                                    await self.bot.db.execute('UPDATE rank_system SET points = 0 WHERE player_id = $1', winner_id)

                                                if int(loser_points) < 0:
                                                    await self.bot.db.execute('UPDATE rank_system SET points = 0 WHERE player_id = $1', loser_id)

                                                #Awarding streak
                                                if winner_details_updated[0]['streak'] >= 20:
                                                    emoji = '<:swiff:930428662711484486>'

                                                    if winner_check[0]['badges'] is None:
                                                        await self.bot.db.execute('UPDATE registered SET badges = $1 WHERE player_id = $2', emoji, winner_id)

                                                    else:
                                                        if emoji not in winner_check[0]['badges'].split():
                                                            new_badges = winner_check[0]['badges'] + f' {emoji}'

                                                            await self.bot.db.execute('UPDATE registered SET badges = $1 WHERE player_id = $2', new_badges, winner_id)

                                                        else:
                                                            pass

                                                if loser_details_updated[0]['streak'] < 0:
                                                    await self.bot.db.execute('UPDATE rank_system SET streak = 0 WHERE player_id = $1', loser_id)

                                                #Updating rank of winner

                                                if (int(winner_points) >= 0) and (int(winner_points) <= 83):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze1, bronze_value, winner_id)

                                                elif (int(winner_points) >= 84) and (int(winner_points) <= 167):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze2, bronze_value, winner_id)

                                                elif (int(winner_points) >= 168) and (int(winner_points) <= 250):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze3, bronze_value, winner_id)

                                                elif (int(winner_points) >= 251) and (int(winner_points) <= 333):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver1, silver_value, winner_id)

                                                elif (int(winner_points) >= 334) and (int(winner_points) <= 416):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver2, silver_value, winner_id)

                                                elif (int(winner_points) >= 417) and (int(winner_points) <= 500):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver3, silver_value, winner_id)

                                                elif (int(winner_points) >= 501) and (int(winner_points) <= 583):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold1, gold_value, winner_id)

                                                elif (int(winner_points) >= 584) and (int(winner_points) <= 667):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold2, gold_value, winner_id)

                                                elif (int(winner_points) >= 668) and (int(winner_points) <= 750):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold3, gold_value, winner_id)

                                                elif (int(winner_points) >= 751) and (int(winner_points) <= 833):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum1, platinum_value, winner_id)

                                                elif (int(winner_points) >= 834) and (int(winner_points) <= 916):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum2, platinum_value, winner_id)

                                                elif (int(winner_points) >= 917) and (int(winner_points) <= 1249):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum3, platinum_value, winner_id)

                                                elif int(winner_points) >= 1250:
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', dominant, dominant_value, winner_id)

                                                #Updating rank of loser

                                                if (int(loser_points) >= 0) and (int(loser_points) <= 83):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze1, bronze_value, loser_id)

                                                elif (int(loser_points) >= 84) and (int(loser_points) <= 167):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze2, bronze_value, loser_id)

                                                elif (int(loser_points) >= 168) and (int(loser_points) <= 250):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', bronze3, bronze_value, loser_id)

                                                elif (int(loser_points) >= 251) and (int(loser_points) <= 333):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver1, silver_value, loser_id)

                                                elif (int(loser_points) >= 334) and (int(loser_points) <= 416):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver2, silver_value, loser_id)

                                                elif (int(loser_points) >= 417) and (int(loser_points) <= 500):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', silver3, silver_value, loser_id)

                                                elif (int(loser_points) >= 501) and (int(loser_points) <= 583):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold1, gold_value, loser_id)

                                                elif (int(loser_points) >= 584) and (int(loser_points) <= 667):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold2, gold_value, loser_id)

                                                elif (int(loser_points) >= 668) and (int(loser_points) <= 750):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', gold3, gold_value, loser_id)

                                                elif (int(loser_points) >= 751) and (int(loser_points) <= 833):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum1, platinum_value, loser_id)

                                                elif (int(loser_points) >= 834) and (int(loser_points) <= 916):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum2, platinum_value, loser_id)

                                                elif (int(loser_points) >= 917) and (int(loser_points) <= 1249):
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', platinum3, platinum_value, loser_id)

                                                elif int(loser_points) >= 1250:
                                                    await self.bot.db.execute('UPDATE rank_system SET player_rank = $1, rank_value = $2 WHERE player_id = $3', dominant, dominant_value, loser_id)

                                                #Giving wishes to 100+ points
                                                if winner_points >= 100:
                                                    if winner_details_updated[0]['streak'] > 2:
                                                        wishes = registered_check[0]['wishes'] + math.ceil((winner_details_updated[0]['streak']/2)) - 1
                                                        await self.bot.db.execute('UPDATE registered SET wishes = $1 WHERE player_id = $2', wishes, winner.id)

                                                    else:
                                                        await self.bot.db.execute('UPDATE registered SET wishes = wishes + 1 WHERE player_id = $1', winner.id)

                                            elif str(reaction_add) == '❌':
                                                await ctx.send('Cancelled.')

                                    elif (self.modulus(winner_rank - loser_rank) >= 2) or (self.modulus(loser_rank - winner_rank) >= 2):
                                        await ctx.send("You can't log those 2 people. Either of them are 2 or more ranks above or below the other.") 

                                elif winner_details and not loser_details:
                                    await ctx.send(f'{loser.name} has not registered for ranked battles yet.')

                                elif not winner_details and loser_details:
                                    await ctx.send(f'{winner.name} has not registered for ranked battles yet.')

                                else:
                                    await ctx.send('Both of them have not registered for ranked battles yet.')

                            elif (not winner_ban_list) and loser_ban_list:
                                await ctx.send(f'{loser.name} is banned from ranked battles.')

                            elif winner_ban_list and (not loser_ban_list):
                                await ctx.send(f'{winner.name} is banned from ranked battles.')

                            elif winner_ban_list and loser_ban_list:
                                await ctx.send('Both of them are banned from ranked battles.')

                        elif ranked_enable == 0:
                            await ctx.send('Ranked battles are currently not enabled.')

                    else:
                        await ctx.send('Either of those players have not registered. Use `d!start` to register.')
            else:
                await ctx.send("You can't use this command.")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @admin_command.command(name = 'vieasdwinv', aliases = ['vinvdh','vfdiewinventory'])
    async def admin_view_inventory_command(self, ctx, member : discord.Member = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = str(server[0]['admins'])

            admins_list = self.listing(admins)

            if int(ctx.author.id) in admins_list:
                if member is None:
                    em = discord.Embed(
                        title = 'Admin',
                        description = "**View a player's inventory.**\n\nd!admin viewinv [mention]",
                        colour = discord.Colour.blue()
                    )

                    await ctx.send(embed = em)

                else:
                    member_inv = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', member.id)

                    if member_inv:
                        scrap_emoji = '<:dust:930037866891993128>'

                        banner_emoji = '<:banner:930034973967274014>'

                        pc_emoji = '<:pc:930036538933391400>'

                        inv_embed = discord.Embed(
                            title = f"{member.name}'s inventory",
                            description = 'Use `d!wish` to obtain items!',
                            colour = discord.Colour.dark_gold()
                        )

                        inv_embed.add_field(name = f'{scrap_emoji} Scraps', value = f'x{member_inv[0]["scraps"]}')
                        inv_embed.add_field(name = f'{banner_emoji} Banner pieces', value = f'x{member_inv[0]["banner_pieces"]}')
                        inv_embed.add_field(name = f'{pc_emoji} 40K PC', value = f'x{member_inv[0]["pc"]}')
                        inv_embed.add_field(name = '🌟 Wishes', value = f'x{member_inv[0]["wishes"]}')

                        await ctx.send(embed = inv_embed)

                    else:
                        await ctx.send('That person has not registered yet!')

            else:
                await ctx.send("You can't use this command.")
        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @admin_command.command(name = "rteam", aliases = ["rt"])
    async def dadmin_floor_command(self, ctx, member: discord.Member = None, floor: int = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)
            admins = str(server[0]['admins'])
            admins_list = self.listing(admins)
            if int(ctx.author.id) in admins_list:
                if (member is None) or (floor is None):
                    em = discord.Embed(
                        title = "Admin",
                        description = "**Change a player's team rank.**\n\nd!admin rt [mention] [rank]",
                        colour = discord.Colour.blue()
                    )

                    await ctx.send(embed = em)

                else:
                    member_inv = await self.bot.db.fetch('SELECT * FROM rank_system WHERE player_id = $1', member.id)

                    if member_inv:
                        if (floor > 6) or (floor < 0):
                            await ctx.send("Invalid team.")

                        else:
                            await self.bot.db.execute("UPDATE rank_system SET floor = $1 WHERE player_id = $2", floor, member.id)

                            await ctx.send(f"Set {member.mention} team rank to {floor}.")

                    else:
                        await ctx.send("That person has not started ranked yet!")

            else:
                await ctx.send("You do not have permission to use that command.")
        
        else:
            await ctx.send("You have not registered yet! Use `d!start` to register.")
    @admin_command.command(name = "cteam", aliases = ["ct"])
    async def admin_cteam_command(self, ctx, member: discord.Member = None, floor: int = None):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            guild_id = ctx.guild.id

            server = await self.bot.db.fetch('SELECT * FROM server_constants WHERE guild_id = $1', guild_id)

            admins = str(server[0]['admins'])

            admins_list = self.listing(admins)

            if int(ctx.author.id) in admins_list:
                if (member is None) or (floor is None):
                    em = discord.Embed(
                        title = "Admin",
                        description = "**Change a player's team rank.**\n\nd!admin ct [mention] [rank]",
                        colour = discord.Colour.blue()
                    )

                    await ctx.send(embed = em)

                else:
                    member_inv = await self.bot.db.fetch('SELECT * FROM common_system WHERE player_id = $1', member.id)

                    if member_inv:
                        if (floor > 6) or (floor < 0):
                            await ctx.send("Invalid team.")

                        else:
                            await self.bot.db.execute("UPDATE common_system SET floor = $1 WHERE player_id = $2", floor, member.id)
                            await ctx.send(f"Set {member.mention} team rank to {floor}.")

                    else:
                        await ctx.send("That person has not started ranked yet!")

            else:
                await ctx.send("You do not have permission to use that command.")
        
        else:
            await ctx.send("You have not registered yet! Use `d!start` to register.")


def setup(bot):
    bot.add_cog(AdminCommands(bot))