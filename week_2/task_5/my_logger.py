import abc

class IHandler(abc.ABC):
    @abc.abstractmethod
    def log(self, formatter, message):
        raise NotImplementedError

class Logger:
    def __init__(self):
        self.formatter = "%Y.%m.%d %H:%M:%S"
        self._handlers = list()

    def add_handler(self, handler: IHandler):
        self._handlers.append(handler)

    def del_handler(self, handler: IHandler):
        self._handlers.remove(handler)

    def log(self, message):
        for i in self._handlers:
            i.log(self.formatter, message)
