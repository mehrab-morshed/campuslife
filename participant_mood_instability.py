import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab

def main():

  # load file names and sort
  files = os.listdir('asd-days')
  files.sort(key=natural_keys)

  device_mi = {}

  for filename in files:
    file_path = os.path.join('asd-days', filename)
    df = loadData(file_path, ',')

    for index, row in df.iterrows():
      device = row['device']
      if device in device_mi.keys():
        device_mi[device].append(row['label'])
      else:
        device_mi[device] = []
        device_mi[device].append(row['label'])

  i = 1
  for device in device_mi.keys():
    plt.figure(i)
    i += 1

    x = [x for x in range(2, len(device_mi[device])+2)]
    plt.plot(x, device_mi[device], '-o', linewidth=1, label=device)

    plt.xlabel("Number of days")
    plt.ylabel("MI class")
    plt.xticks(np.arange(min(x), max(x) + 1, 1.0))
    pylab.legend(loc='upper left')


  plt.show()

  print device_mi

def atoi(text):
  return int(text) if text.isdigit() else text

def natural_keys(text):
  '''
  alist.sort(key=natural_keys) sorts in human order
  http://nedbatchelder.com/blog/200712/human_sorting.html
  (See Toothy's implementation in the comments)
  '''
  return [atoi(c) for c in re.split('(\d+)', text)]

def loadData(filepath, sep):
  return pd.read_csv(filepath, sep=sep)

if __name__ == '__main__':
  main()