from dft import discreteFourierTransform
import time
import sys
sys.path.append('../')
from lab1.signalGenerator import createSignal

def getDFTComplexity(stepsCount, harmonics, maxFrequency, dataType):
  elapsed = []
  size = []
  for i in range(stepsCount):
    count = int(10 * (i + 1))
    size.append(count)
    signal = createSignal(harmonics, maxFrequency, count)
    start = time.perf_counter()
    discreteFourierTransform(signal, dataType)
    stop = time.perf_counter()
    elapsed.append(stop - start)
  average = sum(elapsed)/stepsCount
  return size, elapsed, average