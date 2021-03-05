import matplotlib.pyplot as plt
from dft import discreteFourierTransform
from complexity import getDFTComplexity

import sys
sys.path.append('../')
from lab1.signalGenerator import createSignal

HARMONICS = 12
MAX_FREQUENCY = 2400
DISCRETE_CALLS = 1024
COMPLEXITY_COUNT_LOOPS = 200

signal = createSignal(
  HARMONICS,
  MAX_FREQUENCY,
  DISCRETE_CALLS
)
spectreDict = discreteFourierTransform(signal, "dict")
spectreList = discreteFourierTransform(signal, "list")
lens, elapsedList, avgList = getDFTComplexity(
  COMPLEXITY_COUNT_LOOPS,
  HARMONICS,
  MAX_FREQUENCY,
  "list"
)
_, elapsedDict, avgDict = getDFTComplexity(
  COMPLEXITY_COUNT_LOOPS,
  HARMONICS,
  MAX_FREQUENCY,
  "dict"
)

file = open("timeTest.txt", "w+")
file.write('DFT with list() average time: ' + str(avgList) + '\n' +
  'DFT with dict() average time: ' + str(avgDict))
file.close()

fig, axs = plt.subplots(3, 1)
plt.subplots_adjust(left=0.05, top=0.94, bottom=0.05, right=0.97, hspace=0.25)
fig.suptitle('Lab 2.1')

axs[0].plot(signal, linewidth=0.8)
axs[0].set_title('Generated signal')
axs[0].set(xlabel='time', ylabel='generated signal')

axs[1].plot(spectreList, color='r', linewidth=0.8)
axs[1].set_title('Discrete Fourier transform')
axs[1].set(xlabel='p', ylabel='F(p)')

axs[2].plot(lens, elapsedList, color='g')
axs[2].set_title('DFT complexity')
axs[2].set(xlabel='signal size', ylabel='time')
fig.savefig('graphs/lab2-1.png')

fig, axs = plt.subplots(3, 1)
plt.subplots_adjust(left=0.05, top=0.94, bottom=0.05, right=0.97, hspace=0.25)
fig.suptitle('Additional task')

axs[0].plot(spectreList, linewidth=0.8)
axs[0].set_title('DFT with list()')
axs[0].set(xlabel='o', ylabel='F(p)')

axs[1].plot(spectreDict.values(), color='r', linewidth=0.8)
axs[1].set_title('DFT with dict()')
axs[1].set(xlabel='p', ylabel='F(p)')

axs[2].plot(lens, elapsedList, color='g', label='list()')
axs[2].plot(lens, elapsedDict, color='b', label='dict()')
axs[2].set_title('Complexity comparison')
axs[2].set(xlabel='signal size', ylabel='time')
axs[2].legend()
fig.savefig('graphs/additionalTask.png')
plt.show()
