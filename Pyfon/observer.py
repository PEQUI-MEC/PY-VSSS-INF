class Subscriber:
    def __init__(self, name):
        self.name = name

    def update(self, action):
        print('{} recebeu "{}"'.format(self.name, action))


class Publisher:
    def __init__(self, events):
        self.subscribers = {
            event: dict()
            for event in events
        }

    def get_subscribers(self, event):
        return self.subscribers[event]

    def register(self, event, who, callback=None):
        if callback is None:
            callback = getattr(who, 'update')
        self.get_subscribers(event)[who] = callback

    def unregister(self, event, who):
        del self.get_subscribers(event)[who]

    def dispatch(self, event, action):
        for subscriber, callback in self.get_subscribers(event).items():
            callback(action)
