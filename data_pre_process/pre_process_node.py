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
                # ts_sec = ts_ms / 1000
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

    total_t = 0.0

    first_block_height_in_kth_adjustment_list = []
    last_block_height_in_kth_adjustment_list = []
    total_t_list = []
    avg_t_list = []
    block_difficulty_list = []
    last_difficulty = None

    def last_window(lb: int, t: int, c: int):
        last_block_height_in_kth_adjustment_list.append(lb)
        total_t_list.append(t)
        avg_t_list.append(t / c)
        return

    with open(NODE_MID_PROCESSED_DATA, "r") as f:
        reader = csv.DictReader(f)
        counter = 0
        pre_last_block = 0

        for row in reader:
            difficulty = float(row["difficulty"])

            if counter == 0:
                last_difficulty = difficulty
                block_difficulty_list.append(difficulty)
                first_block_height_in_kth_adjustment_list.append(
                    int(row["block_height_i"])
                )

            counter += 1

            if difficulty != last_difficulty:
                last_block_height_in_kth_adjustment_list.append(
                    int(row["block_height_i"])
                )
                total_t_list.append(total_t)
                avg_t_list.append(total_t / counter)
                last_difficulty = difficulty
                total_t = 0
                counter = 0

            total_t += float(row["delta_t_min"])
            pre_last_block = int(row["block_height_i_plus_1"])

        if counter != 0:
            last_window(pre_last_block, total_t, counter)

    with open(NODE_PROCESSED_DATA, "w") as f:
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
        previous_hash_rate_est = 0
        hash_rate_growth = 0
        expected_event_interval = 600

        for i in range(len(block_difficulty_list)):
            first_block = first_block_height_in_kth_adjustment_list[i]
            last_block = last_block_height_in_kth_adjustment_list[i]
            total_time = total_t_list[i]
            avg_time_min = avg_t_list[i]
            avg_time_sec = avg_t_list[i] * 60
            d = block_difficulty_list[i]
            hash_est = d * 2**32 / avg_time_sec
            if previous_hash_rate_est != 0:
                hash_rate_growth = np.log(hash_est / previous_hash_rate_est)
                expected_event_interval = (
                    avg_t_list[i - 1]
                    * 60
                    * ((1 - np.e ** (-hash_rate_growth)) / (hash_rate_growth))
                )
            previous_hash_rate_est = hash_est
            writer.writerow(
                [
                    first_block,
                    last_block,
                    total_time,
                    avg_time_min,
                    avg_time_sec,
                    d,
                    hash_est,
                    hash_rate_growth,
                    expected_event_interval,
                ]
            )
