#!/usr/bin/env python3

import picamera

import sys
sys.path.append("..")

import traction


def tmatch(trigger):
    if trigger.data.get('plugin', '') != 'rpicamera':
        return False
    if trigger.data.get('action', '') != 'record':
        return False
    return True


class RecordAction(traction.Action):
    # TODO run in other process
    def trigger(self, trigger, context):
        # TODO get attributes from trigger
        # TODO get filename from trigger
        filename = 'test.h264'
        # TODO get camera from context
        # capture image
        with picamera.PiCamera() as camera:
            camera.start_recording(filename)
            camera.wait_recording(10)
            camera.stop_recording()
        # TODO return filename as trigger
        # return filename


traction.register_trigger(tmatch, RecordAction)
traction.run()
