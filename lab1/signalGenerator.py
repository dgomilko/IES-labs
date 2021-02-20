import random
import math

def createSignal(harmonics, maxFrequency, calls):
  sumsArr = [0] * calls
  frequencyStep = maxFrequency / harmonics
  for i in range(harmonics):
    frequency = frequencyStep * (i + 1)
    amplitude = random.random()
    phase = random.random()
    for t in range(calls):
      sumsArr[t] += amplitude * math.sin(frequency * t + phase)
  return sumsArr

def createSignalAT(harmonics, maxFrequency, calls):
  sumsArr = [0] * calls
  frequencyStep = maxFrequency / harmonics
  for i in range(harmonics):
    frequency = frequencyStep * (i + 1)
    for t in range(calls):
      amplitude = random.random()
      phase = random.random()
      sumsArr[t] += amplitude * math.sin(frequency * t + phase)
  return sumsArr