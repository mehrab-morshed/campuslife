import datetime
import pandas as pd
import numpy as np

def main():
  df = loadData("./day1.csv")
  user_epochs = parseEpochs(df, 1)

  # convert dict to df and write to csv
  df = pd.DataFrame(user_epochs)
  df.to_csv('userepochs.csv', sep='\t', index=False)

def parseEpochs(df, minutes):
  # Create a dataframe with label and per minute energy value |l| *
  # (60/minutes)*24
  user_epochs = dict()

  prev_minute = None
  prev_label = None
  minute_vals = []
  for index, row in df.iterrows():
    if row['label'] not in user_epochs:
      user_epochs[row['label']] = [0 for i in range((60/minutes)*24)]
      user_epochs[row['label']+'count'] = [0 for i in range((60/minutes)*24)]

    row_date = datetime.datetime.fromtimestamp(row['timestamp']/1000.0)
    current_minute = row_date.hour*60 + row_date.minute
    current_label = row['label']

    if prev_minute == None:
      prev_minute = current_minute
      prev_label = current_label

    if current_minute - prev_minute >= minutes or current_label != prev_label:
      np_arr = np.asarray(minute_vals)
      num_samples = np_arr.shape[0]
      user_epochs[prev_label][prev_minute] = np.mean(np.sum((np_arr ** 2), axis=1), axis=0)
      user_epochs[prev_label+'count'][prev_minute] = num_samples

      minute_vals = []
      prev_minute = current_minute
      prev_label = current_label

    minute_vals.append((row['x'], row['y'], row['z']))

  if len(minute_vals) > 0:
    np_arr = np.asarray(minute_vals)
    num_samples = np_arr.shape[0]
    user_epochs[prev_label][prev_minute] = np.mean(np.sum((np_arr ** 2), axis=1), axis=0)
    user_epochs[prev_label+'count'][prev_minute] = num_samples

  return user_epochs

def loadData(filepath):
  return pd.read_csv(filepath, sep='\t')

if __name__ == '__main__':
  main()
