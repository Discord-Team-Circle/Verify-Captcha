from flask import Flask, render_template, request, redirect, url_for, jsonify
from dotenv import load_dotenv
from flask_xcaptcha import XCaptcha
from flask_discord import DiscordOAuth2Session
from utils import createLogger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import requests
import setting

app = Flask(__name__)
limiter = Limiter(app,key_func=get_remote_address,default_limits=["100 per day", "10 per hour"])
load_dotenv(verbose=True)

app.secret_key = b"locus-verify"
app.config["DISCORD_CLIENT_ID"] = os.getenv('client_id')
app.config["DISCORD_CLIENT_SECRET"] = os.getenv('client_secret')
app.config["DISCORD_REDIRECT_URI"] = f"{os.getenv('redirect_url')}/callback"
app.config["DISCORD_BOT_TOKEN"] = os.getenv('TOKEN')
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "false"

app.config['XCAPTCHA_SITE_KEY'] = os.getenv('recaptcha_site_key')
app.config['XCAPTCHA_SECRET_KEY'] = os.getenv('recaptcha_secret_key')
app.config['XCAPTCHA_THEME'] = "dark"

recaptcha = XCaptcha(app=app)

discord = DiscordOAuth2Session(app)

logger = createLogger("web")

logger.info(f"[Web]: ✅ Loaded app.py")

@app.route('/', methods=["GET", "POST"])
def core():
  if request.method == "GET":
    if discord.authorized:
      user = discord.fetch_user()
      logger.info(f"[Web]: ✅ {user} is verifying...")
      return render_template('index.html', captcha=0)
    else:
      logger.info(f"[Web]: ✅ Someone is requesting sign in...")
      return discord.create_session(scope=["identify"])
  else:
    if discord.authorized:
      if recaptcha.verify():
        user = discord.fetch_user()
        logger.info(f"[Web]: ✅ {user}'s captcha is success.")
        # SUCCESS
        try: 
          requests.put(
              "https://discord.com/api/v9/guilds/" +
              setting.config.GUILD_ID + "/members/" +
              str(user.id) + "/roles/" + setting.config.ROLE_ID, 
              headers={"Authorization": "Bot " + os.getenv("TOKEN")}
          )
          return render_template('success.html')
        except:
          return render_template('failed.html')
      else:
        user = discord.fetch_user()
        logger.info(f"[Web]: ⛔ {user}'s captcha is failed.")
        # FAILED
        return render_template('index.html', captcha=1)
    else:
      logger.info(f"[Web]: ✅ Someone is requesting sign in...")
      return discord.create_session(scope=["identify"])

@app.route('/check/captcha', methods=["POST"])
async def captcha_session():
  if discord.authorized:
    user = discord.fetch_user()
    print(request.form['type'])
    if request.form['type'] == "1":
      logger.info(f"[Web]: ⛔ {user}'s captcha is unknown data.")
      return jsonify({"status": 200, "message": "The request was successfully processed."})
    elif request.form['type'] == "2":
      logger.info(f"[Web]: 🕘 {user} is requesting verify.")
      return jsonify({"status": 200, "message": "The request was successfully processed."})
    else:
      logger.info(f"[Web]: ⛔ {user} is requesting unknown checking session parameter.")
      return jsonify({"status": 404, "message": "This is an unusual request."})
  else:
      logger.info(f"[Web]: ⛔ Someone is not found session but requesting captcha.")
      return jsonify({"status": 401, "message": "Please login first."})

@app.route('/callback', methods=["GET", "POST"])
async def callback():
  discord.callback()
  return redirect(url_for(".core"))

#app.run(host='0.0.0.0', port=5000, debug=True, load_dotenv=True)
app.run(host='0.0.0.0', port=8091, debug=False, load_dotenv=True)
