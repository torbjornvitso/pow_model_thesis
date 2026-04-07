import csv

import requests

base_url = "https://blockstream.info/api"


def get_total_block_height():
    resp_height = requests.get(f"{base_url}/blocks/tip/height", timeout=30)
    resp_height.raise_for_status()
    resp_height.text.strip()
    return resp_height.text.strip()


def get_block_hash_by_height(height: int):
    resp_hash = requests.get(f"{base_url}/block-height/{height}", timeout=30)
    resp_hash.raise_for_status()
    return resp_hash.text.strip()


def get_block_data_by_hash(hash: int):
    resp_block_data = requests.get(f"{base_url}/block/{hash}", timeout=30)
    resp_block_data.raise_for_status()
    return resp_block_data.json()


def get_btc_data(length: int):
    block_height_list = []
    timestamps_list = []
    difficulty_list = []

    last_block_index = get_total_block_height()

    start_block = int(last_block_index) - length

    for block_index in range(start_block, int(last_block_index) + 1):
        block_height_list.append(block_index)
        current_block_hash = get_block_hash_by_height(block_index)
        current_block_data = get_block_data_by_hash(current_block_hash)
        current_block_timestamp = current_block_data["timestamp"]
        current_block_difficulty = current_block_data["difficulty"]
        timestamps_list.append(current_block_timestamp)
        difficulty_list.append(current_block_difficulty)

    with open("event_data_btc/raw_data/event_data.csv", "w", newline="") as f:
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

        for i in range(len(block_height_list) - 1):
            b1 = block_height_list[i]
            b2 = block_height_list[i + 1]
            t1 = timestamps_list[i]
            t2 = timestamps_list[i + 1]
            delta_t = (t2 - t1) / 60
            d = difficulty_list[i]
            writer.writerow([b1, b2, t1, t2, delta_t, d])
    return


if __name__ == "__main__":
    get_btc_data(5)
