import csv

input_path = "data/kaggle/dataset_events.csv"
output_path = "data/kaggle/inter_events_processed_data.csv"
final_path = "data/kaggle/avg_k_events_processed_data.csv"


def pre_process_kaggle_data():

    heights: list[int] = []
    timestamps: list[int] = []
    difficulties: list[float] = []

    with open(input_path, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            h = int(row["height"])
            ts_ms = int(row["timestamp"])
            ts_sec = ts_ms / 1000
            d = float(row["difficulty"])

            heights.append(h)
            timestamps.append(ts_sec)
            difficulties.append(d)

        # heights = heights[-201600:]
        # timestamps = timestamps[-201600:]
        # difficulties = difficulties[-201600:]

    with open(output_path, "w", newline="") as f:
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


def procces_kaggle_data():
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

    with open(output_path, "r") as f:
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

    with open(final_path, "w") as f:
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
            ]
        )

        for i in range(len(block_difficulty_list)):
            first_block = first_block_height_in_kth_adjustment_list[i]
            last_block = last_block_height_in_kth_adjustment_list[i]
            total_time = total_t_list[i]
            avg_time_min = avg_t_list[i]
            avg_time_sec = avg_t_list[i] * 60
            d = block_difficulty_list[i]
            hash_est = d * 2**32 / avg_time_sec
            writer.writerow(
                [
                    first_block,
                    last_block,
                    total_time,
                    avg_time_min,
                    avg_time_sec,
                    d,
                    hash_est,
                ]
            )

    return


if __name__ == "__main__":
    pre_process_kaggle_data()
    procces_kaggle_data()
