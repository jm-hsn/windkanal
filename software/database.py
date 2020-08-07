import numpy as np
from datetime import datetime
import csv

class Table:
  def __init__(self, columns, nRows = 2**16):
    self.columnNames = ['datetime'] + columns
    self.nCols = len(columns)
    self.nRows = nRows
    self.rows = self.ys = np.ndarray(shape=(self.nRows, self.nCols), dtype=float)
    self.rows.fill(float('NaN'))
    self.timestamps = np.ndarray(shape=(self.nRows), dtype='datetime64[ns]')
    self.timestamps.fill(datetime.now())
    self.rowIndex = 0

  def reset(self):
    self.rows.fill(float('NaN'))
    self.rowIndex = 0

  def rowIdToOffset(self, id):
    return self.nRows - (id % self.nRows) - 1

  def addRow(self, values):
    offset = self.rowIdToOffset(self.rowIndex)
    self.rows[offset] = values
    self.timestamps[offset] = datetime.now()
    self.rowIndex += 1

  def getLastRows(self, n):
    nRead = min(n, self.nRows)
    readStart = self.rowIdToOffset(self.rowIndex - 1)
    readEnd = self.rowIdToOffset(self.rowIndex - nRead - 1)
    if readEnd > readStart:
      return self.rows[readStart:readEnd]
    else:
      return np.concatenate((self.rows[readStart:], self.rows[:readEnd]), axis=0)

  def getLastTimestamps(self, n):
    nRead = min(n, self.nRows)
    readStart = self.rowIdToOffset(self.rowIndex - 1)
    readEnd = self.rowIdToOffset(self.rowIndex - nRead - 1)
    if readEnd > readStart:
      return self.timestamps[readStart:readEnd]
    else:
      return np.concatenate((self.timestamps[readStart:], self.timestamps[:readEnd]), axis=0)


  def getLastValues(self, n, column):
    col = self.columnNames.index(column)
    if col > 0:
      return self.getLastRows(n)[:,col-1]
    else:
      return self.getLastTimestamps(n)

  def getLastValue(self, column):
    return self.getLastValues(1, column)[0]

  def saveAsCsv(self, fd):
    csvWriter = csv.writer(fd,delimiter=',')
    csvWriter.writerow(self.columnNames)
    timestamps = self.getLastTimestamps(self.rowIndex)
    for ts, vals in zip(self.getLastTimestamps(self.rowIndex), self.getLastRows(self.rowIndex)):
      csvWriter.writerow([ts] + list(vals))

if __name__ == "__main__":
  t = Table(["col1", "col2"])
  for i in range(99):
    t.addRow([i, 2])
  print(t.getLastRows(100))
  t.addRow([3, 4])
  print(t.getLastRows(1))
  t.saveAsCsv('test.csv')