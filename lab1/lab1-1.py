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

signalAT = signalGenerator.createSignalAT(
  HARMONICS,
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
fig.savefig('graphs/lab1-1.png')

plt.figure()
plt.plot(signalAT, linewidth='0.75')
plt.title('Additional task')
plt.xlabel('time')
plt.ylabel('generated signal')
plt.savefig('graphs/additionalTask(1-1).png')
plt.show()
