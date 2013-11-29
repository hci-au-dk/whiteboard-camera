#!/usr/bin/env python
import requests
import RPi.GPIO as GPIO
import socket
import time

def issue_request():
    ip = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        ip = s.getsockname()[0]
    except:
        print 'Error in network'
    pi_location = 'http://' + ip + '/button-snapshot'
    r = requests.get(pi_location)

GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.IN)

#initialise a previous input variable to 0 (assume button not pressed last)
prev_input = True
while True:
    input = GPIO.input(11) #take a reading
  #if the last reading was low and this one high, print
    if ((not prev_input) and input):
        issue_request()
    prev_input = input #update previous input
    time.sleep(0.05) #slight pause to debounce
