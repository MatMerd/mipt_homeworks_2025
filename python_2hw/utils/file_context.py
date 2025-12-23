import aiofiles
import logging

logger = logging.getLogger("file_context")


class AsyncFileContext:
    def __init__(self, filepath: str, mode: str = "w", encoding: str = "utf-8", newline: str = ""):
        self.filepath = filepath
        self.mode = mode
        self.encoding = encoding
        self.newline = newline
        self.file = None

    async def __aenter__(self):
        self.file = await aiofiles.open(self.filepath, self.mode, encoding=self.encoding, newline=self.newline)
        logger.debug(f"Opened file {self.filepath} in mode {self.mode}")
        return self.file

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            await self.file.close()
            logger.debug(f"Closed file {self.filepath}")