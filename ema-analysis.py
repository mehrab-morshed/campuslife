import math
import datetime
import pandas as pd
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess

def main():
  #loadData("/home/schawla32/studydata/schawla32/quedget_responses.txt")
  loadDataWithValenceArousal("./quedget_with_valence_arousal.txt")

def findLambda(delvalence, delarousal, deltime, mediantime):
  arousaln = 1
  mindetstatarousal = float("inf")
  for n in range(1, 11):
    lamda = (1.0/n)

    asdarousal = delarousal/((deltime/mediantime)**lamda)
    # asdvalence = delvalence/((deltime/mediantime)**lamda)

    if len(asdarousal.index) > 0:
      expectedasdarousal = lowess(asdarousal, np.arange(0, len(asdarousal.index)))
      carousal = expectedasdarousal[:,1].mean()
      detstat = ((expectedasdarousal[:,1] - carousal)**2).sum()
      if(detstat < mindetstatarousal):
        mindetstatarousal = detstat
        arousaln = n

  lamda = 1.0/arousaln
  print 'lamda: ',lamda

  return lamda

def loadDataWithValenceArousal(filepath):
  df = pd.read_csv(filepath, sep=',', parse_dates=['timestamp'])

  min_ts = None
  max_ts = None

  # find min and max timestamp
  for id, devicedf in df.groupby(['device_id']):
    devicedf = devicedf.loc[devicedf['timestamp'].shift() != devicedf['timestamp']]

    if min_ts is None or devicedf.iloc[0]['timestamp'] < min_ts:
      min_ts = devicedf.iloc[0]['timestamp']
    if max_ts is None or devicedf.iloc[-1]['timestamp'] > max_ts:
      max_ts = devicedf.iloc[-1]['timestamp']

  # FIXME - start from day 15
  min_ts = min_ts.replace(day=15)
  num_days = (max_ts-min_ts).days

  print 'numdays:', num_days

  with open('asd.txt', 'w') as asd_file:
    miscores = []

    asd_file.write("device,madasdarousal,madasdvalence,sum\n")
    for id, devicedf in df.groupby(['device_id']):

      devicedf = devicedf.loc[devicedf['timestamp'].shift() != devicedf['timestamp']]

      numresponses = len(devicedf.index)
      # FIXME setting response threshold to 5
      if numresponses < 6:
        print 'ignoring deviceid: ', id , '\n'
        continue

      print 'deviceid: ', id, '#responses: ', numresponses
      delvalence = devicedf['valence'].diff().dropna()
      delarousal = devicedf['arousal'].diff().dropna()
      deltime = devicedf['timestamp'].diff().dropna()

      mediantime = deltime.median()

      lamda = findLambda(delvalence, delarousal, deltime, mediantime)

      asdarousal = delarousal / ((deltime / mediantime) ** lamda)
      asdvalence = delvalence / ((deltime / mediantime) ** lamda)

      if len(asdarousal.index) > 0:
        meanasdarousal = asdarousal.mean()
        madasdarousal = np.fabs(asdarousal-meanasdarousal).mean()
        print "madasdarousal: ", madasdarousal

        meanasdvalence = asdvalence.mean()
        madasdvalence = np.fabs(asdvalence-meanasdvalence).mean()
        print "madasdvalence: ", madasdvalence

        miscores.append((id, madasdarousal, madasdvalence, madasdarousal+madasdvalence))

        asd_file.write("{0},{1:.5f},{2:.5f},{3:.5f}\n".format
                       (id,
                        madasdarousal,
                        madasdvalence,
                        madasdarousal+madasdvalence))

  miscoresdf = pd.DataFrame(miscores, columns=('device', 'arousal', 'valence', 'sum'))
  medianscore = miscoresdf['sum'].median()
  miscoresdf['label'] = np.where(miscoresdf['sum'] <= medianscore, '0', '1')

  miscoresdf.to_csv('asd2.txt', index=False)


def loadData(filepath):
  column_names = ['uuid', 'device_id', 'question_id', 'question_content', 'question_set', 'responsecode_0', 'timestamp', 'date_answered']
  dateparse = lambda x: datetime.datetime.fromtimestamp(long(x)/1000.0)

  df = pd.read_csv(filepath, sep='\t', header=None, names=column_names, parse_dates=['timestamp'], date_parser=dateparse)
  # select only PAM responses
  df = df.loc[df.question_set == 'PAM']
  # drop rows where responsecode is None
  df = df.dropna(subset=['responsecode_0'])

  def add_valence_arousal(row):
    if 'afraid' in row['responsecode_0']:
      return -2, 2
    if 'angry' in row['responsecode_0']:
      return -1, 1
    if 'calm' in row['responsecode_0']:
      return 1, -1
    if 'delighted' in row['responsecode_0']:
      return 2, 2
    if 'excited' in row['responsecode_0']:
      return 1, 2
    if 'frustrated' in row['responsecode_0']:
      return -2, 1
    if 'glad' in row['responsecode_0']:
      return 2, 1
    if 'gloomy' in row['responsecode_0']:
      return -2, -2
    if 'happy' in row['responsecode_0']:
      return 1, 1
    if 'miserable' in row['responsecode_0']:
      return -2, -1
    if 'sad' in row['responsecode_0']:
      return -1, -1
    if 'satisfied' in row['responsecode_0']:
      return 2, -1
    if 'serene' in row['responsecode_0']:
      return 2, -2
    if 'sleepy' in row['responsecode_0']:
      return 1, -2
    if 'tense' in row['responsecode_0']:
      return -1, 2
    if 'tired' in row['responsecode_0']:
      return -1, -2

  df['valence'] = df.apply(lambda row: add_valence_arousal(row)[0] ,axis=1)
  df['arousal'] = df.apply(lambda row: add_valence_arousal(row)[1] ,axis=1)

  df.to_csv('quedget_with_valence_arousal.txt', index=False)

  print 'Number of responses:', len(df.index)


if __name__ == '__main__':
  main()
