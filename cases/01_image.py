#!/usr/bin/env python3

import picamera

import sys
sys.path.append("..")

import traction

# setup picamera plugin
# attach trigger to capture
# when capture is done, report recent image?
# trigger
# {
#   'plugin': 'rpicamera',
#   'action': 'capture',
#   'attributes': ...,
#   'arguments': ...,
# }
# filename
# capture arguments (or picamera attributes)


def tmatch(trigger):
    if trigger.data.get('plugin', '') != 'rpicamera':
        return False
    if trigger.data.get('action', '') != 'capture':
        return False
    return True


class CaptureAction(traction.Action):
    # TODO run in other process
    def trigger(self, trigger, context):
        # TODO get attributes from trigger
        # TODO get filename from trigger
        filename = 'test.jpg'
        # TODO get camera from context
        # capture image
        with picamera.PiCamera() as camera:
            camera.capture(filename)
        # TODO return filename as trigger
        # return filename


traction.register_trigger(tmatch, CaptureAction)
traction.run()
