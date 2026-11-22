from storage import load, save

# перевірки функції load()
# перевіряємо функцію на відсутньому файлі
assert load("missing_file.txt") == [] 

# перевіряємо зчитування порожнього файлу
with open("empty_file.txt", "w", encoding="utf-8"):
    pass
assert load("empty_file.txt") == [] 

# перевіряємо зчитування правильного запису
with open("test_load.txt", "w", encoding="utf-8") as f: 
    f.write("Ліки;Здоровʼя;1000;2026-12-05;заплановано\n")

records = load("test_load.txt")
assert len(records) == 1 
assert records[0]["name"] == "Ліки" 

# перевіряємо пропускання пошкодженого запису
with open("test_load2.txt", "w", encoding="utf-8") as f: 
    f.write("Ліки;Здоровʼя;1000;2026-12-05;заплановано\n")
    f.write("Ютуб;Підписки;grgr;2026-12-21;заплановано\n")

records = load("test_load2.txt") 
assert len(records) == 1 
assert records[0]["name"] == "Ліки" 

print("усі перевірки для функції load() пройдено")

# перевірки функції save()
# перевіряємо чи зберігається запис правильно
records = [
    {
        "name": "Ліки",
        "category": "Здоровʼя",
        "amount": 1000.0,
        "due_date": "2026-12-05",
        "status": "заплановано"
    }
]

save("test_save.txt", records)

with open("test_save.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

assert len(lines) == 1
assert "Ліки" in lines[0]

# перевіряємо додавання другого запису
records.append(
    {
        "name": "Ютуб",
        "category": "Підписки",
        "amount": 299.0,
        "due_date": "2026-12-21",
        "status": "заплановано"
    }
)

save("test_save.txt", records)

with open("test_save.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

assert len(lines) == 2

print("усі перевірки для функції save() пройдено")