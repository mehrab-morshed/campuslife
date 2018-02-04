import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
  df = loadData('userepochs.csv')
  plotData(df)

def loadData(filepath):
  return pd.read_csv(filepath, sep='\t')

def plotData(df):
  labels = []
  for i in range(0, len(df.columns)):
    if i % 2 == 0: # FIXME dirty hack to ignore count columns
      labels.append(df.columns[i])

  df.plot(y=labels, x=np.arange(df.shape[0])+1, style='.-')
  plt.markersize = 0.2
  plt.show()

if __name__ == '__main__':
  main()
