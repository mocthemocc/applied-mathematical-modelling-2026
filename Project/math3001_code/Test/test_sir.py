import numpy as np
import matplotlib.pyplot as plt

# Basic SIR model, solved with RK4 to sanity-check the environment
beta = 0.5   # infection rate
gamma = 0.05  # recovery rate
N = 100000    # total population

def sir_deriv(y):
    S, I, R = y
    dS = -beta * S * I / N
    dI = beta * S * I / N - gamma * I
    dR = gamma * I
    return np.array([dS, dI, dR])

def rk4_step(y, h):
    k1 = sir_deriv(y)
    k2 = sir_deriv(y + h / 2 * k1)
    k3 = sir_deriv(y + h / 2 * k2)
    k4 = sir_deriv(y + h * k3)
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

t0, t_end, h = 0, 365, 0.5
steps = int((t_end - t0) / h)
y = np.array([N - 1, 1, 0], dtype=float)

t_vals = np.zeros(steps + 1)
y_vals = np.zeros((steps + 1, 3))
y_vals[0] = y

for i in range(steps):
    y = rk4_step(y, h)
    t_vals[i + 1] = t_vals[i] + h
    y_vals[i + 1] = y

plt.plot(t_vals, y_vals[:, 0], label="Susceptible")
plt.plot(t_vals, y_vals[:, 1], label="Infected")
plt.plot(t_vals, y_vals[:, 2], label="Recovered")
plt.xlabel("Time (days)")
plt.ylabel("Population")
plt.title("SIR Model Test")
plt.legend()
plt.savefig("sir_test_output.png")
print("Peak infected:", round(y_vals[:, 1].max()))
print("Test complete - environment working.")
