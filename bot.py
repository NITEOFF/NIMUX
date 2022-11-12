import disnake
from disnake.ext import commands


bot = commands.InteractionBot()

@bot.event
async def on_ready():
    print("Bot is ready! Use /help")
    while True:
        await bot.change_presence(status=disnake.Status.online, activity=disnake.Game("/help"))
    
#Role Menu
@bot.slash_command(description="test")
@commands.has_permissions(administrator=True)
async def profile(inter):
    select = disnake.ui.Select(
        min_values=0,
        max_values=1,
        placeholder='Choose roles',
        options=[
        disnake.SelectOption(label="Hátegsvegur", emoji="<:hategs:1023928327662227456>"),
        disnake.SelectOption(label="Skólavörðuholt", emoji="<:skolavordu:1023929424166522940>"),
        disnake.SelectOption(label="Hafnarfjörður", emoji="<:hafnafj:1023920359017304115>"),
        ]
    )
    
    buttonremove = disnake.ui.Button(
        style=disnake.ButtonStyle.danger,
        custom_id='cancel',
        label='Remove roles'
    )

    
    async def my_callback(inter = disnake.MessageInteraction):
        hts = disnake.utils.get(inter.guild.roles, id=1023916199282745344)
        skl = disnake.utils.get(inter.guild.roles, id=1023916443428995074)
        haf = disnake.utils.get(inter.guild.roles, id=1022460562178838528)
        member = inter.author
        emb = disnake.Embed(
            description='> **You got roles!**',
            colour=disnake.Colour.green()
        )
        await inter.response.defer(with_message= True, ephemeral= True)
        await inter.edit_original_message(embed=emb)
        
        if 'Hátegsvegur' in select.values and hts not in member.roles:
            await member.add_roles(hts)
        if 'Skólavörðuholt' in select.values and skl not in member.roles:
            await member.add_roles(skl)
        if 'Hafnarfjörður' in select.values and haf not in member.roles:
            await member.add_roles(haf)
        else:
            pass
        if 'Hátegsvegur' not in select.values and hts in member.roles:
            await member.remove_roles(hts)
        if 'Skólavörðuholt' not in select.values and skl in member.roles:
            await member.remove_roles(skl)
        if 'Hafnarfjörður' not in select.values and haf in member.roles:
            await member.remove_roles(haf)
        else:
            pass
        

    select.callback = my_callback
    view = disnake.ui.View(timeout= None)
    view.add_item(select)
    view.add_item(buttonremove)
    embed = disnake.Embed(
        description='**Role menu**',

    )
    embed.add_field(name="⠀", value="<:hategs:1023928327662227456> — **Hátegsvegur** \n<:skolavordu:1023929424166522940> — **Skólavörðuholt**", inline=True)
    embed.add_field(name="⠀", value="<:hafnafj:1023920359017304115> - **Hafnarfjörður**", inline=True)
    embed.set_footer(text='developed by - nite')
    embed.set_image(url='')
    await inter.response.send_message(embed=embed, view=view)
    
    async def buttoncallback(inter = disnake.MessageInteraction):
        hts = disnake.utils.get(inter.guild.roles, id=1023916199282745344)
        skl = disnake.utils.get(inter.guild.roles, id=1023916443428995074)
        haf = disnake.utils.get(inter.guild.roles, id=1022460562178838528)
        member = inter.author
        if inter.component.custom_id == "cancel" and hts in member.roles or skl in member.roles or haf in member.roles:
            emb = disnake.Embed(
                description='> **Role was sucefully taken!**',
                colour=disnake.Colour.green()
            )
            await inter.response.defer(with_message= True, ephemeral= True)
            await inter.edit_original_message(embed=emb)
        if 'Hátegsvegur' in select.values and hts in member.roles:
            await member.remove_roles(hts)
        else:
            pass
        if 'Skólavörðuholt' in select.values and skl in member.roles:
            await member.remove_roles(skl)
        else:
            pass
        if 'Hafnarfjörður' in select.values and haf in member.roles:
            await member.remove_roles(haf)
        else:
            emb = disnake.Embed(
                description='> **You dont have any roles**',
                colour=disnake.Colour.red()
            )
            await inter.response.defer(with_message= True, ephemeral= True)
            await inter.edit_original_message(embed=emb)
            return
    buttonremove.callback = buttoncallback



@bot.slash_command(name='help', description='command with all cmd list', guild_ids='')
@commands.has_permissions(administrator=True)
async def help (interaction: disnake.CommandInteraction):
     await interaction.send("Use **Say/DM** and mod. command = **Ban/Kick**", ephemeral=True)


@bot.slash_command(name = 'say', description='Says message')
#@commands.has_any_role(32942384823490823094)
@commands.has_permissions(administrator=True)
async def say(inreraction: disnake.CommandInteraction, message: str):
    await inreraction.channel.send(message)
    await inreraction.send('Message has been sent', ephemeral=True)
    
    
@bot.slash_command(name='dm', description='Sends dm message')
@commands.has_permissions(administrator=True)
async def dm(inreraction: disnake.CommandInteraction, member: disnake.Member, text):
    await member.send(text)
    await inreraction.send('Message has been sent', ephemeral=True)
    
    
@bot.slash_command(name="ban", description="Command to ban a member")
@commands.has_permissions(administrator=True)
async def ban(inreraction:  disnake.CommandInteraction, member: disnake.Member, text):
    await member.ban(reason=text)
    await inreraction.send('Member has been banned', ephemeral=True)
        
        
@bot.slash_command(name= "kick", description= "Command to kick a user from server")
@commands.has_permissions(administrator=True)
async def kick(inreraction: disnake.CommandInteraction, member: disnake.Member, text):
    await member.kick(reason=text)
    await inreraction.send('ember has been kicked', ephemeral=True)
    
    
@bot.slash_command(name='clear')
@commands.has_permissions(administrator=True)
async def clear(self, ctx, amount: int=5) -> None:
    """Clear a certain amount of messages."""
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Cleared {amount} messages.')
    


bot.run("TOKEN")
