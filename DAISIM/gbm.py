import numpy as np
import matplotlib.pyplot as plt
#https://stackoverflow.com/questions/45021301/geometric-brownian-motion-simulation-in-python

def gen_paths(S0, r, sigma, T, M, I):
    dt = float(T) / M
    paths = np.zeros((M + 1, I), np.float64)
    paths[0] = S0
    for t in range(1, M + 1):
        rand = np.random.standard_normal(I)
        paths[t] = paths[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt +
                                         sigma * np.sqrt(dt) * rand)
    return paths


if __name__ == "__main__":
    S0=300
    r=.008
    sigma=.1
    T=10 # num periods ( "10 days")
    M=24 # frequency (samples per period -- "24 Hours")
    I=50 # num paths to generate

    paths=gen_paths(S0,r,sigma,T,M,I)

    for p in paths.T:
        plt.plot(p)
    
    plt.show()