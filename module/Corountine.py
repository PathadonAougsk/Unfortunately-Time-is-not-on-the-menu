# Why the hell is there Threading and async in the same one???
import asyncio
import threading


class Corountine:
    def __init__(self, func, seconds) -> None:
        self.__func = func
        self.__seconds = seconds
        self.__should_stop = False

    def start(self):
        self.__should_stop = False

        self.background_task = threading.Thread(target=self.__func, daemon=True)
        self.background_task.start()

    def stop(self):
        self.__should_stop = True

    async def __main(self):
        while True:
            if self.__should_stop:
                return

            await asyncio.sleep(self.__seconds)
            self.__func()
