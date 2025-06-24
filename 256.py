# AdS Prime Model (High-Precision) - Colab Ready
# --------------------------------------------------
# 安装依赖
!pip install mpmath numpy scipy --quiet

# 导入模块
import numpy as np
from scipy.optimize import differential_evolution
from mpmath import mp, mpf, log, cos, exp
import matplotlib.pyplot as plt

# 设置高精度
mp.dps = 50

# Riemann 零点（可拓展）
zeta_zeros_high = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005150, 49.773832,
    52.970321, 56.446247, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546401, 72.067158, 75.704690, 77.144840,
    79.337375, 82.910380, 84.735493, 87.425274, 88.809111
]  # 可拓展到100+

# pi(x) 查表
pi_lookup_high = {100: 25, 500: 95, 1000: 168, 10000: 1229}

# 拟合主函数（支持多点、轨迹输出、正则）
def fit_ads_batch(xs, lambda_reg=mpf("1e-4"), max_freqs=10, target_error=mpf("1e-8")):
    results = []
    for x in xs:
        print(f"\n=== Fitting x = {x} ===")
        logx = log(x)
        true_val = mpf(pi_lookup_high[x]) / mpf(x)
        used_freqs = []

        for n in range(1, max_freqs + 1):
            def resonance_score(t): return abs((t * logx) % (2 * mp.pi) - mp.pi)
            candidate = sorted([z for z in zeta_zeros_high if z not in used_freqs], key=resonance_score)[0]
            used_freqs.append(candidate)
            N = len(used_freqs)

            bounds = [(0.05, 0.1)] * N + [(-np.pi, np.pi)] * N  # 初始化缩窄

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

            result = differential_evolution(loss, bounds, strategy='best1bin', tol=1e-7, maxiter=500, seed=42)
            pred = rho_ads(result.x)
            abs_error = abs(pred - true_val)

            A_values = result.x[:N]
            theta_values = result.x[N:]

            print(f"Iteration {n}: Error = {abs_error}")
            print(f"A_n = {np.round(A_values, 8)}")
            print(f"theta_n = {np.round(theta_values, 6)}")

            results.append({"x": x, "n": n, "error": float(abs_error),
                            "A_n": A_values, "theta_n": theta_values})

            if abs_error < target_error:
                print(f"✅ Converged for x={x} with {n} frequencies\n")
                break
        else:
            print("❌ 未达到目标误差")

    return results

# ▶️ 运行测试：支持多个 x
x_values = [100, 500, 1000, 10000]
fit_ads_batch(x_values, max_freqs=10, lambda_reg=mpf("1e-3"))

