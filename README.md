# Devman-bot

Using this script, you can receive your lessons check notifications from [dvmn.org](https://dvmn.org/).
 

The script uses following external API's: 
- [telegram-api](https://api.telegram.org)
- [devman-api](https://dvmn.org/api/long_polling)

Once, you run the script you'll receive notification messages to your telegram account.
If something wrong happen, during invoking [devman-api](https://dvmn.org/api/long_polling), bot will send you log-error messages.

## How to install
Python3 should be already installed.
```bash
$ git clone https://github.com/nicko858/devman-bot.git
$ cd devman-bot
$ pip install -r requirements.txt
```
- Create file `.env` in the script directory


### Telegram instructions
You have to create telegram-channel, telegram-bot and get access-token.
[This arcticle](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/) will helps you to do all of this things.
If everything is fine, you'll get `telegram_bot_token`, `telegram_bot_url` and  `telegram_channel_name`.
Next thing you should do is to get a proxy address (actual for Russian Federation).
Check [spys.one](http://spys.one/proxys/US/) and get `https` proxy-address.
  
Add the following records to the `.env-file`:  

   ```bash
TELEGRAM_BOT_TOKEN=Your bot token
TELEGRAM_BOT_URL=Your bot address
TELEGRAM_CHANNEL_NAME=Your telegram channel
HTTPS_PROXY=<proxy address from spys.one>
  ```


## How to run

```bash
    python devman_bot.py
 ```
 
 ## How to deploy
 - Fork current repository
 - Make sure, that you have `Procfile` in the repo root and it has this inside:
   ```  bot: python3 devman_bot.py ```
 - Create account on [heroku](https://id.heroku.com) or use existing
 - Create new app and connect your github-account
 - After successfull github connection, go to `deploy section`
 - Choose `Manual deploy` and click `Deploy Branch`(by default -from master) 
 - After successfull deploy, go to `Settings` and create environment variables in `Config Vars` section (like `.env-file` from Telegram instructions)
 - Go to `Resources` and make sure that you have ``` bot: python3 devman_bot.py ``` in `Free Dynos` - section
 - Run bot by clicking pencil-icon


### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
