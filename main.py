import os
import discord
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
NOTIFY_CHANNEL_ID = int(os.getenv("NOTIFY_CHANNEL_ID"))

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_voice_state_update(member, before, after):

    if before.channel != after.channel:
        notify_channel = client.get_channel(NOTIFY_CHANNEL_ID)
        voice_channel_ids = [channel.id for channel in client.get_all_channels() if channel.type == discord.ChannelType.voice]

        # 退室通知
        if before.channel is not None and before.channel.id in voice_channel_ids:
            await notify_channel.send(f":wave: {member.name} *が* {before.channel.name} *から退室しました。*")

        # 入室通知
        if after.channel is not None and after.channel.id in voice_channel_ids:
            await notify_channel.send(f":wave: {member.name} *が* {after.channel.name} *に参加しました。*")


client.run(DISCORD_TOKEN)
