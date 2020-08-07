from spidev import SpiDev
import time
 
class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
 
    def open(self):
        self.spi.open(self.bus, self.device)
    
    def read(self, channel = 0):
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def getVoltage(self, channel):
        return self.read(channel) / 1023.0 * 5
            
    def close(self):
        self.spi.close()

if __name__ == "__main__":
  adc = MCP3008(0,0)
  while True:
    print('\t'.join(["{}: {:8.3f} V".format(i, adc.getVoltage(i)) for i in range(4)]))
    time.sleep(.3)
