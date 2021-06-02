import matplotlib
import matplotlib.pyplot as plt
from random import choice
from queueGenerator import generateTasks
from fifo import FIFO
from dynamicSchedulers import RM, EDF

def printResult(schedRes, type):
  tasks = schedRes.result
  out = (
    f'Scheduling using {type}:\n' 
    f'\tAverage waiting time: {schedRes.avgWait}\n'
    f'\tIdle time percent: {schedRes.idlePercent}%'
    f'(total: {round(schedRes.totalTime, 4)}, '
    f'idle: {round(schedRes.idleTime, 4)})\n'
    f'\tMissed tasks count: {schedRes.missedTasksCount} '
    f'({schedRes.missedTasksPercent}% out of total {len(tasks)})\n'
  )
  for i, task in enumerate(tasks):
    out += (
      f'\nTask {i + 1}: arrived: {task.arrival}, waited: {task.waitingTime}, '
      f'started processing: {round(task.start, 4)}, '
      f'finish: {round(task.end, 4)}; '
    )
    if (task.deadlineMissed): out += f'DEADLINE MISSED'
  print(out)

def intensityData(scheduler):
  tasksNum = 32
  intensities = [i * 0.05 for i in range(1, 1000, 2)]
  avgWait, idlePercent, missedPercent = list(), list(), list()
  for intensity in intensities:
    tasks = generateTasks(intensity, tasksNum)
    results = scheduler(tasks)
    avgWait.append(results.avgWait)
    idlePercent.append(results.idlePercent)
    missedPercent.append(results.missedTasksPercent)
  return intensities, avgWait, idlePercent, missedPercent

def sizeData(scheduler):
  intensity = 2
  lens = [i for i in range(2, 200)]
  avgWait, missedPercent = list(), list()
  for len in lens:
    tasks = generateTasks(intensity, len)
    results = scheduler(tasks)
    avgWait.append(results.avgWait)
    missedPercent.append(results.missedTasksPercent)
  return lens, avgWait, missedPercent

def runSchedulers(size):
  hex_colors_dic, rgb_colors_dic = dict(), dict()
  hex_colors_only = list()
  for name, hex in matplotlib.colors.cnames.items():
    hex_colors_only.append(hex)
    hex_colors_dic[name] = hex
    rgb_colors_dic[name] = matplotlib.colors.to_rgb(hex)

  tasks = generateTasks(3, size)
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

def plot(titles, stats):
  size = len(titles)
  fig, axs = plt.subplots(size)
  plt.subplots_adjust(left=0.05, bottom=0.05, right=0.97, top=0.95, hspace=0.27)
      
  for title, data in stats.items():
    axs[0].plot(data[0], data[1], label=title, linewidth=0.9)
    axs[1].plot(data[0], data[2], label=title, linewidth=0.9)
    if size == 3: axs[2].plot(data[0], data[3], label=title, linewidth=0.9)

  for i, title in enumerate(titles):
    axes = titles[title]
    axs[i].set_title(title)
    axs[i].set(xlabel=axes[0], ylabel=axes[1])
    axs[i].legend()

def showGraphs():
  titlesInt = {
    'Intensity - wait time': ['intensity', 'average wait time'],
    'Intensity - idle percent': ['intensity', 'idle time percent'],
    'Intensity - missed deadlines': ['intensity', 'missed percent']
  }
  titlesLen = {
    'Tasks amount - average wait time': ['queue length', 'wait time'],
    'Tasks amount - missed deadlines': ['queue length', 'missed percent']
  }
  schedulers = {
    'FIFO': FIFO,
    'EDF': EDF,
    'RM': RM
  }
  resStats = {t: [intensityData(s), sizeData(s)] for t, s in schedulers.items()}
  plot(titlesInt, {k: v[0] for k, v in resStats.items()})
  plot(titlesLen, {k: v[1] for k, v in resStats.items()})