# Collapse Rho(x) - 精确拟合 + 共振可视化
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# === 1. 目标设置 ===
x_values = np.linspace(10, 200, 1000)
target_rho = 1 / np.log(x_values)

# === 2. 加载前 N 个 Riemann 零点 γ_n ===
gamma_list = np.array([
    14.134725, 21.022040, 25.010858, 30.424876, 32.935061,
    37.586178, 40.918719, 43.327073, 48.005150, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831780, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704690, 77.144840
])
N = len(gamma_list)

# === 3. 定义 rho(x) 模型 ===
def rho_model(x, A, theta):
    terms = [A[i] * np.cos(gamma_list[i] * np.log(x) + theta[i]) for i in range(N)]
    return 1 / np.log(x) + np.sum(terms, axis=0)

# === 4. 定义损失函数 ===
def loss(params):
    A = params[:N]
    theta = params[N:]
    rho_pred = np.array([rho_model(x, A, theta) for x in x_values])
    return np.mean((rho_pred - target_rho) ** 2)

# === 5. 初始化参数并优化 ===
np.random.seed(42)
A0 = np.ones(N) * 0.1
theta0 = np.random.uniform(-np.pi, np.pi, N)
params0 = np.concatenate([A0, theta0])

result = minimize(loss, params0, method='L-BFGS-B', options={'maxiter': 1000})
A_opt = result.x[:N]
theta_opt = result.x[N:]
rho_fit = np.array([rho_model(x, A_opt, theta_opt) for x in x_values])

# === 6. 可视化 ===
plt.figure(figsize=(10, 5))
plt.plot(x_values, target_rho, label='1 / log(x)', color='black', linestyle='--')
plt.plot(x_values, rho_fit, label='Collapse Rho(x) Fit', color='blue')
plt.title("Collapse Rho(x) Approximation vs 1/log(x)")
plt.xlabel("x")
plt.ylabel("ρ(x)")
plt.legend()
plt.grid(True)
plt.show()

# === 7. 输出误差和参数 ===
print(f"\n✅ 最终 MSE 误差: {loss(result.x):.30f}")
print("\nA_n =", np.round(A_opt, 8))
print("\nθ_n =", np.round(theta_opt, 8))

