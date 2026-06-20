import csv
import numpy as np

from data_io import NODE_MID_PROCESSED_DATA, NODE_PROCESSED_DATA, NODE_DATA


def pre_process_data(from_height: int | None = None, to_height: int | None = None):

    heights: list[int] = []
    timestamps: list[int] = []
    difficulties: list[float] = []

    with open(NODE_DATA, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            h = int(row["height"])
            if from_height <= h <= to_height:
                ts_sec = int(row["time"])
                d = float(row["difficulty"])

                heights.append(h)
                timestamps.append(ts_sec)
                difficulties.append(d)

    with open(NODE_MID_PROCESSED_DATA, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "block_height_i",
                "block_height_i_plus_1",
                "t_i",
                "t_i_plus_1",
                "delta_t_min",
                "difficulty",
            ]
        )

        for i in range(len(heights) - 1):
            b1 = heights[i]
            b2 = heights[i + 1]
            t1 = timestamps[i]
            t2 = timestamps[i + 1]

            delta_t_min = (t2 - t1) / 60.0
            d = difficulties[i + 1]

            writer.writerow([b1, b2, t1, t2, delta_t_min, d])

    WINDOW = 2016

    rows = []
    with open(NODE_MID_PROCESSED_DATA, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    num_windows = len(rows) // WINDOW
    rows = rows[: num_windows * WINDOW]

    with open(NODE_PROCESSED_DATA, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "first_block_height_in_kth_adjustment_list",
                "last_block_height_in_kth_adjustment",
                "total_t",
                "avg_t_min",
                "avg_t_sec",
                "block_difficulty",
                "estimated_hash_rate",
                "estimated_hash_rate_growth",
                "expected_event_interval",
            ]
        )

        previous_hash_rate_est = 0.0

        for k in range(num_windows):
            window = rows[k * WINDOW : (k + 1) * WINDOW]

            first_block = int(window[0]["block_height_i"])
            last_block = int(window[-1]["block_height_i_plus_1"])

            delta_t_list = [float(r["delta_t_min"]) for r in window]
            total_time_min = sum(delta_t_list)
            avg_time_min = total_time_min / WINDOW
            avg_time_sec = avg_time_min * 60

            d = float(window[0]["difficulty"])

            hash_est = d * 2**32 / avg_time_sec

            hash_rate_growth = 0.0
            expected_event_interval = 600.0

            if previous_hash_rate_est != 0:
                hash_rate_growth = np.log(hash_est / previous_hash_rate_est)
                if hash_rate_growth != 0:
                    expected_event_interval = (
                        avg_time_sec
                        * (1 - np.exp(-hash_rate_growth))
                        / hash_rate_growth
                    )

            previous_hash_rate_est = hash_est

            writer.writerow(
                [
                    first_block,
                    last_block,
                    total_time_min,
                    avg_time_min,
                    avg_time_sec,
                    d,
                    hash_est,
                    hash_rate_growth,
                    expected_event_interval,
                ]
            )
