import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
  #FIXME for loop
  #for i in range(6, 16):
  for i in range(6, 10):
    df = loadData("userepochs-day"+str(i)+".csv")
    plotDataV2(df, i)

  plt.show()

def loadData(filepath):
  return pd.read_csv(filepath, sep='\t')

def plotDataV2(df, i):
  plotdf = pd.DataFrame()
  for group in df.groupby([df.label]):
    groupdf = pd.DataFrame()
    groupdf[group[0]] = group[1]['mean']
    groupdf[group[0]+'-minute'] = group[1]['timestamp']*60 + group[1]['timestamp.1']
    groupdf = groupdf.set_index(group[0]+'-minute').reindex(range(0, 60*24)).fillna(0).reset_index()

    plotdf[group[0]] = groupdf[group[0]]

  fig, ax = plt.subplots()
  fig.canvas.set_window_title('Day '+str(i))
  ax.set_title('Click on legend line to toggle line on/off')
  lines = []
  for column in plotdf.columns:
    line, = ax.plot(np.arange(60 * 24)+1, plotdf[column], lw=1.5, label=column, linestyle='-', marker=',', markersize=5)
    lines.append(line)

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
    origline = lined[legline]
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
