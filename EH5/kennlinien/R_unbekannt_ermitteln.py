import numpy as np

data = np.loadtxt('/home/epr/Desktop/einheit5/i(u)_kennlinie_R.csv',skiprows=1, delimiter=',')

I = data[:,0]
U = data[:,1]

R = U.mean() / I.mean()

print(R)