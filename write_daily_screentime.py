from amvd import *

def main():

  with open('daily-screen-time.txt', 'w') as screen_time_file:
    screen_time_file.write("day,device_id,minutes\n")
    # april
    for i in range(15, 31):
      print 'Processing April', i

      screen_df = loadData("./screen-days/daym4d" + str(i) + "-screen.csv")
      screenacitivity_data = screenactivity(screen_df)
      for row in screenacitivity_data:
        screen_time_file.write("daym4d"+str(i)+","+row[0]+","+str(row[1])+"\n")

    # may
    for i in range(1, 7):
      print 'Processing May', i

      screen_df = loadData("./screen-days/daym5d" + str(i) + "-screen.csv")
      screenacitivity_data = screenactivity(screen_df)
      for row in screenacitivity_data:
        screen_time_file.write("daym5d" + str(i) + "," + row[0] + "," + str(row[1]) + "\n")

def loadData(filepath):
  return pd.read_csv(filepath, sep='\t', parse_dates=['timestamp'])

if __name__ == '__main__':
  main()
