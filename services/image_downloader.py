import os
import ssl
import aiohttp
import aiofiles
import logging

logger = logging.getLogger(__name__)

class ImageDownloader:
    def __init__(self, image_directory: str):
        self.image_directory = image_directory

        if not os.path.exists(self.image_directory):
            os.makedirs(self.image_directory)

    async def download_image(self, url: str) -> str:

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, ssl=False) as response:
                    if response.status == 200:
                        filename = os.path.join(self.image_directory, url.split("/")[-1])

                        async with aiofiles.open(filename, 'wb') as f:
                            await f.write(await response.read())
                            
                        return filename
                    else:
                        logger.error(f"Failed to download image from {url}, status code: {response.status}")
                        return url
            except aiohttp.ClientError as e:
                logger.error(f"Error downloading image from {url}: {str(e)}")
                return url
