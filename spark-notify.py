import yaml
import imp
import os
from core import Provider, Subscriber

try:
    import hashlib
    md = hashlib.md5
except ImportError:
    import md5
    md = md5.new


def load_module(path):
    try:
        modfile = open(path, 'rb')
        return imp.load_source(md(path).hexdigest(), path, modfile)
    finally:
        try:
            modfile.close()
        except Exception, e:
            raise Exception(e)


def load_plugins(queue, plugins):
    for p in plugins:
        modulefile = 'plugins/{}.py'.format(p)
        active_plugins[p] = {}

        try:
            active_plugins[p]['module'] = load_module(modulefile)
            active_plugins[p]['config'] = CONF['plugins'].get(p)
            active_plugins[p]['module'].initialize(CONF)
            print "Loaded plugin " \
                  "- {}".format(active_plugins[p]['module'].MODULE_NAME)
        except AttributeError, e:
            print "Error Loading plugin - {}".format(p, e)


if __name__ == '__main__':

    with open('config.yml') as fh:
        CONF = yaml.safe_load(fh)

    active_plugins = {}
    queue = Provider()

    CONF['messages'] = queue
    CONF['spark']['token'] = os.getenv("SPARK_TOKEN")

    load_plugins(queue, CONF['plugins'].keys())

    spark = Subscriber('SPARK', CONF, queue)
    spark.subscribe()

    while True:
        queue.update()
