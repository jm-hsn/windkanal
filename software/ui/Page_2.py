import tkinter as tk
import tk_tools
import numpy as np
from datetime import datetime
from .Plot import Plot
from .globals import *

class Page_2(tk.Frame):
  plotLen = 100
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    
    # graphs
    self.forcePlot = Plot(xaxis=(-2, 2), yaxis=(-2, 2),
          ytitle="y-Kraft in mV",
          xtitle="x-Kraft in mV",
          title="XY-Graph",
          line_colors=GRAPH_COLORS)
    canvas = self.forcePlot.create_canvas(self)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # legend
    container = tk.Frame(self, relief="solid")
    container.pack(side="bottom", fill="both", padx=20, pady=20)
    
    tk.Label(container, text="Sensor 1").grid(row=0, column=1)
    tk.Frame(container, height = 3,width = 50,bg = GRAPH_COLORS[0]).grid(row=0, column=0)
    tk.Label(container, text="Sensor 2").grid(row=1, column=1)
    tk.Frame(container, height = 3,width = 50,bg = GRAPH_COLORS[1]).grid(row=1, column=0)
    tk.Label(container, text="Sensor 3").grid(row=2, column=1)
    tk.Frame(container, height = 3,width = 50,bg = GRAPH_COLORS[2]).grid(row=2, column=0)

    # right menu
    rightFrame = tk.LabelFrame(self, text="Kräfte")
    rightFrame.pack(side="left", fill="both", padx=5, pady=5)

    tareButton = tk.Button(rightFrame, text='Kräfte tarieren', command=self.controller.forceSensors.tare, justify=tk.LEFT, anchor="w")
    tareButton.pack(side="top", fill="both", padx=5, pady=5)

    gridFrame = tk.Frame(rightFrame, relief="solid")
    gridFrame.pack(side="top", fill="both", padx=20, pady=20)

    self.readOuts = {}
    for sensor in range(4):
      for axis in range(3):
        name = "force_{}_{}".format(chr(ord('X') + axis), 'sum' if sensor==0 else sensor)
        label = tk.Label(gridFrame, text=name)
        label.grid(row=sensor*2, column=axis)
        self.readOuts[name] = tk.StringVar()
        entry = tk.Entry(gridFrame, textvariable=self.readOuts[name], width=10)
        entry.grid(row=sensor*2+1, column=axis)


  def update(self, visible):
    if visible:
      self.forcePlot.plot_data(
        xs=[self.controller.getLastValues(self.plotLen, "force_X_{}".format(i+1)) for i in range(3)] +
            [np.sin(np.linspace(0, 6.282, self.plotLen))],
        ys=[self.controller.getLastValues(self.plotLen, "force_Y_{}".format(i+1)) for i in range(3)] + 
            [np.cos(np.linspace(0, 6.282, self.plotLen))]
      )
      for name in self.readOuts:
        val = self.controller.getLastValue(name)
        if np.isnan(val):
          self.readOuts[name].set("")
        else:
          self.readOuts[name].set("{:1.3f} mV".format(val))