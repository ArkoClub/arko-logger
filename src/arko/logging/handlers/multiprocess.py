from arko.logging.handlers._abc import AbstractHandler, AbstractFileHandler


class MultiProcessHandler(AbstractHandler): ...


class MultiProcessFileHandler(MultiProcessHandler, AbstractFileHandler): ...
