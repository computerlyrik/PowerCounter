#!/usr/bin/python3
from MCP23017.MCP23017 import MCP23017
import logging
logging.basicConfig()
logging.getLogger( "MCP23017" ).setLevel( logging.DEBUG )


chips = [MCP23017(0x20, 1),
          MCP23017(0x21, 1)]

ports = {}
#SET UP SHIELD
chip1 = MCP23017(0x20, 1)
chip1.set_config(IOCON['INTPOL'])
ports.update(chip1.generate_ports({'A':4, 'B':17}))

chip2 = MCP23017(0x21, 1)
chip2.set_config(IOCON['INTPOL'])
ports.update(chip2.generate_ports({'A':22, 'B':27}))

def handler(string):
  print(string)

for name,port in ports.items():
  print(" Setting up port "+name)
  #Set port to input pin
  port.pin_mode(0xff)
  # WRITE Register activate internal pullups
  port.pullup_mode(0xFF)
  #set our callback
  port.set_callback(myCallback)


while 1:
  for name,port in ports.items():
    port.digital_read()
