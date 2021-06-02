from dynamicSchedulers import EDF, RM
from fifo import FIFO
from utils import printResult, runSchedulers, showGraphs
from queueGenerator import generateTasks
import matplotlib.pyplot as plt

schedulers = {
  'FIFO': FIFO,
  'EDF': EDF,
  'RM': RM
}
tasks = generateTasks(2, 10)
for name, sched in schedulers.items():
  printResult(sched(tasks), name)

runSchedulers(10)
showGraphs()
plt.show()
