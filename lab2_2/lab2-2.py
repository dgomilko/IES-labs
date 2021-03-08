import matplotlib.pyplot as plt
from fft import fastFourierTransformRecursion, fastFourierTransformLoop
from complexity import getComplexity
import sys
sys.path.append('../')
from lab1.signalGenerator import createSignal

HARMONICS = 12
MAX_FREQUENCY = 2400
DISCRETE_CALLS = 1024
COMPLEXITY_COUNT_LOOPS = 22

toRealNum = lambda x: list(map(lambda a: abs(a), x)) 

signal = createSignal(
  HARMONICS,
  MAX_FREQUENCY,
  DISCRETE_CALLS
)
spectre = toRealNum(fastFourierTransformRecursion(signal))
spectreAT = toRealNum(fastFourierTransformLoop(signal))

size, elapsedFFT = getComplexity(
  COMPLEXITY_COUNT_LOOPS,
  HARMONICS,
  MAX_FREQUENCY,
  "FFT"
)

fig, axs = plt.subplots(3, 1)
plt.subplots_adjust(left=0.05, top=0.94, bottom=0.05, right=0.97, hspace=0.25)
fig.suptitle('Lab 2.2')

axs[0].plot(signal, color='r', linewidth=0.8)
axs[0].set_title('Generated signal')
axs[0].set(xlabel='time', ylabel='signal')

axs[1].plot(spectre, linewidth=0.8)
axs[1].set_title('Fast Fourier transform')
axs[1].set(xlabel='p', ylabel='F(p)')

axs[2].plot(size, elapsedFFT, color='b')
axs[2].set_title('FFT Complexity')
axs[2].set(xlabel='signal size', ylabel='time')
fig.savefig('graphs/lab2-2.png')

fig, axs = plt.subplots(2, 1)
plt.subplots_adjust(left=0.05, top=0.94, bottom=0.05, right=0.97, hspace=0.25)
fig.suptitle('Additional task')

axs[0].plot(signal, color='r', linewidth=0.8)
axs[0].set_title('Generated signal')
axs[0].set(xlabel='time', ylabel='signal')

axs[1].plot(spectreAT, color='r', linewidth=0.8)
axs[1].set_title('FFT')
axs[1].set(xlabel='p', ylabel='F(p)')

fig.savefig('graphs/additionalTask.png')
plt.show()