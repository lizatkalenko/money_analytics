# Paylist
*програма, яка допомагає планувати обов'язкові витрати на наступний місяць та краще контролювати вільні гроші*
---

## Можливості застосунку
Додавання платежів — збереження назви, категорії, суми, дати та статусу платежу.

Перегляд платежів — відображення всіх збережених записів.

Пошук і фільтрація — пошук платежів за категорією та статусом.

Редагування платежів — зміна назви, категорії, суми, дати, статусу за номером запису або ж видалення.

Формування звітів — розрахунок загальної суми витрат, сплачених і несплачених сум, а також розподілу витрат за категоріями.

---

## Запуск через cli.py
### Додавання платежу
```python3 cli.py add "НАЗВА" "КАТЕГОРІЯ" СУМА ДАТА СТАТУС```

### Перегляд усіх платежів
```python3 cli.py list```

### Пошук платежів
Пошук за категорією:
```python3 cli.py find "КАТЕГОРІЯ"```

Пошук за категорією та статусом:
```python3 cli.py find "КАТЕГОРІЯ" "СТАТУС"```

*Якщо параметри пошуку не вказані, програма відображає всі платежі, що відповідають заданим умовам.*

### Редагування платежу
```python3 cli.py edit НОМЕР ПОЛЕ НОВЕ_ЗНАЧЕННЯ```

*Номер платежу можна переглянути за допомогою команди list. Редагувати можна такі поля: назва, категорія, сума, дата, статус.*

### Формування звіту
Звіт за всіма платежами:
```python3 cli.py report```

Звіт за конкретний місяць:
```python3 cli.py report 2026-12```

*У звіті можна переглянути загальну суму обовʼязкових платежів, суму сплачених і несплачених платежів та розподіл витрат за категоріями.*

---
## Запуск через app.py

```python app.py```
API відкривається за адресою http://127.0.0.1:5000.

### Додати запис
```bash 
curl -i -X POST http://127.0.0.1:5000/payments \
-H "Content-Type: application/json" \
-d '{"name": "ліки", "category": "здоровʼя", "amount": 250, "due_date": "2026-12-15", "status": "заплановано"}
```

### Редагування запису
```bash
curl -i -X PUT http://127.0.0.1:5000/payments/1 \
  -H "Content-Type: application/json" \
  -d '{"amount": 300}' 
```

### Перегляд записів
```bash
curl -i http://127.0.0.1:5000/payments
curl -i "http://127.0.0.1:5000/payments?category=їжа"
```
### Видалення записів
```curl -i -X DELETE http://127.0.0.1:5000/payments/1```

### Отримання звіту
```url -i http://127.0.0.1:5000/report```

### Формат даних
data.db — один запис: назва платежу; категорія; сума; дата платежу (РРРР-ММ-ДД); статус оплати.

## Розгортання
### Розгортання коду

cd ~
``` bash
git clone https://github.com/lizatkalenko/money_analytics.git
cd money_analytics
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
pip freeze > requirements.txt
```

### Запуск Gunicorn
```gunicorn -w 2 -b 127.0.0.1:8000 app:app```

### Налаштування автоматичного запуску через systemd
``` bash 
sudo cp deploy/myproject.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now myproject
sudo systemctl status myproject
```

### Налаштування Nginx
``` bash 
sudo cp deploy/nginx.conf /etc/nginx/sites-available/myproject
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

### Отримання HTTPS-сертифіката
``` bash 
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/local/bin/certbot
sudo certbot --nginx -d api.paylist.pp.ua
sudo certbot renew --dry-run
```

### Перевірка роботи API
```curl -i https://api.paylist.pp.ua/payments```

сайт відкривається за посиланням: https://api.paylist.pp.ua/payments.