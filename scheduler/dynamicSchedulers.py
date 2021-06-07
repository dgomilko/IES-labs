from functools import partial
from copy import deepcopy
from task import ProcessedTask, SchedulingResult
from consts import TACT_SIZE

tasks, activeTasks = list(), list()

def taskID(task):
  return f'{task.arrivalTime}{task.period}{task.deadline}'

def areTasksEqual(taskA, taskB):
  return taskID(taskA) == taskID(taskB)

def checkForNewTasks(time):
    global tasks, activeTasks
    futureTasks = lambda x: x.arrivalTime > time
    arrivedTasks = lambda x: x.arrivalTime <= time
    arrived = list(filter(arrivedTasks, tasks))
    if not arrived: return False
    activeTasks += arrived
    tasks = list(filter(futureTasks, tasks))
    return True

def waitForTasks(curTime, interval, clb):
    global activeTasks 
    maxWaitTime = curTime + interval
    if not checkForNewTasks(maxWaitTime): return None
    clb(activeTasks)
    return activeTasks[0]

def checkMissedTasks(tasks, resTasks):
  diff = list()
  for task in tasks:
    processed = False
    for taskRes in resTasks:
      if task.arrivalTime == taskRes.arrival \
        and task.deadline == taskRes.deadline:
          processed = True
    if not processed: diff.append(task)
  return diff

def BaseDynamicScheduler(estimatePriority, allTasks):
  global tasks, activeTasks
  tasks = deepcopy(allTasks)
  tasks.sort(key=lambda x: x.arrivalTime)
  timestamps = dict()
  curTime, tactCount, idle = 0, 0, 0
  for task in tasks: timestamps[taskID(task)] = list()
  resTasks = list()
  while activeTasks or tasks:
    if tasks: checkForNewTasks(curTime)
    activeTasks = list(filter(lambda x: x.deadline > curTime, activeTasks))
    missed = list(filter(lambda x: x.deadline <= curTime, activeTasks))
    estimatePriority(activeTasks)
    for missedTask in missed:
      task = ProcessedTask(
        missedTask.arrivalTime,
        missedTask.deadline,
        [curTime, curTime],
        True
      )
      resTasks.append(task)
      
    remainedTime = tactCount or TACT_SIZE
    task = None
    if activeTasks:
      task = activeTasks[0]
    else:
      task = waitForTasks(curTime, remainedTime, estimatePriority)
      if not task:
        idle += remainedTime
        curTime += remainedTime
        if tactCount: tactCount = 0
        continue

    if task.arrivalTime > curTime:
        diff = task.arrivalTime - curTime
        idle += diff
        curTime = task.arrivalTime
        tactCount -= diff
    
    timestamps[taskID(task)].append(curTime)
    fitsIntoTact = task.wcet < remainedTime
    elapsedInTact = task.wcet if fitsIntoTact else remainedTime
    newTask = waitForTasks(curTime, elapsedInTact, estimatePriority)
    if newTask and not areTasksEqual(task, newTask):
      task.wcet -= newTask.arrivalTime - curTime
      curTime = newTask.arrivalTime
      timestamps[taskID(task)].append(curTime)
      task = newTask
      timestamps[taskID(task)].append(curTime)
      fitsIntoTact = task.wcet < remainedTime
      elapsedInTact = task.wcet if fitsIntoTact else remainedTime
    curTime += elapsedInTact
    timestamps[taskID(task)].append(curTime)
    if not fitsIntoTact:
      task.wcet -= remainedTime
      tactCount = 0
    else:
      missed = task.deadline < curTime
      task = ProcessedTask(
        task.arrivalTime,
        task.deadline,
        timestamps[taskID(task)],
        missed
      )
      resTasks.append(task)
      activeTasks.pop(0)
      tactCount = remainedTime - elapsedInTact

  missed = checkMissedTasks(allTasks, resTasks)
  if missed:
    for task in missed: 
      task = ProcessedTask(
        task.arrivalTime,
        task.deadline,
        [curTime, curTime],
        True
      )
      resTasks.append(task)
  return SchedulingResult(resTasks, idle, curTime)

def estimatePriorityEDF(tasks):
    return tasks.sort(key=lambda x: (x.deadline, x.wcet))  

def estimatePriorityRM(tasks):
    return tasks.sort(key=lambda x: (x.period, x.wcet, x.deadline))  

EDF = partial(BaseDynamicScheduler, estimatePriorityEDF)
RM = partial(BaseDynamicScheduler, estimatePriorityRM)