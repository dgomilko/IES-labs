mean = lambda vals: sum(vals) / len(vals)

def variance(vals):
  M = mean(vals)
  N = len(vals)
  return sum((x - M) ** 2 for x in vals) / (N - 1)

def correlation(signalX, signalY = []):
  N = len(signalX)
  calcRange = N / 2
  Mx = mean(signalX)
  My = mean(signalY) if signalY else Mx
  comparedSignal = signalY or signalX
  correlation = []
  for tau in range(int(calcRange)):
    res = 0
    for t in range(int(calcRange)):
      res += (signalX[t] - Mx) * (comparedSignal[t + tau] - My)
    correlation.append(res / (calcRange - 1))
  return correlation