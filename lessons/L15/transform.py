"""Урок L15: преобразование заказов. Задание — дописать transform_orders."""


def transform_orders(rows):
    """Очистить заказы и посчитать итоги по дням.

    rows — список словарей с ключами order_id, event_date, category, amount_rub (все значения — строки).

    Правила:
    1. Строка отбраковывается, если amount_rub не целое число или <= 0, если event_date не дата
       в формате ГГГГ-ММ-ДД или если пусты order_id или category.
    2. Из правильных строк для каждого order_id берётся только первая; остальные — повторы.
    3. Итоги по дням: для каждой event_date число заказов и сумма amount_rub (целым числом).

    Вернуть (summary, stats):
      summary — список {"event_date": str, "orders": int, "amount_rub": int}, отсортированный по дате;
      stats   — {"accepted": int, "duplicates": int, "rejected": list исходных строк-словарей}.
    """
    raise NotImplementedError("Допишите transform_orders: проверка строк, повторы, итоги по дням")
