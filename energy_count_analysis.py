import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def main():
  df = loadData('gregory.txt')
  daily_count(df)

def daily_count(df):
  bins = np.arange(9.5, 12 + 0.1, 0.1)
  df['mean'].hist(cumulative=True, normed=1, by=df['device_id'], bins=bins)

  mapping = {'0': 0, 'unknown': 0, 'still': 0, 'running': 1, 'walking': 1, 'on_foot': 1, 'on_bicycle': 2, 'in_vehicle': 3, 'tilting': 4}
  df['activity_name'] = df['activity_name'].apply(lambda s: mapping.get(s) if s in mapping else 0)
  axarr = df['activity_name'].hist(cumulative=True, normed=1, by=df['device_id'], bins=range(0, 6, 1))
  for ax in axarr.flatten():
    ax.xaxis.set_major_formatter(ticker.NullFormatter())

    # Customize minor tick labels
    ax.xaxis.set_minor_locator(ticker.FixedLocator([0.5, 1.5, 2.5, 3.5, 4.5]))
    ax.xaxis.set_minor_formatter(ticker.FixedFormatter(['1', '2', '3', '4', '5']))

    ax.set_xticklabels(['still', 'moving', 'cycling', 'driving', 'tilting'], ha='center', minor=True, rotation = 0)

  plt.show()

def loadData(filepath):
  return pd.read_csv(filepath, sep='\t')

if __name__ == '__main__':
  main()

