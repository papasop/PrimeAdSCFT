import numpy as np
import math
from scipy.optimize import minimize

# 预定义前 100 个 ζ 零点（频率）
zeta_zeros = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178, 40.918719,
    43.327073, 48.005151, 49.773832, 52.970321, 56.446247, 59.347044, 60.831779,
    65.112544, 67.079811, 69.546401, 72.067158, 75.704690, 77.144840, 79.337376,
    82.910380, 84.735493, 87.425274, 88.809112, 92.491899, 94.651344, 95.870634,
    98.831194, 101.317852, 103.725538, 105.446623, 107.168611, 111.029535,
    111.874659, 114.320221, 116.226680, 118.790782, 121.370125, 122.946829,
    124.256818, 127.516084, 129.578704, 131.087688, 133.497737, 134.756509,
    138.116042, 139.736209, 141.123707, 143.111845, 146.000982, 147.422765,
    150.053520, 150.925257, 153.024693, 156.112909, 157.597591, 158.849988,
    161.188964, 163.030709, 165.537069, 167.184438, 169.094515, 169.911976,
    173.411536, 174.754191, 176.441434, 178.377407, 179.916484, 182.207078,
    184.874468, 185.598783, 187.228922, 189.416158, 192.026656, 193.079726,
    195.265397, 196.876482, 198.015308, 201.264751, 202.493594, 204.189671,
    207.906258, 209.576509, 211.690862, 213.347919, 215.548097, 216.169538,
    219.067596, 220.714918, 221.430705, 224.007000, 224.983324, 227.421444,
    229.337413, 231.250188, 231.987235, 233.693404
]

# 实际 π(x) 查表（部分常见值）
pi_lookup = {
    16: 6, 100: 25, 256: 54, 1000: 168, 10000: 1229, 100000: 9592,
    1000000: 78498, 10000000: 664579, 100000000: 5761455,
    1000000000: 50847534, 10000000000: 455052511
}

def fit_until_error(x, target_error=1e-6, lambda_reg=0.0001, max_freqs=30):
    logx = math.log(x)
    true_val = pi_lookup[x] / x if x in pi_lookup else 1 / logx
    used_freqs = []
    errors = []

    for n in range(1, max_freqs + 1):
        def score(t): return abs((t * logx) % (2 * np.pi) - np.pi)
        best_new = sorted([z for z in zeta_zeros if z not in used_freqs], key=score)[0]
        used_freqs.append(best_new)

        N = len(used_freqs)
        init_A = np.ones(N)
        init_theta = np.zeros(N)
        init_params = np.concatenate([init_A, init_theta])
        bounds = [(0.01, 2)] * N + [(-np.pi, np.pi)] * N

        def rho_ads(params):
            s = 1 / logx
            for i in range(N):
                A = params[i]
                theta = params[N + i]
                s += A * math.cos(used_freqs[i] * logx + theta)
            return s

        def loss(params):
            return (rho_ads(params) - true_val)**2 + lambda_reg * np.sum(np.exp(-params[:N]))

        result = minimize(loss, init_params, bounds=bounds, method='L-BFGS-B')
        error = abs(rho_ads(result.x) - true_val)
        errors.append(error)

        if error <= target_error:
            return {
                "x": x,
                "logx": logx,
                "frequencies_used": used_freqs,
                "optimized_A": result.x[:N],
                "optimized_theta": result.x[N:],
                "ads_density": rho_ads(result.x),
                "true_density": true_val,
                "absolute_error": error,
                "structure_energy": np.sum(result.x[:N]),
                "frequencies_count": N
            }

    return {"error": "Target not reached", "min_error": min(errors)}

# 示例运行
if __name__ == "__main__":
    x_input = input("请输入自然数 x：")
    x = int(x_input)
    result = fit_until_error(x)
    if "error" in result:
        print("❌ 未达到目标精度。")
    else:
        print(f"\n📌 AdS拟合 @ x = {result['x']} (log x ≈ {result['logx']:.4f})")
        print(f"✅ True density  = {result['true_density']:.10f}")
        print(f"📈 AdS density   = {result['ads_density']:.10f}")
        print(f"📉 Absolute error= {result['absolute_error']:.2e}")
        print(f"⚡ Structure energy = {result['structure_energy']:.4f}")
        print(f"🎯 Frequencies used ({result['frequencies_count']}):")
        for i, t in enumerate(result["frequencies_used"]):
            print(f"  t_{i+1} = {t:.6f}")
        print(f"\n🔧 Amplitudes A:")
        print(np.round(result['optimized_A'], 6))
        print(f"\n🔧 Phases θ:")
        print(np.round(result['optimized_theta'], 6))
