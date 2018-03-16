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

def quedget_responses(df):
  df = df[df['question_set'].isin(['Emotion Regulation', 'State Self Esteem', 'Dartmouth'])] # select entries where question set belongs to one of the categories
  df['minute'] = df.timestamp.dt.hour*60 + df.timestamp.dt.minute
  minute_groups = df.groupby([df.device_id, df.minute])
  xrange = np.arange(60 * 24)

  quedget_df = minute_groups[['question_id','question_content','question_set','responsecode_0']].agg(lambda x: stats.mode(x)[0]).reset_index()
  iterables = [quedget_df['device_id'].unique(), xrange]
  quedget_df = quedget_df.set_index(['device_id', 'minute'])
  print quedget_df.index.is_unique
  quedget_df = quedget_df.reindex(index=pd.MultiIndex.from_product(iterables, names=['device_id', 'minute']), fill_value=0).reset_index()

  return quedget_df

