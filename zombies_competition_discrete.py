import numpy as np
import matplotlib.pyplot as plt


def discrete_lotka_volterra(L, Z, alpha, beta, rho, gamma, delta, dt):
    """
    Discrete-time version of the Lotka-Volterra model.
    Uses Euler method to discretize the continuous equations.
    """
    # Update for L (prey)
    dL = ((alpha - beta) * L - gamma * L * Z) * dt
    new_L = L + dL

    # Update for Z (predator)
    dZ = (rho * beta * L + (gamma - delta) * L * Z) * dt
    new_Z = Z + dZ

    return max(0, new_L), max(0, new_Z)  # Ensure populations don't go negative


# Parameter sets
param_sets = [
    {
        "name": "Set 1",
        "alpha": 0.15,
        "beta": 0.1,
        "rho": 0.1,
        "gamma": 0.5,
        "delta": 0.6,
        "L0": 9,
        "Z0": 1,
    },
    {
        "name": "Set 2",
        "alpha": 0.15,
        "beta": 0.1,
        "rho": 0.1,
        "gamma": 0.005,
        "delta": 0.006,
        "L0": 70,
        "Z0": 20,
    },
]

# Simulation parameters
dt = 0.1  # Time step
time_steps = 1000  # Number of time steps
time = np.arange(0, time_steps * dt, dt)  # Time array

plt.figure(figsize=(12, 8))

for i, params in enumerate(param_sets):
    # Initialize arrays to store population values
    L_values = np.zeros(time_steps)
    Z_values = np.zeros(time_steps)

    # Set initial conditions
    L_values[0] = params["L0"]
    Z_values[0] = params["Z0"]

    # Run discrete simulation
    for t in range(1, time_steps):
        L_values[t], Z_values[t] = discrete_lotka_volterra(
            L_values[t - 1],
            Z_values[t - 1],
            params["alpha"],
            params["beta"],
            params["rho"],
            params["gamma"],
            params["delta"],
            dt,
        )

    # Plot time series
    plt.subplot(2, 1, i + 1)
    plt.plot(time, L_values, "b-", label="L (prey)")
    plt.plot(time, Z_values, "r-", label="Z (predator)")
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.title(f"Discrete Model - Set {i+1}: Initial L={params['L0']}, Z={params['Z0']}")
    plt.legend()
    plt.grid(True)

plt.tight_layout()
# Get filename without extension
filename = __file__.split("/")[-1].split(".")[0]
# Save the figure with the same name as the Python file
plt.savefig(f"./results/{filename}.png")
plt.show()

print(f"Simulation complete. Results saved as '{filename}.png'")
