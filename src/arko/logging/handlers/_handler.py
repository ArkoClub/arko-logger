from arko.logging.handlers._abc import AbstractHandler


class Handler(AbstractHandler):
    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass



class FileHandler(Handler):
    ...