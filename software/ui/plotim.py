# # P L O T . I M # #
# https://github.com/tbartos14/plotim
# version 0.5.5, 5/22/2018

# readme needs update for residual plots


import tkinter as tk
import math
import numpy as np


class linear_plot(object):
    def __init__(self, bordernorth=50, bordersouth=50, bordereast=30, borderwest=50,
                 title="Linear Plot", \
                 draw_lines=True, draw_points=False, ytitle="y", xtitle="x", line_colors=["#0000bb"],
                 image=None):
        self.bordernorth = bordernorth
        self.bordersouth = bordersouth
        self.bordereast = bordereast
        self.borderwest = borderwest
        self.yaxistitle = ytitle
        self.xaxistitle = xtitle
        self.yaxis = [0, 10]
        self.xaxis = [0, 10]
        self.title = title
        self.draw_lines = draw_lines
        self.draw_points = draw_points
        self.linecolors = line_colors
        self.image = image

    def create_canvas(self, master):
        self.master = master

        self.canvas = tk.Canvas(self.master)
        self.canvas.bind("<Configure>", self.on_resize)
        self.windowx = self.canvas.winfo_reqwidth()
        self.windowy = self.canvas.winfo_reqheight()

        self.on_resize()
        return self.canvas

    def set_scale(self, xaxis, yaxis):
        self.yaxis = yaxis
        self.xaxis = xaxis

    def on_resize(self,event = None):

        if event:
          self.windowx = event.width - 4
          self.windowy = event.height - 4

        self.canvas.config(width=self.windowx, height=self.windowy)

        self.canvas.delete("all")

        self.graphx = self.windowx - self.bordereast - self.borderwest
        self.graphy = self.windowy - self.bordernorth - self.bordersouth
       
        self.canvas.create_text(self.borderwest + self.graphx / 2, self.bordernorth / 2, text=self.title, font=("Arial","26"))
        self.canvas.create_text(self.borderwest / 3, self.bordernorth + self.graphy / 2, text=self.yaxistitle, angle=90)
        self.canvas.create_text(self.borderwest + self.graphx / 2, self.windowy - self.bordersouth / 3, text=self.xaxistitle)

        self.canvas.create_rectangle(self.bordernorth, self.borderwest, (self.windowx - self.bordereast),
                                     (self.windowy - self.bordersouth), fill="white", outline="white")

        # finding limits for axis

        self.yrange = abs(self.yaxis[1] - self.yaxis[0]) - 1
        self.xrange = abs(self.xaxis[1] - self.xaxis[0]) - 1

        # choosing what kind of scale to use

        self.yrangefactor = -round(math.log10(self.yrange) - 1)
        self.xrangefactor = -round(math.log10(self.xrange) - 1)

        # determining how many lines need to be placed
        # minimums/maximums for ease of reading
        self.yrangemin = ((int((self.yaxis[0]) * (10 ** (self.yrangefactor)))) / (10 ** (self.yrangefactor)))
        self.xrangemin = ((int((self.xaxis[0]) * (10 ** (self.xrangefactor)))) / (10 ** (self.xrangefactor)))
        self.yrangemax = ((int((self.yaxis[0]) * (10 ** (self.yrangefactor)))) / (10 ** (self.yrangefactor)) + (
                (int(self.yrange * (10 ** self.yrangefactor)) + 1) * (10 ** (-1 * self.yrangefactor))))
        self.xrangemax = ((int((self.xaxis[0]) * (10 ** (self.xrangefactor)))) / (10 ** (self.xrangefactor)) + (
                (int(self.xrange * (10 ** self.xrangefactor)) + 1) * (10 ** (-1 * self.xrangefactor))))

        # determining increments
        # finding if scales are appropriate
        self.additionalscaley = 0
        self.additionalscalex = 0

        # seeing if data needs more space (y)
        while True:
            if self.yaxis[1] > self.yrangemax:
                self.additionalscaley = self.additionalscaley + 1
                self.yrangemax = (
                        (int((self.yaxis[0]) * (10 ** (self.yrangefactor)))) / (10 ** (self.yrangefactor)) + (
                        (int(self.yrange * (10 ** self.yrangefactor)) + 1 + self.additionalscaley) * (
                        10 ** (-1 * self.yrangefactor))))
            else:
                break

        # (x)
        while True:
            if self.xaxis[1] > self.xrangemax:
                self.additionalscalex = self.additionalscalex + 1
                self.xrangemax = (
                        (int((self.xaxis[0]) * (10 ** (self.xrangefactor)))) / (10 ** (self.xrangefactor)) + (
                        (int(self.xrange * (10 ** self.xrangefactor)) + 1 + self.additionalscalex) * (
                        10 ** (-1 * self.xrangefactor))))
            else:
                break
        self.yincrement = int(self.yrange * (10 ** self.yrangefactor)) + self.additionalscaley + 1
        self.xincrement = int(self.xrange * (10 ** self.xrangefactor)) + self.additionalscalex + 1

        # now we determine y
        for increment in range(0, self.yincrement + 1):
            self.canvas.create_line(self.borderwest + 1,
                                    (self.windowy - self.bordersouth) - (increment / self.yincrement) * (
                                            self.windowy - self.bordernorth - self.bordersouth), \
                                    self.borderwest + self.graphx,
                                    (self.windowy - self.bordersouth) - (increment / self.yincrement) * (
                                            self.windowy - self.bordernorth - self.bordersouth), fill="#bbbbbb",
                                    dash=(2, 2), width=2 if increment % 5 == 0 else 1)
            if increment % 5 == 0:
              self.canvas.create_text(self.borderwest - 12,
                                    (self.windowy - self.bordersouth) - (increment / self.yincrement) * (
                                            self.windowy - self.bordernorth - self.bordersouth), \
                                    text="{0:4.4}".format((int((self.yaxis[0]) * (10 ** (self.yrangefactor)))) / (
                                            10 ** (self.yrangefactor)) + (
                                                                  (increment) * (10 ** (-1 * self.yrangefactor)))))

        # determining x
        for increment in range(0, self.xincrement + 1):
            self.canvas.create_line(
                self.bordersouth + (increment / self.xincrement) * (self.windowx - self.bordereast - self.borderwest),
                (self.windowy - self.bordersouth) - 1, \
                self.bordersouth + (increment / self.xincrement) * (self.windowx - self.bordereast - self.borderwest),
                (self.windowy - self.bordersouth - self.graphy), fill="#bbbbbb", dash=(2, 2), width=2 if increment % 5 == 0 else 1)
            if increment % 5 == 0:
              self.canvas.create_text(
                self.borderwest + (increment / self.xincrement) * (self.windowx - self.bordereast - self.borderwest),
                (self.windowy - self.bordersouth) + 12, \
                text="{0:4.4}".format((int((self.xaxis[0]) * (10 ** (self.xrangefactor)))) / (10 ** (self.xrangefactor)) + (
                        (increment) * (10 ** (-1 * self.xrangefactor)))))

        self.canvas.create_line(self.bordernorth, self.borderwest, self.bordernorth, (self.windowy - self.bordersouth))
        self.canvas.create_line(self.borderwest, (self.windowy - self.bordersouth), (self.windowx - self.bordereast),
                                (self.windowy - self.bordersouth))
        return self.canvas

    def point_to_coords(self, x, y, offsetX=0, offsetY=0):
      return ((x - self.xrangemin) * (self.windowx - self.bordereast - self.borderwest) / (self.xrangemax - self.xrangemin) + self.borderwest + offsetX, 
              (self.windowy - self.bordersouth) - (y - self.yrangemin) * (self.windowy - self.bordernorth - self.bordersouth) / (self.yrangemax - self.yrangemin) + offsetY)

    def point_to_coords_np(self, coords, offsetX=0, offsetY=0):
      coords[:,0] = (coords[:,0] - self.xrangemin) * (self.windowx - self.bordereast - self.borderwest) / (self.xrangemax - self.xrangemin) + self.borderwest + offsetX
      coords[:,1] = (self.windowy - self.bordersouth) - (coords[:,1] - self.yrangemin) * (self.windowy - self.bordernorth - self.bordersouth) / (self.yrangemax - self.yrangemin) + offsetY

    ovals = []
    images = []
    def plot_data(self, xs, ys):
        #self.canvas.delete("graph")
        # adding lines
        if self.draw_lines == True:
          self.canvas.delete("line")
          for plot in range(len(xs)):
            xpoints = xs[plot]
            ypoints = ys[plot]
            linecolor = self.linecolors[plot]
            if isinstance(xpoints, (np.ndarray)) and isinstance(ypoints, (np.ndarray)):
              coords = np.stack((xpoints, ypoints), axis=1)
              coords = coords[~np.isnan(coords[:,1])]
              self.point_to_coords_np(coords)
              coords = coords.flatten().tolist()
            else:
              coords = []
              for point in range(0, len(xpoints)):
                if not math.isnan(ypoints[point]):
                  coord = self.point_to_coords(xpoints[point], ypoints[point])
                  coords.append(coord[0])
                  coords.append(coord[1])

            if len(coords) > 2:
              self.canvas.create_line(
                  coords,
                  fill=linecolor, tags="line", width=3)


        # adding points!
        if self.draw_points == True:
          while len(self.ovals) < len(xs):
            self.ovals.append([None] * len(xs[0]))
          for plot in range(len(xs)):
            xpoints = xs[plot]
            ypoints = ys[plot]
            for point in range(0, len(xpoints)):
                if math.isnan(ypoints[point]):
                  self.canvas.delete(self.ovals[plot][point])
                  self.ovals[plot][point] = None
                elif self.ovals[plot][point] != None:
                  self.canvas.coords(
                    self.ovals[plot][point],
                    *self.point_to_coords(xpoints[point], ypoints[point], 3, 3),
                    *self.point_to_coords(xpoints[point], ypoints[point], -3, -3),
                  )
                else:
                  self.ovals[plot][point] = self.canvas.create_oval(
                    *self.point_to_coords(xpoints[point], ypoints[point], 3, 3),
                    *self.point_to_coords(xpoints[point], ypoints[point], -3, -3),
                    fill="white", tags="oval")

        # use an image?
        if self.image != None:
          while len(self.images) < len(xs):
            self.images.append([None] * len(xs[0]))
          for plot in range(len(xs)):
            xpoints = xs[plot]
            ypoints = ys[plot]
            pointimage = tk.PhotoImage(file=self.image)
            for point in range(0, len(xpoints)):
                if math.isnan(ypoints[point]):
                  self.canvas.delete(self.images[plot][point])
                  self.images[plot][point] = None
                elif self.images[plot][point] != None:
                  self.canvas.coords(
                    self.images[plot][point],
                    *self.point_to_coords(xpoints[point], ypoints[point])
                  )
                else:
                  self.images[plot][point] = self.canvas.create_image(
                    *self.point_to_coords(xpoints[point], ypoints[point]),
                    image=pointimage, tags="image")

        return self.canvas



if __name__ == "__main__":
    # Datetime,RecNbr,WS_mph_Avg,PAR_Den_Avg,WS_mph_S_WVT,WindDir_SD1_WVT,AirTF_Avg,Rain_in_Tot,RH,WindDir_D1_WVT
    #!/usr/bin/env python3
    import urllib.request
    import time

    xpoints = []
    ypoints = []
    time = 0

    newlines = range(0, 100)

    for line in newlines:
        xpoints.append(time)
        time = time + (1 / 60)
        ypoints.append(line)

    plot1 = linear_plot(line_of_best_fit=True, \
                        ytitle="Temperature F\u00B0", \
                        xtitle="Time (hours)", \
                        title="Temperature in Durham NH Today", \
                        line_color="#2222ff", \
                        windowx=1000, \
                        windowy=700, )
    plot1.set_data(xpoints, ypoints)
    plot1.plot_data()
