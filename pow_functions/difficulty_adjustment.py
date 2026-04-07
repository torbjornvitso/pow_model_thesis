def difficulty_adjustment_update_btc(d_k: float, u_k: float):
    d_k_plus_one = d_k * u_k
    return d_k_plus_one


def difficulty_adjustment_update_eth(d_k: float, u_k: int):
    d_k_plus_one = d_k + (d_k // 2048) * u_k
    return d_k_plus_one


def difficulty_bomb(block_number: int, delay_blocks: int = 0):
    n = block_number - delay_blocks
    exponent = (n // 100000) - 2
    bomb = 2**exponent
    return bomb
