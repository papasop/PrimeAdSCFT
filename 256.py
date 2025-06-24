# === 安装依赖（仅第一次运行时需要） ===
!pip install mpmath

# === 引入必要库 ===
import numpy as np
import matplotlib.pyplot as plt
from mpmath import zetazero, mp, cos, log, pi
from scipy.optimize import minimize

# === 设置高精度（50 位小数）===
mp.dps = 50  # decimal places

# === 生成前 N 个 Riemann 零点（虚部）===
def get_riemann_zeros(n):
    return np.array([float(zetazero(i).imag) for i in range(1, n + 1)])

# === φ(x) 目标函数 ===
def phi(x, A, theta, gamma):
    return sum(A[i] * float(cos(gamma[i] * log(x) + theta[i])) for i in range(len(A)))

# === 损失函数（最小化 φ(x) 与目标值之间的误差）===
def loss(params, x_target, y_target, gamma, lambda_reg):
    n = len(gamma)
    A = params[:n]
    theta = params[n:]
    y_pred = phi(x_target, A, theta, gamma)
    error = (y_pred - y_target) ** 2
    reg = lambda_reg * np.sum(A**2)
    return float(error + reg)

# === 参数设置 ===
x_target = 100              # 拟合目标点 φ(x_target)
y_target = 0.0              # 假设目标值为 0（可改为其他）
lambda_reg = 1e-6           # 正则化参数
errors = []
N_values = list(range(1, 21))  # 零点数量 1 ~ 20

# === 主循环：不断增加零点数量进行测试 ===
for N in N_values:
    gamma = get_riemann_zeros(N)
    A0 = np.full(N, 0.1)
    theta0 = np.random.uniform(-np.pi, np.pi, N)
    init_params = np.concatenate([A0, theta0])

    res = minimize(
        loss,
        init_params,
        args=(x_target, y_target, gamma, lambda_reg),
        method='L-BFGS-B'
    )

    final_error = loss(res.x, x_target, y_target, gamma, lambda_reg)
    errors.append(final_error)
    print(f"Iteration {N}: Error = {final_error:.50f}")

# === 绘图展示误差曲线 ===
plt.figure(figsize=(10, 6))
plt.plot(N_values, errors, marker='o')
plt.yscale('log')
plt.xlabel('Number of Zeros (N)')
plt.ylabel('Final Error (log scale)')
plt.title(f'Error vs. Number of Riemann Zeros for φ(x={x_target})')
plt.grid(True)
plt.show()
