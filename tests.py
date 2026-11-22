# перевірки функцій з файлу logic.py
from logic import (
    add_payment,
    list_payments,
    find_payments,
    update_payment,
    delete_payment,
    make_report,
)

payments = [
    {
        "name": "Netflix",
        "category": "Підписки",
        "amount": 300.0,
        "due_date": "2026-12-10",
        "status": "сплачено",
    },
    {
        "name": "Англійська",
        "category": "Навчання",
        "amount": 4500.0,
        "due_date": "2026-12-15",
        "status": "заплановано",
    },
    {
        "name": "Психолог",
        "category": "Здоровʼя",
        "amount": 7500.0,
        "due_date": "2027-01-05",
        "status": "скасовано",
    },
]

# тестування add_payment()
records = []
payment = payments[0].copy()
add_payment(records, payment)
assert len(records) == 1 and records[0] == payment

records = []
payment = payments[0].copy() # гранична, відʼємна сума
payment["amount"] = -100.0
add_payment(records, payment)
assert records == []

# тестування list_payments()
assert list_payments(payments) == payments
assert list_payments([]) == [] # гранична, порожній список

# тестування find_payments()
found = find_payments(
    payments, category="Навчання", status="заплановано"
)
assert len(found) == 1 and found[0]["name"] == "Англійська"
assert find_payments(payments, category="Розстрочки") == [] # гранична, відсутня категорія

# тестування update_payment()
records = [p.copy() for p in payments]
update_payment(records, 1, {"amount": 350.0})
assert records[0]["amount"] == 350.0

records = [p.copy() for p in payments] # гранична, неможлививй платіж
before = [p.copy() for p in records]
update_payment(records, 0, {"amount": 999.0})
assert records == before

# тестування delete_payment()
records = [p.copy() for p in payments]
delete_payment(records, 2)
assert len(records) == 2 and records[1]["name"] == "Психолог"

records = [p.copy() for p in payments] # гранична, відсутній платіж
before = [p.copy() for p in records]
delete_payment(records, len(records) + 1)
assert records == before

# тестування make_report()
report = make_report(payments, "2026-12")
assert report == {
    "total": 4800.0,
    "paid": 300.0,
    "unpaid": 4500.0,
    "by_category": {
        "Підписки": 300.0,
        "Навчання": 4500.0,
    },
}

assert make_report([]) == { 
    "total": 0,
    "paid": 0,
    "unpaid": 0,
    "by_category": {},
} # гранична, вдісутні дані

print("усі перевірки функцій з файлу logic.py пройдено")