#!/usr/bin/python3
import requests
import json
from queue import Queue, Empty
import time
import datetime
from threading import Thread
import re
import quick2wire.i2c as i2c
import RPi.GPIO as GPIO

from PC4004B import PC4004B

# no such animal (yet)
#from IOShield import IOShield


def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0


tick_service_url = "http://localhost:8080/powercounter/tick"
display_service_url = "http://localhost:8080/powercounter/stats/overall"
service_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}


ticks_queue = Queue()

display = PC4004B()
display.send_text("Initializing...", 1)

def display_show_failure(message):
  display.send_text("FAILURE",1)
  display.send_text(message[:PC4004B.DISPLAY_WIDTH],2)

# iopi chip i2c addresses
expander_addresses = { 0x20, 0x21 }
# registers in sequential mode. increment by one for input msb. or use autoincrement when reading or writing two bytes.
# this is ONLY for iocon.bank=0
expander_registers = {
    "iocon": 0x0A, 
    "iodir": 0x00, 
    "ipol": 0x02, 
    "gpinten": 0x04, 
    "defval": 0x06,
    "intcon": 0x08,
    "gppu": 0xC, 
    "intf": 0x0E,
    "intcap": 0x10,
    "gpio": 0x12,
    "olat": 0x14 
    }

with i2c.I2CMaster() as bus:
  for address in expander_addresses:
# configure IOCON
# bit7            ...               bit1   bit8
# BANK MIRROR SEQOP DISSLW HAEN ODR INTPOL None
# POS for all bits is 0
# bank: 0 => register organization sequential
# mirror: 1 => both IRQ pins are internally connected (16bit mode)
# seqop: 0 => do autoincrement address pointer on read
# disslw: 0 => do not deslew SDA
# haen: 0 => address pin config enable, MCP23S17 only (not used)
# odr: 0 => interrupt pins work as open drains TODO clarify electrical connection
# intpol: 0 => if odr is disabled, controls int pins driving polarity
# 
    try:
      bus.transaction(i2c.writing_bytes(address, expander_registers["iocon"], 0b0100000))
# configure all pins for input
      bus.transaction(i2c.writing_bytes(address, expander_registers["iodir"], 0xFF, 0xFF))
# configure all pins for internal pullup 
# TODO wire the pins through the optical couplers to logical ground
      bus.transaction(i2c.writing_bytes(address, expander_registers["gppu"], 0xFF, 0xFF))
# input polarity is inverted. opto open = pullup active. therefore, invert.
      bus.transaction(i2c.writing_bytes(address, expander_registers["ipol"], 0xFF, 0xFF))
# configure interrupt behavior: trigger when input changes to high.
# this is actually default, but needs to be parameterized
      bus.transaction(i2c.writing_bytes(address, expander_registers["defval"], 0x00, 0x00))
# configure interrupt behavior: trigger on compare with DEFVAL instead of both flanks
      bus.transaction(i2c.writing_bytes(address, expander_registers["intcon"], 0xFF, 0xFF))
# interrupt source pins: all
      bus.transaction(i2c.writing_bytes(address, expander_registers["gpinten"], 0xFF, 0xFF))

    except IOError as ex:
      display_show_failure(str(ex))
      while True:
        time.sleep(1) # keep the display ports initialized until terminated.... 

#set up one interrupt line for each MCP23017 chips. INTA and INTB are initialized as synced.
GPIO.setmode(GPIO.BCM)
# pin 15, MCP configured for open drain = enabled pullup
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# pin 13
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def json_tick_consumer():
  while True:
    try:
      tick = ticks_queue.get(block=False)
    except Empty:
      time.sleep(1)
      continue
    try:
      data = {'pin': tick[0], 'bank': tick[1], 'address': tick[2], 'occurence': tick[3]}
      r = requests.post(tick_service_url, data=json.dumps(data), headers=service_headers)
    except Exception as ex:
      ticks_queue.put(tick)
      display_show_network_error(tick_service_url,str(ex))
      time.sleep(2)

def mock_tick_producer():
  while True:
    ticks_queue.put((7,0,23,int(unix_time_millis(datetime.datetime.utcnow()))))
    time.sleep(1)

# expects a simple response in the form of {lineid: 'text', lineid: 'text2'} where lineid is an int from 1-4
# only affected lines are updated
def json_display_data_updater():
  while True:
    try:
      r = requests.get(display_service_url)
      display_json = r.json
      for display_line in display_json:
        display.send_text(display_json[display_line][:PC4004B.DISPLAY_WIDTH], display_line)
    except Exception as ex:
        display_show_network_error(display_service_url, str(ex))
    time.sleep(10)    

def json_display_current_wattage_updater():
  while True:
    try:
      r = requests.get(display_service_url)
      display_json = r.json
      display.send_text("Aktueller Verbrauch:", 1)
      display.send_text("{0} Watt".format(display_json['overall']), 2)
    except Exception as ex:
      display_show_network_error(display_service_url,str(ex))
    time.sleep(2)
    

def display_show_network_error(url, message):
  display.send_text("Network down? Webserver down?", 1)
  display.send_text("request failed:", 2)
  display.send_text(url[:PC4004B.DISPLAY_WIDTH], 3)
  display.send_text(message[:PC4004B.DISPLAY_WIDTH], 4)


def iopi_tick_producer():
 with i2c.I2CMaster() as bus:
  mcp_inputs = [
# read the initial gpio state.
#      bus.transaction(i2c.reading(expander_addresses[0], expander_registers["gpio"], 2)),
#      bus.transaction(i2c.reading(expander_addresses[1], expander_registers["gpio"], 2))
    "\0\0",
    "\0\0"
  ]
  while True:
    GPIO.wait_for_edge(23, GPIO.FALLING)



#shield = IOShield(0x20, 0x21)
#shield.set_input()
#shield.activate_interrupts()

thread_consumer = Thread(target = json_tick_consumer)
thread_consumer.start()
thread_producer = Thread(target = mock_tick_producer)
thread_producer.start()
thread_update = Thread(target = json_display_current_wattage_updater)
thread_update.start()

thread_consumer.join()
thread_producer.join()
thread_update.join()
