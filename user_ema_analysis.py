import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

def loadData(filepath):
  return pd.read_csv(filepath, sep='\t')

def autolabel(rects, energyvals):
  """
  Attach a text label above each bar displaying its height
  """
  i = 0
  for rect in rects:
    print energyvals[i]
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., 5, "{}".format(energyvals[i].replace('[', '').replace(']', '')), ha='center', va='bottom')
    i = i+1

if __name__ == '__main__':
  df = loadData('4eb47c96-7193-471c-8d49-1588d0d4db74.txt')

  xdict = []
  for day, daydf in df.groupby(['device_id']):
    removeids = range(1,28) # for SSE analysis
    daydf = daydf[~daydf['question_id'].isin(removeids)]

    daydf.ix[(daydf.question_id >= 40) & (daydf.responsecode_0 > 2), 'responsecode_new'] = 'positive'
    daydf.ix[(daydf.question_id >= 40) & (daydf.responsecode_0 <= 2), 'responsecode_new'] = 'negative'
    daydf.ix[(daydf.question_id < 40) & (daydf.responsecode_0 > 2), 'responsecode_new'] = 'negative'
    daydf.ix[(daydf.question_id < 40) & (daydf.responsecode_0 <= 2), 'responsecode_new'] = 'positive'

    yvals = [day, 0, 0, 0]
    for label, count in daydf.groupby('responsecode_new'):
      if label == 'positive':
        yvals[1] = count.responsecode_new.count()
      else:
        yvals[2] = count.responsecode_new.count()
    yvals[3] = daydf['ecdf'].iloc[0]

    xdict.append(yvals)

  print xdict

  fig, ax = plt.subplots()
  width = 0.35
  rects1 = ax.bar(np.arange(len(xdict)), [item[1] for item in xdict], width, alpha=0.5, color='g')
  rects2 = ax.bar(np.arange(len(xdict))+width, [item[2] for item in xdict], width, alpha=0.5, color='r')
  plt.xticks(rotation=45)
  ax.set_xticklabels([item[0] for item in xdict])
  ax.set_xticks(np.arange(len(xdict)) + width/ 2)

  autolabel(rects1, [item[3] for item in xdict])

  plt.show()

  ecdfs = [float(item[3].replace('[', '').replace(']', '')) for item in xdict]

  mu, std = norm.fit(ecdfs)
  print mu, std

  for ecdf in ecdfs:
    print ecdf, norm.cdf(ecdf, mu, std), np.fabs(0.5-(norm.cdf(ecdf, mu, std)))


