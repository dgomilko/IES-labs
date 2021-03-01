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
spectre = discreteFourierTransform(signal)
lens, elapsed = getDFTComplexity(
  COMPLEXITY_COUNT_LOOPS,
  HARMONICS,
  MAX_FREQUENCY
) 

fig, axs = plt.subplots(3, 1)
plt.subplots_adjust(left=0.05, top=0.94, bottom=0.05, right=0.97, hspace=0.25)
fig.suptitle('Lab 2.1')

axs[0].plot(signal, linewidth=0.8)
axs[0].set_title('Generated signal')
axs[0].set(xlabel='time', ylabel='generated signal')

axs[1].plot(spectre, color='r', linewidth=0.8)
axs[1].set_title('Discrete Fourier transform')
axs[1].set(xlabel='p', ylabel='F(p)')

axs[2].plot(lens, elapsed, color='g')
axs[2].set_title('DFT complexity')
axs[2].set(xlabel='time', ylabel='signal size')

plt.show()
fig.savefig('graphs/lab1-2.png')