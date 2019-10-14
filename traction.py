#!/usr/bin/env python3

import http.client
import http.server
import json
import socketserver
import time
import urllib.request

# TODO plugins
# import plugins


def server_url_from_context(context):
    (ip, port) = context.request.getsockname()
    return 'http://%s:%i%s' % (ip, port, context.path)


def send_post(url, data, no_reply=True):
    req = urllib.request.Request(url)
    req.add_header("Content-Type", "application/json")
    bs = json.dumps(data).encode('ascii')
    req.add_header("Content-Length", len(bs))
    try:
        res = urllib.request.urlopen(req, bs)
    except http.client.RemoteDisconnected as e:
        if no_reply:
            return
        raise e


class Trigger(object):
    def __init__(self, data):
        self.data = data
        # creation time
        self.ctime = time.time()
        self.enabled = True

    def disable(self):
        self.enabled = False

    # TODO pickle/pack function (to allow saving and restarting)
    # TODO timeout?


class Action(object):
    """
    methods here should return quickly as all actions
    run in the same thread
    """
    def trigger(self, trigger, context):
        # might enable/disable/start/stop
        # TODO release trigger? to keep track of what should be restarted
        # context should allow:
        # - sending triggers
        # - replying to http message [for streaming, image reply, etc]
        pass

    #def enable(self, context, trigger=None):
    #    pass

    #def disable(self, context, trigger=None):
    #    pass

    #def start(self, trigger, context):
    #    pass

    #def stop(self, trigger, context):
    #    pass

    #def run(self, trigger, context):
    #    pass

    # TODO destroy/kill? for uncooperative actions


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        #print("==== GET ====")
        #d = vars(self)
        #for k in d:
        #    print(k, d[k])
        # TODO serve up static files?
        # TODO serve up templated html file
        if (self.path == "/"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write("<html><p>Hi</p></html>".encode())

    def do_POST(self):
        #print("==== POST ====")
        if (
                ("Content-Length" not in self.headers) or
                ("Content-Type" not in self.headers)):
            # TODO error, invalid
            return
        nb = self.headers["Content-Length"]
        if not nb.isdigit():
            # TODO error, invalid
            return
        nb = int(nb)
        if nb < 1:
            # TODO error, invalid
            return
        body = self.rfile.read(nb)
        if self.headers["Content-Type"] != "application/json":
            # TODO error, invalid
            return
        # read in json data
        jdata = json.loads(body.decode('ascii'))
        # make new trigger
        t = Trigger(jdata)

        # look for resulting actions
        self.server.process_trigger(t, self)


class TractionServer(socketserver.ThreadingMixIn, http.server.HTTPServer, object):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, address, handler):
        super(TractionServer, self).__init__(address, handler)
        self.actions = {}
        self.triggers = {}
        self._registrations = []

    def register_trigger(self, trigger_match, action):
        self._registrations.append((trigger_match, action))

    def process_trigger(self, trigger, context):
        print("Process trigger: %s[%s]" % (trigger, vars(trigger)))
        # TODO log trigger
        for r in self._registrations:
            mf, action = r
            if mf(trigger):
                print("Starting action: %s" % action.__name__)
                a = action()
                a.trigger(trigger, context)
                # TODO release trigger?
                # TODO store action?

    def run(self):
        self.serve_forever()


server = TractionServer(
    ("", 8000),
    RequestHandler)


def register_trigger(trigger_match, action):
    server.register_trigger(trigger_match, action)


def run():
    server.run()


if __name__ == '__main__':
    run()
    #server = TractionServer(
    #    ("", 8000),
    #    RequestHandler)
    #server.run()
