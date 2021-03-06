import disnake
import setting
import os
from disnake.ext import commands
from dotenv import load_dotenv
from setting.link_b import Link
from utils import createLogger
from datetime import datetime, timedelta
from asyncio import sleep

bot = commands.Bot(command_prefix = [";"], intents = disnake.Intents.all(), owner_ids=[902700864748273704, 602459845534416896]) 
load_dotenv(verbose=True)
logger = createLogger("bot")

@bot.event
async def on_ready():
  logger.info(f"[Bot]: β Loaded bot.py")
  try:
      bot.load_extension("jishaku")
      logger.info(f"[Bot]: β Loaded jishaku")
  except:
      logger.error(f"[Bot]: β Load failed jishaku")

@bot.event
async def on_member_join(member):
  # Alts Kicker
  days = datetime.now().replace(tzinfo=None) - member.created_at.replace(tzinfo=None)
  if days < timedelta(days=30):
      await member.kick()
      logger.info("[Bot]: π¨ Kicked an alt ({member.name}#{member.discriminator})")
      setup_name = bot.get_guild(setting.config.setup_id)
      try:
        embed = disnake.Embed(
          title = f"{setup_name} μΈμ¦ μ€ν¨",
          description = f'Discord κ³μ μ΄ κ°μνμ§ 5μΌμ΄ κ²½κ³Όλμ§ μμμ΄μ.\nνλ¬ λ°©μ§ μ°¨μμΌλ‘ μ΄λ° μ‘°μΉλ₯Ό μ·¨νκ² λμ΄ μν΄ λΆνλλ €μ.'
        )
        await member.send(embed = embed, view = Link())
        logger.info(f"[Bot]: β Sent a DM to the kicked member. ({member.name}#{member.discriminator})")
      except:
        logger.error(f"[Bot]: β Couldn't send a DM to the kicked member. ({member.name}#{member.discriminator})")

@bot.command(name="verify")
async def verify_bot(ctx):
  # Verify
  await ctx.message.delete()

  setup_name = bot.get_guild(setting.config.setup_id)
  embed = disnake.Embed(
    title = f"{setup_name} μΈμ¦νκΈ°",
    description = f'{setup_name} μΈμ¦μ μλ£νμλ €λ©΄ μλ URL λ²νΌμ λλ¬ μΈμ¦ νμ΄μ§λ‘ μ΄λν΄ μ£ΌμΈμ. {setup_name}μ λ°©λ¬Έν΄μ£Όμμ κ°μ¬ν©λλ€!',
  )
  embed.set_footer(text="5μ΄ λ€ λ©μμ§κ° μλ μ­μ λ©λλ€.")
  
  msg = await ctx.send(embed = embed, view = Link())
  await sleep(5)
  await msg.delete()
      
bot.run(os.getenv('TOKEN'))
