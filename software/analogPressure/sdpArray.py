if __name__ == "__main__":
  from mcp3008 import MCP3008
else:
  from .mcp3008 import MCP3008

import time

class SdpArray:
  def __init__(self):
    self.adcs = (
      MCP3008(0, 0), 
      MCP3008(0, 1)
    )

  def getVoltage(self, channel):
    if channel < 8:
      return adc[0].getVoltage(channel) 
    else:
      return adc[1].getVoltage(channel-8)

if __name__ == "__main__":
  sdps = SdpArray()
  while True:
    print("Anliegende Spannung:", sdps.getVoltage(0))
    time.sleep(1)