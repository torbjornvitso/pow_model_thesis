from data_io import (
    read_dataset_btc,
    write_sim_data,
)
from plots import plot_sim_data
from data_pre_process import pre_process_data
from pow_functions import (
    bounded_correction_map,
    calculate_inter_event_times_btc,
    difficulty_adjustment_update_btc,
    error_ratio,
    event_rate,
    low_pass_filter,
    probability_of_success_btc,
    timestamps,
)

h_real_data = []
d_real_data = []

h_sim_data = []
d_sim_data = []
p_k_sim_data = []
lambda_k_sim_data = []
t_sim_data = []
delta_t_sim_data = []
t_obs_sim_data = []
e_k_sim_data = []
u_k_sim_data = []


def pow_feedback_mechanism_windowed_bounded_proportional_controller(
    N: int,
    T_ref: int,
    e_min: float,
    e_max: float,
    u_min: float,
    u_max: float,
    processed_data_path: str,
    sim_data_path: str,
    from_height: int | None = None,
    to_height: int | None = None,
):
    pre_process_data(from_height, to_height)

    read_dataset_btc(processed_data_path, h_real_data, d_real_data)
    d_0 = d_real_data[0]
    u_0 = 1
    t_0 = 0

    d_k = d_0 * u_0
    t_i = t_0

    for h_k in h_real_data:
        h_sim_data.append(h_k)
        d_sim_data.append(d_k)

        p_k = probability_of_success_btc(d_k)
        lambda_k = event_rate(h_k, p_k)
        t_i_k = timestamps(lambda_k, N, t_i)
        delta_t_i_k = calculate_inter_event_times_btc(t_i_k)
        T_obs_k = low_pass_filter(delta_t_i_k)
        e_k = error_ratio(T_obs_k, T_ref)
        u_k = bounded_correction_map(e_k, e_min, e_max, u_min, u_max)
        d_k_plus_one = difficulty_adjustment_update_btc(d_k, u_k)

        d_k = d_k_plus_one
        t_i = t_i_k[-1]

        p_k_sim_data.append(p_k)
        lambda_k_sim_data.append(lambda_k)
        t_sim_data.append(t_i_k)
        delta_t_sim_data.append(delta_t_i_k)
        t_obs_sim_data.append(T_obs_k)
        e_k_sim_data.append(e_k)
        u_k_sim_data.append(u_k)

    write_sim_data(
        sim_data_path,
        h_sim_data,
        d_sim_data,
        delta_t_sim_data,
        p_k_sim_data,
        lambda_k_sim_data,
        t_obs_sim_data,
        e_k_sim_data,
        u_k_sim_data,
    )
    plot_sim_data(T_ref, processed_data_path, sim_data_path, from_height, to_height, N)
