#!/usr/bin/python3
import logging

import datetime
import time
from threading import Thread
from queue import Queue, Empty

from PC4004B import PC4004B
from MCP23017 import MCP23017, IOCON

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

#SET UP SHIELD
chip1 = MCP23017(0x20, 1)
chip2 = MCP23017(0x21, 1)

chip1.init_ports({'A':4, 'B':17})
chip1.set_config(IOCON['INTPOL'])
chip1.set_interrupt_handler(myCallback)

chip2.init_ports({'A':22, 'B':27})
chip2.set_config(IOCON['INTPOL'])
chip2.set_interrupt_handler(myCallback)


thread_consumer = Thread(target = json_tick_consumer)
thread_consumer.start()
thread_consumer.join()



