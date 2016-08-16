class Publisher(object):

    def __init__(self, msg_center):
        self.provider = msg_center

    def publish(self, msg):
        self.provider.notify(msg)
