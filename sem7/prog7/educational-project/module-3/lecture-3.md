# Лекция 3: Интеграция различных образовательных сервисов

**Продолжительность:** 2 академических часа

## Цель лекции

Научиться интегрировать различные сервисы и API для автоматизации работы учителя: отправка email, работа с облачными хранилищами, планирование задач.

---

## 1. Отправка Email (smtplib)

### Простая отправка письма

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(to_email, subject, body, attachment_path=None):
    """Отправка email с вложением"""
    
    # Настройки SMTP (пример для Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"  # Используйте пароль приложения!
    
    # Создание сообщения
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    
    # Добавление текста письма
    message.attach(MIMEText(body, "plain", "utf-8"))
    
    # Добавление вложения
    if attachment_path:
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachment_path}",
            )
            message.attach(part)
    
    # Отправка
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        print(f"✅ Письмо отправлено на {to_email}")
        return True
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        return False

# Использование
send_email(
    to_email="parent@example.com",
    subject="Уведомление об успеваемости",
    body="Уважаемые родители! Ваш ребёнок показывает отличные результаты.",
    attachment_path="отчёт.pdf"
)
```

### Массовая рассылка родителям

```python
import pandas as pd
import time

def send_bulk_notifications(csv_file):
    """Массовая рассылка уведомлений"""
    
    # Загрузка данных
    df = pd.read_csv(csv_file)
    
    for _, row in df.iterrows():
        student_name = row['Ученик']
        parent_email = row['Email_родителя']
        average_grade = row['Средний_балл']
        
        # Формирование письма
        subject = f"Успеваемость: {student_name}"
        body = f"""
Уважаемые родители {student_name}!

Информируем Вас об успеваемости за текущий период:

Средний балл: {average_grade}

{"Ваш ребёнок показывает отличные результаты!" if average_grade >= 4.5 
 else "Успеваемость на хорошем уровне." if average_grade >= 3.5 
 else "Рекомендуем обратить внимание на успеваемость."}

С уважением,
Классный руководитель
"""
        
        send_email(parent_email, subject, body)
        time.sleep(2)  # Задержка между письмами
```

---

## 2. Работа с Google Drive API

### Настройка

1. Перейдите на https://console.cloud.google.com/
2. Создайте проект
3. Включите Google Drive API
4. Создайте Service Account
5. Скачайте JSON с credentials

### Установка библиотеки

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Загрузка файла на Google Drive

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def upload_to_drive(file_path, file_name, folder_id=None):
    """Загрузка файла на Google Drive"""
    
    # Авторизация
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    service = build('drive', 'v3', credentials=credentials)
    
    # Метаданные файла
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    
    # Загрузка
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()
    
    print(f"✅ Файл загружен: {file.get('webViewLink')}")
    return file

# Использование
upload_to_drive('отчёт.pdf', 'Отчёт_9А_класс.pdf')
```

---

## 3. Планировщик задач (schedule)

```bash
pip install schedule
```

### Автоматические напоминания и отчёты

```python
import schedule
import time
from datetime import datetime

def daily_report():
    """Ежедневный отчёт"""
    print(f"📊 Формирование отчёта за {datetime.now().strftime('%d.%m.%Y')}")
    # Здесь код для создания и отправки отчёта
    
def weekly_summary():
    """Еженедельная сводка"""
    print("📈 Еженедельная сводка успеваемости")
    # Здесь код для еженедельной сводки

def homework_reminder():
    """Напоминание о домашнем задании"""
    print("📚 Отправка напоминания о домашнем задании")
    # Отправка уведомлений

# Настройка расписания
schedule.every().day.at("18:00").do(homework_reminder)
schedule.every().day.at("20:00").do(daily_report)
schedule.every().monday.at("09:00").do(weekly_summary)

print("⏰ Планировщик запущен!")

# Запуск
while True:
    schedule.run_pending()
    time.sleep(60)  # Проверка каждую минуту
```

---

## 4. Работа с API (requests)

```bash
pip install requests
```

### Пример: Получение информации о погоде

```python
import requests

def get_weather(city):
    """Получение погоды (пример API)"""
    api_key = "YOUR_API_KEY"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        
        return f"Погода в {city}: {temp}°C, {description}"
    except Exception as e:
        return f"Ошибка: {e}"

print(get_weather("Moscow"))
```

