import numpy as np

data = np.loadtxt('/home/epr/Desktop/einheit5/i(u)_kennlinie_LED.csv', skiprows=10, delimiter=',')

I = data[:,0]
U = data[:,1]

coeff = np.polyfit(I,U,deg=1)
m,b = coeff

y_0 = b
print(f'Flussspannung: {b}')

