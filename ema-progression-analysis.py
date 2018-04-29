import datetime
import pandas as pd
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess

def main():
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

  return lamda


def loadDataWithValenceArousal(filepath):
  # column_names = ['uuid', 'device_id', 'question_id', 'question_content', 'question_set', 'responsecode_0', 'timestamp', 'date_answered']
  df = pd.read_csv(filepath, sep=',', parse_dates=['timestamp'])

  # magic numbers, deal with it!
  min_ts = datetime.datetime(2016, 4, 20)
  max_ts = datetime.datetime(2016, 4, 30)

  num_days = (max_ts-min_ts).days

  common_devices = []
  init = False

  for i in range(0, num_days):
    miscores = []

    curr_ts = min_ts + datetime.timedelta(days=i)

    for id, devicedf in df.groupby(['device_id']):
      devicedf = devicedf.loc[devicedf['timestamp'].shift() != devicedf['timestamp']] # remove duplicates
      devicedf = devicedf.loc[(devicedf['timestamp'] >= curr_ts) & (devicedf['timestamp'] <= curr_ts+datetime.timedelta(days=1))]
      if (len(devicedf.index) > 0): # if number of responses greater than 0
        miscores.append(id)

    if init is False:
      common_devices = miscores
      init = True

    common_devices = list(set(common_devices) & set(miscores))

  # intersect common devices with the 23 devices from asd analysis
  devices = []
  with open('users.txt', 'r') as users_file:
    for device in users_file:
      devices.append(device.strip())

  common_devices = list(set(common_devices) & set(devices))

  print 'num devices:', len(common_devices)

  for i in range(0, num_days):
    miscores = []

    curr_ts = min_ts + datetime.timedelta(days=i+1)

    for id, devicedf in df.groupby(['device_id']):
      if id not in common_devices:
        continue

      ###
      devicedf = devicedf.loc[devicedf['timestamp'].shift() != devicedf['timestamp']]  # remove duplicates

      devicedf = devicedf.loc[(devicedf['timestamp'] >= min_ts) & (devicedf['timestamp'] <= curr_ts)]

      numresponses = len(devicedf.index)
      print 'numdays:', i, 'device:', id, 'numresponses:', numresponses

      delvalence = devicedf['valence'].diff().dropna()
      delarousal = devicedf['arousal'].diff().dropna()
      deltime = devicedf['timestamp'].diff().dropna()

      mediantime = deltime.median()

      lamda = findLambda(delvalence, delarousal, deltime, mediantime)

      asdarousal = delarousal / ((deltime / mediantime) ** lamda)
      asdvalence = delvalence / ((deltime / mediantime) ** lamda)

      if len(asdarousal.index) > 0:
        meanasdarousal = asdarousal.mean()
        madasdarousal = np.fabs(asdarousal - meanasdarousal).mean()

        meanasdvalence = asdvalence.mean()
        madasdvalence = np.fabs(asdvalence - meanasdvalence).mean()

        miscores.append((id, madasdarousal, madasdvalence, madasdarousal + madasdvalence))

    miscoresdf = pd.DataFrame(miscores, columns=('device', 'arousal', 'valence', 'sum'))

    if (len(miscoresdf.index) < len(common_devices)):  # only write if we have data for all devices
      print 'i', i, 'len:', len(miscoresdf.index)
      continue

    medianscore = miscoresdf['sum'].median()
    miscoresdf['label'] = np.where(miscoresdf['sum'] <= medianscore, '0', '1')

    miscoresdf.to_csv('asd-days/asdm' + str(curr_ts.month) + 'd' + str(curr_ts.day) + '.txt', index=False)


if __name__ == '__main__':
  main()
