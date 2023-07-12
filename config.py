# Шаг округления транзакции в меньшую сторону
step = 0.1

# Bridge | ETH --> Scroll | Значения верхнего и нижнего порога перевода
eth_to_scroll_down, eth_to_scroll_up = 1.2, 1.49

# Bridge | Scroll --> ETH | Значения верхнего и нижнего порога перевода
scroll_to_eth_down, scroll_to_eth_up = 1.2, 1.49

# Bridge Orbiter | ETH --> Scroll and Scroll --> ETH | Значения верхнего и нижнего порога перевода
orbiter_down, orbiter_up = 0.001, 0.1

# Uniswap Transfer | WETH и ETH | Значения верхнего и нижнего порога перевода
swap_down, swap_up = 0.001, 0.1

# Число транзакций на кошелек от и до
transfer_min, transfer_max = 8, 10

# Случайное ожидание между транзакциями в мин
time_down, time_up = 1, 5