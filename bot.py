import nextcord
from nextcord.ext.commands import Bot
import json
import os
import requests

bot = Bot(intents=nextcord.Intents.all())

with open("config.json","r") as f: #讀取config.json
    data = json.load(f)
headertoken = data["TOKEN"]
headers = {
    "Authorization": f"Bot {headertoken}" #給予標頭以通過驗證
}


@bot.event
async def on_ready():
    print("此開源由Man頭(´・ω・)#8870製作,使用請註明來源")
    print(f"-----------------{bot.user.name} 啟動成功!----------------")
    url = f"https://discord.com/api/v10/applications/{bot.user.id}/commands"
    requests.post(url, headers=headers, json=json1) #註冊全域斜線指令
    print("註冊斜線指令成功!")

#加載Cog部分由機車的開源提供
for file in os.listdir('./cogs'):  # 抓取所有cog資料夾裡的檔案
    if file.endswith('.py'):  # 判斷檔案是否是python檔
        try:
            # 載入cog,[:-3]是字串切片,為了把.py消除
            bot.load_extension(f'cogs.{file[:-3]}')
            print(f'✅ 已加載 {file}')
        except Exception as error:  # 如果cog未正確載入
            print(f'❌ {file} 發生錯誤  {error}')




json1 = { #斜線指令的json，如何撰寫可參閱 https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
    "name": "setchannel",
    "description": "設定遊玩的頻道",
    "type": 1,
    "options": [
            {
            "name": "頻道",
            "type": 7,
            "description": "選擇一個頻道",
            "required": True,
        }
    ]
}

if __name__ == "__main__":
    token = data["TOKEN"] #定義token
    bot.run(token)