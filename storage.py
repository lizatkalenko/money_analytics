def load(filename):
    records = []
    try:  
        f = open(filename, "r", encoding="utf-8")
    except FileNotFoundError:
        return records 
    with f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            parts = line.split(";")
            try:
                record = {
                    "name": parts[0],
                    "category": parts[1],
                    "amount": float(parts[2]),
                    "due_date": parts[3],
                    "status": parts[4],
                }
            except (IndexError, ValueError):
                print("пропущено пошкоджений рядок:", line)
                continue
            records.append(record)
    return records

def save(filename, records):
    with open(filename, "w", encoding="utf-8") as f:
        for r in records:
            f.write(f"{r['name']};{r['category']};{r['amount']};{r['due_date']};{r['status']}\n")

