# ⬛️ 高精度 SEA-G 零点干涉拟合框架 (Colab 版)

## ✅ 功能：拟合 φ(x) ≈ ∑ Aₙ cos(γₙ log x + θₙ) 并最小化误差

!pip install mpmath numpy scipy

import numpy as np
from mpmath import zetazero, mp
from scipy.optimize import minimize

# 设置精度
mp.dps = 50

# 获取前 N 个黎曼非平凡零点 γₙ
def get_riemann_zeros(N):
    return np.array([float(zetazero(n).imag) for n in range(1, N+1)])

# 定义 φ(x) = 1 / sqrt(x)
def phi_target(x):
    return 1 / np.sqrt(x)

# 构造结构 φ̂(x) = ∑ Aₙ cos(γₙ log x + θₙ)
def phi_reconstruct(x, A, theta, gamma):
    return np.sum(A * np.cos(gamma * np.log(x) + theta))

# 构造优化目标函数：误差平方
def loss(params, x, gamma):
    N = len(gamma)
    A = params[:N]
    theta = params[N:]
    y_pred = phi_reconstruct(x, A, theta, gamma)
    y_true = phi_target(x)
    return (y_pred - y_true) ** 2

# 主执行函数
def run_fit(x_val=100, N_zeros=50):
    gamma = get_riemann_zeros(N_zeros)
    A0 = np.ones(N_zeros) * 0.1
    theta0 = np.random.uniform(-np.pi, np.pi, N_zeros)
    init_params = np.concatenate([A0, theta0])

    result = minimize(loss, init_params, args=(x_val, gamma), method='L-BFGS-B')
    N = N_zeros
    A_fit = result.x[:N]
    theta_fit = result.x[N:]
    final_error = loss(result.x, x_val, gamma)

    print(f"✅ 最终误差: {final_error:.50f}")
    print("\nA_n =", np.round(A_fit, 8).tolist())
    print("\ntheta_n =", np.round(theta_fit, 8).tolist())

# 示例运行
run_fit(x_val=100, N_zeros=50)
