# 安装必要库（如未安装）
!pip install mpmath --quiet

import numpy as np
from scipy.optimize import differential_evolution
from mpmath import mp, mpf, log, cos, exp
import matplotlib.pyplot as plt

# 设置高精度（推荐 50 位）
mp.dps = 50

# Riemann ζ 零点（前 50 个，可扩展）
zeta_zeros_high = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005150, 49.773832,
    52.970321, 56.446247, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546401, 72.067158, 75.704690, 77.144840,
    79.337376, 82.910380, 84.735493, 87.425274, 88.809112,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317852,
    103.725538, 105.446623, 107.168611, 111.029535, 111.874659,
    114.320221, 116.226680, 118.790782, 121.370125, 122.946829,
    124.256818, 127.516084, 129.578704, 131.087688, 133.497737,
    134.756509, 138.116042, 139.736209, 141.123707, 143.111845
]

# pi(x) 查表（部分常用值）
pi_lookup_high = {
    100: 25, 1000: 168, 10000: 1229, 100000: 9592, 1000000: 78498
}

# 拟合函数
def fit_ads_high_precision_de_fast(x, lambda_reg=mpf("1e-4"), max_freqs=10, target_error=mpf("1e-10")):
    logx = log(x)
    true_val = mpf(pi_lookup_high[x]) / mpf(x)
    used_freqs = []
    for n in range(1, max_freqs + 1):
        def resonance_score(t): return abs((t * logx) % (2 * mp.pi) - mp.pi)
        candidate = sorted([z for z in zeta_zeros_high if z not in used_freqs], key=resonance_score)[0]
        used_freqs.append(candidate)
        N = len(used_freqs)
        bounds = [(0.01, 0.1)] * N + [(-float(mp.pi), float(mp.pi))] * N

        def rho_ads(params):
            s = mpf(1) / logx
            for i in range(N):
                A = mpf(params[i])
                theta = mpf(params[N + i])
                s += A * cos(used_freqs[i] * logx + theta)
            return s

        def loss(params):
            prediction = rho_ads(params)
            mse = (prediction - true_val) ** 2
            reg = lambda_reg * sum([exp(-mpf(p)) for p in params[:N]])
            return float(mse + reg)

        result = differential_evolution(loss, bounds, strategy='best1bin', tol=1e-7, maxiter=300, polish=True, seed=42)
        final_pred = rho_ads(result.x)
        abs_error = abs(final_pred - true_val)
        print(f"Iteration {n}: Error = {abs_error}")
        print(f"A_n = {result.x[:N]}")
        print(f"θ_n = {result.x[N:]}")
        if abs_error < target_error:
            break

    return float(abs_error)

# 多组 x 点测试
x_values = [100, 1000, 10000]
freqs_to_test = [5, 10, 15, 20]
results = {x: [] for x in x_values}

for x in x_values:
    for maxf in freqs_to_test:
        print(f"\n🔍 Testing x={x}, max_freqs={maxf}")
        err = fit_ads_high_precision_de_fast(x, max_freqs=maxf)
        results[x].append(err)

# 可视化误差
for x in x_values:
    plt.plot(freqs_to_test, results[x], label=f"x = {x}")
plt.xlabel("使用的零点数量 max_freqs")
plt.ylabel("绝对误差")
plt.yscale("log")
plt.title("AdS 模型拟合误差随零点数量变化")
plt.grid(True)
plt.legend()
plt.show()

