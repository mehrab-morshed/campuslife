import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

def main():
  #FIXME for loop
  #for i in range(6, 16):
  for i in range(6, 11):
    df = loadData("userepochs-day"+str(i)+".csv")
    plotDataV2(df, i)
  plt.show()

def loadData(filepath):
  return pd.read_csv(filepath, sep='\t')

def plotDataV2(df, i):
  xrange = np.arange(60 * 24)

  plotdf = pd.DataFrame()
  for group in df.groupby([df.label]):
    groupdf = pd.DataFrame()
    groupdf[group[0]] = group[1]['mean']

    # FIXME remove the follwing three lines - no longer needed, the missing values are filled on compute_amvd.py now
    # groupdf[group[0]+'-minute'] = group[1]['minute']
    # groupdf[group[0]+'-minute'] = group[1]['timestamp']*60 + group[1]['timestamp.1']
    # groupdf = groupdf.set_index(group[0]+'-minute').reindex(xrange).fillna(0).reset_index()

    plotdf[group[0]] = groupdf[group[0]].values
    plotdf[group[0]+'-delta'] = group[1]['delta'].values

  fig, ax = plt.subplots()
  fig.canvas.set_window_title('Day '+str(i))
  ax.set_title('Click on legend line to toggle line on/off')
  lines = []
  for column in plotdf.columns:
    if 'delta' in column:
      continue
    line, = ax.plot(xrange, plotdf[column], lw=1.5, label=column, linestyle='-', marker=',', markersize=5)
    # poly = ax.fill_between(xrange, plotdf[column], where=plotdf[column]>10.05, facecolor=line.get_color(), alpha=0.5)
    poly = ax.fill_between(xrange, plotdf[column], where=(plotdf[column]>9.6).values & (plotdf[column+'-delta'].abs() > 0.025).values, facecolor=line.get_color(), alpha=0.5)
    lines.append((line, poly))  # 0 is the line, 1 is the filled polygon

  # set x axis to display time
  def timeformatter(x, pos):
    'The two args are the value and tick position'
    return "{:02d}:{:02d}".format(int(x)/60, int(x)%60)
  formatter = plt.FuncFormatter(timeformatter)
  ax.xaxis.set_major_formatter(formatter)

  # set axis names
  plt.xlabel('Time')
  plt.ylabel('Acceleration(magnitude)')

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
    origline = lined[legline][0] # 0 is the line, 1 is the filled polygon
    poly = lined[legline][1]
    vis = not origline.get_visible()
    origline.set_visible(vis)
    poly.set_visible(vis)

    # Change the alpha on the line in the legend so we can see what lines
    # have been toggled
    if vis:
      legline.set_alpha(1.0)
    else:
      legline.set_alpha(0.2)
    fig.canvas.draw()

  fig.canvas.mpl_connect('pick_event', onpick)

def plotData(df):
  labels = []
  for i in range(0, len(df.columns)):
    if i % 2 == 0: # FIXME dirty hack to ignore count columns
      labels.append(df.columns[i])

  df.plot(y=labels, x=np.arange(df.shape[0])+1, style='.-')
  plt.markersize = 0.2
  plt.show()

if __name__ == '__main__':
  main()
