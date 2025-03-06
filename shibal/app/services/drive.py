# ---
# TODO:
# ---
# 1. Write external service for this things
# 2. Until then atleast sanitize filenames
# ---
class DriveService:
    def put(self, name: str, content: bytes) -> str:
        with open("/tmp/{}".format(name), "wb") as wh:
            wh.write(content)
        return name

    def put_from(self, name: str, name_from: str) -> str:
        with open(name_from, "rb") as rh:
            content = rh.read()
        return self.put(name, content)

    def get(self, name: str) -> bytes:
        with open("/tmp/{}".format(name), "rb") as rh:
            return rh.read()

    def get_to(self, name: str, to_name: str) -> None:
        content = self.get(name)
        with open(to_name, "wb") as wh:
            wh.write(content)
