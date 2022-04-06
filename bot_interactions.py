# Find the commands : https://realpython.com/how-to-make-a-discord-bot-python/#creating-a-guild
# from discord_slash import SlashCommand, SlashContext
# from discord_slash.utils.manage_commands import create_choice, create_option

# bot.run()command_prefix='$'
# slash = SlashCommand(bot, sync_commands=True)

# That was the legacy librairy that's now interactions
# But it can give an idea of how it does work

import os
import interactions
# doc available in https://discord-py-slash-command.readthedocs.io/en/latest/
# Source code https://github.com/interactions-py/library

bot = interactions.Client(os.getenv('BOT_TOKEN'))

scoreboards = {}

# Here goes your server ID
my_guild_id = 0 

async def __print_msg(ctx: interactions.CommandContext, msg):
    await ctx.send(msg)


@bot.command(
    name = "hello",
    description = "Says hello",
)
async def __hello(ctx: interactions.CommandContext):
    await ctx.send("World!")


# ***************************
#       New Scoreboard
# ***************************

@bot.command(
    name='s_new',
    description='Create a new Scoreboard named as u wish',
    scope=my_guild_id,
    options=[
        interactions.Option(
            name = "sc_name",
            description = "Name your scoreboard!",
            type=interactions.OptionType.STRING,
            required = True,
        )
    ]
)
async def create_scoreboard(ctx: interactions.CommandContext, sc_name:str):
    try:
        scoreboards[sc_name]
        # break
    except KeyError:
        scoreboards[sc_name] = {}
        await __print_msg(ctx, "The "+ sc_name +" scoreboard has been created")
        return
    await __print_msg(ctx, "The "+ sc_name +" scoreboard already exists")

# ***************************
#     Delete Scoreboard
# ***************************

@bot.command(
    name='s_del',
    description='Delete the Scoreboard of ur dreams',
    scope=my_guild_id,
    options=[
        interactions.Option(
            name = "sc_name",
            description = "Name ur target!",
            type=interactions.OptionType.STRING,
            required = True,
        )
    ]
)
async def delete_scoreboard(ctx: interactions.CommandContext, sc_name):
    try:
        del scoreboards[sc_name]
        # break
    except KeyError:
        await __print_msg(ctx, "The "+ sc_name +" scoreboard doesn't exist!")
        return
    await __print_msg(ctx, "The "+ sc_name +" scoreboard has been removed")


# ***************************
#     Show Scoreboard
# ***************************

@bot.command(
    name='s_show',
    description='Show the Scoreboard of ur dreams',
    scope=my_guild_id,
    options=[
        interactions.Option(
            name = "sc_name",
            description = "Name ur target!",
            type=interactions.OptionType.STRING,
            required = True,
        )
    ]
)
async def print_scoreboard(ctx: interactions.CommandContext, sc_name):
    try:
        sc = scoreboards[sc_name]
        # break
    except KeyError:
        await __print_msg(ctx, "The "+ sc_name +" scoreboard doesn't exist!")
        return

    msg = "   __**"+sc_name+" :**__\n"
    list_sc = sorted(sc.items(), key=lambda item: item[1]).reverse()
    i = 1
    msg += str(list_sc)
    if list_sc.__class__ == None.__class__ or len(list_sc) == 0:
        msg += "The scoreboard "+sc_name+" is empty"
    else:
        for usr_score in list_sc:
            msg +=" *"+str(i)+"* - "+usr_score[0] +" : "+ str(usr_score[1]) + "\n"
    await __print_msg(ctx, msg)


# ***************************
#     Add som1 to Sc
# ***************************

