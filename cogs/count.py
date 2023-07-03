import disnake
import json
import aiohttp
import os

from disnake.ext import commands
from disnake import ApplicationCommandInteraction,TextChannel, Option, Embed, OptionType, Webhook
from typing import Optional
from sympy import sympify
from sympy.core.sympify import SympifyError
from dotenv import load_dotenv


class count(commands.Cog): #定義class並繼承Cog
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.count = 1
        self.author = 0
        load_dotenv()
        parts = os.getenv("WEBHOOK_URL").split("/")
        self.webhook_id = int(parts[-2])    
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
    
    @commands.slash_command(name="setcount",description="設定現在的數字 (此為管理者使用)")
    async def setchannnel(self, interaction:ApplicationCommandInteraction, count:int = Option(name="目前數字", description="就數字", required=True, type=OptionType.integer)):
        if interaction.user.guild_permissions.administrator:
            with open("config.json","r") as f: #讀取json
                data = json.load(f)
            success_embed = Embed(title="✅ | 設定成功!",description=f"現在的數字為 `{count}` 下一位數字為 `{count+1}`",colour=disnake.Colour.green())
            self.count = count + 1
            change_embed = Embed(title="⚠ | 管理方更改了目前數字!",description=f"現在的數字為 `{count}` 下一位數字為 `{count+1}`",colour=disnake.Colour.green())
            channel = self.bot.get_channel(int(data["Gamechannel"]))
            await channel.send(embed=change_embed)
            await interaction.response.send_message(embed=success_embed)
        else:
            await interaction.response.send_message(":x: 你沒有管理者權限!", ephemeral=True)

    
    @commands.Cog.listener()
    async def on_message(self, message:disnake.Message):
        if message.author == self.bot.user: #忽視bot發送的訊息
            return
        
        if message.author.id == self.webhook_id:
            await message.add_reaction("✅") #添加反應
            return

        with open("config.json","r") as f: #讀取json
            data = json.load(f)
        if message.channel.id == data["Gamechannel"]: #偵測發送訊息的頻道是否為剛設定的頻道
            try:
                content = sympify(message.content) #讓算式也可以被偵測
                result = content.evalf()
                try:
                    if int(result) == self.count and message.author.id != self.author: #判定目前數字是否跟發送的一樣，且不為上個人發送的
                        await message.add_reaction("✅") #添加反應
                        self.author = message.author.id
                        self.count += 1
                    elif int(result) and message.author.id == self.author:
                        await message.add_reaction("❌")
                        top = self.count - 1
                        wrong_embed = Embed(title=f":x: | {message.author.name} 你不能一次講兩個數字! 這次的最高紀錄為 `{top}` !",description="現在，從1開始吧!", colour=disnake.Colour.red())
                        wrong_embed.set_footer(text="Made by 鰻頭(´・ω・)")
                        await message.channel.send(embed=wrong_embed)
                        self.count = 1
                        self.author = 0
                    else:
                        await message.add_reaction("❌")
                        top = self.count - 1
                        wrong_embed = Embed(title=f":x: | {message.author.name} 失誤了! 這次的最高紀錄為 `{top}` !",description="現在，從1開始吧!", colour=disnake.Colour.red())
                        wrong_embed.set_footer(text="Made by 鰻頭(´・ω・)")
                        await message.channel.send(embed=wrong_embed)
                        self.count = 1

                except TypeError:
                    pass
            except SympifyError:
                pass
        else:
            pass

    @commands.Cog.listener()
    async def on_message_delete(self, message:disnake.Message):
        if message.author == self.bot.user or message.author.id == self.webhook_id: #忽視bot發送的訊息
            return 
        with open("config.json","r") as f: #讀取json
            data = json.load(f)
        if message.channel.id == data["Gamechannel"]: #偵測發送訊息的頻道是否為剛設定的頻道
            try:
                content = sympify(message.content) #讓算式也可以被偵測
                result = content.evalf()
                try:
                    if int(result) == (self.count - 1): #判定目前數字是否跟發送的一樣
                        async with aiohttp.ClientSession() as session:
                            try:
                                self.author = message.author.id
                                webhook = Webhook.from_url(os.getenv("WEBHOOK_URL"), session=session)
                                await webhook.send(content=message.content, avatar_url=message.author.display_avatar.url, username=message.author.name, wait=True)
                            except RuntimeError:
                                session.close()
                                raise
                except TypeError:
                    pass
            except SympifyError:
                pass

def setup(bot):
    bot.add_cog(count(bot))
