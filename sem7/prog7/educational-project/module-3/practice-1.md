# Практическая работа 1: Автоматическое генерирование заданий и тестов

**Продолжительность:** 4 академических часа  
**Модуль:** Автоматизация педагогических задач

## Цель работы

Создать систему автоматической генерации вариантов контрольных работ и тестов с различными параметрами сложности. Система должна генерировать уникальные задания для каждого ученика, сохранять результаты в документах Word и вести базу сгенерированных заданий.

---

## Задание

Разработать программу, которая:

1. **Генерирует математические задания** разных типов (уравнения, задачи, примеры)
2. **Создаёт несколько вариантов** контрольных работ (минимум 10)
3. **Сохраняет каждый вариант** в отдельный Word документ
4. **Создаёт файл с ответами** для учителя
5. **Поддерживает разные уровни сложности**
6. **Ведёт журнал** созданных вариантов

---

## Краткое решение

```python
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import random
import json
from datetime import datetime

class TestGenerator:
    """Генератор контрольных работ"""
    
    def __init__(self, subject="Математика", class_name="9А"):
        self.subject = subject
        self.class_name = class_name
        self.variants_log = []
    
    def generate_quadratic_equation(self):
        """Генерация квадратного уравнения"""
        a = random.randint(1, 5)
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        
        # Вычисление корней для ответа
        discriminant = b**2 - 4*a*c
        
        if discriminant >= 0:
            x1 = (-b + discriminant**0.5) / (2*a)
            x2 = (-b - discriminant**0.5) / (2*a)
            answer = f"x₁ = {x1:.2f}, x₂ = {x2:.2f}"
        else:
            answer = "Нет действительных корней"
        
        task = {
            'question': f"Решите уравнение: {a}x² + {b}x + {c} = 0",
            'answer': answer,
            'points': 3
        }
        return task
    
    def generate_arithmetic_task(self):
        """Генерация арифметической задачи"""
        num1 = random.randint(10, 100)
        num2 = random.randint(10, 100)
        operations = ['+', '-', '*']
        op = random.choice(operations)
        
        if op == '+':
            answer = num1 + num2
        elif op == '-':
            answer = num1 - num2
        else:
            answer = num1 * num2
        
        task = {
            'question': f"Вычислите: {num1} {op} {num2}",
            'answer': str(answer),
            'points': 1
        }
        return task
    
    def generate_word_problem(self):
        """Генерация текстовой задачи"""
        scenarios = [
            {
                'template': 'Товар стоил {price} руб. После скидки {discount}% его цена составила {final} руб. Какова была скидка в рублях?',
                'price': random.randint(1000, 5000),
                'discount': random.randint(10, 30)
            },
            {
                'template': 'Автомобиль проехал {distance} км за {time} часов. Какова средняя скорость?',
                'distance': random.randint(100, 500),
                'time': random.randint(2, 8)
            }
        ]
        
        scenario = random.choice(scenarios)
        
        if 'price' in scenario:
            price = scenario['price']
            discount = scenario['discount']
            final = price * (1 - discount/100)
            discount_amount = price - final
            question = scenario['template'].format(price=price, discount=discount, final=int(final))
            answer = f"{discount_amount:.0f} руб."
        else:
            distance = scenario['distance']
            time = scenario['time']
            speed = distance / time
            question = scenario['template'].format(distance=distance, time=time)
            answer = f"{speed:.1f} км/ч"
        
        task = {
            'question': question,
            'answer': answer,
            'points': 2
        }
        return task
    
    def generate_test_variant(self, variant_number, num_tasks=10):
        """Генерация варианта теста"""
        tasks = []
        
        # 40% квадратные уравнения
        for _ in range(int(num_tasks * 0.4)):
            tasks.append(self.generate_quadratic_equation())
        
        # 30% арифметика
        for _ in range(int(num_tasks * 0.3)):
            tasks.append(self.generate_arithmetic_task())
        
        # 30% текстовые задачи
        for _ in range(num_tasks - len(tasks)):
            tasks.append(self.generate_word_problem())
        
        random.shuffle(tasks)
        
        return {
            'variant': variant_number,
            'tasks': tasks,
            'total_points': sum(t['points'] for t in tasks),
            'date': datetime.now().strftime('%d.%m.%Y')
        }
    
    def create_word_document(self, variant_data, filename):
        """Создание Word документа с заданиями"""
        doc = Document()
        
        # Заголовок
        title = doc.add_heading(f'Контрольная работа по {self.subject}', 0)
        title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        
        # Информация
        info = doc.add_paragraph()
        info.add_run(f'Класс: {self.class_name}\n').bold = True
        info.add_run(f'Вариант: {variant_data["variant"]}\n').bold = True
        info.add_run(f'Дата: {variant_data["date"]}\n')
        info.add_run(f'Максимальный балл: {variant_data["total_points"]}\n')
        
        doc.add_paragraph('Фамилия, Имя: _' + '_' * 40)
        doc.add_paragraph('-' * 60)
        
        # Задания
        for i, task in enumerate(variant_data['tasks'], 1):
            doc.add_heading(f'Задание {i} ({task["points"]} балл.)', level=2)
            doc.add_paragraph(task['question'])
            doc.add_paragraph('\nОтвет: _' + '_' * 50 + '\n')
        
        # Черновик
        doc.add_page_break()
        doc.add_heading('Черновик', level=1)
        
        doc.save(filename)
        return filename
    
    def create_answers_document(self, all_variants, filename='ответы_учителя.docx'):
        """Создание документа с ответами для учителя"""
        doc = Document()
        
        title = doc.add_heading('ОТВЕТЫ К КОНТРОЛЬНЫМ РАБОТАМ', 0)
        title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        
        doc.add_paragraph(f'Предмет: {self.subject}')
        doc.add_paragraph(f'Класс: {self.class_name}')
        doc.add_paragraph(f'Дата: {datetime.now().strftime("%d.%m.%Y")}')
        doc.add_paragraph('=' * 60)
        
        for variant_data in all_variants:
            doc.add_heading(f'Вариант {variant_data["variant"]}', level=1)
            
            for i, task in enumerate(variant_data['tasks'], 1):
                p = doc.add_paragraph()
                p.add_run(f'Задание {i}: ').bold = True
                p.add_run(task['question'] + '\n')
                p.add_run('Ответ: ').bold = True
                answer_run = p.add_run(task['answer'])
                answer_run.font.color.rgb = RGBColor(0, 128, 0)
                doc.add_paragraph()
            
            doc.add_paragraph('-' * 60)
        
        doc.save(filename)
        return filename
    
    def save_log(self, filename='variants_log.json'):
        """Сохранение журнала вариантов"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.variants_log, f, ensure_ascii=False, indent=2)
        return filename
    
    def generate_all(self, num_variants=10, num_tasks=10):
        """Генерация всех вариантов"""
        print(f"\n{'='*60}")
        print(f"ГЕНЕРАЦИЯ КОНТРОЛЬНЫХ РАБОТ")
        print(f"{'='*60}\n")
        
        all_variants = []
        
        for i in range(1, num_variants + 1):
            print(f"Генерация варианта {i}/{num_variants}...", end=' ')
            
            variant_data = self.generate_test_variant(i, num_tasks)
            all_variants.append(variant_data)
            
            # Создание документа
            filename = f'контрольная_вариант_{i}.docx'
            self.create_word_document(variant_data, filename)
            
            # Добавление в журнал
            self.variants_log.append({
                'variant': i,
                'filename': filename,
                'date': variant_data['date'],
                'tasks_count': len(variant_data['tasks']),
                'total_points': variant_data['total_points']
            })
            
            print("✅")
        
        # Создание документа с ответами
        print("\nСоздание файла с ответами...", end=' ')
        answers_file = self.create_answers_document(all_variants)
        print("✅")
        
        # Сохранение журнала
        print("Сохранение журнала...", end=' ')
        log_file = self.save_log()
        print("✅")
        
        print(f"\n{'='*60}")
        print(f"ГЕНЕРАЦИЯ ЗАВЕРШЕНА!")
        print(f"{'='*60}")
        print(f"\nСоздано:")
        print(f"  - Вариантов контрольных: {num_variants}")
        print(f"  - Файл с ответами: {answers_file}")
        print(f"  - Журнал вариантов: {log_file}")
        print(f"\n{'='*60}\n")

# ИСПОЛЬЗОВАНИЕ
if __name__ == "__main__":
    generator = TestGenerator(subject="Математика", class_name="9А")
    generator.generate_all(num_variants=10, num_tasks=8)
```

---

## Критерии оценивания

| Критерий | Баллы |
|----------|-------|
| Генерация разных типов заданий | 20 |
| Создание Word документов | 20 |
| Файл с ответами для учителя | 15 |
| Уровни сложности | 15 |
| Журнал вариантов | 10 |
| Качество кода | 10 |
| Оформление документов | 10 |
| **Итого** | **100** |

---

## Дополнительные задания (бонусы)

1. **Генерация заданий по шаблонам** из файла (+10 баллов)
2. **Экспорт в PDF** вместо Word (+5 баллов)
3. **База данных заданий** для повторного использования (+10 баллов)
4. **Разные предметы** (не только математика) (+10 баллов)

Удачи! 📝

