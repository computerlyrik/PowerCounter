import time
import quick2wire.i2c as i2c
#from smbus import SMBus
import re
import logging

# support for the "PC4004B" displays floating around the lab. 
# there is no datasheet - althought the PFY claims to have one
# pinouts have been determined by checking the controller outputs
# it contains two HD44780 compatible controllers selected by E and E2 

# for a pinout and pinmap see the accompanying documentation directory

# usage
# shield = IOShield()
# display.send_text("Up up in the butt", 1, 2) # line, chip - this will display the text in the 3rd line

log = logging.getLogger("MCP23017")
BUS = i2c.I2CMaster()

class The_Callback:
  lock = Lock()
  def __init__(self, prefix, callback):
    GPIO.add_event_detect(gpio_pin, GPIO.FALLING, callback = self.the_callback(callback))

  def the_callback(callback):
    lock.acquire()
    #READ INTF TO FIND OUT INITIATING PIN
    #READ GPIO TO GET CURRENTLY ACTIVATED PINS
    #SOMEHOW TAKE A INTERNAL STATE
    #CALL CALLBACK WITH STATE /CHANGES
    callback()
    lock.release()
class MCP23017:
  ADDRESS = 0x21
  PORTS = {0:0x00, 1:0x10}
  INTERRUPTS = None

  # Register Mapping for Bank=1 mode
  REGISTER_IODIR = 0X00
  REGISTER_IPOL = 0X01
  REGISTER_GPINTEN = 0X02
  REGISTER_DEFVAL = 0X03
  REGISTER_INTCON = 0X04
  REGISTER_IOCON = 0X05
  REGISTER_GPPU = 0X06
  REGISTER_INTF = 0X07
  REGISTER_INTCAP = 0X08
  REGISTER_GPIO = 0X09
  REGISTER_OLAT = 0X0A


  # mapping of pins inside icocon register
  IOCON = {'BANK':0b10000000, 'MIRROR': 0b01000000, 'DISSLW': 0b00010000, 'HAEN': 0b00001000, 'ODR': 0b00000100, 'INTPOL': 0b00000010}


  def __init__(self, address, interrupts):
    #self._lock = Lock()
    self.ADDRESS = address
    self.INTERRUPTS = interrupts
    #Set BANK = 1 for easier Addressing of banks (IOCON register)
    #EVERYTHING else goes to zero
    BUS.transaction( 
      i2c.writing_bytes(self.ADDRESS,0x0A, self.IOCON['BANK']))

  '''
  This method basically sets up the chip for further operations and 
  defines the electrical wiring as followes:
   - internal pullups are activated
   - connects to ground if power meter closes circuit
  '''
  def activate_interrupts(self):
      for name, prefix in self.PORTS.items():
        log.info("Configuring port 0x{0:x}".format(prefix))
        BUS.transaction(
          #Set port to input pin
          i2c.writing_bytes(self.ADDRESS,prefix|self.REGISTER_IODIR,0xff),

          ## WRITE Register configure Interrupt mode to interrupt on pin change (INTCON)
          #self.BUS.write_byte_data(chip,bank|self.REGISTER_INTCON, 0x00)
          # WRITE Register configure Interrupt mode to compare on Value(INTCON)
          i2c.writing_bytes(self.ADDRESS,prefix|self.REGISTER_INTCON, 0xff),
          # WRITE Register set compare Value 
          i2c.writing_bytes(self.ADDRESS,prefix|self.REGISTER_DEFVAL, 0xff),
          # WRITE Register activate internal pullups
          i2c.writing_bytes(self.ADDRESS,prefix|self.REGISTER_GPPU, 0xff),
          # WRITE Register Interrupt activate (GPINTEN)
          i2c.writing_bytes(self.ADDRESS,prefix|self.REGISTER_GPINTEN,0xff),
        )
  def activate_mirror(self):
    # Set MIRROR = 1 for INTA and INTB OR'd (IOCON register)
    self.set_config(self.IOCON['MIRROR'])


  def set_config(self, config):
      log.info("Register Access IOCON, adding: 0b{0:b}".format(config))
      iocon = BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, self.REGISTER_IOCON),
              i2c.reading(self.ADDRESS, 1))
      log.debug("IOCON before 0b{0:b}".format(iocon[0][0]))
      BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, self.REGISTER_IOCON, iocon[0][0] | config))
      log.debug("IOCON after 0b{0:b}".format(iocon[0][0] | config))

  def unset_config(self, config):
      log.info("Register Access IOCON, removing: 0b{0:b}".format(config))
      iocon = BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, self.REGISTER_IOCON),
              i2c.reading(self.ADDRESS, 1))
      log.debug("IOCON before 0b{0:b}".format(iocon[0][0]))
      BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, self.REGISTER_IOCON, iocon[0][0] & ~ config))
      log.debug("IOCON after 0b{0:b}".format(iocon[0][0] & ~ config))

  def add_interrupt_handler(self, callback_method):
    for name, prefix in self.PORTS.items():
      the_callback = The_Callback(prefix, callback_method)


  def read(self, register):
    byte = BUS.transaction(
              i2c.writing_bytes(self.ADDRESS, register),
              i2c.reading(self.ADDRESS, 1))
    log.debug("Reading register 0x{0:x} value 0b{1:b}".format(register, byte[0][0]))
    return byte[0][0]

'''
  def write(self, register):
    bus.transaction(i2c.writing_bytes(address, expander_registers["gpinten"], 0xFF, 0xFF))
  except IOError as ex:
    try:
      bus.close()
    except:
      pass
    display_show_failure(str(ex))
    while True:
      time.sleep(1)
''' 
