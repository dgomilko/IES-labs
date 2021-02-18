import matplotlib.pyplot as plt
import signalGenerator
import calc
import complexity

HARMONICS = 12
MAX_FREQUENCY = 2400
DISCRETE_CALLS = 1024
COMPLEXITY_COUNT_LOOPS = 200

signal = signalGenerator.createSignal(
  HARMONICS,
  MAX_FREQUENCY,
  DISCRETE_CALLS
)

mean = calc.mean(signal)
variance = calc.variance(signal)
print('Mean: ', mean)
print('Variance: ', variance)

harmonics, time = complexity.getGenerationComplexity(
  COMPLEXITY_COUNT_LOOPS,
  MAX_FREQUENCY,
  DISCRETE_CALLS
)

fig, axs = plt.subplots(2)
fig.suptitle('Lab 1.1')

axs[0].plot(signal)
axs[0].axhline(y=mean, color='r')
axs[0].set_title('Generated signal and average value')
axs[0].set(xlabel='time', ylabel='generated signal')

axs[1].plot(harmonics, time)
axs[1].set_title('Signal generation complexity')
axs[1].set(xlabel='n', ylabel='elapsed time (seconds)')

plt.show()
fig.savefig('graphs/lab1-1.png')
