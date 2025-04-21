import numpy as np
import math
from scipy.optimize import minimize

# ζ 函数前 100 个非平凡零点
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

def structured_ads_fit_for_x(x_input, lambda_fixed=0.0001, top_k_freqs=5):
    # 检查输入是否是2的幂次方（即 x = 2^N）
    if "2^" in x_input:
        n = int(x_input.split('^')[1])
        x = 2**n
        print(f"\n检测到输入是 2 的幂次方：x = 2^{n} = {x}")
    else:
        x = int(x_input)  # 输入的直接值作为 x

    x_max = 2**512  # 扩展最大支持到 2^512
    if x > x_max:
        raise ValueError(f"x 超过上限：2^512 ≈ {x_max}")
    
    logx = math.log(x)  # 计算 log(x)

    def resonance_score(t):
        return abs((t * logx) % (2 * np.pi) - np.pi)

    t_selected = sorted(zeta_zeros, key=resonance_score)[:top_k_freqs]
    N = len(t_selected)
    true_val = 1 / logx

    init_A = np.ones(N)
    init_theta = np.zeros(N)
    init_params = np.concatenate([init_A, init_theta])
    bounds = [(0.01, 2)] * N + [(-np.pi, np.pi)] * N

    def rho_ads_logx(params):
        s = 1 / logx
        for i in range(N):
            A = params[i]
            theta = params[N + i]
            s += A * math.cos(t_selected[i] * logx + theta)
        return s

    def objective(params):
        fit_loss = (rho_ads_logx(params) - true_val) ** 2
        structure_loss = lambda_fixed * np.sum(np.exp(-params[:N]))  # 激活控制
        return fit_loss + structure_loss

    result = minimize(objective, init_params, bounds=bounds, method='L-BFGS-B')
    fitted_val = rho_ads_logx(result.x)
    abs_error = abs(fitted_val - true_val)
    structure_energy = np.sum(result.x[:N])

    # 打印结果
    print(f"\n📌 AdS 密度拟合 @ x = {x}")
    print(f"✅ log(x) = {logx:.4f}")
    print(f"🎯 模拟真实密度 (1/log x) = {true_val:.10f}")
    print(f"📈 拟合密度 (AdS)         = {fitted_val:.10f}")
    print(f"📉 绝对误差               = {abs_error:.2e}")
    print(f"⚡ 结构激活能量 (∑A_i)    = {structure_energy:.4f}")
    print(f"\n🔢 使用频率组合（ζ 零点）:")
    for i, t in enumerate(t_selected):
        print(f"  t_{i+1} = {t:.6f}")
    print(f"\n🔧 最优幅度 A:")
    print(np.round(result.x[:N], 6))
    print(f"\n🔧 最优相位 θ:")
    print(np.round(result.x[N:], 6))

# 用户输入部分
if __name__ == "__main__":
    x_str = input("请输入 x（可以是 2 的幂次方形式，如 2^256 或直接输入数值）：")
    structured_ads_fit_for_x(x_str)
