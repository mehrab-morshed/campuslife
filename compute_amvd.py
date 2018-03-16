import pandas as pd
from amvd import *

def main():
  for i in range(18, 25):
    df = loadData("/coc/pcba1/schawla32/days/day"+str(i)+".csv")
    energy_df = amvd(df)

    google_df = loadData("/coc/pcba1/schawla32/days/day"+str(i)+"-googleactivity.csv")
    googleactivity_df = googleactivity(google_df)

    quedget_df = loadData("/coc/pcba1/schawla32/days/day"+str(i)+"-quedget.csv")
    quedget_df = quedget_responses(quedget_df)

    energy_df = energy_df.merge(googleactivity_df)
    energy_df = energy_df.merge(quedget_df)
    energy_df.to_csv("userepochs-day" + str(i) + ".csv", sep='\t', index=False)

def loadData(filepath):
  return pd.read_csv(filepath, sep='\t', parse_dates=['timestamp'])

if __name__ == '__main__':
  main()
