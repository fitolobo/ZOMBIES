import numpy as np
import matplotlib.pyplot as plt

# Parámetros del modelo
alpha = 1.0
beta = 0.3
beta_CZ = 0.02
epsilon_CZ = 0.005
beta_MZ = 0.015
gamma_MZ = 0.025
E = 0.2
rho = 0.1

# Variables fijas
M_fixed = 10
Z_fixed = 10
C_fixed = 100

# Crear figura con 3 subplots para cada combinación
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# -------------------------------
# Plano (C, Z) con M fijo
# -------------------------------
C_vals = np.linspace(0, 1000, 20)
Z_vals = np.linspace(0, 1000, 20)
C, Z = np.meshgrid(C_vals, Z_vals)

dCdt = (alpha - beta - E) * C - beta_CZ * C * Z
dZdt = (beta_CZ - epsilon_CZ) * C * Z + rho * beta * (C + M_fixed) + (beta_MZ - gamma_MZ) * Z * M_fixed

axes[0].streamplot(C, Z, dCdt, dZdt, color='gray')
axes[0].set_title("Plano (C, Z) con M fijo")
axes[0].set_xlabel("Civiles (C)")
axes[0].set_ylabel("Zombis (Z)")

# -------------------------------
# Plano (C, M) con Z fijo
# -------------------------------
C_vals = np.linspace(0, 1000, 20)
M_vals = np.linspace(0, 1000, 20)
C, M = np.meshgrid(C_vals, M_vals)

dCdt = (alpha - beta - E) * C - beta_CZ * C * Z_fixed
dMdt = E * C - beta * M - beta_MZ * Z_fixed * M

axes[1].streamplot(C, M, dCdt, dMdt, color='gray')
axes[1].set_title("Plano (C, M) con Z fijo")
axes[1].set_xlabel("Civiles (C)")
axes[1].set_ylabel("Militares (M)")

# -------------------------------
# Plano (Z, M) con C fijo
# -------------------------------
Z_vals = np.linspace(0, 1000, 20)
M_vals = np.linspace(0, 1000, 20)
Z, M = np.meshgrid(Z_vals, M_vals)

dZdt = (beta_CZ - epsilon_CZ) * C_fixed * Z + rho * beta * (C_fixed + M) + (beta_MZ - gamma_MZ) * Z * M
dMdt = E * C_fixed - beta * M - beta_MZ * Z * M

axes[2].streamplot(Z, M, dZdt, dMdt, color='gray')
axes[2].set_title("Plano (Z, M) con C fijo")
axes[2].set_xlabel("Zombis (Z)")
axes[2].set_ylabel("Militares (M)")

# -------------------------------
# Mostrar
# -------------------------------
plt.tight_layout()
plt.show()
