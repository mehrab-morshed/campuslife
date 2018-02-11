import pandas as pd
from amvd import amvd

def main():
  for i in range(6, 11):
    df = loadData("./day"+str(i)+".csv")
    energy_df = amvd(df)
    energy_df.to_csv("userepochs-day" + str(i) + ".csv", sep='\t')

def loadData(filepath):
  return pd.read_csv(filepath, sep='\t', parse_dates=['timestamp'])

if __name__ == '__main__':
  main()
