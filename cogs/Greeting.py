import nextcord # type: ignore
from nextcord import Interaction, FFmpegPCMAudio # type: ignore
from nextcord.ext import commands # type: ignore
import http.client
import ast


serverID = 1121448423447597056

class Subscriptions (nextcord.ui.View):
    def __init__ (self):
        super().__init__()
        self.value = None
    
    @nextcord.ui.button (label="Subscribe", style=nextcord.ButtonStyle.gray)
    async def subscribe(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message("Thank u", ephemeral=False)
        self.value = True
        self.stop()


class GreetingCog(commands.Cog):
    def __init__ (self, client):
        self.client = client


    @nextcord.slash_command(name="test",description="Mannu is a good boy", guild_ids=[serverID])
    async def test(self, interaction: Interaction):
        await interaction.response.send_message("Hello!", ephemeral=True)
    
    @nextcord.slash_command(name="oh",description="Mannu is a good boy", guild_ids=[serverID] )
    async def oh(self, interaction: Interaction):
        await interaction.response.send_message("Hello!", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        # await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.streaming, name="with your mom"))
        await self.client.change_presence(status=nextcord.Status.online, activity=nextcord.Streaming( name="with your mom", url="https://www.twitch.tv/monstercat"))
        channel = self.client.get_channel(1254671506903138388)
        view = Subscriptions()
        await channel.send("I am online", view=view)

    @commands.command(name="ping")
    async def ping(self, ctx):
        conn = http.client.HTTPSConnection("jokes34.p.rapidapi.com")

        headers = {
            'x-rapidapi-key': "9aa5b68ef6msh21d0a3f4c978207p1d84b1jsn30a1f31c1abd",
            'x-rapidapi-host': "jokes34.p.rapidapi.com"
        }

        conn.request("GET", "/v1/jokes?q=Did%20you%20hear%20about%20the%20butcher%20who%20backed", headers=headers)

        res = conn.getresponse()
        data = res.read()
        joke = ast.literal_eval(data.decode())[0]['joke']
        await ctx.send(joke)

    @commands.command()
    async def join(self, ctx):
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio("piano.mp3")
            player = voice.play(source)
        else:
            await ctx.send("You are not in a voice channel!")

    @commands.command()
    async def leave(self, ctx):
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("I left the voice channel")
        else:
            await ctx.send("I am not in a voice channel")

    @commands.command()
    async def pause(self, ctx):
        voice = nextcord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("I am not playing anything")

    @commands.command()
    async def resume(self, ctx):
        voice = nextcord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("I am not paused")

    @commands.command()
    async def stop(self, ctx):
        voice = nextcord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.content.startswith("hello"):
            await message.channel.send("Hi!")
        elif message.content == "check":
            await message.delete()
            await message.channel.send("Message deleted")

        if ("happy" in message.content):
            emoji = "😀"
            await message.add_reaction(emoji)

    @commands.command()
    async def embed(self, ctx):
        embed = nextcord.Embed(title="???", url="https://google.com", description="This is a description", color=0x00ff00)
        embed.set_author(name=ctx.author.display_name, url="https://launchmoby.com", icon_url=ctx.author.avatar)
        embed.set_thumbnail(url="https://coin98.net/_next/image?url=https%3A%2F%2Ffiles.amberblocks.com%2Fthumbnail%2Fchnbzaa92ook5tnj%2Fposts%2Fpuy4zicegdckiinp%2Ff47rc2n6ynf63040ywof6b0b89xgv2hs%2Fmoby-la-gi.jpg&w=1200&q=100")
        embed.add_field(name="T", value="A", inline=True)
        embed.add_field(name="T", value="A", inline=True)
        embed.add_field(name="T", value="A", inline=False)
        embed.set_footer(text="This is a footer", icon_url=ctx.author.avatar )
        await ctx.send(embed=embed)

    # DM User
    @commands.command()
    async def message(self, ctx, user: nextcord.Member, *, message=None):
        message = "Welcome to the server!"
        embed = nextcord.Embed(title=message)
        await user.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        await channel.send(f"{user} reacted with {reaction.emoji}")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        channel = reaction.message.channel
        await channel.send(f"{user} removed {reaction.emoji}")

    @commands.command(name="addRole")
    @commands.has_permissions(manage_roles=True)
    async def addRole(self, ctx, user:nextcord.Member, *, role: nextcord.Role):
        if (role in user.roles):
            await ctx.send("User already has that role")
        else:
            await user.add_roles(role)
            await ctx.send(f"{user} has been given the role {role}")
    
    @addRole.error
    async def addRole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the required permissions")

    @commands.command(name="removeRole")
    @commands.has_permissions(manage_roles=True)
    async def removeRole(self, ctx, user:nextcord.Member, *, role: nextcord.Role):
        if (role in user.roles):
            await user.remove_roles(role)
            await ctx.send(f"{user.mention} remove the role {role}")
        else:
            await ctx.send("User already has the role")
    
    @removeRole.error
    async def removeRole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the required permissions")

def setup (client):
    client.add_cog(GreetingCog(client))

