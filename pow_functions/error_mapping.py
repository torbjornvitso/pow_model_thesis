def error_ratio(T_obs_k: float, T_ref: int):
    e_k = T_ref / T_obs_k
    return e_k


def quantized_timing_index(T_obs_k: float, phi_timing_parameter: int):
    e_k = T_obs_k // phi_timing_parameter
    return e_k
