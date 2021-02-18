import time
import signalGenerator
import calc

def getGenerationComplexity(stepsCount, maxFrequency, calls):
  elapsed = []
  harmonics = []
  for i in range(stepsCount):
    count = int(10 * (i + 1))
    harmonics.append(count)
    start = time.perf_counter()
    signalGenerator.createSignal(count, maxFrequency, calls)
    stop = time.perf_counter()
    elapsed.append(stop - start)
  return harmonics, elapsed

def getCorrealtionComplexity(stepsCount, harmonics, maxFrequency):
  elapsed = []
  harmonics = []
  for i in range(stepsCount):
    count = int(10 * (i + 1))
    harmonics.append(count)
    signal = signalGenerator.createSignal(count, maxFrequency, count)
    start = time.perf_counter()
    calc.correlation(signal)
    stop = time.perf_counter()
    elapsed.append(stop - start)
  return harmonics, elapsed