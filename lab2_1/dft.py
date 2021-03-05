import math

def fourierCoefficient(pk, N):
  arg = 2 * math.pi * pk / N
  return complex(math.cos(arg), -math.sin(arg))

def discreteFourierTransform(signal, dataType):
  N = len(signal)
  spectre = list() if (dataType == "list") else dict()
  for p in range(N):
    sum = 0
    for k in range(N):
      x = signal[k]
      w = fourierCoefficient(p*k, N)
      sum += w * x
    res = abs(sum)
    if (dataType == "list"):
      spectre.append(res)
    else:
      spectre[p] = abs(res)
  return spectre