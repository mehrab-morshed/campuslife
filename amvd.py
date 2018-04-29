## Acceleration moving variance detector ##

import numpy as np
import pandas as pd
from scipy import stats

def amvd(df):
  # group by minutes and compute minute means
  minute_groups = df.groupby([df.label, df.timestamp.dt.hour, df.timestamp.dt.minute])
  minute_groups_means = minute_groups.transform('mean')

  # subtract means from x,y,z
  df_minus_mean = df[['x', 'y', 'z']].sub(minute_groups_means[['x', 'y', 'z']])
  df_minus_mean['timestamp'] = df['timestamp']
  df_minus_mean['minute'] = df.timestamp.dt.hour*60 + df.timestamp.dt.minute
  df_minus_mean['device_id'] = df['device_id']
  df_minus_mean['label'] = df['label']
  # compute magnitude
  df_minus_mean['magnitude'] = ((df['x'] ** 2) + (df['y'] ** 2) + (df['z'] ** 2)).apply(np.sqrt)

  # group by label and minute and fill missing minute values
  minute_groups = df_minus_mean.groupby([df_minus_mean.device_id, df_minus_mean.minute])
  xrange = np.arange(60 * 24)
  # key is (label, minute) and value is mean, count
  energy_df = minute_groups['magnitude'].agg(['mean', 'count']).reset_index()
  iterables = [energy_df['device_id'].unique(), xrange]
  energy_df = energy_df.set_index(['device_id', 'minute'])
  energy_df = energy_df.reindex(index=pd.MultiIndex.from_product(iterables, names=['device_id', 'minute']), fill_value=0).reset_index()
  # compute delta
  energy_df = energy_df.set_index(['device_id', 'minute'])
  energy_df['delta'] = energy_df['mean'] - energy_df['mean'].shift(-1)
  # set delta to 0 where mean is 0 FIXME see if this can be improved - compiler throws a userful warning
  energy_df['delta'][energy_df['mean'] == 0] = 0
  energy_df = energy_df.reset_index()

  return energy_df

def googleactivity(df):
  df = df[df['confidence'] > 50] # select entries where confidence is greater than 50
  df['minute'] = df.timestamp.dt.hour*60 + df.timestamp.dt.minute
  minute_groups = df.groupby([df.device_id, df.minute])
  xrange = np.arange(60 * 24)

  googleactivity_df = minute_groups['activity_name'].agg(lambda x: stats.mode(x)[0]).reset_index()
  iterables = [googleactivity_df['device_id'].unique(), xrange]
  googleactivity_df = googleactivity_df.set_index(['device_id', 'minute'])
  googleactivity_df = googleactivity_df.reindex(index=pd.MultiIndex.from_product(iterables, names=['device_id', 'minute']), fill_value=0).reset_index()

  return googleactivity_df

### Computes time periods between status 3 and 0 (unlocked to screen off)
def screenactivity(df):
  # status =  0=off, 1=on, 2=locked, 3=unlocked
  # Notes - Ideally every incident of unlock should be preceded by screen on and every incident of lock
  # should be preceded by screen off

  # look for time periods between 3 and 0
  device_screen_count = []
  for device, devicedf in df.groupby(['device_id']):
    start_time = None
    screentime = 0
    for index, row in devicedf.iterrows():
      if start_time is None and row.status == 3:
        start_time = row.timestamp
      if start_time is not None and row.status == 0:
        screentime += pd.Timedelta(row.timestamp - start_time).seconds / 60.0
        start_time = None

    device_screen_count.append((device, screentime))

  return device_screen_count

def audioactivity(df):
  device_screen_count = []
  for device, devicedf in df.groupby(['device_id']):
    start_time = None
    screentime = 0
    for index, row in devicedf.iterrows():
      if start_time is None and row.inference == 2:
        start_time = row.timestamp
      if start_time is not None and row.inference != 2:
        screentime += pd.Timedelta(row.timestamp - start_time).seconds
        start_time = None

    device_screen_count.append((device, screentime/60.0))

  return device_screen_count

def appactivity(df):
  # look for time periods between facebook/twitter and next app
  app_screen_count = []
  for device, devicedf in df.groupby(['device_id']):
    start_time = None
    screentime = 0

    social_apps = ['groupme', 'facebook', 'twitter', 'snapchat', 'reddit', 'quora', 'whatsapp']

    for index, row in devicedf.iterrows():
      if start_time is None and any(app in row.package for app in social_apps):
        start_time = row.timestamp
      # ('facebook' not in row.package and 'twitter' not in row.package and 'snapchat' not in row.package)
      if start_time is not None and all(app not in row.package for app in social_apps):
        screentime += pd.Timedelta(row.timestamp - start_time).seconds
        start_time = None

    app_screen_count.append((device, screentime))

  return app_screen_count

def quedget_responses(df):
  df = df[df['question_set'].isin(['Emotion Regulation', 'State Self Esteem', 'Dartmouth'])] # select entries where question set belongs to one of the categories
  df['minute'] = df.timestamp.dt.hour*60 + df.timestamp.dt.minute
  minute_groups = df.groupby([df.device_id, df.minute])
  xrange = np.arange(60 * 24)

  quedget_df = minute_groups[['question_id','question_content','question_set','responsecode_0']].agg(lambda x: stats.mode(x)[0]).reset_index()
  iterables = [quedget_df['device_id'].unique(), xrange]
  quedget_df = quedget_df.set_index(['device_id', 'minute'])
  quedget_df = quedget_df.reindex(index=pd.MultiIndex.from_product(iterables, names=['device_id', 'minute']), fill_value=0).reset_index()

  return quedget_df

