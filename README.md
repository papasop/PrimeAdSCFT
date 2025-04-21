## Features in Detail

- **Adaptive Precision:**  
  The tool supports precision up to arbitrary accuracy. By dynamically increasing the number of ζ zeros and optimizing the amplitudes and phases, the model can reach extremely small fitting errors (e.g. \( 10^{-8} \), \( 10^{-12} \), or lower), depending on the target.

- **Automatic Frequency Matching:**  
  Automatically selects the best matching frequencies based on resonance alignment with \( \log(x) \), using a score-based selection strategy.

- **Spectral Kernel Compression:**  
  Stores optimized frequency–amplitude–phase structures as reusable kernels, supporting rapid recalculation, transfer learning, and structural explanation.

- **Scalability to Large Numbers:**  
  Capable of estimating prime density for \( x \) values up to \( 2^{512} \) and beyond. Since the model operates in \( \log x \)-space, it remains efficient at very large scales.

- **Physical Interpretability:**  
  Based on the AdS/CFT holographic duality, this model reveals deep structural resonance between prime distributions and zeta zero frequencies, offering insight aligned with both number theory and mathematical physics.


Holographic Duality of Prime Numbers and Riemann Zeros in AdS/CFT
https://zenodo.org/records/15232851



## **Installation**

To use the **PrimeAdSCFT** tool, install the necessary dependencies with the following command:

```bash
pip install numpy scipy


 


