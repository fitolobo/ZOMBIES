import numpy as np
import matplotlib.pyplot as plt


def discrete_lotka_volterra(
    L,
    Z,
    alpha,
    beta,
    rho,
    gamma,
    delta,
    dt,
    time_step,
    vaccine_period=50,
    zombie_removal_ratio=0.1,
):
    """
    Discrete-time version of the Lotka-Volterra model with periodic zombie removal.
    Uses Euler method to discretize the continuous equations.

    A fraction of the zombie population is removed periodically to simulate a vaccine or control effort.
    """
    exogenous_zombie_remover = 0
    if time_step % vaccine_period == 0 and time_step > 0:
        exogenous_zombie_remover = zombie_removal_ratio * Z

    dL = ((alpha - beta) * L - gamma * L * Z) * dt
    new_L = L + dL

    dZ = (rho * beta * L + (gamma - delta) * L * Z) * dt - exogenous_zombie_remover
    new_Z = Z + dZ

    return max(0, new_L), max(0, new_Z)


# Parameter sets
param_sets = [
    {
        "name": "Set 1",
        "alpha": 0.145,
        "beta": 0.1,
        "rho": 0.1,
        "gamma": 0.5,
        "delta": 0.6,
        "L0": 9,
        "Z0": 1,
    },
    {
        "name": "Set 2",
        "alpha": 0.145,
        "beta": 0.1,
        "rho": 0.1,
        "gamma": 0.005,
        "delta": 0.006,
        "L0": 70,
        "Z0": 20,
    },
]

# Simulation parameters
dt = 0.1
time_steps = 1000
time = np.arange(0, time_steps * dt, dt)

# Vaccine (zombie removal) parameters
vaccine_period = 20
zombie_removal_ratio = 0.1  # 10% of Z removed periodically

plt.figure(figsize=(12, 10))

for i, params in enumerate(param_sets):
    L_values = np.zeros(time_steps)
    Z_values = np.zeros(time_steps)

    L_values[0] = params["L0"]
    Z_values[0] = params["Z0"]

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
            t,
            vaccine_period,
            zombie_removal_ratio,
        )

    # Plot time series for populations
    plt.subplot(2, 2, i * 2 + 1)
    plt.plot(time, L_values, "b-", label="L (prey)")
    plt.plot(time, Z_values, "r-", label="Z (zombies)")
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.title(f"Zombie Removal - Set {i+1}: L0={params['L0']}, Z0={params['Z0']}")
    plt.legend()
    plt.grid(True)

    # Run original model (no zombie removal)
    L_orig = np.zeros(time_steps)
    Z_orig = np.zeros(time_steps)
    L_orig[0] = params["L0"]
    Z_orig[0] = params["Z0"]

    for t in range(1, time_steps):
        L_orig[t], Z_orig[t] = discrete_lotka_volterra(
            L_orig[t - 1],
            Z_orig[t - 1],
            params["alpha"],
            params["beta"],
            params["rho"],
            params["gamma"],
            params["delta"],
            dt,
            t,
            999999,  # No removal
            0,
        )

    plt.subplot(2, 2, i * 2 + 2)
    plt.plot(time, L_values, "b-", label="L (with removal)")
    plt.plot(time, Z_values, "r-", label="Z (with removal)")
    plt.plot(time, L_orig, "b--", label="L (no removal)")
    plt.plot(time, Z_orig, "r--", label="Z (no removal)")
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.title(f"Comparison - Set {i+1}")
    plt.legend()
    plt.grid(True)

plt.tight_layout()

# Save the figure using script name
import os
filename = os.path.basename(__file__).split(".")[0]
plt.savefig(f"./results/{filename}.png")
plt.show()

print(f"Simulation complete. Results saved as './results/{filename}.png'")
