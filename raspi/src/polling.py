#!/usr/bin/python3
from MCP23017 import MCP23017
import logging
logging.basicConfig()
logging.getLogger( "MCP23017" ).setLevel( logging.DEBUG )

chips = [MCP23017(0x20, 1),
          MCP23017(0x21, 1)]





#enable interrupts:
chip[0].init_interrupts({'A': 4, 'B': 17})
chip[1].init_interrupts({'A': 22, 'B':27})

def handler(string):
  print(string)

chip[0].set_interrupt_handler(handler)
chip[0].set_interrupt_handler(handler)

while 1:
  for chip in chips:
    chip.read(0x09)
    chip.read(0x19)
