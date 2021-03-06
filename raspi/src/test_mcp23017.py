#!/usr/bin/python3
import MCP23017
import unittest
import logging

log = logging.getLogger("Test.MCP23017")

class ChipTest(unittest.TestCase):
  chip1 = MCP23017.MCP23017(0x20, {'A': 17})#, 'B': 0x00})
  chip2 = MCP23017.MCP23017(0x21, {'A': 27})#, 'B': 0x00})
  def test_test_set_config(self):
    self.chip1.set_config(self.chip1.IOCON['MIRROR'])

  def test_read_registers_bank_set(self):
    self.chip1.set_config(self.chip1.IOCON['BANK'])
    for i in range(0x1B):
      byte = self.chip1.read(i)
      log.info(byte)

  def test_unset_config(self):
    self.chip1.unset_config(self.chip1.IOCON['MIRROR'])

  def test_set_callback(self):
    def myCallback(ticklist): #one byte, the ports where ticks have been detectet are set
      log.info(ticklist)
    self.chip1.set_interrupt_handler(myCallback)
      

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger( "MCP23017" ).setLevel( logging.DEBUG )
    log.setLevel(logging.DEBUG)
    unittest.main()
