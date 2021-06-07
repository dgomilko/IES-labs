from dynamicSchedulers import EDF, RM
from fifo import FIFO
from utils import printResult, showGraphs, runSchedulers
from queueGenerator import generateTasks
import matplotlib.pyplot as plt

INTERVAL = 2.5
INTENSITY = 7
LIMIT = 5
schedulers = {
  'FIFO': FIFO,
  'EDF': EDF,
  'RM': RM
}
tasks = generateTasks(INTENSITY, INTERVAL, LIMIT)
for name, sched in schedulers.items():
  printResult(sched(tasks), name)
  
showGraphs()
plt.show()
