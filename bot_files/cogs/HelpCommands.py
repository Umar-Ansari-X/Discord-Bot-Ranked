import discord
from discord.ext import commands
import asyncio

color = 0x32006e

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='help', invoke_without_command=True)
    async def help_command(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:

            try:
                embed = discord.Embed(
                    title='Help',
                    description='**Use `d!help [category]` for help about a command.**',
                    color=color
                )

                embed.add_field(name='Battling', value='`log` `casual` `casualleaderboard` `rareleaderboard` `comleaderboard` `weekly` `info` `rules`', inline=False)
                embed.add_field(name='Clan', value='`clans` `career` `warlog` `add` `remove` `memberenable` `memberadd` `memberremove` `leaderadd` `leaderremove` `setavatar`', inline=False)
                embed.add_field(name='Misc', value='`profile` `render` `set` `catalog` `setcolor` `inventory` `view` `open`', inline=False)
                embed.add_field(name='Trading', value='`shop` `buy` `trade` `market` `market add` `market remove` `market buy`  `market mine`\n\n`roll` `rand` `gambleleaderboard`', inline=False)

                embed.set_author(name="Command List")
                embed.set_footer(text="Need more help? Join our support server.")

                await ctx.send(embed=embed)
            except Exception as e:
                print(e)

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')


    @help_command.command(name = 'trading')
    async def tourney_help_subcommand(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            em = discord.Embed(
                title = 'Trading',
                description = 'Commands related to trading:',
                colour = color
            )
            em.add_field(name = 'd!shop [item type] [filter]', value = 'View the shop.\n[item type] banner, border, avaborder\n[filter] SS,S,A,B,C,D, price, >(number), <(number) name of item',inline=False)

            em.add_field(name = 'd!buy [item type] ', value = 'View the shop.\n[item type] keys, banner, border, avaborder',inline=False)

            em.add_field(name = 'd!trade [user] ', value = 'Trade with a user.',inline=False)

            em.add_field(name = 'd!market [item type] [filter]', value = 'View the market.\n[item type] banner, border, avaborder\n[filter] SS,S,A,B,C,D, price, >(number), <(number) name of item',inline=False)

            em.add_field(name = 'd!market add [item type] [item name] [price]', value = 'Add items to the market.',inline=False)

            em.add_field(name = 'd!market remove [item type] [item ID]', value = 'Remove items from the market.',inline=False)

            em.add_field(name = 'd!market buy [item type] [item ID]', value = 'Buy items from the market.',inline=False)

            em.add_field(name = 'd!market mine', value = 'My items listed in the market.',inline=False)

            em.add_field(name = 'd!roll [user]', value = "Gamble using rolls with a user or don't mention for a single roll",inline=False)

            em.add_field(name = 'd!rand', value = "Dex a random Pokemon",inline=False)

            em.add_field(name = 'd!gambleleaderboard', value = "View the gambling leaderboard.",inline=False)

            em.add_field(name = 'd!marketmine', value = 'My items listed in the market.',inline=False)

            await ctx.send(embed = em)

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @help_command.command(name = 'Battling', aliases = ['battle'])
    async def ranked_help_subcommand(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            em1 = discord.Embed(
                title = 'Battling',
                description = 'Commands related to battles: *(Page 1/2)*',
                colour = color
            )

            em1.add_field(name = 'd!log rare [mention] [score]', value = 'Log a rare ranked battles match.',inline=False)

            em1.add_field(name = 'd!log com [mention] [score]', value = 'Log a common ranked battles match.',inline=False)

            em1.add_field(name = 'd!log casual [mention] [score]', value = 'Log a casual battles match.',inline=False)

            em1.add_field(name = 'd!log war [War ID] [mention]', value = 'Log a clan war match.',inline=False)

            em1.add_field(name = 'd!rareleaderboard', value = 'View the top players in ranked battles.',inline=False)

            em1.add_field(name = 'd!comleaderboard', value = 'View the top players in ranked battles.',inline=False)

            em1.add_field(name = 'd!casualleaderboard', value = 'View the top players in ranked battles.',inline=False)

            em1.add_field(name = 'd!weekly', value = 'View Weekly leaderboard.',inline=False)

            em1.add_field(name = 'd!ranked info/i', value = 'Learn about rank battles.',inline=False)

            em1.add_field(name = 'd!rules', value = 'View rules for battling.',inline=False)



            await ctx.send(embed = em1)


        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @help_command.command(name = 'clan')
    async def clan_help_subcommand(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            em1 = discord.Embed(
                    title = 'Clans [Aliases: cl]',
                    description = 'Commands related to clans *(Page 1/2)*:',
                    colour = color
                )

            em1.add_field(name = 'd!clans', value = 'View the top official clans, their rankings and points.',inline=False)

            em1.add_field(name = 'd!clan career/cr [clan name]', value = 'View the top official clans, their rankings and points.',inline=False)

            em1.add_field(name = 'd!clan warlog', value = 'View the top official clans, their rankings and points.*(Admin exclusive)*',inline=False)

            em1.add_field(name = 'd!clan [clan name]', value = 'View the info about a clan.')

            em1.add_field(name = 'd!clan add|a [clan name]', value = 'Add a new clan.*(Admin exclusive)*')

            em1.add_field(name = 'd!clan remove|r [clan name]', value = 'Remove an exisiting clan. Removing an existing clan resets their points to zero.*(Admin exclusive)*',inline=False)

            em1.add_field(name = 'd!clan memberenable|me [channel]', value = 'Enable a channel to log member joins and leaves.*(Admin exclusive)*',inline=False)



            em2 = discord.Embed(
                title = 'Clan',
                description = 'Commands related to clans (2):',
                colour = color
            )
            em2.add_field(name = 'd!clan memberadd|ma [mention] [clan name]', value = 'Add a new member to a clan and log it.*(Admin exclusive)*',inline=False)

            em2.add_field(name = 'd!clan memberremove|mr [mention] [clan name]', value = 'Remove an existing member from a clan and log it.*(Admin exclusive)*',inline=False)

            em2.add_field(name = 'd!clan members|m [clan name]', value = 'Get a list of all existing members in a clan.',inline=False)

            em2.add_field(name = 'd!clan leaderadd|lda [mention] [clan name]', value = 'Add a new leader to clan. Leaders have permissions to set clan settings and add members.*(Admin exclusive)*',inline=False)

            em2.add_field(name = 'd!clan leaderremove|ldr [mention] [clan name]', value = 'Remove an existing leader from a clan.*(Admin exclusive)*',inline=False)

            em2.add_field(name = 'd!clan setavatar|setav [clan name]', value = 'Set an avatar for your clan.*(Admin and leader exclusive)*',inline=False)


            embeds = [em1, em2]

            current_page = 0

            clans_msg = await ctx.send(embed = em1)

            await clans_msg.add_reaction('\U000025C0')
            await clans_msg.add_reaction('\U000025B6')

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

                            await clans_msg.edit(embed = embeds[current_page])

                        elif current_page == 1:
                            current_page = 0

                            await clans_msg.edit(embed = embeds[current_page])

        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

    @help_command.command(name = 'misc')
    async def misc_help_subcommand(self, ctx):
        registered_check = await self.bot.db.fetch('SELECT * FROM registered WHERE player_id = $1', ctx.author.id)

        if registered_check:
            em1 = discord.Embed(
                title = 'Misc',
                description = 'Miscellaneous commands: *(Page 1/2)*',
                colour = color
            )

            em1.add_field(name = 'd!profile', value = "View your or any other registered player's profile.",inline=False)

            em1.add_field(name = 'd!render', value = "Render your registered player profile.",inline=False)

            em1.add_field(name = 'd!set [item type] [item name]', value = 'Set your banner, border, avatar border or title.\n[item type] banner,border,avaborder,title',inline=False)

            em1.add_field(name = 'd!inventory [item type]', value = 'View all your items in an inventory.')

            em1.add_field(name = 'd!catalog [item type] [filter]', value = 'View the whole catalog of the item type and see which items you own.\n[item type] banner,border,avaborder,title\n[filter] SS,S,A,B,C,D,owned or search the item',inline=False)

            em1.add_field(name = 'd!view [item type] [item name]', value = 'View the item.\n[item type] banner,border,avaborder,title\n[filter] SS,S,A,B,C,D or search the item',inline=False)

            em1.add_field(name = 'd!open', value = 'Open a lootbox.',inline=False)


            em1.add_field(name = 'd!setcolor [color in hexadecimal with the #]', value = 'Set your player profile Text color.\nSearch "Color picker" on google and use the hex code.',inline=False)



 
            await ctx.send(embed = em1)


        else:
            await ctx.send('You have not registered yet! Use `d!start` to register.')

def setup(bot):
    bot.add_cog(HelpCommands(bot))