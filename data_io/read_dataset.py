import csv


def read_dataset_btc(
    path: str,
    h_k: list,
    d_k: list,
    h_g: list = None,
    exp_e_t: list = None,
    t_obs: list = None,
):

    if t_obs is None:
        t_obs = []

    if h_g is None:
        h_g = []

    if exp_e_t is None:
        exp_e_t = []

    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            h_k.append(float(row["estimated_hash_rate"]))
            d_k.append(float(row["block_difficulty"]))
            t_obs.append(float(row["avg_t_sec"]))
            h_g.append(float(row["estimated_hash_rate_growth"]))
            exp_e_t.append(float(row["expected_event_interval"]))


def read_dataset_eth(path: str, h_k: list, d_k: list, t_total: list):

    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            h_k.append(float(row["estimated_hash_rate"]))
            d_k.append(float(row["block_difficulty"]))
            t_total.append(int(row["delta_t_sec"]))


def read_dataset_shock_test(path: str, h_k: list, d_k: list):

    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            h_k.append(float(row["hash_rate"]))
            d_k.append(float(row["difficulty"]))
