from simulation import (
    pow_feedback_mechanism_windowed_bounded_proportional_controller,
    pow_feedback_mechanism_incremental_bounded_proportional_controller,
)

from data_io import SIM_RESULTS_BTC, NODE_PROCESSED_DATA
from data_io import ETH_PROCESSED_DATA, SIM_RESULTS_ETH


def main():
    print("Staringing PoW simulation..")

    ## BTC design choices ##

    N = 2016  # Number of events before adjustment update
    T_ref = 600  # Reference inter-event time
    e_min = 0.25  # Lower bound error ratio
    e_max = 4  # Upper bound error ratio
    u_min = 0.25  # Lower bound difficulty adjustment
    u_max = 4  # Upper bound difficulty adjustment

    # Blockheight dataset is from height 0 to 936363, difficulty adjustment mechanism is activated from 32256
    from_blockheight = 32256
    to_blockheight = 936363

    pow_feedback_mechanism_windowed_bounded_proportional_controller(
        N,
        T_ref,
        e_min,
        e_max,
        u_min,
        u_max,
        NODE_PROCESSED_DATA,
        SIM_RESULTS_BTC,
        from_blockheight,
        to_blockheight,
    )

    ## ETH design choices ##

    N = 1  # Number of events before adjustment update
    phi = 10  # Quantized timing index
    u_min = -99
    u_max = 1

    # Blockheight dataset is from 1150000 to 1372221 (Homestead)
    # Blockheight dataset is from 12965000 to 13772999 (London)
    from_blockheight = 1150000
    to_blockheight = 1372221

    pow_feedback_mechanism_incremental_bounded_proportional_controller(
        N,
        phi,
        u_min,
        u_max,
        ETH_PROCESSED_DATA,
        SIM_RESULTS_ETH,
        from_blockheight,
        to_blockheight,
    )


if __name__ == "__main__":
    main()
