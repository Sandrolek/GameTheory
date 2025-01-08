import random

def simulate_dynamic_game(player1_probs, player2_probs, slot_values, invalid_pairs, num_simulations=10000):
    """
    Симуляция динамического анализа для двухдневной игры с учетом взаимосвязей между днями.

    :param player1_probs: Вероятности выбора слотов Игроком 1 для двух дней (dict).
    :param player2_probs: Вероятности выбора слотов Игроком 2 для двух дней (dict).
    :param slot_values: Словарь с ценностями слотов (dict).
    :param invalid_pairs: Список пар недопустимых слотов между днями (list).
    :param num_simulations: Количество симуляций (int).
    :return: Средние выигрыши для каждого игрока.
    """
    player1_total = 0
    player2_total = 0

    for _ in range(num_simulations):
        # День 1: Выборы игроков
        day1_p1 = random.choices(list(player1_probs["day1"].keys()), weights=player1_probs["day1"].values(), k=2)
        day1_p2 = random.choices(list(player2_probs["day1"].keys()), weights=player2_probs["day1"].values(), k=2)

        # Обработка конфликтов в День 1
        conflict_slots = set(day1_p1) & set(day1_p2)
        day1_slots_p1 = set(day1_p1) - conflict_slots
        day1_slots_p2 = set(day1_p2) - conflict_slots

        # День 2: Определение доступных слотов
        valid_day2_p1 = [s for s in player1_probs["day2"] if all((d1, s) not in invalid_pairs for d1 in day1_slots_p1)]
        valid_day2_p2 = [s for s in player2_probs["day2"] if all((d1, s) not in invalid_pairs for d1 in day1_slots_p2)]

        # День 2: Выборы игроков
        day2_p1 = random.choices(valid_day2_p1, weights=[player1_probs["day2"].get(s, 0) for s in valid_day2_p1], k=2)
        day2_p2 = random.choices(valid_day2_p2, weights=[player2_probs["day2"].get(s, 0) for s in valid_day2_p2], k=2)

        # Обработка конфликтов в День 2
        conflict_slots_day2 = set(day2_p1) & set(day2_p2)
        day2_slots_p1 = set(day2_p1) - conflict_slots_day2
        day2_slots_p2 = set(day2_p2) - conflict_slots_day2

        # Подсчёт выигрышей
        player1_total += sum(slot_values[slot] for slot in day1_slots_p1) + sum(slot_values[slot] for slot in day2_slots_p1)
        player2_total += sum(slot_values[slot] for slot in day1_slots_p2) + sum(slot_values[slot] for slot in day2_slots_p2)

    # Ожидаемые выигрыши
    player1_avg = player1_total / num_simulations
    player2_avg = player2_total / num_simulations

    return player1_avg, player2_avg

# Пример вероятностей и ценностей слотов
player1_probs = {
    "day1": {"S1": 0.3, "S2": 0.2, "S3": 0.5},
    "day2": {"S4": 0.6, "S5": 0.2, "S6": 0.2}
}

player2_probs = {
    "day1": {"S1": 0.3, "S2": 0.3, "S3": 0.4},
    "day2": {"S4": 0.4, "S5": 0.3, "S6": 0.3}
}

slot_values = {"S1": 1, "S2": 2, "S3": 3, "S4": 1, "S5": 2, "S6": 3}
invalid_pairs = [("S1", "S4"), ("S2", "S5"), ("S3", "S6")]

day1_avg, day2_avg = simulate_dynamic_game(player1_probs, player2_probs, slot_values, invalid_pairs)

print(f"Средний выигрыш Игрока 1: {day1_avg}")
print(f"Средний выигрыш Игрока 2: {day2_avg}")
