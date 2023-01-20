import nextcord
from nextcord.ext.commands import Bot
import json
import os

bot = Bot(intents=nextcord.Intents.all())

@bot.event
async def on_ready():  
    print("此開源由Man頭(´・ω・)#8870製作,使用請註明來源")
    print(f"-----------------{bot.user.name} 啟動成功!----------------")

#加載Cog部分由機車的開源提供
for file in os.listdir('./cogs'):  # 抓取所有cog資料夾裡的檔案
    if file.endswith('.py'):  # 判斷檔案是否是python檔
        try:
            # 載入cog,[:-3]是字串切片,為了把.py消除
            bot.load_extension(f'cogs.{file[:-3]}')
            print(f'✅ 已加載 {file}')
        except Exception as error:  # 如果cog未正確載入
            print(f'❌ {file} 發生錯誤  {error}')

with open("config.json","r") as f: #讀取cconfig.json
    data = json.load(f)
if __name__ == "__main__":
    token = data["TOKEN"] #定義token
    bot.run(token)