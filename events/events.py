class Observe:
    def __init__(self, event_name : str):
        self.eventName = event_name

    def __call__(self, func):
        def ObserverWrapper(inst, *args, **kwargs):
            r = func(inst, *args, **kwargs)

            for handler in inst.eventHandlers[self.eventName]:
                handler()

            return r

        return ObserverWrapper


class Observable:
    eventHandlers = dict()

    def __init__(self):
        print(self.__class__, self.__annotations__)




