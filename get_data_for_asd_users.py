import pandas as pd
import numpy as np
import re
import os
from itertools import chain

from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier

## Util functions for natural sorting
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def main():
  asddf = loadData('asd-alldays.txt', ',')

  # screen time counts
  screentimedf = loadData('daily-screen-time.txt', ',')
  screen_time_counts = screentimedf.groupby('device_id')[['day', 'minutes']]\
    .apply(lambda x: x.set_index('day').to_dict(orient='index'))\
    .to_dict()

  # app time counts
  apptimedf = loadData('daily-app-time.txt', ',')
  app_time_counts = apptimedf.groupby('device_id')[['day', 'minutes']] \
    .apply(lambda x: x.set_index('day').to_dict(orient='index')) \
    .to_dict()

  # voice time counts
  audiotimedf = loadData('daily-audio-time.txt', ',')
  audio_time_counts = audiotimedf.groupby('device_id')[['day', 'minutes']] \
    .apply(lambda x: x.set_index('day').to_dict(orient='index')) \
    .to_dict()

  # google activity counts
  activity_counts = {}
  for device in asddf['device']:
    activity_counts[device] = {}

  active_labels = ['on_foot', 'walking', 'running', 'on_bicycle']
  day_labels = []
  for filename in os.listdir('google-data'):
    file_path = os.path.join('google-data', filename)
    df = loadData(file_path, '\t')

    day_label = re.split('\.|-', filename)[1]
    day_labels.append(day_label)

    for device, devicedf in df.groupby(['device_id']):
      if device in activity_counts:
        activedevicedf = devicedf[devicedf['activity_name'].isin(active_labels)]
        activecount = len(activedevicedf.index)
        activity_counts[device][day_label] = activecount

  day_labels.sort(key=natural_keys)

  # remove devices where data is less than 5 days
  print 'before: ', len(activity_counts)
  for device in activity_counts.keys():
    if device in screen_time_counts and device in app_time_counts:
      if len(activity_counts[device]) < 10 or len(app_time_counts[device]) < 5 or len(screen_time_counts[device]) < 5:
        del activity_counts[device]
      else:
        # FIXME
        if device not in audio_time_counts:
          del activity_counts[device]
    else:
      del activity_counts[device]
  print 'after: ', len(activity_counts)

  # calculate start day and end day from all data
  allcounts = list(chain(*app_time_counts.values()))
  start_day = min(allcounts)
  end_day = max(allcounts)

  num_devices = len(activity_counts)
  start_day_index = day_labels.index(start_day)
  end_day_index = day_labels.index(end_day)
  num_days = end_day_index - start_day_index + 1


  for days in range(2, num_days+1):
    # create vector from start day to end day
    # training_data = np.empty((0, (num_days*3)+1))  # *2 for activity and screen, +1 for label
    training_data = np.empty((0, (1 * 4) + 2 + 1))  # *2 for activity and screen, +1 for label

    for device in activity_counts.keys():
      ## device check
      # if device not in screen_time_counts or device not in app_time_counts:
      #   continue

      active_daily_count = []

      # separate days
      # for i in range(start_day_index, end_day_index+1):
      #   day = day_labels[i]
      #
      #   # add activity count
      #   daycount = 0
      #   if day in activity_counts[device]:
      #     daycount = activity_counts[device][day]
      #   active_daily_count.append(daycount)
      #
      #   # add screen time count
      #   screentime = 0
      #   if day in screen_time_counts[device]:
      #     screentime = screen_time_counts[device][day]['minutes']
      #   active_daily_count.append(screentime)
      #
      #   # add app time count
      #   apptime = 0
      #   if day in app_time_counts[device]:
      #     apptime = app_time_counts[device][day]['minutes']
      #   active_daily_count.append(apptime)

      # average
      daycount = []
      screentime = []
      audiotime = []
      apptime = []
      for i in range(start_day_index, end_day_index+1):
        day = day_labels[i]

        if day in activity_counts[device]:
          daycount.append(activity_counts[device][day])

        if day in screen_time_counts[device]:
          screentime.append(screen_time_counts[device][day]['minutes'])

        if day in audio_time_counts[device]:
          audiotime.append(audio_time_counts[device][day]['minutes'])

        if day in app_time_counts[device]:
          apptime.append(app_time_counts[device][day]['minutes'])

      daycount = np.array(daycount)
      # print 'len -', len(daycount)
      daycount = daycount[:days]
      active_daily_count.append(daycount.mean())
      active_daily_count.append(daycount.std())
      active_daily_count.append(np.diff(daycount).mean())
      active_daily_count.append(np.diff(daycount).std())

      # screentime = np.array(screentime)
      # screentime = screentime[:days]
      # active_daily_count.append(screentime.mean())
      # active_daily_count.append(screentime.std())
      # active_daily_count.append(np.diff(screentime).mean())
      # active_daily_count.append(np.diff(screentime).std())

      audiotime = np.array(audiotime)
      audiotime = audiotime[:days]
      active_daily_count.append(audiotime.mean())
      active_daily_count.append(audiotime.std())
      # active_daily_count.append(np.diff(audiotime).mean())
      # active_daily_count.append(np.diff(audiotime).std())

      # apptime = np.array(apptime)
      # # print 'len -', len(apptime)
      # apptime = apptime[:days]
      # active_daily_count.append(apptime.mean())
      # active_daily_count.append(apptime.std())
      # active_daily_count.append(np.diff(apptime).mean())
      # active_daily_count.append(np.diff(apptime).std())


      # append label
      active_daily_count.append(asddf.loc[asddf['device'] == device, 'label'].iloc[0])

      training_data = np.append(training_data, np.array([active_daily_count]), axis=0)

    ## CLASSIFICATION (KNN)
    # for i in range(1, 15):
    #   neigh = KNeighborsClassifier(n_neighbors=i)
    #   scores = cross_val_score(neigh, training_data[:,:-1], training_data[:,-1], cv=5)
    #   print 'knn:', 'n-'+str(i), scores, np.mean(scores)

    ## CLASSIFICATION (SVM)

    # clf = svm.SVC(gamma=0.01, C=11)
    # scores = cross_val_score(clf, training_data[:, :-1], training_data[:, -1], cv=5)
    # mean_score = np.mean(scores)
    # print 'result svm:', scores, mean_score, 'days:', days

    best_mean_score = 0
    best_scores = None
    best_c = 0
    best_gamma = 0
    for i in range(0, 6):


      gamma = 0.1/(10**i)

      for j in range(1, 1000, 10):
        c = j
        # clf = svm.SVC(gamma=0.001, C=100000.)
        clf = svm.SVC(gamma=gamma, C=c)
        scores = cross_val_score(clf, training_data[:,:-1], training_data[:,-1], cv=5)
        mean_score = np.mean(scores)
        if mean_score > best_mean_score:
          best_scores = scores
          best_mean_score = mean_score
          best_c = c
          best_gamma = gamma
          # print 'svm:', best_scores, best_mean_score, best_c, best_gamma

    # print 'best svm:', best_scores, best_mean_score, best_c, best_gamma, 'days:', days
    print best_mean_score, days

def loadData(filepath, sep):
  return pd.read_csv(filepath, sep=sep)

if __name__ == '__main__':
  main()
