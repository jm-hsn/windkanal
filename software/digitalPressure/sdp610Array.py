import smbus
import time

class Spd610Array():
  i2cAddresses = (
    0x21,
    0x41,
    0x61,
    0x31,
    0x39,
    0x29,
    0x35,
    0x40
  )
  def __init__(self):
    self.bus = smbus.SMBus(0)

  def readValue(self, addr):
    try:
      self.bus.write_byte_data(addr, 0, 0xF1)
      block = self.bus.read_i2c_block_data(addr, 0, 3)
      value = (block[0] * 256 + block[1]) / 240.0
      crc = block[2]
      return value
    except OSError as e:
      print("ERROR:   I2C SPD610 {:X}: ".format(addr), e)
      return None

  def getValues(self):
    values = [0] * len(self.i2cAddresses)
    for i in range(len(self.i2cAddresses)):
      values[i] = self.readValue(self.i2cAddresses[i])
    return values

if __name__ == "__main__":
  sdp = Spd610Array()
  while True:
    print(sdp.getValues())
    time.sleep(1)

