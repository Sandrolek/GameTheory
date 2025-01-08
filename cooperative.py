import itertools

def maximize_cooperative_strategy(slot_values, invalid_pairs):
    """
    Вычисляет кооперативную стратегию для максимизации общей суммы выигрышей за два дня.

    :param slot_values: Словарь с ценностями слотов (dict).
    :param invalid_pairs: Список пар недопустимых слотов между днями (list).
    :return: Оптимальная стратегия и максимальная сумма выигрышей.
    """
    strategies_day1 = list(itertools.combinations(["S1", "S2", "S3"], 2))
    strategies_day2 = list(itertools.combinations(["S4", "S5", "S6"], 2))

    best_total_value = 0
    best_combination = None

    for strategy1_p1, strategy1_p2 in itertools.product(strategies_day1, repeat=2):
        conflict_slots_day1 = set(strategy1_p1) & set(strategy1_p2)
        strategy1_p1_actual = set(strategy1_p1) - conflict_slots_day1
        strategy1_p2_actual = set(strategy1_p2) - conflict_slots_day1

        for strategy2_p1, strategy2_p2 in itertools.product(strategies_day2, repeat=2):
            if any((s1, s2) in invalid_pairs for s1 in strategy1_p1_actual for s2 in strategy2_p1):
                continue
            if any((s1, s2) in invalid_pairs for s1 in strategy1_p2_actual for s2 in strategy2_p2):
                continue

            conflict_slots_day2 = set(strategy2_p1) & set(strategy2_p2)
            strategy2_p1_actual = set(strategy2_p1) - conflict_slots_day2
            strategy2_p2_actual = set(strategy2_p2) - conflict_slots_day2

            total_value = (
                sum(slot_values[s] for s in strategy1_p1_actual) +
                sum(slot_values[s] for s in strategy1_p2_actual) +
                sum(slot_values[s] for s in strategy2_p1_actual) +
                sum(slot_values[s] for s in strategy2_p2_actual)
            )

            if total_value > best_total_value:
                best_total_value = total_value
                best_combination = {
                    "day1": {"player1": strategy1_p1, "player2": strategy1_p2},
                    "day2": {"player1": strategy2_p1, "player2": strategy2_p2},
                }

    return best_combination, best_total_value

slot_values = {"S1": 1, "S2": 2, "S3": 3, "S4": 1, "S5": 2, "S6": 3}
invalid_pairs = [("S1", "S4"), ("S2", "S5"), ("S3", "S6")]

optimal_strategy, max_value = maximize_cooperative_strategy(slot_values, invalid_pairs)

print(f"Оптимальная стратегия: {optimal_strategy}")
print(f"Максимальная сумма выигрышей: {max_value}")
