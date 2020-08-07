if __name__ == "__main__":
  from GSV4BT import GSV4BT
else:
  from .GSV4BT import GSV4BT
  

import time
import bluetooth
import threading
import ctypes
import numpy as np

class LoadCells():
  def __init__(self):
    self.cells = (
      GSV4BT("00:0B:CE:04:F6:66"),
      GSV4BT("00:0B:CE:04:F6:67"),
      GSV4BT("00:0B:CE:04:F6:68"),
    )
    self.tareValues = np.ndarray(shape=(len(self.cells),3), dtype=float)
    self.tareValues.fill(0)

  def connect(self):
    success = True
    for cell in self.cells:
      if not self.running:
        return
      elif cell.isConnected():
        if cell.requiresSetup:
          cell.setNormalMode()
          cell.stopTransmission()
          cell.setFrequency(20) # Hz
          cell.setGain(0, '2mV')
          cell.setGain(1, '2mV')
          cell.setGain(2, '2mV')
          mode = cell.getMode()
          if mode and mode[0] == 0x01:
            cell.requiresSetup = False

      elif cell.connect():
        cell.requiresSetup = True
      else:
        success = False
        cell.requiresSetup = True
    return success

  def reconnectThread(self):
    while self.running:
      time.sleep(1)
      self.connect()

  def start(self):
    self.running = True
    self.thread = threading.Thread(target=self.reconnectThread)
    self.thread.daemon = True
    self.thread.start()
  

  def tare(self):
    for i in range(len(self.cells)):
      cell = self.cells[i]
      if (not cell.isConnected()) or cell.requiresSetup:
        self.tareValues[i].fill(0)
      else:
        cell.getValue()
        self.tareValues[i] = cell.getForces()
    self.tareValues[np.isnan(self.tareValues)] = 0

  def stop(self):
    for cell in self.cells:
      cell.disconnect()
    self.running = False

  def getForces(self):
    res = np.ndarray(shape=(len(self.cells),3), dtype=float)
    for i in range(len(self.cells)):
      cell = self.cells[i]
      if (not cell.isConnected()) or cell.requiresSetup:
        res[i].fill(float('NaN'))
      else:
        cell.getValue()
        res[i] = cell.getForces()
    return res - self.tareValues

  def scan(self):
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("Found {} devices.".format(len(nearby_devices)))

    for addr, name in nearby_devices:
      print("  {} - {}".format(addr, name))

if __name__ == "__main__":
  cells = LoadCells()

  cells.scan()
  try:
    cells.start()
    while True:
      for vals in cells.getForces():
        if not np.isnan(vals[0]):
          print('cell: ' + ' '.join(["ch {}: {:8.3f} mV/V".format(i, vals[i]) for i in range(len(vals))]))
      time.sleep(.3)


  except KeyboardInterrupt as e:
    cells.stop()