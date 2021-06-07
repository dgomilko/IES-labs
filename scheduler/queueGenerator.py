from math import exp
from random import uniform, triangular
from consts import possibleTasks
from task import Task

def poisson(lambdaVal):
  exponent = exp(-lambdaVal)
  randEl = uniform(0.0, 1.0)
  temp = exponent
  factorial = 1
  pow = 1
  generated = 0
  while randEl > temp:
    generated += 1
    factorial = generated * factorial
    pow = pow * lambdaVal
    temp = temp + pow * exponent / factorial
  return generated * 0.1

def getPeriods(meanLambda, interval):
  upperBound = meanLambda * 1.5
  lowerBound = meanLambda / 1.5
  mean = 3 * meanLambda - lowerBound - upperBound
  lams = [triangular(lowerBound, upperBound, mean) for _ in possibleTasks]
  periods = [round(interval / (poisson(l) or uniform(0.01, 0.5)), 4) for l in lams]
  return periods

def generateTasks(intensity, interval, limit = 20):
  curTime = 0
  timeLimit = limit * interval
  queue = list()
  tasks = dict()
  periods = getPeriods(intensity, interval)
  for i, task in enumerate(possibleTasks):
    period = periods[i]
    tasks[task] = [period, period]
  while curTime < timeLimit:
    for wcet, val in tasks.items():
      period, lastArrival = val
      arrival = lastArrival + period
      if arrival > curTime: continue
      task = Task(round(arrival, 4), wcet, period)
      queue.append(task)
      tasks[wcet][1] = arrival
    curTime += interval
  return queue
