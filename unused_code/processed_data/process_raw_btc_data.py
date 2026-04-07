import csv


def procces_raw_btw_data():
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

    with open("event_data_btc/raw_data/event_data.csv", "r") as f:
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
                    ["block_height_i_plus_1"]
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

    with open("event_data_btc/processed_data/processed_btc_data.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "first_block_height_in_kth_adjustment_list",
                "last_block_height_in_kth_adjustment",
                "total_t",
                "avg_t",
                "block_difficulty",
                "estimated_hash_rate",
            ]
        )

        for i in range(len(block_difficulty_list)):
            first_block = first_block_height_in_kth_adjustment_list[i]
            last_block = last_block_height_in_kth_adjustment_list[i]
            total_time = total_t_list[i]
            avg_time = avg_t_list[i]
            d = block_difficulty_list[i]
            hash_est = 0
            writer.writerow(
                [first_block, last_block, total_time, avg_time, d, hash_est]
            )

    return


if __name__ == "__main__":
    procces_raw_btw_data()
