from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
KAGGLE_DATA_DIR = DATA_DIR / "kaggle"
NODE_DATA_DIR = DATA_DIR / "node"
ETH_DATA_DIR = DATA_DIR / "eth_blocks"
SIM_DATA_DIR = DATA_DIR / "sim"
HASHRATE_SHOCK_DIR = DATA_DIR / "hashrate_shock"

NODE_DATA = NODE_DATA_DIR / "dataset_node.csv"
KAGGLE_DATA = KAGGLE_DATA_DIR / "dataset_kaggle.csv"
ETH_DATA = ETH_DATA_DIR / "eth_blocks_homestead.csv"
HASH_RATE_SHOCK_DATA = HASHRATE_SHOCK_DIR / "dataset_hashrate_shock.csv"

KAGGLE_MID_PROCESSED_DATA = KAGGLE_DATA_DIR / "inter_events_processed_data.csv"
NODE_MID_PROCESSED_DATA = NODE_DATA_DIR / "inter_events_processed_data.csv"
ETH_MID_PROCESSED_DATA = ETH_DATA_DIR / "mid_processed_data.csv"

KAGGLE_PROCESSED_DATA = KAGGLE_DATA_DIR / "avg_k_events_processed_data.csv"
NODE_PROCESSED_DATA = NODE_DATA_DIR / "avg_k_events_processed_data.csv"
ETH_PROCESSED_DATA = ETH_DATA_DIR / "processed_data.csv"


SIM_RESULTS_KAGGLE = SIM_DATA_DIR / "sim_data_kaggle.csv"
SIM_RESULTS_BTC = SIM_DATA_DIR / "sim_data_btc.csv"
SIM_RESULTS_ETH = SIM_DATA_DIR / "sim_data_eth.csv"
SIM_RESULTS_SHOCK_TEST = SIM_DATA_DIR / "sim_data_shock_test.csv"
