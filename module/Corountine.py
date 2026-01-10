import asyncio


class Corountine:
    def __init__(self, func, seconds) -> None:
        self.func = func
        self.seconds = seconds
        self.should_stop = False

    def start(self):
        self.should_stop = False
        asyncio.run(self.__main())

    def stop(self):
        self.should_stop = True

    async def __main(self):
        try:
            while True:
                if self.should_stop:
                    return

                self.func()
                await asyncio.sleep(self.seconds)
        except asyncio.CancelledError:
            # Just in case
            return
