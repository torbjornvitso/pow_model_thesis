import csv

hash_rate_data = []
difficulty_data = []


def create_shock_data(num_windows: int, h0: int, gain: int):
    h_prev = h0
    l_k = 0.06931471806

    d_k = (h_prev) / (2**32 * l_k)

    difficulty_data.append(d_k)
    hash_rate_data.append(h_prev)

    for m in range(1):
        for k in range(1, num_windows + 1):
            if k <= num_windows / 10:
                h_k = h0
            else:
                h_k = h0 * gain ** (m + 1)
                # h_k = h0

            d_k = (h_prev) / (2**32 * l_k)

            difficulty_data.append(d_k)
            hash_rate_data.append(h_k)

            h_prev = h_k


def hashrate_shock_simulation_data_eth(
    num_windows: int,
    h0: int,
    gain: int,
    path: str,
):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "adjustment_window_k",
                "hash_rate",
                "difficulty",
            ]
        )

        create_shock_data(num_windows, h0, gain)

        for k in range(len(hash_rate_data)):
            h_k = hash_rate_data[k]
            d_k = difficulty_data[k]

            writer.writerow([k, h_k, d_k])
