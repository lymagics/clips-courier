from src.domain.clip import Clip
from src.domain.post import Post, StoredPost


class PlainClip(Clip):
    def __init__(self, clip: Clip):
        self.origin = clip

    async def post(self) -> Post:
        return StoredPost((await self.origin.post()).files(), "")
