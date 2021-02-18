import matplotlib.pyplot as plt
import signalGenerator
import calc
import complexity

HARMONICS = 12
MAX_FREQUENCY = 2400
DISCRETE_CALLS = 1024
COMPLEXITY_COUNT_LOOPS = 200

signalX = signalGenerator.createSignal(
  HARMONICS,
  MAX_FREQUENCY,
  DISCRETE_CALLS
)
signalY = signalGenerator.createSignal(
  HARMONICS,
  MAX_FREQUENCY,
  DISCRETE_CALLS
)
autocorrelation = calc.correlation(signalX)
correlation = calc.correlation(signalX, signalY)

harmonics, time = complexity.getCorrealtionComplexity(
  COMPLEXITY_COUNT_LOOPS,
  MAX_FREQUENCY,
  DISCRETE_CALLS
)

len = int(DISCRETE_CALLS / 2)
correlationRange = list(range(len))

fig, axs = plt.subplots(2, 2)
plt.subplots_adjust(left=0.05, bottom=0.1, right=0.97, wspace=0.1)
fig.suptitle('Lab 1.2')

axs[0, 0].plot(signalX, color='r', linewidth=0.75, label='signal X')
axs[0, 0].plot(signalY, color='g', linewidth=0.75, label = 'signal Y')
axs[0, 0].set_title('Generated signals')
axs[0, 0].set(xlabel='time', ylabel='generated signal')
axs[0, 0].legend()

axs[0, 1].plot(correlationRange, autocorrelation, color='r', linewidth=0.8)
axs[0, 1].set_title('Autocorrelation (signal X)')
axs[0, 1].set(xlabel='t', ylabel='correlation')

axs[1, 0].plot(correlationRange, correlation, linewidth=0.8)
axs[1, 0].set_title('Cross-correlation')
axs[1, 0].set(xlabel='t', ylabel='correlation')

axs[1, 1].plot(harmonics, time)
axs[1, 1].set_title('Correlation calculation complexity')
axs[1, 1].set(xlabel='n', ylabel='elapsed time (seconds)')

plt.show()
fig.savefig('graphs/lab1-2.png')