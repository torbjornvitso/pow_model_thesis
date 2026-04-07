def bounded_correction_map(
    e_k: float, e_min: float, e_max: float, u_min: float, u_max: float
):

    if e_k < e_min:
        u_k = u_min
    if e_min <= e_k <= e_max:
        u_k = e_k
    if e_k > e_max:
        u_k = u_max

    return u_k


def quantized_correction_map(e_k: float, u_min: int, u_max: int):
    u_k = max(u_max - e_k, u_min)
    return u_k
