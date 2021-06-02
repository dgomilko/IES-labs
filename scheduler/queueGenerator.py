from math import exp
from random import uniform, sample, choice
from consts import possibleTasks, TACT_SIZE
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
  return generated

def getNewTasks(intensity):
  availableTasksNum = len(possibleTasks)
  newTasksNum = poisson(intensity)
  newTasks = list()
  if newTasksNum < availableTasksNum:
    newTasks = sample(possibleTasks, newTasksNum) 
  else:
    newTasks = [choice(possibleTasks) for _ in range(newTasksNum)]
  return newTasks

def generateTasks(intensity, queueSize):
  framesCount = 0
  queue = list()
  while len(queue) < queueSize:
    newTasks = getNewTasks(intensity)
    for wcet in newTasks:
      startTime = framesCount * TACT_SIZE
      arrival = round(uniform(startTime, startTime + TACT_SIZE), 5)
      queue.append(Task(arrival, wcet))
      if len(queue) == queueSize: break
    framesCount = framesCount + 1  
  return queue
