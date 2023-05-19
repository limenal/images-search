import asyncio
import httpx
from config.settings import UNSPLASH_ACCESS_KEY

async def get_link(query: str, current_page: int):
    headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
    params = {'query': query, 'per_page': 1, 'page': current_page}
    url = 'https://api.unsplash.com/search/photos'

    async with httpx.AsyncClient() as client:
        res = await client.get(url, headers=headers, params=params)
        if res.status_code == 200:
            response = res.json()
            return response.get('results')[0].get('urls').get('raw')

async def search_image(query: str, count: int):
    current_page = 0
    images = await asyncio.gather(
        *(get_link(query, count) for count in range(current_page, count)),
        return_exceptions=True
    )
    return images
