from fft import fastFourierTransformRecursion
import time
import sys
sys.path.append('../')
from lab1.signalGenerator import createSignal
from lab2_1.dft import discreteFourierTransform

def getComplexity(stepsCount, harmonics, maxFrequency, type):
  elapsed = []
  size = []
  for i in range(stepsCount):
    count = int(2 ** (i + 1))
    size.append(count)
    signal = createSignal(harmonics, maxFrequency, count)
    start = time.perf_counter()
    if (type == "DFT"):
      discreteFourierTransform(signal, "list")
    else:
      fastFourierTransformRecursion(signal)
    stop = time.perf_counter()
    elapsed.append(stop - start)
  return size, elapsed