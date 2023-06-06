import asyncio
import httpx
import aiofiles

from config.settings import UNSPLASH_ACCESS_KEY
from .models import Image
from typing import List

async def get_link(query: str, current_page: int) -> str:
    headers = {'Authorization': f'Client-ID {UNSPLASH_ACCESS_KEY}'}
    params = {'query': query, 'per_page': 1, 'page': current_page}
    url = 'https://api.unsplash.com/search/photos'

    async with httpx.AsyncClient() as client:
        res = await client.get(url, headers=headers, params=params)
        if res.status_code == 200:
            response = res.json()
            return response.get('results')[0].get('urls').get('raw')

async def search_image(query: str, count: int) -> List[str]:
    current_page = 0
    images = await asyncio.gather(
        *(get_link(query, count) for count in range(current_page, count)),
        return_exceptions=True
    )
    return images

async def download_file(user_id: int, url: str, query: str) -> None:
    async with httpx.AsyncClient() as client:
        file_name = f"media/{user_id}/{url.split('/')[-1]}"
        res = await client.get(url.split('?')[0])
        async with aiofiles.open(file_name, 'wb+') as f:
            await f.write(res.read())

    await Image.objects.acreate(title=query, url=file_name, user_id=user_id)


async def save_images(user_id: int, query: str, count: int) -> List[str]:
    link_images = await search_image(query, count)
    await asyncio.gather(
        *(download_file(user_id, url, query) for url in link_images),
        return_exceptions=True
    )
    return link_images

