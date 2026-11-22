import sys
import storage
import logic

FILE = "data.txt"

def main():
    if len(sys.argv) < 2:
        print("Потрібно вибрати функцію: add, list, find або report")
        return

    command = sys.argv[1]
    records = storage.load(FILE)

    if command == "add":
        if len(sys.argv) != 7:
            print(
                "Використання: python cli.py add "
                '"НАЗВА" "КАТЕГОРІЯ" СУМА ДАТА СТАТУС'
            )
            return

        try:
            amount = float(sys.argv[4])
        except ValueError:
            print("Помилка: сума має бути числом")
            return

        if amount < 0:
            print("Помилка: сума не може бути від'ємною")
            return

        payment = {
            "name": sys.argv[2],
            "category": sys.argv[3],
            "amount": amount,
            "due_date": sys.argv[5],
            "status": sys.argv[6],
        }

        logic.add_payment(records, payment)
        storage.save(FILE, records)
        print("Платіж додано")

    elif command == "list":
        if not records:
            print("Платежів поки немає")
            return

        for number, payment in enumerate(records, start=1):
            print(
                f"{number}. {payment['name']} | "
                f"{payment['category']} | "
                f"{payment['amount']:.2f} грн | "
                f"{payment['due_date']} | "
                f"{payment['status']}"
            )

    elif command == "find":
        category = None
        status = None

        if len(sys.argv) > 2:
            category = sys.argv[2]

        if len(sys.argv) > 3:
            status = sys.argv[3]

        found = logic.find_payments(records, category, status)

        if not found:
            print("Платежів за заданими умовами не знайдено")
            return

        for payment in found:
            print(
                f"{payment['name']} | "
                f"{payment['category']} | "
                f"{payment['amount']:.2f} грн | "
                f"{payment['due_date']} | "
                f"{payment['status']}"
            )

    elif command == "report":
        month = sys.argv[2] if len(sys.argv) > 2 else None
        report = logic.make_report(records, month)

        print(f"Загальна сума: {report['total']:.2f} грн")
        print(f"Сплачено: {report['paid']:.2f} грн")
        print(f"Не сплачено: {report['unpaid']:.2f} грн")
        print("Суми за категоріями:")

        if not report["by_category"]:
            print("Платежів немає")
        else:
            for category, amount in report["by_category"].items():
                print(f"{category}: {amount:.2f} грн")

    elif command == "edit":
        if len(sys.argv) != 5:
            print(
                "Використання: python3 cli.py edit "
                "НОМЕР ПОЛЕ НОВЕ_ЗНАЧЕННЯ"
            )
            print("Доступні поля: назва, категорія, сума, дата, статус")
            return

        try:
            number = int(sys.argv[2])
        except ValueError:
            print("Помилка: номер платежу має бути цілим числом")
            return

        field_names = {
            "назва": "name",
            "категорія": "category",
            "сума": "amount",
            "дата": "due_date",
            "статус": "status",
        }

        field = field_names.get(sys.argv[3].lower())
        value = sys.argv[4]

        if field is None:
            print("Помилка: невідоме поле")
            print("Доступні поля: назва, категорія, сума, дата, статус")
            return

        if field == "amount":
            try:
                value = float(value)
            except ValueError:
                print("Помилка: сума має бути числом")
                return

            if value < 0:
                print("Помилка: сума не може бути від'ємною")
                return

        if number < 1 or number > len(records):
            print("Помилка: такого номера платежу немає")
            return

        logic.update_payment(records, number, {field: value})
        storage.save(FILE, records)
        print("Платіж оновлено")
        
    else:
        print("Невідома команда:", command)


if __name__ == "__main__":
    main()