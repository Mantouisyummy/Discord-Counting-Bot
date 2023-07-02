import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction,TextChannel, Option, Embed
from typing import Optional
from sympy import sympify
import json

class count(commands.Cog): #定義class並繼承Cog
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.count = 1
        super().__init__()

    @commands.slash_command(name="setchannel",description="設定遊玩的頻道",name_localizations={"zh-TW":"設定頻道"})
    async def setchannnel(self, interaction:ApplicationCommandInteraction, channel:Optional[TextChannel] = Option(name="頻道", description="選擇一個頻道", required=True)):
        with open("config.json","r") as f: #讀取json
            data = json.load(f)
        data["GamechannelID"] = channel.id #將遊戲頻道的ID寫入至config.json
        with open("config.json","w") as f: #寫入json
            json.dump(data,f)
        success_embed = Embed(title="✅ | 設定成功!",description=f"你可以在 {channel.mention} 遊玩了!",colour=disnake.Colour.green())
        success_embed.set_footer(text="Made by 鰻頭(´・ω・)")
        await interaction.response.send_message(embed=success_embed)
        channel_embed = Embed(title="✅ | 此頻道已變成計數遊戲的頻道",description=f"試著打 1 開始遊戲吧!",colour=disnake.Colour.purple())
        channel_embed.set_footer(text="Made by 鰻頭(´・ω・)")
        await channel.send(embed=channel_embed)
    
    @commands.Cog.listener()
    async def on_message(self, message:disnake.Message):
        if message.author == self.bot.user: #忽視bot發送的訊息
            return 
        with open("config.json","r") as f: #讀取json
            data = json.load(f)
        if message.channel.id == data["Gamechannel"]: #偵測發送訊息的頻道是否為剛設定的頻道
            content = sympify(message.content) #讓算式也可以被偵測
            result = content.evalf()
            if int(result) == self.count: #判定目前數字是否跟發送的一樣
                await message.add_reaction("✅") #添加反應
                self.count += 1
            else:   
                await message.add_reaction("❌")
                top = self.count - 1
                wrong_embed = Embed(title=f":x: | {message.author.name} 失誤了! 這次的最高紀錄為 `{top}` !",description="現在，從1開始吧!", colour=disnake.Colour.red())
                wrong_embed.set_footer(text="Made by 鰻頭(´・ω・)")
                await message.channel.send(embed=wrong_embed)
                self.count = 1
        else:
            pass

def setup(bot):
    bot.add_cog(count(bot))