@bot.command(
    name='s_add',
    description='Pin some1 to the Board!',
    scope=my_guild_id,
    options=[
        interactions.Option(
            name = "sc_name",
            description = "Name ur target scoreboard!",
            type=interactions.OptionType.STRING,
            required = True,
        ),
        interactions.Option(
            name = "usr_name",
            description = "Name ur target user!",
            type=interactions.OptionType.STRING,
            required = True,
        )
    ]
)
async def add_scoreboard(ctx: interactions.CommandContext, sc_name, usr_name):
    try:
        sc = scoreboards[sc_name]
        # break
    except KeyError:
        await __print_msg(ctx, "The "+ sc_name +" scoreboard doesn't exist!")
        return
    try:
        sc[usr_name]
        # break
    except KeyError:
        sc[usr_name] = 0
        await __print_msg(ctx, "The entry for "+ usr_name +" was created!")
        return
    await __print_msg(ctx, "The entry for "+ usr_name +" was already existing!")


# ***************************
#     Change som1 score
# ***************************
@bot.command(
    name='s_change',
    description='Change the score of some1!',
    scope=my_guild_id,
    options=[
        interactions.Option(
            name = "sc_name",
            description = "Name ur target scoreboard!",
            type=interactions.OptionType.STRING,
            required = True,
        ),
        interactions.Option(
            name = "usr_name",
            description = "Name ur target user!",
            type=interactions.OptionType.STRING,
            required = True,
        ),
        interactions.Option(
            name = "value",
            description = "Enter the new value!",
            type=interactions.OptionType.STRING,
            required = True,
        )
    ]
)
async def chg_scoreboard(ctx: interactions.CommandContext, sc_name, usr_name, value):
    try:
        sc = scoreboards[sc_name]
        # break
    except KeyError:
        await __print_msg(ctx, "The "+ sc_name +" scoreboard doesn't exist!")
        return
    try:
        sc[usr_name]
        # break
    except KeyError:
        sc[usr_name] = int(value)
        await __print_msg(ctx, "The entry for "+ usr_name +" was created!")
        return

    sc[usr_name] = int(value)
    await __print_msg(ctx, "The entry for "+ usr_name +" was changed to "+value+"!")
    await __print_msg(ctx, "The entry for "+ str(sc) +' '+ usr_name +" was created!")


# ***************************
#     Roll dices
# ***************************

def parse_dice(dices_txt:str):
    nb = 0
    type = 0
    modi = 0

    parse = dices_txt.split('d')
    nb = int(parse[0])

    parse = parse[1].split('+') # then parses = ["j","x-y"]
    if (len(parse)==1): # (j-y)
        parse = parse[0].split('-') # then parses = ["j","y"]
        type = int(parse[0])
        if (len(parse)==2): # (idj  -x)
            modi -= int(parse[1])
    else: # (idj +x -?)
        parse = parse[1].split('-') # then parses = ["j","x","y"]
        type = int(parse[0])
        if (len(parse)==2): # (idj +x -y)
            modi -= int(parse[1])
            modi += int(parse[0])
        else:  # (idj +x)
            modi += int(parse[0])
    # modi += int(parse[1])
    # parse = parse[0].split('-')
    # if (len(parse)==2):
    #     modi -= int(parse[1])

    return [nb, type, modi]

@bot.command(
    name='roll',
    description='Roll some dices!',
    scope=my_guild_id,
    options=[
        interactions.Option(
            name = "dices_txt",
            description = "kind of launch",
            type=interactions.OptionType.STRING,
            required = True,
        )
    ]
)
async def roll_dices(ctx: interactions.CommandContext, dices_txt):
    nb = 0
    modi = 0
    try:
        parse = dices_txt.split('d')
        nb = int(parse[0])
        parse = parse[1].split('+')
        if (len(parse)==2):
            modi += int(parse[1])
        parse = parse[0].split('-')
        if (len(parse)==2):
            modi -= int(parse[1])
        # break
    except KeyError:
        await __print_msg(ctx, "The "+ sc_name +" scoreboard doesn't exist!")
        return
    try:
        sc[usr_name]
        # break
    except KeyError:
        sc[usr_name] = int(value)
        await __print_msg(ctx, "The entry for "+ usr_name +" was created!")
        return

    sc[usr_name] = int(value)
    await __print_msg(ctx, "The entry for "+ usr_name +" was changed to "+value+"!")
    await __print_msg(ctx, "The entry for "+ str(sc) +' '+ usr_name +" was created!")




## Routines start

bot.start()
