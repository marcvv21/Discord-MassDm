import aiohttp
import asyncio

token = ''
guild_id = ''

headers = {
    'Authorization': f'Bot {token}',
    'Content-Type': 'application/json'
}

async def fetch_members():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://discord.com/api/v10/guilds/{guild_id}/members?limit=1000', headers=headers) as response:
            return await response.json()

async def send_dm(member):
    async with aiohttp.ClientSession() as session:
        user_id = member['user']['id']
        username = member['user']['username']
        dm_data = {
            'recipient_id': user_id
        }
        async with session.post('https://discord.com/api/v10/users/@me/channels', headers=headers, json=dm_data) as response:
            dm_channel = await response.json()
        message_data = {
            'content': '' #enter ur msg here
        }
        async with session.post(f'https://discord.com/api/v10/channels/{dm_channel["id"]}/messages', headers=headers, json=message_data) as response:
            if response.status == 200:
                print(f"Sent DM to {username} ({user_id})")
            else:
                print(f"Error sending message to user {username} ({user_id})!")

async def main():
    members = await fetch_members()
    tasks = [send_dm(member) for member in members if not member['user'].get('bot', False)]
    await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
