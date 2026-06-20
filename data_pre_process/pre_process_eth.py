import csv
import numpy as np

from data_io import ETH_DATA, ETH_MID_PROCESSED_DATA, ETH_PROCESSED_DATA


def pre_process_data_eth(from_height: int | None = None, to_height: int | None = None):

    heights: list[int] = []
    timestamps: list[int] = []
    difficulties: list[float] = []

    with open(ETH_DATA, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            h = int(row["number"])

            if from_height is None and to_height is None:
                pass

            elif not (from_height <= h <= to_height):
                continue

            ts_sec = int(row["timestamp_sec"])
            d = float(row["difficulty"])

            heights.append(h)
            timestamps.append(ts_sec)
            difficulties.append(d)

    with open(ETH_MID_PROCESSED_DATA, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "block_height_i",
                "block_height_i_plus_1",
                "t_i",
                "t_i_plus_1",
                "delta_t_sec",
                "difficulty",
            ]
        )

        for i in range(len(heights) - 1):
            b1 = heights[i]
            b2 = heights[i + 1]
            t1 = timestamps[i]
            t2 = timestamps[i + 1]

            delta_t_min = t2 - t1
            d = difficulties[i + 1]

            writer.writerow([b1, b2, t1, t2, delta_t_min, d])

    estimated_hash_rate = []
    avg_time = []
    total_time = 0.0
    total_difficulty = 0.0
    counter = 0

    def lastWindow(d: float, t: float, c: int):
        d = d / c
        estimated_hash_rate.append((d * (2**32)) / (t / c))
        avg_time.append(t / c)

    with open(ETH_MID_PROCESSED_DATA, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            total_time += float(row["delta_t_sec"])
            total_difficulty += float(row["difficulty"])
            counter += 1

            if counter == 2048:
                difficulty = total_difficulty / counter
                avg = total_time / counter
                avg_time.append(avg)
                estimated_hash_rate.append((difficulty * (2**32)) / avg)
                total_time = 0.0
                total_difficulty = 0.0
                counter = 0

            pre_last_difficulty = total_difficulty

        if counter != 0:
            lastWindow(pre_last_difficulty, total_time, counter)

    with open(ETH_PROCESSED_DATA, "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "block_height_i",
                "block_height_i_plus_1",
                "t_i",
                "t_i_plus_1",
                "delta_t_sec",
                "avg_t_sec",
                "quantized_timing",
                "correction_term",
                "block_difficulty",
                "estimated_hash_rate",
            ]
        )

        for i in range(len(heights) - 1):
            b1 = heights[i]
            b2 = heights[i + 1]
            t1 = timestamps[i]
            t2 = timestamps[i + 1]

            delta_t_sec = t2 - t1

            e_k = np.floor(delta_t_sec / 10)
            u_k = np.maximum(1 - e_k, -99)

            d = difficulties[i + 1]

            est_h_r = estimated_hash_rate[i // 2048]
            avg_time_window = avg_time[i // 2048]

            writer.writerow(
                [b1, b2, t1, t2, delta_t_sec, avg_time_window, e_k, u_k, d, est_h_r]
            )
