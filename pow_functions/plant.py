import numpy as np


def probability_of_success_btc(d_k: float):
    p_k = 1 / (d_k * 2**32)
    return p_k


def probability_of_success_eth(d_k: float):
    p_k = 1 / (d_k * 2**32)
    return p_k


def event_rate(h_k: float, p_k: float):
    lambda_k = h_k * p_k
    return lambda_k


def timestamps(lambda_k: float, N: int, t_0: float):
    dt = np.random.exponential(scale=(1 / lambda_k), size=N)
    t_i = t_0 + np.cumsum(dt)
    return t_i
