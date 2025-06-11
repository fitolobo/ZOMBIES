import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def lotka_volterra(t, y, alpha, beta, rho, gamma, delta):
    L, Z = y
    dLdt = (alpha - beta) * L - gamma * L * Z
    dZdt = rho * beta * L + (gamma - delta) * L * Z
    return [dLdt, dZdt]


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

# Time span for simulation
t_span = (0, 100)
t_eval = np.linspace(0, 100, 100)

plt.figure(figsize=(12, 8))

for i, params in enumerate(param_sets):
    # Solve the differential equations
    solution = solve_ivp(
        lotka_volterra,
        t_span,
        [params["L0"], params["Z0"]],
        args=(
            params["alpha"],
            params["beta"],
            params["rho"],
            params["gamma"],
            params["delta"],
        ),
        t_eval=t_eval,
    )

    # Plot time series
    plt.subplot(2, 1, i + 1)
    plt.plot(solution.t, solution.y[0], "b-", label="L (prey)")
    plt.plot(solution.t, solution.y[1], "r-", label="Z (predator)")
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.title(f"Parameter Set {i+1}: Initial L={params['L0']}, Z={params['Z0']}")
    plt.legend()
    plt.grid(True)

plt.tight_layout()
# Get filename without extension
filename = __file__.split("/")[-1].split(".")[0]
# Save the figure with the same name as the Python file
plt.savefig(f"./results/{filename}.png")
plt.show()

print(f"Simulation complete. Results saved as './results/{filename}.png'")
