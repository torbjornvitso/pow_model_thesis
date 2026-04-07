def low_pass_filter(delta_t_i_k):
    total_time = 0
    for i in delta_t_i_k:
        total_time += i
    return total_time / len(delta_t_i_k)
