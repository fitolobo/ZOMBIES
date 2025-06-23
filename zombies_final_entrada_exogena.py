import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Parámetros fijos (condiciones de coexistencia)
alpha = 0.033
beta = 0.009
beta_CZ = 0.009
epsilon_CZ = 0.006
beta_MZ = 0.0009
gamma_MZ = 0.022
E = 0.0015
rho = 0.009
params = [alpha, beta, beta_CZ, epsilon_CZ, beta_MZ, gamma_MZ, E, rho]

# Condiciones iniciales
C0, Z0, M0, D0 = 48, 2, 50, 0
init_discrete = np.array([C0, Z0, M0, D0])
init_continuous = [C0, Z0, M0, D0]

# Tiempo
t_max = 1500
t = np.arange(0, t_max + 1)

# ---------- Pulsos exógenos ----------
def military_pulse(t, magnitude=10, interval=300):
    """Simula una entrada tipo delta de Dirac como pulso discreto periódico."""
    return magnitude if t % interval == 0 and t > 0 else 0

# ---------- Modelo discreto ----------
def simulate_discrete(params):
    alpha, beta, beta_CZ, epsilon_CZ, beta_MZ, gamma_MZ, E, rho = params
    C, Z, M, D = init_discrete.copy()
    result = [[C, Z, M, D]]
    for step in range(1, t_max + 1):
        pulse = military_pulse(step)
        Ct1 = C + (alpha - beta - E) * C - beta_CZ * C * Z
        Zt1 = Z + (beta_CZ - epsilon_CZ) * C * Z + rho * beta * (C + M) + (beta_MZ - gamma_MZ) * Z * M
        Mt1 = M + E * C - beta * M - beta_MZ * Z * M + pulse  # <- entrada exógena
        Dt1 = D + (1 - rho) * beta * (C + M) + epsilon_CZ * C * Z + gamma_MZ * Z * M
        if any(x < 0 for x in [Ct1, Zt1, Mt1, Dt1]):
            print("Invalid set of parameters: negative population in discrete model.")
            return None
        C, Z, M, D = Ct1, Zt1, Mt1, Dt1
        result.append([C, Z, M, D])
    return np.array(result)

# ---------- Modelo continuo ----------
def continuous_model(t, y, params):
    C, Z, M, D = y
    alpha, beta, beta_CZ, epsilon_CZ, beta_MZ, gamma_MZ, E, rho = params
    pulse = military_pulse(int(t))  # Discreto dentro del continuo
    dC = (alpha - beta - E) * C - beta_CZ * C * Z
    dZ = (beta_CZ - epsilon_CZ) * C * Z + rho * beta * (C + M) + (beta_MZ - gamma_MZ) * Z * M
    dM = E * C - beta * M - beta_MZ * Z * M + pulse
    dD = (1 - rho) * beta * (C + M) + epsilon_CZ * C * Z + gamma_MZ * Z * M
    return [dC, dZ, dM, dD]

# ---------- Ejecutar modelo discreto ----------
res_discrete = simulate_discrete(params)
if res_discrete is None:
    exit()

# ---------- Ejecutar modelo continuo ----------
sol_continuous = solve_ivp(
    fun=lambda t, y: continuous_model(t, y, params),
    t_span=(0, t_max),
    y0=init_continuous,
    t_eval=t
)

if np.any(sol_continuous.y < 0):
    print("Invalid set of parameters: negative population in continuous model.")
    exit()

# ---------- Imprimir resultados ----------
labels = ["Civiles", "Zombies", "Militares", "Muertos"]
print("Resultados finales del modelo discreto:")
for i, label in enumerate(labels):
    print(f"{label}: {res_discrete[-1, i]:.2f}")

print("\nResultados finales del modelo continuo:")
for i, label in enumerate(labels):
    print(f"{label}: {sol_continuous.y[i, -1]:.2f}")

# ---------- Graficar modelo discreto ----------
plt.figure(figsize=(10, 5))
for i, label in enumerate(labels):
    plt.plot(t, res_discrete[:, i], label=label)
plt.title("Modelo Discreto con Pulsos Militares")
plt.xlabel("Tiempo")
plt.ylabel("Población")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ---------- Graficar modelo continuo ----------
plt.figure(figsize=(10, 5))
for i, label in enumerate(labels):
    plt.plot(t, sol_continuous.y[i], label=label)
plt.title("Modelo Continuo con Pulsos Militares")
plt.xlabel("Tiempo")
plt.ylabel("Población")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
