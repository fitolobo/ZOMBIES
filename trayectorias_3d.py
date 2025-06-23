import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parámetros del modelo
alpha = 1.0
beta = 0.3
beta_CZ = 0.02
epsilon_CZ = 0.005
beta_MZ = 0.015
gamma_MZ = 0.025
E = 0.2
rho = 0.1
M_fixed = 10  # valor fijo de M

# Definimos el campo vectorial para C y Z
C_vals = np.linspace(0, 1000, 150)
Z_vals = np.linspace(0, 1000, 150)
C, Z = np.meshgrid(C_vals, Z_vals)

# Ecuaciones en plano (C, Z), M = constante
dCdt = (alpha - beta - E) * C - beta_CZ * C * Z
dZdt = (beta_CZ - epsilon_CZ) * C * Z + rho * beta * (C + M_fixed) + (beta_MZ - gamma_MZ) * Z * M_fixed

# Definimos el sistema
def model(t, y):
    C, Z, M = y
    dCdt = (alpha - beta - E) * C - beta_CZ * C * Z
    dZdt = (beta_CZ - epsilon_CZ) * C * Z + rho * beta * (C + M) + (beta_MZ - gamma_MZ) * Z * M
    dMdt = E * C - beta * M - beta_MZ * Z * M
    return [dCdt, dZdt, dMdt]

# Trayectorias desde varias condiciones iniciales
init_conditions = [
    [10, 5, 2],
    [40, 20, 10],
    [80, 40, 5],
    [60, 10, 30]
]

t_span = (0, 1000)
t_eval = np.linspace(*t_span, 1000)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

for init in init_conditions:
    sol = solve_ivp(model, t_span, init, t_eval=t_eval)
    ax.plot(sol.y[0], sol.y[1], sol.y[2], label=f'C0={init[0]}, Z0={init[1]}, M0={init[2]}')

ax.set_xlabel('C')
ax.set_ylabel('Z')
ax.set_zlabel('M')
ax.set_title("Trayectorias en el espacio de estados (C, Z, M)")
ax.legend()
plt.show()
