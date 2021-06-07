from task import ProcessedTask, SchedulingResult
from copy import deepcopy

def FIFO(allTasks):
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
  return SchedulingResult(processedTasks, round(idleTime, 4), round(curTime, 4))    
