import tkinter as tk
import tk_tools
import numpy as np
from datetime import datetime
from .Plot import Plot
from .globals import *

from .globals import *
class Page_4(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    frame = tk.LabelFrame(self, text="Einstellungen")
    frame.pack(side=tk.LEFT, fill=tk.BOTH)

    tk.Label(frame, text="Aktualisierungsinterval in ms").pack(padx=5, pady=5)
    self.intervalSlider = tk.Scale(frame, from_=50, to=1000, resolution=10, orient=tk.HORIZONTAL)
    self.intervalSlider.set(300)
    self.intervalSlider.pack(side="top", fill="both", padx=5, pady=5)

    tk.Label(frame, text="PID-Interval in ms").pack(padx=5, pady=5)
    self.pidSlider = tk.Scale(frame, from_=5, to=500, resolution=1, orient=tk.HORIZONTAL)
    self.pidSlider.set(100)
    self.pidSlider.pack(side="top", fill="both", padx=5, pady=5)

    gridFrame = tk.LabelFrame(self, text="System Check")
    gridFrame.pack(side=tk.LEFT, fill=tk.BOTH)

    tk.Label(gridFrame, padx=5, pady=5, text="{:32s}".format("Messwerte")).grid(row=0, column=0)
    self.rowCountLabel = tk.Label(gridFrame, padx=5, pady=5, text="")
    self.rowCountLabel.grid(row=0, column=1)

    self.sysLabels = []
    for i in range(1, len(self.controller.columnNames)):
      name = controller.columnNames[i]
      la = tk.Label(gridFrame, fg='red', padx=5, pady=5, text="{:32s}".format(name))
      la.grid(row=i, column=0)
      lb = tk.Label(gridFrame, fg='red', padx=5, pady=5, text="")
      lb.grid(row=i, column=1)
      self.sysLabels.append((la, lb))

  def update(self, visible):
    if visible:
      self.controller.intervalDelay = self.intervalSlider.get()
      self.controller.pidDelay = self.pidSlider.get()
      row = self.controller.getLastRows(1)[0]
      for i in range(len(row)):
        nameLabel, valueLabel = self.sysLabels[i]
        color = 'red' if np.isnan(row[i]) else 'black' if row[i] == 0 else 'green'
        nameLabel.config( fg = color)
        valueLabel.config(fg = color, text="{:5.4f}".format(row[i]))
      self.rowCountLabel.config(text="{:d} / {:d}".format(min(self.controller.rowIndex, self.controller.nRows), self.controller.nRows))