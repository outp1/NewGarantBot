import asyncio

import aiohttp

async def create_bill():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://vk.com/feed') as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print('Body:', html, '...')


loop = asyncio.get_event_loop()
loop.run_until_complete(create_bill())