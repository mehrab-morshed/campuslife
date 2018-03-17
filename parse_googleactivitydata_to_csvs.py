import datetime
import pandas as pd
import numpy as np

def main():
  loadDataForDays("/coc/pcba1/schawla32/google_activity.txt", 0, 60)

# https://stackoverflow.com/questions/28239529/conditional-row-read-of-csv-in-pandas
def valid(chunks, startdate, enddate):
  for chunk in chunks:
    mask = ((chunk['timestamp'] >= np.datetime64(startdate)) & (chunk['timestamp'] <= np.datetime64(enddate)))
    print chunk['timestamp'].iloc[0], mask.any()
    if not mask.any():
      continue

    if mask.all():
      yield chunk
    else:
      yield chunk.loc[mask]

def loadDataForDays(filepath, skipdays, numdays):
  # read first date from file
  start_date = None
  with open(filepath) as fp:
    first_line = fp.readline()
    first_line_splits = first_line.strip().split('\t')
    start_date = datetime.datetime.fromtimestamp(long(first_line_splits[1])/1000.0)

  if start_date is None:
    return

  # add skip days
  start_date = start_date + datetime.timedelta(days=skipdays)
  end_date = start_date + datetime.timedelta(days=numdays)
  start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
  end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
  print 'start date:', start_date, ', end date:', end_date

  # Read file in chunks
  chunksize = 10 ** 5

  column_names = ['timestamp', 'device_id', 'activity_name', 'activity_type', 'confidence']
  column_indexes = [1, 2, 3, 4, 5]
  dateparse = lambda x: datetime.datetime.fromtimestamp(long(x)/1000.0)

  chunks = pd.read_csv(filepath, sep='\t', header=None, names=column_names, usecols=column_indexes,
                       chunksize=chunksize, parse_dates=['timestamp'], date_parser=dateparse)
  df = pd.concat(valid(chunks, start_date, end_date))

  for i in range(0, numdays):
    mask = (df['timestamp'] >= np.datetime64(start_date)) & (df['timestamp'] <= np.datetime64((start_date + datetime.timedelta(days=1))))
    df_masked = df[mask]

    # stop writing if an empty day is found
    if len(df_masked.index) == 0:
      break

    # sort by device_id first, time second
    df_dayi = df_masked.sort_values(['device_id', 'timestamp'])
    df_dayi.to_csv('day' + 'm' + str(start_date.month) + 'd' + str(start_date.day) + '-googleactivity.csv', sep='\t', index=False)

    start_date = start_date + datetime.timedelta(days=1)

if __name__ == '__main__':
  main()
