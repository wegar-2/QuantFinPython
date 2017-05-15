import numpy as np
import math


# 1. Ornstein-Uhlenbeck
def do_ou_trajectory(x_0, n, d_t, theta, kappa, sigma):
    res = [x_0]
    for i in range(n-1):
        d_x = theta*(kappa-res[i])*d_t + sigma*np.random.randn()*math.sqrt(d_t)
        res.append(res[i] + d_x)
    return res


class FellerConditionViolation(Exception):
    pass


# 2. Square-root diffusion (CIR model)
def do_square_root_trajectory(x_0, n, d_t, theta, kappa, sigma):
    res = [x_0]
    # check whether Feller condition is satisfied
    if 2*theta*kappa > sigma**2:
            for i in range(n-1):
                d_x = theta*(kappa-res[i])*d_t + \
                 sigma*math.sqrt(res[i])*math.sqrt(d_t)*np.random.randn()
                res.append(res[i]+d_x)
            return res
    else:
        raise FellerConditionViolation("Feller condition for process "
                                       "nonnegativity violated...")


# 3. Arithmetic brownian motion
def do_abm_trajectory(x_0, n, d_t, mu, sigma):
    res = [x_0]
    for k in range(n-1):
        res.append(res[k] + mu*d_t + sigma*np.random.randn()*math.sqrt(d_t))
    return res


# 4. Geometric brownian motion

class NegativeStartPriceException(Exception):
    pass


class NonPositiveSigma(Exception):
    pass


def do_gbm_trajectory(x_0, n, d_t, mu, sigma):
    if x_0 <= 0:
        raise NegativeStartPriceException("Negative start price for GBM!")
    if sigma <= 0:
        raise NonPositiveSigma("Sigma passed is negative or zero!")
    res = [x_0]
    for k in range(n-1):
        res.append(res[k]*(1 + mu*d_t + math.sqrt(d_t)*np.random.randn()*sigma))
    return res
