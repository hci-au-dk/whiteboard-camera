#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

from util import printer

GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.IN)

#initialise a previous input variable to 0 (assume button not pressed last)
prev_input = True
printer = printer.ThermalPrinter()

while True:
    input = GPIO.input(11) #take a reading
  #if the last reading was low and this one high, print
    if ((not prev_input) and input):
        printer.print_text("Button pressed!")
        printer.linefeed(3)
    prev_input = input #update previous input
    time.sleep(0.1) #slight pause to debounce
