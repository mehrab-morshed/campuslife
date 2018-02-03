import datetime
import pandas as pd

def main():
  loadDataPerDate("./accel.txt", 1)

def loadDataPerDate(filepath, numdays):

  #column_names = ['timestamp', 'device_id', 'x', 'y', 'z', 'label']
  #column_indexes = [1, 2, 3, 4, 5, 7]

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
