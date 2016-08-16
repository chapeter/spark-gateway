
class Provider(object):

    def __init__(self):
        self.msg_queue = []
        self.subscribers = []

    def notify(self, msg):
        self.msg_queue.append(msg)

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, msg, subscriber):
        self.subscribers.remove(subscriber)

    def update(self):
        for msg in self.msg_queue:
            for sub in self.subscribers:
                sub.run(msg)
        self.msg_queue = []
