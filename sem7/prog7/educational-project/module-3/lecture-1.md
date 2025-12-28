# Лекция 1: Автоматизация работы с документами

**Продолжительность:** 2 академических часа

## Цель лекции

Изучить методы автоматизации работы с офисными документами: Word, Excel и PDF. Научиться программно создавать и редактировать документы, что значительно ускорит рутинные задачи учителя.

---

## 1. Работа с Word документами (python-docx)

### Установка

```bash
pip install python-docx
```

### Создание простого документа

```python
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

# Создание нового документа
doc = Document()

# Добавление заголовка
doc.add_heading('Контрольная работа по математике', 0)

# Добавление параграфа
doc.add_paragraph('Класс: 9А')
doc.add_paragraph('Дата: 15.11.2025')
doc.add_paragraph('Фамилия, Имя: _________________________')

# Добавление заданий
doc.add_heading('Задание 1', level=2)
doc.add_paragraph('Решите уравнение: x² + 5x + 6 = 0')

doc.add_heading('Задание 2', level=2)
doc.add_paragraph('Найдите площадь треугольника со сторонами 3, 4, 5.')

# Сохранение
doc.save('контрольная_работа.docx')
print("✅ Документ создан!")
```

### Генерация заданий по шаблону

```python
from docx import Document
import random

def create_math_test(student_name, variant):
    """Создание контрольной работы для ученика"""
    doc = Document()
    
    doc.add_heading(f'Контрольная работа. Вариант {variant}', 0)
    doc.add_paragraph(f'Ученик: {student_name}')
    doc.add_paragraph('Класс: 9А')
    doc.add_paragraph('-' * 50)
    
    # Задание 1: Решение уравнения
    a = random.randint(1, 5)
    b = random.randint(1, 10)
    c = random.randint(1, 10)
    
    doc.add_heading('Задание 1 (3 балла)', level=2)
    doc.add_paragraph(f'Решите уравнение: {a}x² + {b}x + {c} = 0')
    doc.add_paragraph('Ответ: _________________________')
    doc.add_paragraph('')
    
    # Задание 2: Площадь треугольника
    side_a = random.randint(3, 15)
    side_b = random.randint(3, 15)
    side_c = random.randint(3, 15)
    
    doc.add_heading('Задание 2 (2 балла)', level=2)
    doc.add_paragraph(f'Найдите периметр треугольника со сторонами {side_a}, {side_b}, {side_c}.')
    doc.add_paragraph('Ответ: _________________________')
    doc.add_paragraph('')
    
    # Задание 3: Простая арифметика
    num1 = random.randint(10, 50)
    num2 = random.randint(10, 50)
    
    doc.add_heading('Задание 3 (2 балла)', level=2)
    doc.add_paragraph(f'Вычислите: {num1} × {num2} + {num1 + num2}')
    doc.add_paragraph('Ответ: _________________________')
    
    # Место для решения
    doc.add_page_break()
    doc.add_heading('Черновик', level=2)
    
    filename = f'контрольная_{student_name.replace(" ", "_")}_вариант_{variant}.docx'
    doc.save(filename)
    return filename

# Создание контрольных для класса
students = ['Иванов И.', 'Петрова М.', 'Сидоров П.']
for i, student in enumerate(students, 1):
    filename = create_math_test(student, i)
    print(f"✅ Создан файл: {filename}")
```

---

## 2. Работа с Excel (openpyxl)

### Установка

```bash
pip install openpyxl
```

### Создание и заполнение таблицы

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

# Создание книги
wb = Workbook()
ws = wb.active
ws.title = "Журнал успеваемости"

# Заголовки
headers = ['№', 'Ученик', 'Математика', 'Русский', 'Физика', 'Средний балл']
ws.append(headers)

# Форматирование заголовков
for cell in ws[1]:
    cell.font = Font(bold=True, size=12)
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    cell.font = Font(bold=True, color="FFFFFF")

# Данные учеников
students = [
    ['Иванов И.И.', 5, 4, 5],
    ['Петрова М.А.', 4, 5, 4],
    ['Сидоров П.С.', 3, 4, 3]
]

for i, (name, math, russian, physics) in enumerate(students, 1):
    avg = (math + russian + physics) / 3
    ws.append([i, name, math, russian, physics, round(avg, 2)])

# Формулы для средних баллов
ws['G1'] = 'Средний по предмету'
ws['G2'] = '=AVERAGE(C2:C4)'
ws['G3'] = '=AVERAGE(D2:D4)'
ws['G4'] = '=AVERAGE(E2:E4)'

# Автоподбор ширины столбцов
for column in ws.columns:
    max_length = 0
    column_letter = column[0].column_letter
    for cell in column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
        except:
            pass
    adjusted_width = (max_length + 2)
    ws.column_dimensions[column_letter].width = adjusted_width

wb.save('журнал_успеваемости.xlsx')
print("✅ Excel файл создан!")
```

### Чтение и обработка существующего Excel

```python
from openpyxl import load_workbook

# Открытие файла
wb = load_workbook('журнал_успеваемости.xlsx')
ws = wb.active

# Чтение данных
print("Данные из журнала:")
for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0]:  # Проверка, что строка не пустая
        print(f"{row[1]}: Математика={row[2]}, Русский={row[3]}, Физика={row[4]}, Средний={row[5]}")
