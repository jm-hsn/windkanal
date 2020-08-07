#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import bluetooth
import time

class GSV4BT():
  # https://www.manualslib.com/manual/1380505/Me-Gsv-4.html?page=30#manual
  scalings = {
    # (ID, value for 0xFFFF, unit)
    '2mV':    (0x01, 2.1 , 'mV/V'),  # Measuring range ±2 mV/V (set_gain 0xB2 <p1> <p2>) with p1=ch, p2=0x01
    '10mV':   (0x02, 10.5, 'mV/V'),  # Measuring range ±10 mV/V (set_gain 0xB2 <p1> <p2>) with p1=ch, p2=0x02
    '5V':     (0x03, 5.25, 'V'   ),  # Measuring range 0-5 V (set_gain 0xB2 <p1> <p2>) with p1=ch, p2=0x03
    '10V':    (0x07, 10.5, 'V'   ),  # Measuring range 0-10 V (set_gain 0xB2 <p1> <p2>) with p1=ch, p2=0x07
    'PT1000': (0x04, 1050, '°C'  ),  # Measuring range PT1000 (set_gain 0xB2 <p1> <p2>) with p1=ch, p2=0x04
    'K':      (0x06, 1050, '°C'  )   # Measuring range K-thermocouple cable (set_gain 0xB2 <p1> <p2>) with p1=ch, p2=0x06
  }
  channelModes = [
    None,
    None,
    None,
    None
  ]

  values = [0] * 4

  frequencies = [
    # (ID, fNom in Hz, fEff in Hz)
    (0xA0, 0.63, 0.625),
    (0xA1, 1.25, 1.250),
    (0xA2, 2.5 , 2.500),
    (0xA3, 3.75, 3.750),
    (0xA4, 6.25, 6.250),
    (0xA5, 7.5 , 7.500),
    (0xA6, 12.5, 12.40),
    (0xA7, 15  , 14.7 ),
    (0xA8, 25  , 24.4 ),
    (0xA9, 125 , 125  ),
    (0xAA, 250 , 250  ),
    (0xAB, 500 , 500  ),
    (0xAC, 937.5, 900 ),
  ]

  def __init__(self, addr):
    self.addr = addr
    self.uuid = None
    self.sock = None
    self.requiresSetup = True

  def printError(self, msg, var = ""):
    print("ERROR:   GSV4BT {}:".format(self.addr), msg, var)

  def printWarning(self, msg, var = ""):
    print("WARNING: GSV4BT {}:".format(self.addr), msg, var)

  def connect(self):
    if self.sock:
      return True
    
    service_matches = bluetooth.find_service(address=self.addr, uuid=bluetooth.SERIAL_PORT_CLASS)
    if len(service_matches) == 0:
      self.printError("BT device not found.")
      return False
    
    first_match = service_matches[0]
    self.port = first_match["port"]
    self.name = first_match["name"]
    self.host = first_match["host"]

    self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    try:
      ret = self.sock.connect((self.addr, self.port))
    except bluetooth.btcommon.BluetoothError as e:
      self.printError(e)
      self.sock.close()
      self.sock = None
      return False

    self.printWarning("Connected to \"{}\" on {} port {}".format(self.name, self.host, self.port))
    self.sock.settimeout(0.3)
    return True
  
  def isConnected(self):
    return self.sock != None
  
  def disconnect(self):
    if self.sock:
      self.sock.close()
      self.sock == None

  def sendRaw(self, data):
    if self.sock:
      try:
        self.sock.send(data)
      except bluetooth.btcommon.BluetoothError as e:
        self.printError("send", e)

  def sendCommand(self, code, *params):
    data = bytes([code] + list(params))
    return self.sendRaw(data)

  def setNormalMode(self):
    return self.sendRaw(bytes([0x26, 0x01, 0x62, 0x65, 0x72, 0x6C, 0x69, 0x6E]))

  def getMode(self):
    self.sendCommand(0x27)
    return self.waitResponse(0x27)

  def getFirmwareVersion(self):
    self.sendCommand(0x2B)
    return self.waitResponse(0x2B)
  
  def getTxStatus(self):
    self.sendCommand(0x29)
    return self.waitResponse(0x29)

  # https://www.manualslib.com/manual/1380505/Me-Gsv-4.html?page=34#manual
  def setGain(self, channel, scalingName = '2mV'):
    self.channelModes[channel] = scalingName
    self.sendCommand(0xB2, channel, self.scalings[scalingName][0])
    return self.waitResponse(0xB2)

  def setFrequency(self, freq = 10):
    for id, fNom, fEff in self.frequencies:
      value = id
      if freq < fEff:
        break
    self.sendCommand(0x12, value)
    return self.waitResponse(0x12)

  def startTransmission(self):
    self.sendCommand(0x24)
    return self.waitResponse(0x24)

  def stopTransmission(self):
    self.sendCommand(0x23)
    return self.waitResponse(0x23)

  def getValue(self):
    self.sendCommand(0x3B)

  lastFrameCarry = None
  def recvRaw(self):
    if not self.sock:
      return
    data = None
    try:
      data = self.sock.recv(1024)
    except bluetooth.btcommon.BluetoothError as e:
      self.printError("receive", e)

    if data == None:
      return

    if self.lastFrameCarry:
      data = self.lastFrameCarry + data
      self.lastFrameCarry = None

    i = 0
    while i < len(data):
      prefix = data[i]
      start = i
      i += 1
      end = data.find(b'\r\n', start)

      if end == -1:
        self.lastFrameCarry = data[start:]
        break
      else:
        i = end + 2

      if prefix == 0xA5:
        # measured values
        if end+2 - start != 11:
          self.printError("invalid values frame: length {}".format(end+2-start), data[start:end+2])
          continue
        self.parseValues(data[start+1:end])
      elif prefix == 0x3B:
        # response
        if end+2 - start < 10:
          self.printError("invalid response frame: length {}".format(end+2-start), data[start:end+2])
          continue

        code   = int(data[start+1])
        n      = int(data[start+2])
        length = int.from_bytes(data[start+3:start+5], 'big', signed=False)
        no     = data[start+5:start+8].decode('ascii')
        if end+2 - start != length + 10:
          self.printError("incorrect response length field: {}".format(length), data[start:end+2])
          continue
        self.parseResponse(code, n, no, data[start+8:end])

  _valuesCb = None

  def setValuesCb(self, cb):
    self._valuesCb = cb

  def parseValues(self, data):
    for i in range(4):
      self.values[i] = int.from_bytes(data[i*2:i*2+2], 'big', signed=False)
      # map range to units
      if self.channelModes[i] == None:
        continue
      _, scale, unit = self.scalings[self.channelModes[i]]
      self.values[i] = (self.values[i] - 32768) / 32768 * scale
    if self._valuesCb:
      self._valuesCb(self.values)

  _respCode = None
  _respData = None
  def _responseCbWait(self, code, data):
    self._respCode = code
    self._respData = data

  _responseCb = None
  def setResponseCb(self, cb):
    self._responseCb = cb

  def waitResponse(self, sentCode):
    userRespCb = self._responseCb
    self._respCode = None
    self._respData = None
    self.setResponseCb(self._responseCbWait)
    self.recvRaw()
    if self._respCode == None:
      return None
    if self._respCode != sentCode:
      self.printError("invalid response code:", hex(self._respCode))
      return None
    self.setResponseCb(userRespCb)
    return self._respData

  def parseResponse(self, code, n, no, data):
    if n > 1:
      self.printWarning("more than 1 response:", n-1)

    if self._responseCb:
      self._responseCb(code, data)

  def getForces(self):
    self.recvRaw()
    return self.values[0:3]

  def close(self):
    self.sock.close()

if __name__ == "__main__":
  cell = GSV4BT("00:0B:CE:04:F6:66")
  def cb(values):
    print(values)
  while True:
    if cell.isConnected():
      cell.recvRaw()
    else:
      cell.connect()
      cell.setNormalMode()
      cell.setFrequency(20) # Hz
      cell.setGain(0, '2mV')
      cell.setGain(1, '2mV')
      cell.setGain(2, '2mV')
      cell.setGain(3, '5V')
      cell.setValuesCb(cb)
      print(cell.getMode())
    time.sleep(0.3)