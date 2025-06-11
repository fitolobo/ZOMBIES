import numpy as np
import matplotlib.pyplot as plt


# APPROACH
# Modifying the gamma introducing "effective gamma"
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
    vaccine_period=10,
    vaccine_efficacy=0.5,
):
    """
    Discrete-time version of the Lotka-Volterra model with periodic vaccine intervention.
    Uses Euler method to discretize the continuous equations.

    The vaccine is modeled as a periodic dirac delta that reduces the gamma factor
    (which represents infection due to contact with Z population).
    """
    # Apply vaccine effect (reduce gamma) if current time step is a multiple of vaccine_period
    effective_gamma = gamma
    if time_step % vaccine_period == 0 and time_step > 0:
        effective_gamma = gamma * (
            1 - vaccine_efficacy
        )  # Reduce gamma by vaccine_efficacy %

    # Update for L (prey)
    dL = ((alpha - beta) * L - effective_gamma * L * Z) * dt
    new_L = L + dL

    # Update for Z (predator)
    dZ = (rho * beta * L + (effective_gamma - delta) * L * Z) * dt
    new_Z = Z + dZ

    return max(0, new_L), max(0, new_Z)  # Ensure populations don't go negative


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
dt = 0.1  # Time step
time_steps = 1000  # Number of time steps
time = np.arange(0, time_steps * dt, dt)  # Time array

# Vaccine parameters
vaccine_period = 10  # Apply vaccine every 10 time steps
vaccine_efficacy = 0.5  # 50% reduction in gamma when vaccine is applied

plt.figure(figsize=(15, 12))

for i, params in enumerate(param_sets):
    # Initialize arrays to store population values
    L_values = np.zeros(time_steps)
    Z_values = np.zeros(time_steps)
    gamma_effective = np.zeros(time_steps)  # Track effective gamma values

    # Set initial conditions
    L_values[0] = params["L0"]
    Z_values[0] = params["Z0"]
    gamma_effective[0] = params["gamma"]

    # Run discrete simulation
    for t in range(1, time_steps):
        # Determine if vaccine is active at this time step
        is_vaccine_time = t % vaccine_period == 0
        effective_gamma = params["gamma"] * (
            1 - vaccine_efficacy if is_vaccine_time else 1
        )
        gamma_effective[t] = effective_gamma

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
            vaccine_efficacy,
        )

    # Plot time series for populations
    plt.subplot(3, 2, i * 3 + 1)
    plt.plot(time, L_values, "b-", label="L (prey)")
    plt.plot(time, Z_values, "r-", label="Z (predator)")
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.title(f"Vaccine Model - Set {i+1}: Initial L={params['L0']}, Z={params['Z0']}")
    plt.legend()
    plt.grid(True)

    # Plot the effective gamma values to show vaccine timing
    plt.subplot(3, 2, i * 3 + 2)
    plt.plot(time, gamma_effective, "g-")
    plt.xlabel("Time")
    plt.ylabel("Effective γ")
    plt.title(f"Vaccine Effect (γ reduction) - Set {i+1}")
    plt.grid(True)

    # Compare with original model (without vaccine)
    plt.subplot(3, 2, i * 3 + 3)

    # Run original model for comparison
    L_original = np.zeros(time_steps)
    Z_original = np.zeros(time_steps)
    L_original[0] = params["L0"]
    Z_original[0] = params["Z0"]

    for t in range(1, time_steps):
        L_original[t], Z_original[t] = discrete_lotka_volterra(
            L_original[t - 1],
            Z_original[t - 1],
            params["alpha"],
            params["beta"],
            params["rho"],
            params["gamma"],
            params["delta"],
            dt,
            t,
            999999,
            0,  # No vaccine (using large period)
        )

    plt.plot(time, L_values, "b-", label="L (with vaccine)")
    plt.plot(time, Z_values, "r-", label="Z (with vaccine)")
    plt.plot(time, L_original, "b--", label="L (no vaccine)")
    plt.plot(time, Z_original, "r--", label="Z (no vaccine)")
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.title(f"Comparison - Set {i+1}")
    plt.legend()
    plt.grid(True)

plt.tight_layout()
# Get filename without extension
filename = __file__.split("/")[-1].split(".")[0]
# Save the figure with the same name as the Python file
plt.savefig(f"./results/{filename}.png")
plt.show()

print(f"Simulation complete. Results saved as './results/{filename}.png'")
