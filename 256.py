# Collapse Riemann Approximation - High Precision φ(x) Fitting
# Supports expansion via Riemann zeros and nonlinear optimization

import numpy as np
from scipy.optimize import minimize

# === 1. 目标参数设置 ===
x_target = 100           # 你可以替换为任意 x > 0
phi_target = 1 / np.sqrt(x_target)
N_zeros = 50             # 使用前 N 个非平凡零点，可尝试 10 ~ 100+

# === 2. 加载前 N 个 Riemann ζ(s) 零点（虚部） ===
gamma_list = np.array([
    14.134725, 21.022040, 25.010858, 30.424876, 32.935061,
    37.586178, 40.918719, 43.327073, 48.005150, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831780, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704690, 77.144840,
    79.337376, 82.910380, 84.735493, 87.425274, 88.809111,
    92.491899, 94.651345, 95.870634, 98.831194, 101.317851,
    103.725538, 105.446623, 107.168611, 111.029535, 111.874659,
    114.320221, 116.226680, 118.790783, 121.370125, 122.946829,
    124.256818, 127.516084, 129.578704, 131.087688, 133.497737,
    134.756510, 138.116042, 139.736208, 141.123707, 143.111845
])[:N_zeros]

# === 3. φ(x) 展开函数 ===
def phi_approx(params):
    A = params[:N_zeros]
    theta = params[N_zeros:]
    cos_terms = A * np.cos(gamma_list * np.log(x_target) + theta)
    return np.sum(cos_terms)

# === 4. 损失函数（最小化 φ(x) - 目标值）² ===
def loss(params):
    return (phi_approx(params) - phi_target)**2

# === 5. 初始化参数 ===
np.random.seed(42)
A0 = np.ones(N_zeros) * 0.1
theta0 = np.random.uniform(-np.pi, np.pi, N_zeros)
params0 = np.concatenate([A0, theta0])

# === 6. 执行优化 ===
result = minimize(loss, params0, method='L-BFGS-B', options={'maxiter': 1000, 'ftol': 1e-20})
A_opt = result.x[:N_zeros]
theta_opt = result.x[N_zeros:]

# === 7. 输出结果 ===
print(f"\n✅ 最终误差: {loss(result.x):.30f}")
print("\nA_n = [", ", ".join(f"{a:.8f}" for a in A_opt), "]")
print("\nθ_n = [", ", ".join(f"{t:.8f}" for t in theta_opt), "]")
