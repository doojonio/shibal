import httpx

from app.config import settings


class ServiceError(Exception):
    pass


class DriveService:
    def __init__(self):
        self.base_url = str(settings.DRIVE_URL)
        if not self.base_url.endswith("/"):
            self.base_url += "/"

    async def put(self, filename: str, content: bytes) -> str:
        """Returns an id of newly uploaded file"""
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                self.base_url + "put", files={"file": (filename, content)}
            )

            if resp.status_code != 200:
                raise ServiceError(resp.status_code)

            return resp.content.decode()

    async def put_from_file(self, from_path: str) -> str:
        """Returns an id of newly uploaded file"""

        with open(from_path, "rb") as rh:
            async with httpx.AsyncClient() as client:
                resp = await client.post(self.base_url + "put", files={"file": rh})

                if resp.status_code != 200:
                    raise ServiceError(resp.status_code)

                return resp.content.decode()

    async def get(self, id: str) -> bytes:
        async with httpx.AsyncClient() as client:
            resp = await client.get(self.base_url + "get/" + id)

            if resp.status_code != 200:
                raise ServiceError(resp.status_code)

            return resp.content

    async def get_to_file(self, id: str, save_to: str) -> None:
        content = await self.get(id)
        with open(save_to, "wb") as wh:
            wh.write(content)

    # ---
    # Sync alts
    # ---

    def put_sync(self, filename: str, content: bytes) -> str:
        """Returns an id of newly uploaded file"""
        with httpx.Client() as client:
            resp = client.post(
                self.base_url + "put", files={"file": (filename, content)}
            )

            if resp.status_code != 200:
                raise ServiceError(resp.status_code)

            return resp.content.decode()

    def put_from_file_sync(self, from_path: str) -> str:
        """Returns an id of newly uploaded file"""

        with open(from_path, "rb") as rh:
            with httpx.Client() as client:
                resp = client.post(
                    self.base_url + "put", files={"file": ("name.wav", rh)}
                )

                if resp.status_code != 200:
                    raise ServiceError(resp.status_code)

                return resp.content.decode()

    def get_sync(self, id: str) -> bytes:
        with httpx.Client() as client:
            resp = client.get(self.base_url + "get/" + id)

            if resp.status_code != 200:
                raise ServiceError(resp.status_code)

            return resp.content

    def get_to_file_sync(self, id: str, save_to: str) -> None:
        content = self.get_sync(id)
        with open(save_to, "wb") as wh:
            wh.write(content)