```

---

## 3. Работа с PDF

### Создание PDF (reportlab)

```bash
pip install reportlab
```

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Регистрация шрифта для кириллицы (опционально)
# pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

def create_certificate(student_name, course_name, date):
    """Создание сертификата для ученика"""
    filename = f'сертификат_{student_name.replace(" ", "_")}.pdf'
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # Рамка
    c.setLineWidth(2)
    c.rect(2*cm, 2*cm, width-4*cm, height-4*cm)
    
    # Заголовок
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height-5*cm, "СЕРТИФИКАТ")
    
    # Текст
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height-8*cm, "Настоящим подтверждается, что")
    
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-10*cm, student_name)
    
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height-12*cm, "успешно завершил(а) курс")
    
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height-14*cm, course_name)
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height-18*cm, f"Дата: {date}")
    
    # Подпись
    c.line(width/2 - 5*cm, 5*cm, width/2 + 5*cm, 5*cm)
    c.drawCentredString(width/2, 4*cm, "Преподаватель")
    
    c.save()
    print(f"✅ Создан сертификат: {filename}")

# Создание сертификатов
create_certificate("Иванов Иван", "Основы программирования на Python", "15.11.2025")
```

### Чтение PDF (PyPDF2)

```bash
pip install PyPDF2
```

```python
import PyPDF2

def extract_text_from_pdf(filename):
    """Извлечение текста из PDF"""
    with open(filename, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        print(f"Количество страниц: {len(reader.pages)}")
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            print(f"\n--- Страница {page_num + 1} ---")
            print(text)

# Использование
extract_text_from_pdf('document.pdf')
```

---

## 4. Генерация отчётов

### Пример: Автоматический отчёт об успеваемости

```python
from docx import Document
from docx.shared import Pt, RGBColor
from datetime import datetime
import pandas as pd

def create_performance_report(class_name, data_file):
    """Создание отчёта об успеваемости класса"""
    
    # Загрузка данных
    df = pd.read_csv(data_file)
    
    # Создание документа
    doc = Document()
    
    # Заголовок
    title = doc.add_heading(f'Отчёт об успеваемости класса {class_name}', 0)
    title.alignment = 1  # Центрирование
    
    # Дата
    doc.add_paragraph(f'Дата формирования: {datetime.now().strftime("%d.%m.%Y")}')
    
    # Общая статистика
    doc.add_heading('1. Общая статистика', level=1)
    
    stats_text = f"""
Всего учеников: {len(df)}
Средний балл класса: {df['Средний_балл'].mean():.2f}
Отличников (≥4.5): {len(df[df['Средний_балл'] >= 4.5])}
Хорошистов (≥3.5): {len(df[(df['Средний_балл'] >= 3.5) & (df['Средний_балл'] < 4.5)])}
Троечников (<3.5): {len(df[df['Средний_балл'] < 3.5])}
"""
    doc.add_paragraph(stats_text)
    
    # Топ учеников
    doc.add_heading('2. Топ-5 учеников', level=1)
    
    top5 = df.nlargest(5, 'Средний_балл')
    for i, (_, student) in enumerate(top5.iterrows(), 1):
        doc.add_paragraph(
            f"{i}. {student['Ученик']}: {student['Средний_балл']:.2f}",
            style='List Number'
        )
    
    # Рекомендации
    doc.add_heading('3. Рекомендации', level=1)
    
    if df['Средний_балл'].mean() >= 4.0:
        doc.add_paragraph('✓ Успеваемость класса находится на высоком уровне.')
    else:
        doc.add_paragraph('⚠ Рекомендуется усилить работу с отстающими учениками.')
    
    # Сохранение
    filename = f'отчёт_{class_name}_{datetime.now().strftime("%Y%m%d")}.docx'
    doc.save(filename)
    print(f"✅ Отчёт создан: {filename}")

# Использование
# create_performance_report('9А', 'journal.csv')
```

---

## 5. Работа с шаблонами (Jinja2)

```bash
pip install jinja2
```

```python
from jinja2 import Template

# Шаблон документа
template_text = """
УВЕДОМЛЕНИЕ ДЛЯ РОДИТЕЛЕЙ

Уважаемые родители {{ student_name }}!

Информируем Вас об успеваемости вашего ребёнка за {{ period }}:

{% for subject, grade in grades.items() %}
- {{ subject }}: {{ grade }}
{% endfor %}

Средний балл: {{ average }}

{% if average >= 4.5 %}
Ваш ребёнок показывает отличные результаты!
{% elif average >= 3.5 %}
Успеваемость на хорошем уровне.
{% else %}
Рекомендуем обратить внимание на успеваемость.
{% endif %}

С уважением,
Классный руководитель
"""

# Использование шаблона
template = Template(template_text)

students_data = {
    'student_name': 'Иванова Ивана',
    'period': '1 четверть',
    'grades': {
        'Математика': 5,
        'Русский язык': 4,
        'Физика': 5
    },
    'average': 4.67
}

result = template.render(**students_data)
print(result)

# Сохранение в файл
with open('уведомление_родителям.txt', 'w', encoding='utf-8') as f:
    f.write(result)
```

---

## Домашнее задание

1. Создайте программу для генерации контрольных работ по вашему предмету (минимум 5 заданий, 3 варианта)
2. Создайте Excel-журнал с автоматическим расчётом средних баллов и статистики
3. Создайте шаблон отчёта об успеваемости в Word с использованием данных из Excel

---

## Полезные ресурсы

- [python-docx Documentation](https://python-docx.readthedocs.io/)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)
- [ReportLab Documentation](https://www.reportlab.com/docs/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)

---

## Вопросы для самопроверки

1. Как создать новый Word документ с помощью python-docx?
2. Как добавить формулы в Excel через openpyxl?
3. Для чего используется Jinja2?
4. Как извлечь текст из PDF файла?
5. Как автоматизировать создание однотипных документов?

