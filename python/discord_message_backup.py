
import discord
import asyncio

TOKEN = "REDACTED"
CHANNEL_ID = 407579540169424897

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        channel = self.get_channel(CHANNEL_ID)
        
        if channel is None:
            print("Invalid channel ID")
            await self.close()
            return

        permissions = channel.permissions_for(channel.guild.me)
        print(f"{permissions.read_message_history=}")
        
        messages = []
        raw_messages = [message async for message in channel.history(limit=None)]
        for msg in raw_messages:
            messages.append(f"- {msg.author}: {msg.content}")

        with open("discord_messages.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(list(reversed(messages))))
        
        print("Messages saved to discord_messages.txt")
        await self.close()

def main():
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True  # Required higher intents in discord settings

    client = MyClient(intents=intents)
    client.run(TOKEN)

if __name__ == "__main__":
    raise SystemExit(main())
