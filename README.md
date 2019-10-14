Main process can be:

- not running
- streaming (python)
- recording (raspivid or python? python could allow frame extraction)
- still image capture (raspivid or python? python could allow frame extraction)
- primed circular buffer (raspivid or python? python could allow frame extraction)

Triggers:

- rest request (manual trigger)
- timed trigger
- gpio pin change

Triggers maybe have plugins that:

- setup (use web context, other meta?)
- enable
- check?
- disable
- teardown
- timeout?

Maybe have plugins for:

- setup
- triggers
- pre-record event: 
- record event: capture
- post-record event: extract frame
- teardown

Maybe the whole system can be triggers and actions

actions need to be separate processes, might take multiple trigger (prime, capture, etc)

they should be restartable (even across reboots)
on python reboot: read in old triggers & actions and configuration: configure then run triggers

main process:

- run actions as processes
- listen for triggers (from web server, from other plugins [gpio, camera, etc])
- report status (to control server) [do this as a plugin?]

triggers are:

- post requests:
  - request videos
  - request space
  - start capture: grab settings, filename, duration
  - request state
  - time sync: new time
  - stream: grab settings (mjpeg)
  - shutdown system
  - gpio: pin #, IO, state (change day/night mode)
- timer based (via post request? triggered by cron)
- gpio (via post request? triggered by other process?)
- image based
  - motion: grab settings, motion detection settings
  - change in intensity: grab settings, processing settings
  - NN detection: grab settings detection settings

actions are:
- report state
- sync time: set time, return nada
- shutdown system
- modify cron? (for time based recording)
- setup new triggers (install new plugins)
- camera
  - video: record video, return filename when started and done
  - image: record image, return filename when done
  - stream: stream video
- gpio
  - change pin (configure? export? etc?): change pin/return state
- filesystem
    - report space: return space on disk
    - list videos: return list of videos
    - transfer video: return video
    - clean up videos (free up space): remove videos

maybe have actions release triggers (to track which ones are still active), keep track of enabled plugins

triggers might have:
- plugin: (to route and add functionality when needed)
- time (to allow timeouts, etc maybe expiration time instead)
- optional arguments for the trigger

have triggers be chainable (trigger -> action -> trigger -> etc...)

Write the following test cases:
- [picamera] continuous record, split recording on trigger?
- [picamera] take 20s video every 1 minute
- [picamera] trigger continuous capture
- [picamera] stream video
- [filesystem] get disk space
- [filesystem] transfer new videos, clean up old
- [gpio] change pin state
- [gpio] monitor pin, issue trigger when changed {hard to test}
