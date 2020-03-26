# rrNotifications

A python script to received nice Radarr notifications.

## Configuration
### Edit the file
Edit the file and enter your Radarr and Telegram information.
```
# Configuration: Radarr
radarrHost = '192.168.1.5'
radarrPort = '7878'
radarrApiKey = 'xxxxx'
# Configuration: Telegram
telegramToken = 'xxxxx'
telegramChatId = 00000
```
### Create a Telegram bot and get a token
To use the Telegram Bot API, you will first have to create a bot account by chatting with [BotFather](https://core.telegram.org/bots#6-botfather) then get a unique authentication token. The token is a string which looks like ```110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw```.
### Make the file executable (Linux only)
'''sudo chmod +x rrNotifications.py
### Add the script to Radarr
Scripts are added to Radarr via System > Connect > Add > Custom Script
