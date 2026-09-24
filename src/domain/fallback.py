import logging

from src.domain.clip import Clip
from src.domain.fault import Fault
from src.domain.post import Post


class FallbackClip(Clip):
    def __init__(self, first: Clip, second: Clip):
        self.first = first
        self.second = second

    async def post(self) -> Post:
        try:
            post = await self.first.post()
        except Fault as e:
            logging.getLogger(__name__).info("Trying the second backend: %s", e)
            post = await self.second.post()
        return post
