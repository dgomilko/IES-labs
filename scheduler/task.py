from dataclasses import dataclass, field
from random import uniform, randint

def getIntervals(time):
  return [(time[i], time[i + 1] - time[i]) for i in range(0, len(time), 2)]

def getWaitTime(task):
  time = task.timestamps
  diff = time[0] - task.arrival
  if len(time) > 2:
    return diff + sum([time[i] - time[i - 1] for i in range(2, len(time), 2)])
  else: return diff

@dataclass
class Task:
  arrivalTime: float
  wcet: float
  period: float
  deadline: float = field(init=False)
  protected: bool = field(init=False)

  def __post_init__(self):
    chance = randint(0, 100)
    k = uniform(1.0, 3.0) if chance < 5 else uniform(10.0, 20.0)
    self.deadline = round(self.arrivalTime + k * self.wcet, 4)
    self.protected = chance < 10

@dataclass
class ProcessedTask:
  arrival: float
  deadline: float
  timestamps: list[float]
  deadlineMissed: bool
  start: float = field(init=False)
  end: float = field(init=False)
  waitingTime: float = field(init=False)
  
  def __post_init__(self):
    self.start = self.timestamps[0]
    self.end = self.timestamps[-1]
    self.waitingTime = round(getWaitTime(self), 4)

@dataclass
class SchedulingResult:
  result: list[ProcessedTask]
  idleTime: float
  totalTime: float
  idlePercent: float = field(init=False)
  avgWait: float = field(init=False)
  missedTasksCount: int = field(init=False)
  missedTasksPercent: float = field(init=False)
  ganttChartData: list[list[tuple()]] = field(init=False)

  def __post_init__(self):
    waitTimesSum = sum(map(lambda x: x.waitingTime, self.result))
    missedTasks = list(filter(lambda x: x.deadlineMissed, self.result))
    tasksNum = len(self.result)
    self.avgWait = round(waitTimesSum / (tasksNum or 1), 4)
    self.missedTasksCount = len(missedTasks)
    self.missedTasksPercent = round(self.missedTasksCount / (tasksNum or 1) * 100, 4)
    self.idlePercent = round(self.idleTime / (self.totalTime or 1) * 100, 4)
    self.ganttChartData = [getIntervals(t.timestamps) for t in self.result]
