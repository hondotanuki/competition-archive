import matplotlib.pyplot as plt
import numpy as np

# Parameters
Tmax = 10
Tmin = 0.2
nsteps = 100000
Tfactor = -np.log(Tmax / Tmin)  # Exponential cooling factor

# Generate steps
steps = np.arange(1, nsteps + 1)

# Exponential cooling
temperatures_exp = Tmax * np.exp(Tfactor * steps / nsteps)

# Logarithmic cooling (adding a small offset to avoid division by zero)
temperatures_log = Tmax / np.log10(steps + 10)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(steps, temperatures_exp, label="Exponential Cooling", linewidth=2)
plt.plot(
    steps, temperatures_log, label="Logarithmic Cooling", linewidth=2, linestyle="--"
)
plt.xlabel("Steps", fontsize=14)
plt.ylabel("Temperature", fontsize=14)
plt.title("Cooling Schedules: Exponential vs Logarithmic", fontsize=16)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()
