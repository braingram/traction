#!/usr/bin/env python3

import picamera

import sys
sys.path.append("..")

import traction


# TODO TimerAction
# sends periodic triggers (from a separate thread)


def tmatch(trigger):
    if trigger.data.get('plugin', '') != 'rpicamera':
        return False
    if trigger.data.get('action', '') != 'record':
        return False
    return True


class RecordAction(traction.Action):
    def __init__(self):
        self.camera = None

    # TODO run in other process?
    def trigger(self, trigger, context):
        if 'command' not in trigger.data:
            # TODO error
            pass
        elif trigger.data['command'] == 'start':
            if self.camera is not None:
                self.camera.stop_recording()
            else:
                self.camera = picamera.PiCamera()
            # TODO get attributes from trigger
            # TODO get filename from trigger
            filename = 'test.h264'
            # TODO get camera from context
            # capture image
            self.camera.start_recording(filename)
            #with picamera.PiCamera() as camera:
            #    camera.start_recording(filename)
            #    camera.wait_recording(10)
            #    camera.stop_recording()
            # TODO return filename as trigger
            # return filename
        elif trigger.data['command'] == 'stop':
            if self.camera is not None:
                self.camera.stop_recording()
                self.camera.close()
                self.camera = None
            # TODO return filename as trigger
        else trigger.data['command'] == 'split':
            filename = 'test2.h264'
            if self.camera is None
                self.camera = picamera.PiCamera()
                self.camera.start_recording(filename)
            else:
                self.camera.split_recording(filename)
            # TODO return filename as trigger

    def __del__(self):
        if self.camera is not None:
            self.camera.close()


traction.register_trigger(tmatch, RecordAction)
traction.run()
