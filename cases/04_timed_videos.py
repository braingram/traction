#!/usr/bin/env python3

import threading
import time

import picamera

import sys
sys.path.append("..")

import traction


def record_trigger_match(trigger):
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


def timer_trigger_match(trigger):
    if trigger.data.get('plugin', '') != 'timer':
        return False
    return True


class TimerAction(traction.Action):
    timers = {}
    timer_index = 0

    def trigger(self, trigger, context):
        if 'command' not in trigger.data:
            # TODO error
            return
        if trigger.data['command'] == 'start':
            return self.start_timer(trigger, context)
        elif trigger.data['command'] == 'stop':
            return self.stop_timer(trigger, context)

    def start_timer(self, trigger, context):
        # start new timer
        # - repeat?
        # - interval
        # - trigger
        # - name?
        if (
                ('interval' not in trigger.data) or
                ('trigger' not in trigger.data)):
            # TODO error
            return
        repeat = bool(trigger.data.get('repeat', False))
        interval = float(trigger.data['interval'])
        timer_trigger = trigger.data['trigger']
        if 'name' not in trigger.data:
            name = 'timer_%i' % TimerAction.timer_index
            TimerAction.timer_index += 1
        else:
            name = trigger.data['name']

        server_url = traction.server_url_from_context(context)

        # start timer with name
        def run(
                name=name, timer_trigger=timer_trigger,
                interval=interval, repeat=repeat,
                server_url=server_url):
            while name in TimerAction.timers:
                time.sleep(interval)
                # TODO emit trigger
                print("emit trigger: %s" % timer_trigger)
                traction.send_post(server_url, timer_trigger)
                if not repeat:
                    del TimerAction.timers[name]

        t = threading.Thread(target=run, daemon=True)
        TimerAction.timers[name] = t
        t.start()

    def stop_timer(self, trigger, context):
        if 'name' not in trigger.data:
            return
        name = trigger.data['name']
        if name not in TimerAction.timers:
            return
        del TimerAction.timers[name]


traction.register_trigger(record_trigger_match, RecordAction)
traction.register_trigger(timer_trigger_match, TimerAction)
traction.run()
