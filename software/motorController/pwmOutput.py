
#import RPi.GPIO as GPIO
import time
import sys

class PWM:
  def __init__(self, pin):
    self.pin = pin
    #GPIO.setup(self.pin, GPIO.OUT)
    #GPIO.output(self.pin, 0)
    #self.pwm = GPIO.PWM(self.pin, 100)
    #self.pwm.start(0)

  def setDutyCycle(self, val):
    #self.pwm.ChangeDutyCycle(val)
    pass

  def stop(self):
    #self.pwm.stop()
    #GPIO.output(self.pin, 0)
    pass

if __name__ == '__main__':
  try:
    #GPIO.setmode(GPIO.BOARD)
    p = PWM(32)
    while True:
      p.setDutyCycle(int(time.time()*100 % 100))
      time.sleep(.03)
  except KeyboardInterrupt:
    #GPIO.cleanup()
    sys.exit(0)