---

## 5. Комплексный пример: Система автоматизации

```python
import schedule
import time
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EducationAutomationSystem:
    """Система автоматизации для учителя"""
    
    def __init__(self, journal_file, email_config):
        self.journal_file = journal_file
        self.email_config = email_config
    
    def load_data(self):
        """Загрузка данных журнала"""
        return pd.read_csv(self.journal_file)
    
    def send_email(self, to_email, subject, body):
        """Отправка email"""
        message = MIMEMultipart()
        message["From"] = self.email_config['sender']
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain", "utf-8"))
        
        try:
            with smtplib.SMTP(self.email_config['server'], self.email_config['port']) as server:
                server.starttls()
                server.login(self.email_config['sender'], self.email_config['password'])
                server.send_message(message)
            return True
        except Exception as e:
            print(f"Ошибка отправки: {e}")
            return False
    
    def daily_summary(self):
        """Ежедневная сводка"""
        print(f"\n{'='*50}")
        print(f"📊 Ежедневная сводка за {datetime.now().strftime('%d.%m.%Y')}")
        print(f"{'='*50}\n")
        
        df = self.load_data()
        print(f"Всего учеников: {len(df)}")
        print(f"Средний балл класса: {df['Средний_балл'].mean():.2f}")
        
        # Проверка отстающих
        struggling = df[df['Средний_балл'] < 3.5]
        if len(struggling) > 0:
            print(f"\n⚠️  Учеников с низкой успеваемостью: {len(struggling)}")
            for _, student in struggling.iterrows():
                print(f"  - {student['Ученик']}: {student['Средний_балл']:.2f}")
    
    def weekly_report(self):
        """Еженедельный отчёт родителям"""
        print("\n📧 Отправка еженедельных отчётов родителям...")
        
        df = self.load_data()
        
        for _, row in df.iterrows():
            if pd.notna(row.get('Email_родителя')):
                subject = f"Еженедельный отчёт: {row['Ученик']}"
                body = f"""
Уважаемые родители {row['Ученик']}!

Еженедельный отчёт об успеваемости:

Средний балл: {row['Средний_балл']}

{'✅ Отличные результаты!' if row['Средний_балл'] >= 4.5 
 else '👍 Хорошая успеваемость' if row['Средний_балл'] >= 3.5 
 else '📚 Требуется дополнительная работа'}

С уважением,
Классный руководитель
"""
                self.send_email(row['Email_родителя'], subject, body)
                time.sleep(2)
        
        print("✅ Отчёты отправлены!")
    
    def homework_reminder(self):
        """Напоминание о домашнем задании"""
        print("\n📚 Напоминание о проверке домашних заданий")
        # Здесь может быть интеграция с системой домашних заданий
    
    def run(self):
        """Запуск системы"""
        # Настройка расписания
        schedule.every().day.at("18:00").do(self.homework_reminder)
        schedule.every().day.at("20:00").do(self.daily_summary)
        schedule.every().monday.at("09:00").do(self.weekly_report)
        
        print("🚀 Система автоматизации запущена!")
        print("\nРасписание:")
        print("  18:00 - Напоминание о домашних заданиях")
        print("  20:00 - Ежедневная сводка")
        print("  Пн 09:00 - Еженедельный отчёт родителям\n")
        
        # Запуск
        while True:
            schedule.run_pending()
            time.sleep(60)

# Использование
if __name__ == "__main__":
    email_config = {
        'server': 'smtp.gmail.com',
        'port': 587,
        'sender': 'teacher@example.com',
        'password': 'app_password'
    }
    
    system = EducationAutomationSystem('journal.csv', email_config)
    system.run()
```

---

## Домашнее задание

1. Создайте скрипт для автоматической отправки уведомлений родителям об успеваемости
2. Настройте планировщик для еженедельной отправки отчётов
3. Интегрируйте систему с Google Drive для хранения отчётов

---

## Полезные ресурсы

- [smtplib Documentation](https://docs.python.org/3/library/smtplib.html)
- [Google Drive API Documentation](https://developers.google.com/drive/api/v3/about-sdk)
- [schedule Documentation](https://schedule.readthedocs.io/)
- [requests Documentation](https://requests.readthedocs.io/)

Удачи! 🚀

