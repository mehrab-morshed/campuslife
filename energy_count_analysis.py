import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def main():
#  df = loadData('gregory.txt')
#  daily_count_from_google(df)

  df = loadData('userepochs/25a36cd5-9751-4e6e-b047-89e86e740bd5.txt')
  daily_count_from_google(df, '25a36cd5-9751-4e6e-b047-89e86e740bd5')
  df = loadData('userepochs/4eb47c96-7193-471c-8d49-1588d0d4db74.txt')
  daily_count_from_google(df, '4eb47c96-7193-471c-8d49-1588d0d4db74')
  df = loadData('userepochs/7a468788-f9f0-4a80-81f7-de4958df72d8.txt')
  daily_count_from_google(df, '7a468788-f9f0-4a80-81f7-de4958df72d8')
  df = loadData('userepochs/afc17c7b-19fa-49b6-8488-4e03d01a4761.txt')
  daily_count_from_google(df, 'afc17c7b-19fa-49b6-8488-4e03d01a4761')
  df = loadData('userepochs/cfbc3b8e-350f-43d3-b495-adf7e7eb4d82.txt')
  daily_count_from_google(df, 'cfbc3b8e-350f-43d3-b495-adf7e7eb4d82')

  #plt.show()

def daily_count_from_google(df, device_id):
  activity_counts = {}

  # group by device
  for device, devicedf in df.groupby(['device_id']):
    # remove active periods
    active_labels = ['on_foot', 'walking', 'running', 'on_bicycle']
    devicedf = devicedf[~devicedf['activity_name'].isin(active_labels)]

    # get sedentary bouts
    activity_counts[device] = []
    for k, g in devicedf.groupby(devicedf['minute'] - np.arange(devicedf.shape[0])):
        activity_counts[device].append(len(g.index))

  # split sedentary bouts in 10 bins
  xvals = {}
  for device, counts in activity_counts.iteritems():
    ecdf_vals = ecdf(np.transpose(np.asmatrix(counts)), 11)
    xvals[device] = np.squeeze(np.asarray(ecdf_vals))
    area = np.trapz(ecdf_vals)
    print("auc =", area)

  print activity_counts
  plotDataV2(xvals, device_id)


def plotDataV2(dic, device_id):
  fig, ax = plt.subplots()
  fig.canvas.set_window_title('Device '+device_id)
  ax.set_title('Click on legend line to toggle line on/off')
  lines = []

  for device, device_ecdf in dic.iteritems():
    line, = ax.plot(device_ecdf, np.linspace(0, 1, num=11), lw=1.5, label=device, linestyle='-', marker=',', markersize=5)
    lines.append(line)

  # set axis names
  plt.xlabel('Bout Length')
  plt.ylabel('P(Bout Length < X)')

  leg = ax.legend(loc='upper left', fancybox=True, shadow=True)
  leg.get_frame().set_alpha(0.4)
  lined = dict()
  for legline, origline in zip(leg.get_lines(), lines):
    legline.set_picker(5)  # 5 pts tolerance
    lined[legline] = origline

  def onpick(event):
    # on the pick event, find the orig line corresponding to the
    # legend proxy line, and toggle the visibility
    legline = event.artist
    origline = lined[legline] # 0 is the line, 1 is the filled polygon
    vis = not origline.get_visible()
    origline.set_visible(vis)

    # Change the alpha on the line in the legend so we can see what lines
    # have been toggled
    if vis:
      legline.set_alpha(1.0)
    else:
      legline.set_alpha(0.2)
    fig.canvas.draw()

  fig.canvas.mpl_connect('pick_event', onpick)

def ecdf(data, components):
  #
  #   rep = ecdfRep(data, components)
  #
  #   Estimate ecdf-representation according to 
  #     Hammerla, Nils Y., et al. "On preserving statistical characteristics of 
  #     accelerometry data using their empirical cumulative distribution." 
  #     ISWC. ACM, 2013.
  #
  #   Input: 
  #       data        Nxd     Input data (rows = samples).
  #       components  int     Number of components to extract per axis.
  #
  #   Output:
  #       rep         Mx1     Data representation with M = d*components+d
  #                           elements.
  #
  #   Nils Hammerla '15
  #
  data = np.sort(data, axis=0)
  data = data[np.int32(np.around(np.linspace(0,data.shape[0]-1,num=components))),:]
  data = data.flatten(1)
  return data

def daily_count_removeme(df):
  bins = np.arange(9.5, 12 + 0.1, 0.1)
  #df['mean'].hist(cumulative=True, normed=1, by=df['device_id'], bins=bins)
  df['mean'].hist(by=df['device_id'], bins=bins)

  mapping = {'0': 0, 'unknown': 0, 'still': 0, 'running': 1, 'walking': 1, 'on_foot': 1, 'on_bicycle': 2, 'in_vehicle': 3, 'tilting': 4}
  df['activity_name'] = df['activity_name'].apply(lambda s: mapping.get(s) if s in mapping else 0)
  #axarr = df['activity_name'].hist(cumulative=True, normed=1, by=df['device_id'], bins=range(0, 6, 1))
  axarr = df['activity_name'].hist(by=df['device_id'], bins=range(0, 6, 1))
  for ax in axarr.flatten():
    ax.xaxis.set_major_formatter(ticker.NullFormatter())

    # Customize minor tick labels
    ax.xaxis.set_minor_locator(ticker.FixedLocator([0.5, 1.5, 2.5, 3.5, 4.5]))
    ax.xaxis.set_minor_formatter(ticker.FixedFormatter(['1', '2', '3', '4', '5']))

    ax.set_xticklabels(['still', 'moving', 'cycling', 'driving', 'tilting'], ha='center', minor=True, rotation = 0)

  plt.show()

def loadData(filepath):
  return pd.read_csv(filepath, sep='\t')

if __name__ == '__main__':
  main()

