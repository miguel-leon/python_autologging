import logging
import inspect

from functools import wraps

import logs_composer


class AutoLogging:
    def __init__(self, logger=logging.getLogger(), handler=None, loglevel=logging.INFO):
        self.logger = logger

        if handler is None:
            handler = logs_composer.for_callable
        self.handler = handler

        self.loglevel = loglevel

    def loggable(self, target):
        @wraps(target)
        def wrapper(*args, **keywords):
            self.logger.log(self.loglevel, self.handler(target, args, keywords))
            return target(*args, **keywords)

        return wrapper

    def staticmethod_loggable(self, target):
        @wraps(target)
        def wrapper(_, *args, **keywords):
            self.logger.log(self.loglevel, self.handler(target, args, keywords))
            return target(*args, **keywords)

        return wrapper

    def all_by_predicate(self, container, predicate):
        for item in inspect.getmembers(container, predicate=predicate):
            setattr(container, item[0], self.loggable(item[1]))

    def all_methods(self, cls):
        self.all_by_predicate(cls, inspect.ismethod)
        # static methods
        for item in inspect.getmembers(cls, predicate=inspect.isfunction):
            setattr(cls, item[0], self.staticmethod_loggable(item[1]))
        return cls

    def all_functions(self, module):
        self.all_by_predicate(module, inspect.isfunction)
