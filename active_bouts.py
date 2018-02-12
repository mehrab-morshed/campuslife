import pandas as pd
import numpy as np
from thresholds_config import config

def main():
  for i in range(10, 11):
    df = loadData("userepochs-day"+str(i)+".csv")
    outfile = "activebouts-day"+str(i)+".csv"
    activeBouts(df, outfile)

def loadData(filepath):
  return pd.read_csv(filepath, sep='\t')

def activeBouts(df, outfile):

  with open(outfile, 'w') as f:
    for group in df.groupby([df.label]):
      active_minutes = (group[1]['mean']>config['magnitude_threshold']).values & \
      (group[1]['delta'].abs()>config['delta_threshold']).values

      active_minutes_df = group[1][active_minutes]

      for k, g in active_minutes_df.groupby(active_minutes_df['minute'] - np.arange(active_minutes_df.shape[0])):
        group_count = g['minute'].agg(['count'])[0]
        if group_count > 1:
          f.write(group[0] + "\t" + str(g['minute'].iloc[-1]) + "\t" + str(group_count) + "\n")

if __name__ == '__main__':
  main()
