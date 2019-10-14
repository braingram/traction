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
    # TODO need safe way to stop recording
    camera = None

    # TODO run in other process?
    def trigger(self, trigger, context):
        if 'command' not in trigger.data:
            # TODO error
            pass
        elif trigger.data['command'] == 'start':
            if RecordAction.camera is not None:
                RecordAction.camera.stop_recording()
            else:
                RecordAction.camera = picamera.PiCamera()
            # TODO get attributes from trigger
            # TODO get filename from trigger
            filename = 'test.h264'
            # TODO get camera from context
            # capture image
            RecordAction.camera.start_recording(filename)
            #with picamera.PiCamera() as camera:
            #    camera.start_recording(filename)
            #    camera.wait_recording(10)
            #    camera.stop_recording()
            # TODO return filename as trigger
            # return filename
        elif trigger.data['command'] == 'stop':
            if RecordAction.camera is not None:
                RecordAction.camera.stop_recording()
                RecordAction.camera.close()
                RecordAction.camera = None
            # TODO return filename as trigger
        elif trigger.data['command'] == 'split':
            filename = 'test2.h264'
            if RecordAction.camera is None:
                RecordAction.camera = picamera.PiCamera()
                RecordAction.camera.start_recording(filename)
            else:
                RecordAction.camera.split_recording(filename)
            # TODO return filename as trigger


traction.register_trigger(tmatch, RecordAction)
traction.run()
