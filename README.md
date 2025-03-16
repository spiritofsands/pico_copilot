# Pico Copilot

Embedded project aimed to be a companion for a EUC rider.

## Features

* LED control:
	* status LED
	* 8 LED strips control
	* smooth animations
	* light sensor adaptive brightness
	* LED brightness calibration
* Button control
* Operation modes support (startup, poweron, poweroff)
* Failsafe operation
* Testing emulator
* Events logging
* Deployment script

## Planned features

* Test coverage
* CI
* ASPICE requirements clarification and tracing
* Screen support
* Wireless communication support
* External events trigger (Braking initiation, blinker start, etc)
* EUC link (wired, wireless)
* Raspberry Pi Pico powersave / sleep

## Dependencies

Bh1750 library for the light sensor.
Tkinter for the GUI emulator.
Rshell for deployment.

## Usage

Deploying on Pico:
`./deploy.sh clean|deploy|run|ls|get_log`

Testing:
`python3 tests/integration/test_gui.py`
