import matplotlib
import matplotlib.pyplot as plt
from task import SchedulingResult
from queueGenerator import generateTasks
from fifo import FIFO
from dynamicSchedulers import RM, EDF
from random import choice
from itertools import chain

def generalise(schedRes):
  result = list(chain.from_iterable([r.result for r in schedRes]))
  idle = sum(res.idleTime for res in schedRes)
  total = sum(res.totalTime for res in schedRes)
  return SchedulingResult(result, idle, total)

def printResult(schedRes, type):
  general = generalise(schedRes)
  tasks = general.result
  idle = sum(res.idlePercent for res in schedRes) / len(schedRes)
  out = (
    f'Scheduling using {type}:\n' 
    f'\tAverage waiting time: {general.avgWait}\n'
    f'\tIdle time percent: {idle}%)\n'
    f'\tMissed tasks count: {general.missedTasksCount} '
    f'({general.missedTasksPercent}% out of total {len(tasks)})\n'
  )
  for i, task in enumerate(tasks):
    out += (
      f'\nTask {i + 1}: arrived: {task.arrival}, waited: {task.waitingTime}, '
      f'started processing: {round(task.start, 4)}, '
      f'finish: {round(task.end, 4)}; '
    )
    if (task.deadlineMissed): out += f'DEADLINE MISSED'
  print(out)

def runSchedulers():
  hex_colors_dic, rgb_colors_dic = dict(), dict()
  hex_colors_only = list()
  for name, hex in matplotlib.colors.cnames.items():
    hex_colors_only.append(hex)
    hex_colors_dic[name] = hex
    rgb_colors_dic[name] = matplotlib.colors.to_rgb(hex)

  tasks = generateTasks(7, 1.5, 7)
  size = len(tasks)
  schedulers = {
    'FIFO': FIFO,
    'EDF': EDF,
    'RM': RM
  }
  resStats = {t: sched(tasks).ganttChartData for t, sched in schedulers.items()}
  fig, axs = plt.subplots(3)
  plt.subplots_adjust(left=0.05, bottom=0.03, right=0.97, top=0.92, wspace=0.1)
  fig.suptitle('Scheduling results')
  for i, title in enumerate(resStats):
    gnt = axs[i]
    gnt.grid(True)
    gnt.set_title(title)
    gnt.set_yticks([x * 3 + 3 for x in range(size)])
    gnt.set_yticklabels(f'Task {x + 1}' for x in range(size))

  for task in range(size):
    for i, key in enumerate(resStats):
      color = choice(hex_colors_only)
      result = resStats[key]
      data = result[task]
      axs[i].broken_barh(data, (task * 3, 3), facecolors=color)
      axs[i].broken_barh(data, (size * 3, 5), facecolors=color)

def unpackData(data):
  return [[data[j][i] for j in range(len(data))] for i in range(len(data[0]))]

def intensityData(scheduler):
  intensities = [i * 0.1 for i in range(1, 500, 2)]
  avgWait, idlePercent, missedPercent = list(), list(), list()
  for intensity in intensities:
    tasks = generateTasks(intensity, 2.5)
    results = scheduler(tasks)
    general = generalise(results)
    avgWait.append([general.avgWait] + [r.avgWait for r in results])
    idlePercent.append([general.idlePercent] + [r.idlePercent for r in results])
    missedPercent.append([general.missedTasksPercent] + [r.missedTasksPercent for r in results])
  return intensities, unpackData(avgWait), unpackData(idlePercent), unpackData(missedPercent)

def sizeData(scheduler):
  intensity = 15
  results = dict()
  lens, avgWait, missedPercent = list(), list(), list()
  for _ in range(1000):
    tasks = generateTasks(intensity, 2.5)
    result = generalise(scheduler(tasks))
    results[len(tasks)] = [result.avgWait, result.missedTasksPercent]
  for key in sorted(results):
    lens.append(key)
    avgWait.append(results[key][0])
    missedPercent.append(results[key][1])
  return lens, avgWait, missedPercent

def plot(titles, stats, bar = False):
  size = len(titles)
  fig, axs = plt.subplots(size)
  plt.subplots_adjust(left=0.05, bottom=0.05, right=0.97, top=0.95, hspace=0.27)

  width = 0.3
  offset = - width   
  for title, data in stats.items():
    if bar:
      x = [x + offset for x in data[0]]
      axs[0].bar(x, data[1], width, label=title)
      axs[1].bar(x, data[2], width, label=title)
      offset += width
    else:
      axs[0].plot(data[0], data[1], label=title, linewidth=0.9)
      axs[1].plot(data[0], data[2], label=title, linewidth=0.9)
      axs[2].plot(data[0], data[3], label=title, linewidth=0.9)

  for i, title in enumerate(titles):
    axes = titles[title]
    axs[i].set_title(title)
    axs[i].set(xlabel=axes[0], ylabel=axes[1])
    axs[i].legend()

def showGraphs():
  schedulers = {
    'FIFO': FIFO,
    'EDF': EDF,
    'RM': RM
  }
  resStats = {t: [intensityData(s), sizeData(s)] for t, s in schedulers.items()}
  titles = [{
    'Intensity - wait time (total)': ['intensity', 'average wait time'],
    'Intensity - wait time (processor 1)': ['intensity', 'average wait time'],
    'Intensity - wait time (processor 2)': ['intensity', 'average wait time']
    },
    {
    'Intensity - idle percent (total)': ['intensity', 'idle time percent'],
    'Intensity - idle percent (proecssor 1)': ['intensity', 'idle time percent'],
    'Intensity - idle percent (processor 2)': ['intensity', 'idle time percent']
    },
    {
    'Intensity - missed deadlines (total)': ['intensity', 'missed percent'],
    'Intensity - missed deadlines (processor 1)': ['intensity', 'missed percent'],
    'Intensity - missed deadlines (processor 2)': ['intensity', 'missed percent']
    }
  ]
  dataIntensity = {k: v[0] for k, v in resStats.items()}
  for i, title in enumerate(titles): 
    data = {k: (v[0], v[i + 1][0], v[i + 1][1], v[i + 1][2]) for k, v in dataIntensity.items()}
    plot(title, data)

  titlesLen = {
    'Tasks amount - average wait time': ['queue length', 'wait time'],
    'Tasks amount - missed deadlines': ['queue length', 'missed percent']
  }
  plot(titlesLen, {k: v[1] for k, v in resStats.items()}, True)
  