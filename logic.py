def add_payment(records, payment): 
    if payment["amount"] < 0: # перевіряємо чи платіж не відʼємний
        return records

    records.append(payment) # додаємо платіж
    return records

def list_payments(records): 
    return records

def find_payments(records, category=None, status=None):
    found = []

    for payment in records:
        if category is not None and payment["category"] != category: # пропускаємо платіж, якщо не збігається категорія
            continue

        if status is not None and payment["status"] != status: # пропускаємо платіж, якщо не збігається статус
            continue

        found.append(payment) # додаємо платіж

    return found

def update_payment(records, number, updates):
    if number < 1 or number > len(records): # перевіряємо, чи існує платіж із таким номером
        return records

    records[number - 1].update(updates)  # оновлюємо вказані поля платежу
    return records

def delete_payment(records, number):
    if number < 1 or number > len(records):
        return records

    del records[number - 1] # видаляємо платіж за його номером у списку
    return records

def make_report(records, month=None):
    # початкові суми для звіту
    total = 0 # загальна
    paid = 0 # оплачені
    unpaid = 0 # неоплачені
    by_category = {} # за категоріями

    for payment in records:
        if month is not None and not payment["due_date"].startswith(month): # якщо вказаний місяць, пропускаємо платежі з інших місяців
            continue
        # зберігаємо суму та категорію поточного платежу в змінні
        amount = payment["amount"]
        category = payment["category"]

        total += amount
        # розділяємо платежі за статусом
        if payment["status"] == "сплачено":
            paid += amount
        else:
            unpaid += amount
        # створюємо категорію в словнику, якщо ще немає
        if category not in by_category:
            by_category[category] = 0

        by_category[category] += amount
      # повертаємо звіт у вигляді словника 
    return {
        "total": total,
        "paid": paid,
        "unpaid": unpaid,
        "by_category": by_category
    }