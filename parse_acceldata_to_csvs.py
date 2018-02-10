import datetime
import pandas as pd

def main():
  # loadDataPerDate("./accel.txt", 1)
  loadDataForDays("./accel.txt", 10)

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

  column_names = ['timestamp', 'device_id', 'x', 'y', 'z', 'label']
  column_indexes = [1, 2, 3, 4, 5, 7]
  dateparse = lambda x: datetime.datetime.fromtimestamp(long(x)/1000.0)

  chunks = pd.read_csv(filepath, sep='\t', header=None, names=column_names, usecols=column_indexes,
                       chunksize=chunksize, parse_dates=['timestamp'], date_parser=dateparse)
  df = pd.concat(valid(chunks, start_date.day, numdays))

  for i in range(0, numdays):
    mask = df['timestamp'].map(lambda x: x.day) == start_date.day+i
    df_masked = df[mask]
    df_dayi = df_masked.sort_values(['label', 'timestamp'])
    df_dayi.to_csv('day' + str(start_date.day+i) + '.csv', sep='\t', index=False)


def loadDataPerDate(filepath, numdays):

  rows = []
  with open(filepath) as fp:
    previous_day = None
    day_count = 0
    for row in fp:
      row_splits = row.strip().split('\t')
      row_date = datetime.datetime.fromtimestamp(long(row_splits[1])/1000.0)
      if previous_day is not None:
        if row_date.day == previous_day:
          rows.append(parseRow(row_splits))
        else:
          day_count = day_count + 1
          df = pd.DataFrame(rows)
          # FIXME the loop stops when a row is read that has the next date but
          # since the data is not in order there still may be entries in the
          # file that come after the current entry and have the last date.
          # Potential fix - sort all the data before hand, but its a huge file
          # (35G)
          df = df.sort_values(['label', 'timestamp']) # sort data
          df.to_csv('day'+str(day_count)+'.csv', sep='\t', index=False)
          if (day_count >= numdays): # finish reading
            break
          else: # start a new day
            rows = []
            previous_day = row_date.day
            rows.append(parseRow(row_splits))
      else:
        previous_day = row_date.day
        rows.append(parseRow(row_splits))

def parseRow(row_splits):
  rowDict = dict()
  rowDict['timestamp'] = long(row_splits[1])
  rowDict['device_id'] = row_splits[2]
  rowDict['x'] = float(row_splits[3])
  rowDict['y'] = float(row_splits[4])
  rowDict['z'] = float(row_splits[5])
  rowDict['label'] = row_splits[7]

  return rowDict

if __name__ == '__main__':
  main()
