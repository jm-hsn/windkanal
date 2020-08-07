import tkinter as tk
import tk_tools
import numpy as np
from datetime import datetime
from .Plot import Plot
from .globals import *

class Page_3(tk.Frame):
  plotLen = 100
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    # graph
    self.pressurePlot = Plot(xaxis=(0, self.plotLen * .3), yaxis=(-120, 120),
                      ytitle="Druck in Pa",
                      xtitle="vergangene Zeit in s",
                      title="Druckverlauf",
                      line_colors=GRAPH_COLORS)

    canvas = self.pressurePlot.create_canvas(self)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # legend
    container = tk.Frame(self, relief="solid")
    container.pack(side="bottom", fill="both", padx=20, pady=20)
    
    for i in range(8):
      tk.Label(container, text="Sensor {}".format(i)).grid(row=i, column=1)
      tk.Frame(container, height = 3,width = 50,bg = GRAPH_COLORS[i]).grid(row=i, column=0)

    # right menu
    rightFrame = tk.LabelFrame(self, text="Druck")
    rightFrame.pack(side="left", fill="both", padx=5, pady=5)

    gridFrame = tk.Frame(rightFrame, relief="solid")
    gridFrame.pack(side="top", fill="both", padx=20, pady=20)

    self.readOuts = {}
    for sensor in range(8):
      name = "pressure_{}".format(sensor)
      label = tk.Label(gridFrame, text=name)
      label.grid(row=sensor, column=0)
      self.readOuts[name] = tk.StringVar()
      entry = tk.Entry(gridFrame, textvariable=self.readOuts[name], width=10)
      entry.grid(row=sensor, column=1)

  def update(self, visible):
    if visible:
      self.pressurePlot.setTimeScale(self.plotLen, self.controller.intervalDelay)
      timestamps = (np.datetime64(datetime.now()) - self.controller.getLastValues(self.plotLen, "datetime")) / np.timedelta64(1,'s')
      self.pressurePlot.plot_data(
        xs=[timestamps] * 8,
        ys=[self.controller.getLastValues(self.plotLen, "pressure_{}".format(i)) for i in range(8)]
      )
      for name in self.readOuts:
        val = self.controller.getLastValue(name)
        if np.isnan(val):
          self.readOuts[name].set("")
        else:
          self.readOuts[name].set("{:1.3f} Pa".format(val))