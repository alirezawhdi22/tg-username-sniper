from telethon import TelegramClient, functions
from telethon.errors import UsernameOccupiedError, UsernameInvalidError, FloodWaitError
import asyncio

# ----------Settings----------
api_id = 
api_hash = ""
phone = ""   # Additional or unused account number

# ----------Read usernames from file----------
def load_usernames():
    with open("usernames.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

usernames = load_usernames()

# ----------The client----------
client = TelegramClient("sniper_session", api_id, api_hash)

async def main():
    await client.start(phone=phone)

    while usernames:
        for username in usernames.copy():
            try:
                result = await client(functions.account.CheckUsernameRequest(username=username))
                if result:
                    print(f"[FREE] @{username} is free! Registering now...")

                    # Creating a channel
                    channel = await client(functions.channels.CreateChannelRequest(
                        title=username,
                        about="Channel bio",
                        megagroup=False
                    ))

                    # Set username on channel
                    await client(functions.channels.UpdateUsernameRequest(
                        channel=channel.chats[0].id,
                        username=username
                    ))
                    print(f"[SUCCESS] @{username} has been set on the channel ✅")
                    usernames.remove(username)

                else:
                    print(f"[BUSY] @{username} is still taken")
            except UsernameOccupiedError:
                print(f"[BUSY] @{username} is taken")
            except UsernameInvalidError:
                print(f"[INVALID] @{username} is invalid")
            except FloodWaitError as e:
                print(f"[FLOOD] You need to wait {e.seconds} seconds")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"[ERROR] {username}: {e}")

        await asyncio.sleep(30)  # Check every 30 seconds

with client:
    client.loop.run_until_complete(main())
