from core import Publisher

MODULE_NAME = 'MQTT Plugin'
MODULE_VERSION = '0.1a'


try:
    import paho.mqtt.client as mqtt

except ImportError:
    PAHO_INSTALLED = False


def get_plugin_conf(conf):
    """
    Returns plugin specific configuration
    :param conf:
    :return:
    """
    return conf['plugins']['mqtt']


def get_subscription_list(mqtt_conf):
    """
    Returns a list of (topic, qos) tuples

    :param mqtt_conf: mqtt plugin configuration dictionary
    :return: list List of (topic, qos) tuples
    """
    subjects = []
    rooms = mqtt_conf['rooms']
    qos = mqtt_conf['default_qos']
    for r in rooms.keys():
        for topic in rooms[r]:
            subj = (topic, qos)
            subjects.append(subj)
    return subjects


def get_rooms_by_topic(conf, topic):
    """
    :param conf:
    :param topic:
    :return:
    """
    rooms = list()
    for room in conf['rooms'].keys():
        topics = conf['rooms'][room]
        for t in topics:
            if t.endswith('#'):
                # Wildcard topic
                if topic.startswith(t[:-1]):
                    rooms.append(room)
            elif t == topic:
                rooms.append(room)
    return rooms


def initialize(conf):

    mqttc = mqtt.Client()

    # Make configuration available to mqttc
    mqttc.conf = conf
    mqttc.plugin_conf = get_plugin_conf(conf)
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    # Connect
    mqttc.connect(mqttc.plugin_conf['server'], mqttc.plugin_conf['port'], 60)
    # Subscribe
    mqttc.subscribe(get_subscription_list(mqttc.plugin_conf))

    # Start MQTT loop in background thread

    mqttc.loop_start()


def on_connect(mosq, obj, rc):
    print("connected to MQTT broker")


def on_message(mosq, obj, msg):
    global message
    message = msg.topic + " " + str(msg.qos) + " " + str(msg.payload)

    # Determine which room the message goes to based on configuration

    rooms = get_rooms_by_topic(mosq.plugin_conf, msg.topic)
    msg_dict = {'msg': message,
                'rooms': rooms,
                'plugin_data': {
                    'qos': msg.qos,
                    'payload': msg.payload,
                    'topic': msg.topic
                }
                }

    pub = Publisher(mosq.conf['messages'])
    pub.publish(msg_dict)


def on_publish(mosq, obj, mid):
    # print("mid: " + str(mid))
    pass


def on_subscribe(mosq, obj, mid, granted_qos):
    # print("Subscribed: " + str(mid) + " " + str(granted_qos))
    pass


def on_log(mosq, obj, level, string):
    # print(string)
    pass
