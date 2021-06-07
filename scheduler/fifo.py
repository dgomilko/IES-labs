from task import ProcessedTask, SchedulingResult
from multiprocessing import Process, Queue
from copy import deepcopy
from consts import PROC_AMOUNT

def schedule(queue, allTasks):
  tasks = deepcopy(allTasks)
  tasks.sort(key=lambda x: x.arrivalTime)
  processedTasks = list()
  idleTime = 0
  curTime = 0
  for task in tasks:
    arrival = task.arrivalTime
    if curTime < arrival:
      idleTime += arrival - curTime
      curTime = arrival
    startTime = curTime
    missed = curTime + task.wcet > task.deadline
    if not missed: curTime = curTime + task.wcet
    task = ProcessedTask(arrival, task.deadline, [startTime, curTime], missed)
    processedTasks.append(task)  
  queue.put(SchedulingResult(processedTasks, round(idleTime, 4), round(curTime, 4)))

def FIFO(tasks):
  procs = list()
  queue = Queue()
  splitTasks = [tasks[i::PROC_AMOUNT] for i in range(PROC_AMOUNT)]
  for taskSet in splitTasks:
    procs.append(Process(target=schedule, args=(queue, taskSet,)))
  for proc in procs: proc.start()
  for proc in procs: proc.join()
  return [queue.get() for _ in splitTasks]   
