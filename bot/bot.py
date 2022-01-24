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
  logger.info(f"[Bot]: ✅ Loaded bot.py")
  try:
      bot.load_extension("jishaku")
      logger.info(f"[Bot]: ✅ Loaded jishaku")
  except:
      logger.error(f"[Bot]: ❌ Load failed jishaku")

@bot.event
async def on_member_join(member):
  # Alts Kicker
  days = datetime.now().replace(tzinfo=None) - member.created_at.replace(tzinfo=None)
  if days < timedelta(days=30):
      await member.kick()
      logger.info("[Bot]: 🔨 Kicked an alt ({member.name}#{member.discriminator})")
      setup_name = bot.get_guild(setting.config.setup_id)
      try:
        embed = disnake.Embed(
          title = f"{setup_name} 인증 실패",
          description = f'Discord 계정이 가입한지 5일이 경과되지 않았어요.\n테러 방지 차원으로 이런 조치를 취하게 되어 양해 부탁드려요.'
        )
        await member.send(embed = embed, view = Link())
        logger.info(f"[Bot]: ✅ Sent a DM to the kicked member. ({member.name}#{member.discriminator})")
      except:
        logger.error(f"[Bot]: ❌ Couldn't send a DM to the kicked member. ({member.name}#{member.discriminator})")

@bot.command(name="verify")
async def verify_bot(ctx):
  # Verify
  await ctx.message.delete()

  setup_name = bot.get_guild(setting.config.setup_id)
  embed = disnake.Embed(
    title = f"{setup_name} 인증하기",
    description = f'{setup_name} 인증을 완료하시려면 아래 URL 버튼을 눌러 인증 페이지로 이동해 주세요. {setup_name}에 방문해주셔서 감사합니다!',
  )
  embed.set_footer(text="5초 뒤 메시지가 자동 삭제됩니다.")
  
  msg = await ctx.send(embed = embed, view = Link())
  await sleep(5)
  await msg.delete()
      
bot.run(os.getenv('TOKEN'))
