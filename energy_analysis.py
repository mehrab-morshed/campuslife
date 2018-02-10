import datetime
import pandas as pd
import numpy as np

def main():
  #FIXME for loop
  for i in range(6, 16):
    df = loadData("./day"+str(i)+".csv")

    # old version
    # user_epochs = parseEpochs(df, 1)

    # convert dict to df and write to csv
    # df = pd.DataFrame(user_epochs)
    # df.to_csv('userepochs.csv', sep='\t', index=False)

    # v2
    energy_df = parseEpochsV2(df)
    # write to csv
    energy_df.to_csv("userepochs-day"+str(i)+".csv", sep='\t')


def parseEpochsV2(df):
  df['x'] = df['x'] ** 2
  df['y'] = df['y'] ** 2
  df['z'] = df['z'] ** 2
  df['xyz_square'] = ((df['x']**2) + (df['y']**2) + (df['z']**2)).apply(np.sqrt)
  minute_groups = df.groupby([df.label, df.timestamp.dt.hour, df.timestamp.dt.minute])
  # key is (label, hour, minute) and value is mean, count
  energy_df = minute_groups['xyz_square'].agg(['mean', 'count'])
  return energy_df

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
  return pd.read_csv(filepath, sep='\t', parse_dates=['timestamp'])

if __name__ == '__main__':
  main()
