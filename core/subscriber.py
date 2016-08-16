from spark.session import Session
from spark.messages import Message
from spark.rooms import Room


class Subscriber(object):
    """
    A Basic Subscriber class, plugins may subclass this
    """

    def __init__(self, name, conf, queue):
        self.name = name
        self.provider = queue
        self.conf = conf
        self.session = Session(conf['spark']['url'], conf['spark']['token'])

    def _create_new_room(self, room):
        """
        Used if a room is specified in configuration that does not exist

        :param room:
        :return:
        """
        print 'Creating New Room'
        newroom = Room()
        newroom.title = room
        newroom.create(self.session)
        return newroom

    def run(self, msg):
        """

        :param msg: a dictionary containing message info
        :return:
        """

        message = Message()

        for room in msg['rooms']:
            sparkroom = Room.get(self.session, name=room)
            # If Room.get() returns a list, the room needs to be created
            if isinstance(sparkroom, list):
                sparkroom = self._create_new_room(room)

            message.text = msg['msg']
            try:
                sparkroom.send_message(self.session, message).text
            except Exception, e:
                print "Could not send message: {}".format(e)

    def subscribe(self):
        self.provider.subscribe(self)

    def unsubscribe(self):
        self.provider.unsubscribe(self)
