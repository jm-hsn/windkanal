# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

from database import Table
from analogPressure.sdpArray import SdpArray
from analogPressure.mcp3008 import MCP3008
from digitalPressure.sdp610Array import Spd610Array
from wirelessLoadCell.loadCells import LoadCells
from motorController.pwmOutput import PWM
from motorController.pidController import PID
from ui import *

import tkinter as tk
import tk_tools
from tkinter import filedialog
import time
import numpy as np
import threading


class Main(tk.Tk, Table):
  running = True
  def __init__(self, *args, **kwargs):
    print('initializing window...')
    tk.Tk.__init__(self, *args, **kwargs)
    tk.Tk.wm_title(self, "Windkanal-Tool")

    #early response to user
    self.update_idletasks()

    print('initializing sensors...')
    self.adc = MCP3008(0,0)
    self.pressureSensors = Spd610Array()
    self.forceSensors = LoadCells()
    self.forceSensors.start()
    self.motorController = PWM(32)
    self.pid = PID(100/22, 5, 1)
    self.pid.setWindup(1)
    
    print('initializing database...')
    Table.__init__(self, 
    ["windspeed", "set_value", "motor_pwm"] + 
    ["pressure_{}".format(i) for i in range(8)] + 
    ["adc_{}".format(i) for i in range(1)] + 
    ["force_X_sum", "force_Y_sum", "force_Z_sum"] +
    ["force_X_1", "force_Y_1", "force_Z_1"] +
    ["force_X_2", "force_Y_2", "force_Z_2"] + 
    ["force_X_3", "force_Y_3", "force_Z_3"])


    print('initializing GUI...')
    self.menubar = tk.Menu(self)
 
    self.frameVar = tk.StringVar()
    self.menubar.add_radiobutton(indicatoron=0, variable=self.frameVar, value='Page_1', command=self.show_frame, label="Bedienelemente")
    self.menubar.add_radiobutton(indicatoron=0, variable=self.frameVar, value='Page_2', command=self.show_frame, label="Kräfte")
    self.menubar.add_radiobutton(indicatoron=0, variable=self.frameVar, value='Page_3', command=self.show_frame, label="Druck")
    self.menubar.add_radiobutton(indicatoron=0, variable=self.frameVar, value='Page_4', command=self.show_frame, label="Einstellungen")

    self.menubar.add_command(state=tk.DISABLED, label="          ")

    self.motorEnabled = tk.IntVar()
    self.menubar.add_checkbutton(indicatoron=0, variable=self.motorEnabled, background='#dd5252', label="Motor freischalten", command=lambda: 
        self.menubar.entryconfigure("Motor freischalten", background='#dd5252' if self.motorEnabled.get() == 0 else 'green'))
    self.motorEnabled.set(0)

    self.menubar.add_command(state=tk.DISABLED, label="          ")

    self.menubar.add_command(label="Messwerte speichern", command = self.save_dialog)
    self.menubar.add_command(label='Messwerte löschen', command=self.reset)

    self.menubar.add_command(state=tk.DISABLED, label="          ")

    self.menubar.add_command(label="Beenden", foreground="red", command=self.stop)

    tk.Tk.config(self, menu=self.menubar)

    container = tk.Frame(self)
    container.pack(side="top", fill="both", expand = True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    self.frames = {}

    for F in (Page_1, Page_2, Page_3, Page_4):

      frame = F(container, self)

      self.frames[F.__name__] = frame

      frame.grid(row=0, column=0, sticky="nsew")

    self.frameVar.set('Page_1')
    self.show_frame()

    print('program ready!')

    self.windspeed = 0
    self.adcValue = 0
    self.pwmValue = 0
    self.pidDelay = 100

    self.pidThread = threading.Thread(target=self.pidThreadFunction)
    self.pidThread.daemon = True
    self.pidThread.start()

    self.intervalDelay = 300 # ms
    self.interval()

  def show_frame(self):
    self.frames[self.frameVar.get()].tkraise()

  def popupmsg(self, msg=""):
      popup = tk.Toplevel(self.master)
      popup.wm_title("Error!")
      label = tk.Label(popup, text=msg, font=LARGE_FONT)
      label.pack(side="top", fill="x", pady=10)
      b1 = tk.Button(popup, text="Okay", command=popup.destroy)
      b1.pack()
  
  def save_dialog(self):
    f = filedialog.asksaveasfile(mode='w+', defaultextension=".csv")
    if f is None:
      return
    self.saveAsCsv(f)
    f.close()

  def pidThreadFunction(self):
    while self.running:
      start = time.time()
      self.adcValue = self.adc.getVoltage(0)
      self.windSpeed = self.adcValue * 5
      tmp = self.pid.update(self.windSpeed, start)

      if self.motorEnabled.get() == 0:
        self.pid.clear()
        self.pwmValue = 0
      elif tmp > 100:
        self.pwmValue = 100
      elif tmp < 0:
        self.pwmValue = 0
      else:
        self.pwmValue = tmp

      self.motorController.setDutyCycle(self.pwmValue)

      elapsed = time.time() - start
      time.sleep(max(0, self.pidDelay / 1000 - elapsed))

  def interval(self):
    self.after(self.intervalDelay, self.interval)
    start = time.time()

    setValue = self.frames['Page_1'].speedSlider.get()
    self.pid.setInput(setValue)

    i2cValues = self.pressureSensors.getValues()
    btValues = self.forceSensors.getForces()

    self.addRow(
      [self.windSpeed, setValue, self.pwmValue] + 
      i2cValues +
      [self.adcValue] +
      list(np.sum(btValues, axis = 0, initial=0)) +
      list(btValues.flatten())
    )
    print("sensors: {:8.3f} ms".format((time.time() - start)*1000))

    start = time.time()
    for frame in self.frames:
      self.frames[frame].update(frame == self.frameVar.get())

    print("draw:    {:8.3f} ms".format((time.time() - start)*1000))
    
  def stop(self):
    self.motorEnabled.set(0)
    self.running = False
    self.forceSensors.stop()
    self.pidThread.join()
    self.adc.close()
    self.motorController.stop()
    self.quit()