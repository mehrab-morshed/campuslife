import pandas as pd
from amvd import *

def main():
  # april
  for i in range(15, 31):
    print 'Processing April', i
    df = loadData("/coc/pcba1/schawla32/newdays/april/day"+str(i)+".csv")
    energy_df = amvd(df)

    google_df = loadData("/coc/pcba1/schawla32/newdays/april/daym4d"+str(i)+"-googleactivity.csv")
    googleactivity_df = googleactivity(google_df)

    quedget_df = loadData("/coc/pcba1/schawla32/newdays/april/daym4d"+str(i)+"-quedget.csv")
    quedget_df = quedget_responses(quedget_df)

    energy_df = energy_df.merge(googleactivity_df)
    energy_df = energy_df.merge(quedget_df)
    energy_df.to_csv("userepochs-daym4d" + str(i) + ".csv", sep='\t', index=False)

  # may
  for i in range(1, 7):
    print 'Processing May', i
    df = loadData("/coc/pcba1/schawla32/newdays/may/day"+str(i)+".csv")
    energy_df = amvd(df)

    google_df = loadData("/coc/pcba1/schawla32/newdays/may/daym5d"+str(i)+"-googleactivity.csv")
    googleactivity_df = googleactivity(google_df)

    quedget_df = loadData("/coc/pcba1/schawla32/newdays/may/daym5d"+str(i)+"-quedget.csv")
    quedget_df = quedget_responses(quedget_df)

    energy_df = energy_df.merge(googleactivity_df)
    energy_df = energy_df.merge(quedget_df)
    energy_df.to_csv("userepochs-daym5d" + str(i) + ".csv", sep='\t', index=False)

def loadData(filepath):
  return pd.read_csv(filepath, sep='\t', parse_dates=['timestamp'])

if __name__ == '__main__':
  main()
