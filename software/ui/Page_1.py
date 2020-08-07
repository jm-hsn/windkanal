import tkinter as tk
import tk_tools
import numpy as np
from datetime import datetime
from .Plot import Plot
from .globals import *

class Page_1(tk.Frame):
  plotLen = 100
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    # graph
    self.serialPlot = Plot(xaxis=(0, self.plotLen * .3), yaxis=(0, 25),
                      ytitle="Windgeschwindigkeit m/s",
                      xtitle="vergangene Zeit in s",
                      title="Geschwindigkeitsverlauf",
                      line_colors=GRAPH_COLORS)

    canvas = self.serialPlot.create_canvas(self)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # legend
    container = tk.Frame(self, relief="solid")
    container.pack(side="bottom", fill="both", padx=20, pady=20)
    
    tk.Label(container, text="Ist-Geschwindigkeit").grid(row=0, column=1)
    tk.Frame(container, height = 3,width = 50,bg = GRAPH_COLORS[0]).grid(row=0, column=0)
    tk.Label(container, text="Soll-Geschwindigkeit").grid(row=1, column=1)
    tk.Frame(container, height = 3,width = 50,bg = GRAPH_COLORS[1]).grid(row=1, column=0)
    tk.Label(container, text="PWM-Wert, skaliert auf 0-25").grid(row=2, column=1)
    tk.Frame(container, height = 3,width = 50,bg = GRAPH_COLORS[2]).grid(row=2, column=0)

    # right menu
    rightFrame = tk.LabelFrame(self, text="Bedienelemente")
    rightFrame.pack(side="left", fill="both", padx=5, pady=5)

    self.droLabel = tk.Label(rightFrame,font=("Arial","30"),fg="red")
    self.droLabel.pack(side="top", fill="both")

    # controls
    self.speedSlider = tk.Scale(rightFrame, from_=0, to=22, resolution=0.1, orient=tk.HORIZONTAL, width=50)
    self.speedSlider.pack(side="top", fill="both", padx=5, pady=5)
    label2 = tk.Label(rightFrame, text="Ventilator Soll-Wert in m/s")
    label2.pack()


  def update(self, visible):

    if visible:
      self.serialPlot.setTimeScale(self.plotLen, self.controller.intervalDelay)
      timestamps = (np.datetime64(datetime.now()) - self.controller.getLastValues(self.plotLen, "datetime")) / np.timedelta64(1,'s')
      self.serialPlot.plot_data(
        xs=[timestamps, timestamps, timestamps],
        ys=[
          self.controller.getLastValues(self.plotLen, "windspeed"), 
          self.controller.getLastValues(self.plotLen, "set_value"),
          self.controller.getLastValues(self.plotLen, "motor_pwm") / 4
        ]
      )
      self.droLabel.config(text="{:5.3f} V - {:5.2} m/s".format(self.controller.getLastValue("adc_0"), self.controller.getLastValue("windspeed")))