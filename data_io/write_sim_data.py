import csv


def write_sim_data(
    path: str,
    h_k: list,
    d_k: list,
    delta_t: list,
    p_d: list,
    lambda_k: list,
    t_obs: list,
    e_k: list,
    u_k: list,
):

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "hash_rate",
                "difficulty",
                "delta_t_sec",
                "probability_of_success",
                "event_rate",
                "t_obs",
                "error_ratio",
                "adjustment_factor",
            ]
        )

        for k in range(len(h_k)):
            h = h_k[k]
            d = d_k[k]
            d_t = delta_t[k]
            p = p_d[k]
            l_k = lambda_k[k]
            t_avg = t_obs[k]
            e = e_k[k]
            u = u_k[k]

            writer.writerow([h, d, d_t, p, l_k, t_avg, e, u])
