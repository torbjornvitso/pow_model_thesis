def calculate_inter_event_times_btc(t_i_k: list):
    delta_t_i_k = []
    for i in range(len(t_i_k) - 1):
        delta_t_i_k.append(float(t_i_k[i + 1]) - float(t_i_k[i]))
    return delta_t_i_k


def calculate_inter_event_times_eth(t_i_k: float, t_i: float):
    delta_t_i_k = t_i_k - t_i
    return delta_t_i_k
