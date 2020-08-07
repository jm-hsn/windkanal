#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from appWindow import Main
from ui.globals import *

app = Main()
app.geometry("1280x720")
try:
  app.mainloop()
  print('program closed!')
except KeyboardInterrupt as e:
  app.stop()
  pass

sys.exit()