import datetime
import pandas as pd

def main():
  loadDataForDays("/coc/pcba1/schawla32/google_activity.txt", 20)

# https://stackoverflow.com/questions/28239529/conditional-row-read-of-csv-in-pandas
def valid(chunks, startday, numdays):
  for chunk in chunks:
    mask = chunk['timestamp'].map(lambda x: x.day) < startday+numdays
    if mask.all():
      yield chunk
    else:
      yield chunk.loc[mask]
      break

def loadDataForDays(filepath, numdays):
  start_date = None
  with open(filepath) as fp:
    first_line = fp.readline()
    first_line_splits = first_line.strip().split('\t')
    start_date = datetime.datetime.fromtimestamp(long(first_line_splits[1])/1000.0)

  if start_date is None:
    return

  # Read file in chunks
  chunksize = 10 ** 5

  column_names = ['timestamp', 'device_id', 'activity_name', 'activity_type', 'confidence']
  column_indexes = [1, 2, 3, 4, 5]
  dateparse = lambda x: datetime.datetime.fromtimestamp(long(x)/1000.0)

  chunks = pd.read_csv(filepath, sep='\t', header=None, names=column_names, usecols=column_indexes,
                       chunksize=chunksize, parse_dates=['timestamp'], date_parser=dateparse)
  df = pd.concat(valid(chunks, start_date.day, numdays))

  for i in range(0, numdays):
    mask = df['timestamp'].map(lambda x: x.day) == start_date.day+i
    df_masked = df[mask]
    df_dayi = df_masked.sort_values(['device_id', 'timestamp'])
    df_dayi.to_csv('day' + str(start_date.day+i) + '-googleactivity.csv', sep='\t', index=False)

if __name__ == '__main__':
  main()
