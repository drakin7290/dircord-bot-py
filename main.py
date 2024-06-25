import nextcord # type: ignore
from nextcord.ext import commands # type: ignore
import os


intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)

initial_extensions = []
    
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append(f"cogs.{filename[:-3]}")

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
    
bot.run("MTI1NDY2MzY2MDYwMTczNzIyOA.GV1_gZ.ePxtTIGunTFgax4j5bSMgjFeDEe-GWCM8u1Mds")




