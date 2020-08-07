import numpy as np

from .globals import *
from .plotim import linear_plot
       
class Plot(linear_plot):
  def __init__(self, xaxis, yaxis, **kwargs):

    linear_plot.__init__(self, **kwargs)
    self.set_scale(xaxis, yaxis)

  def setTimeScale(self, plotLen, delay):
    newXaxis = (0, plotLen * delay / 1000)
    if newXaxis != self.xaxis:
      self.xaxis = newXaxis
      self.on_resize()