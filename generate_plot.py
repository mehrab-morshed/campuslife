import matplotlib.pyplot as plt
import pylab
import numpy as np

def main():
  # x = np.arange(2, 23)
  x = [x for x in range(2, 23)]
  # Activity
  y1 = [0.7, 0.75, 0.7, 0.7, 0.79, 0.74, 0.75, 0.83, 0.87, 0.88, 0.87, 0.87, 0.96, 0.91, 0.87, 0.91, 0.91, 0.86, 0.87, 0.91, 0.91]
  # App count
  y2 = [0.78, 0.59, 0.72, 0.67, 0.67, 0.67, 0.67, 0.71, 0.75, 0.71, 0.75, 0.67, 0.79, 0.75, 0.71, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75]
  # Screen time
  y3 = [0.59, 0.58, 0.58, 0.58, 0.58, 0.58, 0.58, 0.58, 0.58, 0.62, 0.66, 0.62, 0.62, 0.62, 0.62, 0.58, 0.58, 0.62, 0.58, 0.58, 0.58]
  # Audio time
  y4 = [0.8, 0.76, 0.84, 0.72, 0.65, 0.72, 0.76, 0.73, 0.65, 0.65, 0.61, 0.61, 0.65, 0.65, 0.69, 0.69, 0.69, 0.69, 0.69, 0.69, 0.69]

  # user distribution
  # y = [19, 12, 22, 21, 11, 10, 12, 12, 10, 10, 15, 11, 12, 21, 14, 11, 12, 11, 14, 11, 14, 13, 17, 11]
  #
  # num_bins = 12
  # counts, bin_edges = np.histogram(y, bins=num_bins, normed=True)
  # cdf = np.cumsum(counts)
  #
  # plt.xlabel('Days')
  # plt.ylabel('Fraction of users')
  # pylab.plot(bin_edges[1:], cdf)
  # plt.yticks(np.arange(0.0, 1.1, 0.1))


  pylab.xlim([1, 23])
  plt.plot(x, y1, '-o', linewidth=2, label="Activity count")
  plt.plot(x, y2, '-o', label="Social app time count")
  plt.plot(x, y3, '-o', label="Screen time count")
  plt.plot(x, y4, '-o', label="Voice time count")

  plt.xlabel("Number of days")
  plt.ylabel("Mean accuracy (k-fold cv (k=5)")
  plt.xticks(np.arange(min(x), max(x) + 1, 1.0))
  pylab.legend(loc='upper left')
  plt.show()

if __name__ == '__main__':
  main()