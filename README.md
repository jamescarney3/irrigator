# Irrigator

![mist heads and pea shoots](https://github.com/jamescarney3/irrigator/blob/8fada5d2c96b7cba49bd91c72085cc935a66d202/media/mist_heads.jpg)

This is the software brain that runs a small mist-irrigation system that lives on
a shelving unit in my pantry. The system consists of a 2g reservoir, a diaphragm
pump, and a solenoid valve that opens an closes a drain line. When the solenoid is
closed, the pump can pressurize the main water line which incorporates a series
of misting nozzles. When the solenoid is opened, it allows the depressurized line
to drain back into the reservoir. The plumbing hardware is controlled by the GPIO
pins of a Raspberry Pi through a pair of relays and powered by the AC main through
the appropriate DC adaptors.

This repo includes the I/O scripts that control the GPIO pins, an adaptor module
that manages cron tasks related to this tool, and a simple Flask application that
serves a web UI for scheduling (and unscheduling) said cron tasks.

## Roadmap
- write status logs, serve them in the flask app
- GPIO pin numbers should probably be configurable and passed in a startup script
- almost put "add a frontend that builds to a dist directory" here but I will not
  be doing this because the application only has one resource
