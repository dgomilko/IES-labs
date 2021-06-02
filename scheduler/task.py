from dataclasses import dataclass, field
from random import uniform, randint

def getIntervals(time):
  return [(time[i], time[i + 1] - time[i]) for i in range(0, len(time), 2)]

def getWaitTime(time):
  if len(time) > 2:
    return sum([time[i] - time[i - 1] for i in range(2, len(time), 2)])
  else: return 0

@dataclass
class Task:
  arrivalTime: float
  wcet: float
  deadline: float = field(init=False)

  def __post_init__(self):
    chance = randint(0, 100)
    k = uniform(2.0, 5.0) if chance < 10 else uniform(10.0, 20.0)
    self.deadline = round(self.arrivalTime + k * self.wcet, 4)

@dataclass
class ProcessedTask:
  arrival: float
  timestamps: list[float]
  deadlineMissed: bool
  start: float = field(init=False)
  end: float = field(init=False)
  waitingTime: float = field(init=False)
  
  def __post_init__(self):
    self.start = self.timestamps[0]
    self.end = self.timestamps[-1]
    wait = getWaitTime(self.timestamps)
    self.waitingTime = round(self.start - self.arrival + wait, 4)

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
    self.avgWait = round(waitTimesSum / tasksNum, 4)
    self.missedTasksCount = len(missedTasks)
    self.missedTasksPercent = round(self.missedTasksCount / tasksNum * 100, 4)
    self.idlePercent = round(self.idleTime / self.totalTime * 100, 4)
    self.ganttChartData = [getIntervals(t.timestamps) for t in self.result]
