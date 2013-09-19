#!/usr/bin/python3
import logging

import datetime
import time
from threading import Thread
from queue import Queue, Empty

from PC4004B import PC4004B
from MCP23017 import MCP23017, PortManager, IOCON

# INITIALIZE DISPLAY
display = PC4004B()
display.send_text("Initializing...", 1)

#SET UP SOME HELPER METHODS
def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0

#GLOBAL CONSTANS FOR WEBAPP
tick_service_url = "http://almaz:8080/powercounter/tick"
display_service_url = "http://almaz:8080/powercounter/stats/overall"
service_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

#THE TICKS QUEUE
ticks_queue = Queue()

#CONFIGURE LOGGING
logging.basicConfig()
logging.getLogger( "MCP23017" ).setLevel( logging.DEBUG )
logging.getLogger( "PC4004B" ).setLevel( logging.DEBUG )
log = logging.getLogger("PowerCounter")
log.setLevel(logging.DEBUG)


def json_tick_consumer():
  while True:
    try:
      tick = ticks_queue.get(block=False)
      display.send_text("Pin: {0}".format(
        tick[0]), 2)
      #      (masked[0].bit_length()-1 if masked[0]>0 else masked[1].bit_length()-1)), 2)
      display.send_text("Port/Bank: {0}".format(
        tick[1]), 3)
      #      0 if masked[0]>0 else 1), 3)
      display.send_text("Address: {0}".format(
        tick[2]), 4)
    except Empty:
      time.sleep(1)


#Simply write a small callback that takes a byte reflecting the ticks on pins
def myCallback(ticklist, port, address): 
  log.info(ticklist)
  if ticklist > 0:
    for i in range(8):
      if ticklist & (1 << i):
        log.debug("Adding Tick to Queue (Pin "+str(i)+")")
        ticks_queue.put((
          i, # yields the pin number
          port, # yields the port number associated with the pin which for some reason is called bank
          address, # yields the i2c address of the controller associated with the port
          int(unix_time_millis(datetime.datetime.utcnow()))))

ports = {}
#SET UP SHIELD
chip1 = MCP23017(0x20, 1)
chip1.set_config(IOCON['INTPOL'])
ports.update(chip1.generate_ports({'A':4, 'B':17}))



chip2 = MCP23017(0x21, 1)
chip2.set_config(IOCON['INTPOL'])
ports.update(chip2.generate_ports({'A':22, 'B':27}))



for name,port in ports.items():
  print(" Setting up port "+name)
  '''
  This method basically sets up the chip for further operations and 
  defines the electrical wiring as followes:
  - internal pullups are activated
  - connects to ground if power meter closes circuit
  '''
  #Set port to input pin
  port.pin_mode(0xff)
  # WRITE Register configure Interrupt mode to compare on Value(INTCON)
  port.interrupt_compare(0xff)
  # WRITE Register set compare Value 
  port.interrupt_compare_value(0xff)
  # reflect opposite polarity of pins in GPIO register
  port.input_invert(0x00)
  # WRITE Register activate internal pullups
  port.pullup_mode(0xFF)
  # WRITE Register Interrupt activate (GPINTEN)
  port.interrupt_enable(0xff)
  
  #set our callback
  port.set_callback(myCallback)

thread_consumer = Thread(target = json_tick_consumer)
thread_consumer.start()
thread_consumer.join()



