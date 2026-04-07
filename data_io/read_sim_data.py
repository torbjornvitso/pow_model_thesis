import csv
import ast


def read_sim_data(
    path: str,
    h_k: list,
    d_k: list,
    p_k: list,
    lambda_k: list,
    delta_t: list[list],
    t_obs: list,
    e_k: list,
    u_k: list,
):

    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            h_k.append(float(row["hash_rate"]))
            d_k.append(float(row["difficulty"]))
            p_k.append(float(row["probability_of_success"]))
            lambda_k.append(float(row["event_rate"]))
            t_obs.append(float(row["t_obs"]))
            dt_list = ast.literal_eval(row["delta_t_sec"])
            delta_t.append([float(x) for x in dt_list])
            e_k.append(float(row["error_ratio"]))
            u_k.append(float(row["adjustment_factor"]))
