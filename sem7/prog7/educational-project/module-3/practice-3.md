# Практическая работа 3: Разработка системы автоматического уведомления родителей

**Продолжительность:** 4 академических часа  
**Модуль:** Автоматизация педагогических задач

## Цель работы

Создать автоматизированную систему для отправки уведомлений родителям об успеваемости учеников через email. Система должна генерировать персонализированные отчёты, отправлять их по расписанию и вести журнал отправленных уведомлений.

---

## Задание

Разработать систему, которая:

1. **Загружает данные** об успеваемости из Excel/CSV
2. **Генерирует персонализированные отчёты** для каждого ученика
3. **Отправляет email** родителям с отчётами
4. **Работает по расписанию** (еженедельно/ежемесячно)
5. **Ведёт журнал** отправленных уведомлений
6. **Создаёт статистику** по отправкам

---

## Краткое решение

```python
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import schedule
import time
import json
from docx import Document
from docx.shared import Pt, RGBColor
import os

class NotificationSystem:
    """Система автоматических уведомлений родителям"""
    
    def __init__(self, smtp_config, journal_file):
        self.smtp_config = smtp_config
        self.journal_file = journal_file
        self.notification_log = []
        self.load_log()
    
    def load_log(self):
        """Загрузка журнала уведомлений"""
        try:
            with open('notification_log.json', 'r', encoding='utf-8') as f:
                self.notification_log = json.load(f)
        except:
            self.notification_log = []
    
    def save_log(self):
        """Сохранение журнала"""
        with open('notification_log.json', 'w', encoding='utf-8') as f:
            json.dump(self.notification_log, f, ensure_ascii=False, indent=2)
    
    def load_journal_data(self):
        """Загрузка данных журнала"""
        try:
            if self.journal_file.endswith('.csv'):
                df = pd.read_csv(self.journal_file, encoding='utf-8')
            else:
                df = pd.read_excel(self.journal_file)
            
            print(f"✅ Загружено {len(df)} записей")
            return df
        except Exception as e:
            print(f"❌ Ошибка загрузки данных: {e}")
            return None
    
    def generate_report_document(self, student_data, filename):
        """Генерация Word-отчёта"""
        doc = Document()
        
        # Заголовок
        title = doc.add_heading('ОТЧЁТ ОБ УСПЕВАЕМОСТИ', 0)
        title.alignment = 1
        
        # Дата
        doc.add_paragraph(f'Дата: {datetime.now().strftime("%d.%m.%Y")}')
        doc.add_paragraph(f'Период: {student_data.get("Период", "Текущая четверть")}')
        doc.add_paragraph('-' * 50)
        
        # Информация об ученике
        doc.add_heading('Информация об ученике', level=1)
        info = doc.add_paragraph()
        info.add_run('Ученик: ').bold = True
        info.add_run(f'{student_data["Ученик"]}\n')
        info.add_run('Класс: ').bold = True
        info.add_run(f'{student_data.get("Класс", "9А")}\n')
        
        # Оценки по предметам
        doc.add_heading('Оценки по предметам', level=1)
        
        subjects = [col for col in student_data.index if col not in ['Ученик', 'Класс', 'Email_родителя', 'Средний_балл', 'Период']]
        
        table = doc.add_table(rows=1, cols=2)
        table.style = 'Light Grid Accent 1'
        
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Предмет'
        hdr_cells[1].text = 'Оценка'
        
        for subject in subjects:
            row_cells = table.add_row().cells
            row_cells[0].text = subject
            row_cells[1].text = str(student_data[subject])
        
        # Средний балл
        doc.add_paragraph()
        avg_para = doc.add_paragraph()
        avg_para.add_run('Средний балл: ').bold = True
        avg_run = avg_para.add_run(f'{student_data["Средний_балл"]:.2f}')
        avg_run.font.size = Pt(14)
        
        if student_data["Средний_балл"] >= 4.5:
            avg_run.font.color.rgb = RGBColor(0, 128, 0)
        elif student_data["Средний_балл"] < 3.5:
            avg_run.font.color.rgb = RGBColor(255, 0, 0)
        
        # Комментарий
        doc.add_heading('Комментарий', level=1)
        
        if student_data["Средний_балл"] >= 4.5:
            comment = "Ваш ребёнок показывает отличные результаты! Так держать!"
        elif student_data["Средний_балл"] >= 3.5:
            comment = "Успеваемость на хорошем уровне. Есть потенциал для улучшения результатов."
        else:
            comment = "Рекомендуем обратить внимание на успеваемость. Предлагаем организовать дополнительные занятия."
        
        doc.add_paragraph(comment)
        
        # Рекомендации
        if student_data["Средний_балл"] < 4.0:
            doc.add_heading('Рекомендации', level=1)
            weak_subjects = [subj for subj in subjects if student_data[subj] < 4]
            if weak_subjects:
                doc.add_paragraph('Предметы, требующие внимания:')
                for subj in weak_subjects:
                    doc.add_paragraph(f'  • {subj} ({student_data[subj]})', style='List Bullet')
        
        # Подпись
        doc.add_paragraph()
        doc.add_paragraph('С уважением,')
        doc.add_paragraph('Классный руководитель')
        
        doc.save(filename)
        return filename
    
    def send_email(self, to_email, subject, body, attachment_path=None):
        """Отправка email"""
        message = MIMEMultipart()
        message["From"] = self.smtp_config['sender']
        message["To"] = to_email
        message["Subject"] = subject
        
        message.attach(MIMEText(body, "plain", "utf-8"))
        
        # Вложение
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {os.path.basename(attachment_path)}",
                )
                message.attach(part)
        
        try:
            with smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port']) as server:
                server.starttls()
                server.login(self.smtp_config['sender'], self.smtp_config['password'])
                server.send_message(message)
            return True
        except Exception as e:
            print(f"❌ Ошибка отправки на {to_email}: {e}")
            return False
    
    def send_notifications(self):
        """Массовая отправка уведомлений"""
        print(f"\n{'='*60}")
        print(f"ОТПРАВКА УВЕДОМЛЕНИЙ РОДИТЕЛЯМ")
        print(f"Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        df = self.load_journal_data()
        if df is None:
            return
        
        success_count = 0
        fail_count = 0
        
        for idx, student in df.iterrows():
            student_name = student['Ученик']
            parent_email = student.get('Email_родителя')
            
            if not parent_email or pd.isna(parent_email):
                print(f"⚠️  Пропущен {student_name}: нет email")
                continue
            
            print(f"📧 Отправка для {student_name}...", end=' ')
            
            # Генерация отчёта
            report_filename = f'отчёт_{student_name.replace(" ", "_")}.docx'
            self.generate_report_document(student, report_filename)
            
            # Формирование письма
            subject = f"Отчёт об успеваемости: {student_name}"
            
            avg = student['Средний_балл']
            body = f"""
Уважаемые родители {student_name}!

Направляем Вам отчёт об успеваемости за текущий период.

Средний балл: {avg:.2f}

{'✅ Ваш ребёнок показывает отличные результаты!' if avg >= 4.5 
 else '👍 Успеваемость на хорошем уровне.' if avg >= 3.5 
 else '⚠️  Рекомендуем обратить внимание на успеваемость.'}

Подробный отчёт во вложении.

При возникновении вопросов, пожалуйста, свяжитесь с классным руководителем.

С уважением,
Классный руководитель
"""
            
            # Отправка
            if self.send_email(parent_email, subject, body, report_filename):
                print("✅")
                success_count += 1
                
                # Запись в журнал
                self.notification_log.append({
                    'date': datetime.now().isoformat(),
                    'student': student_name,
                    'email': parent_email,
                    'average': float(avg),
                    'status': 'sent'
                })
            else:
                print("❌")
                fail_count += 1
                
                self.notification_log.append({
                    'date': datetime.now().isoformat(),
                    'student': student_name,
                    'email': parent_email,
                    'average': float(avg),
                    'status': 'failed'
                })
            
            # Удаление временного файла
            if os.path.exists(report_filename):
                os.remove(report_filename)
            
            time.sleep(2)  # Задержка между отправками
        
        self.save_log()
        
        print(f"\n{'='*60}")
        print(f"РЕЗУЛЬТАТЫ:")
        print(f"  ✅ Успешно отправлено: {success_count}")
        print(f"  ❌ Ошибок: {fail_count}")
        print(f"{'='*60}\n")
    
    def get_statistics(self):
        """Получение статистики"""
        if not self.notification_log:
            return "Статистика отсутствует"
        
        df = pd.DataFrame(self.notification_log)
        
        total = len(df)
        sent = len(df[df['status'] == 'sent'])
        failed = len(df[df['status'] == 'failed'])
        
        # Последняя отправка
        df['date'] = pd.to_datetime(df['date'])
        last_send = df['date'].max().strftime('%d.%m.%Y %H:%M')
        
        stats = f"""
╔═══════════════════════════════════════╗
║     СТАТИСТИКА УВЕДОМЛЕНИЙ            ║
╠═══════════════════════════════════════╣
║ Всего отправок: {total:20} ║
║ Успешно: {sent:27} ║
║ Ошибок: {failed:28} ║
║ Последняя отправка: {last_send:14} ║
╚═══════════════════════════════════════╝
"""
        return stats
    
    def schedule_notifications(self, time_str="18:00", day="monday"):
        """Настройка расписания"""
        if day == "daily":
            schedule.every().day.at(time_str).do(self.send_notifications)
            print(f"⏰ Уведомления будут отправляться ежедневно в {time_str}")
        elif day == "monday":
            schedule.every().monday.at(time_str).do(self.send_notifications)
            print(f"⏰ Уведомления будут отправляться по понедельникам в {time_str}")
        elif day == "friday":
            schedule.every().friday.at(time_str).do(self.send_notifications)
            print(f"⏰ Уведомления будут отправляться по пятницам в {time_str}")
    
    def run_scheduler(self):
        """Запуск планировщика"""
        print("\n🚀 Система автоматических уведомлений запущена!")
        print("Нажмите Ctrl+C для остановки\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n\n⏹️  Система остановлена")

# ИСПОЛЬЗОВАНИЕ
if __name__ == "__main__":
    # Конфигурация email
    smtp_config = {
        'server': 'smtp.gmail.com',
        'port': 587,
        'sender': 'teacher@example.com',
        'password': 'your_app_password'  # Используйте пароль приложения!
    }
    
    # Создание системы
    system = NotificationSystem(smtp_config, 'journal.csv')
    
    # Вариант 1: Отправить сейчас
    system.send_notifications()
    
    # Вариант 2: Настроить расписание
    # system.schedule_notifications(time_str="18:00", day="friday")
    # system.run_scheduler()
    
    # Статистика
    print(system.get_statistics())
```

---

## Критерии оценивания

| Критерий | Баллы |
|----------|-------|
| Загрузка данных из файла | 10 |
| Генерация персонализированных отчётов | 20 |
| Отправка email с вложениями | 20 |
| Работа по расписанию | 15 |
| Журнал отправок | 15 |
| Статистика | 10 |
| Обработка ошибок | 10 |
| **Итого** | **100** |

Удачи! 📧

