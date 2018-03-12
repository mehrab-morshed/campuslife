import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from thresholds_config import config
from matplotlib.text import TextPath

def main():
  #FIXME for loop
#  for i in range(6, 7):
#    df = loadData("userepochs-day"+str(i)+".csv")
#    plotdatav2(df, i)
#  plt.show()
  df = loadData('gregory.txt')
  plotDataV2(df, 1)
  plt.show()

def loadData(filepath):
  return pd.read_csv(filepath, sep='\t')

def plotDataV2(df, i):
  xrange = np.arange(60 * 24)

  plotdf = pd.DataFrame()
  for group in df.groupby([df.device_id]):
    groupdf = pd.DataFrame()
    groupdf[group[0]] = group[1]['mean']

    # FIXME remove the follwing three lines - no longer needed, the missing values are filled on compute_amvd.py now
    # groupdf[group[0]+'-minute'] = group[1]['minute']
    # groupdf[group[0]+'-minute'] = group[1]['timestamp']*60 + group[1]['timestamp.1']
    # groupdf = groupdf.set_index(group[0]+'-minute').reindex(xrange).fillna(0).reset_index()

    plotdf[group[0]] = groupdf[group[0]].values
    plotdf[group[0]+'-delta'] = group[1]['delta'].values
    plotdf[group[0]+'-activity'] = group[1]['activity_name'].values

  fig, ax = plt.subplots()
  #fig.canvas.set_window_title('Day '+str(i))
  ax.set_title('Click on legend line to toggle line on/off')
  lines = []
  for column in plotdf.columns:
    if 'delta' in column or 'activity' in column:
      continue
    line, = ax.plot(xrange, plotdf[column], lw=1.5, label=column, linestyle='-', marker=',', markersize=5)
    # new
    activity_groups = plotdf[column+'-activity'].groupby(plotdf[column+'-activity'])
    activity_labels_arr = []
    for name, group in activity_groups:
      if name == '0':
        continue
      print column, group.index
      yvals = plotdf.iloc[group.index]
      activity_labels, = ax.plot(group.index, yvals[column], marker=TextPath((0, 0), name[0], size=10000), color='black', linestyle='', ms=10, label='_nolegend_')
      activity_labels_arr.append(activity_labels)
    # new end
    # poly = ax.fill_between(xrange, plotdf[column], where=plotdf[column]>10.05, facecolor=line.get_color(), alpha=0.5)
    poly = ax.fill_between(xrange, plotdf[column], where=(plotdf[column]>config['magnitude_threshold']).values & (plotdf[column+'-delta'].abs()>config['delta_threshold']).values, facecolor=line.get_color(), alpha=0.5)
    lines.append((line, poly, activity_labels_arr))  # 0 is the line, 1 is the filled polygon

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
    # new
    activity_labels_arr = lined[legline][2]
    for activity_labels in activity_labels_arr:
      activity_labels.set_visible(vis)
    # new end

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
