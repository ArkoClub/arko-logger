from arko.logging.handlers._abc import Handler, FileHandler


class MultiProcessHandler(Handler):
    ...


class MultiProcessFileHandler(MultiProcessHandler, FileHandler):
    ...
