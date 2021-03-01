import math

def fourierCoefficient(pk, N):
  arg = 2 * math.pi * pk / N
  return complex(math.cos(arg), -math.sin(arg))

def discreteFourierTransform(signal):
  N = len(signal)
  spectre = []
  for p in range(N):
    sum = 0
    for k in range(N):
      x = signal[k]
      w = fourierCoefficient(p*k, N)
      sum += w * x
    spectre.append(abs(sum))
  return spectre