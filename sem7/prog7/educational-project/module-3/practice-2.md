# Практическая работа 2: Создание Telegram-бота для взаимодействия с учащимися

**Продолжительность:** 4 академических часа  
**Модуль:** Автоматизация педагогических задач

## Цель работы

Разработать Telegram-бота для образовательных целей, который позволяет проводить тестирование, отправлять материалы, собирать обратную связь и взаимодействовать с учениками в интерактивном режиме.

---

## Задание

Создать Telegram-бота, который включает:

1. **Систему тестирования** (минимум 15 вопросов по предмету)
2. **Отправку учебных материалов** (файлы, ссылки)
3. **Сбор обратной связи** (опросы, вопросы)
4. **Статистику прохождения** тестов
5. **Интерактивное меню** с кнопками
6. **Хранение данных** пользователей

---

## Краткое решение

```python
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import json
from datetime import datetime
import asyncio

# ТОКЕН БОТА (получите у @BotFather)
TOKEN = 'YOUR_BOT_TOKEN_HERE'

# База вопросов
QUESTIONS = [
    # Математика
    {'q': 'Чему равно 2+2?', 'options': ['3', '4', '5', '6'], 'correct': 1, 'subject': 'math'},
    {'q': 'Решите: 3*4', 'options': ['10', '11', '12', '13'], 'correct': 2, 'subject': 'math'},
    {'q': 'Что такое гипотенуза?', 'options': ['Катет', 'Сторона треугольника', 'Самая длинная сторона прямоугольного треугольника', 'Радиус'], 'correct': 2, 'subject': 'math'},
    {'q': 'Площадь квадрата со стороной 5?', 'options': ['20', '25', '30', '10'], 'correct': 1, 'subject': 'math'},
    {'q': 'Чему равен корень из 64?', 'options': ['6', '7', '8', '9'], 'correct': 2, 'subject': 'math'},
    
    # История
    {'q': 'В каком году началась ВОВ?', 'options': ['1939', '1941', '1942', '1945'], 'correct': 1, 'subject': 'history'},
    {'q': 'Кто был первым президентом России?', 'options': ['Горбачёв', 'Ельцин', 'Путин', 'Медведев'], 'correct': 1, 'subject': 'history'},
    {'q': 'В каком веке была Куликовская битва?', 'options': ['12 век', '13 век', '14 век', '15 век'], 'correct': 2, 'subject': 'history'},
    
    # Физика
    {'q': 'Скорость света в вакууме (км/с)?', 'options': ['300 000', '150 000', '500 000', '200 000'], 'correct': 0, 'subject': 'physics'},
    {'q': 'Единица измерения силы?', 'options': ['Джоуль', 'Ньютон', 'Ватт', 'Паскаль'], 'correct': 1, 'subject': 'physics'},
    
    # Информатика
    {'q': 'Что такое HTML?', 'options': ['Язык программирования', 'Язык разметки', 'База данных', 'ОС'], 'correct': 1, 'subject': 'cs'},
    {'q': '1 байт = ? бит', 'options': ['4', '8', '16', '32'], 'correct': 1, 'subject': 'cs'},
    {'q': 'Что делает цикл for?', 'options': ['Проверяет условие', 'Повторяет код', 'Создаёт функцию', 'Удаляет данные'], 'correct': 1, 'subject': 'cs'},
    
    # Русский язык
    {'q': 'Сколько падежей в русском языке?', 'options': ['4', '5', '6', '7'], 'correct': 2, 'subject': 'russian'},
    {'q': 'Что такое метафора?', 'options': ['Прямое значение', 'Переносное значение', 'Антоним', 'Синоним'], 'correct': 1, 'subject': 'russian'}
]

# Хранилище данных пользователей
user_data = {}
user_stats = {}

def load_user_stats():
    """Загрузка статистики"""
    global user_stats
    try:
        with open('user_stats.json', 'r', encoding='utf-8') as f:
            user_stats = json.load(f)
    except:
        user_stats = {}

def save_user_stats():
    """Сохранение статистики"""
    with open('user_stats.json', 'w', encoding='utf-8') as f:
        json.dump(user_stats, f, ensure_ascii=False, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user_id = str(update.effective_user.id)
    user_name = update.effective_user.first_name
    
    if user_id not in user_stats:
        user_stats[user_id] = {
            'name': user_name,
            'tests_completed': 0,
            'total_questions': 0,
            'correct_answers': 0,
            'joined_date': datetime.now().strftime('%d.%m.%Y')
        }
        save_user_stats()
    
    keyboard = [
        [InlineKeyboardButton("📝 Пройти тест", callback_data='start_test')],
        [InlineKeyboardButton("📚 Учебные материалы", callback_data='materials')],
        [InlineKeyboardButton("📊 Моя статистика", callback_data='stats')],
        [InlineKeyboardButton("💬 Задать вопрос", callback_data='question')],
        [InlineKeyboardButton("📋 Обратная связь", callback_data='feedback')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
👋 Привет, {user_name}!

Я образовательный бот для помощи в обучении.

🎓 Что я умею:
• Проводить тестирование по разным предметам
• Отправлять учебные материалы
• Собирать статистику ваших результатов
• Принимать обратную связь

Выберите действие:
"""
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопок"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if query.data == 'start_test':
        await show_test_menu(query)
    
    elif query.data.startswith('test_'):
        subject = query.data.split('_')[1]
        await start_test(query, user_id, subject)
    
    elif query.data.startswith('answer_'):
        answer_index = int(query.data.split('_')[1])
        await check_answer(query, user_id, answer_index)
    
    elif query.data == 'materials':
        await show_materials(query)
    
    elif query.data == 'stats':
        await show_stats(query, user_id)
    
    elif query.data == 'question':
        await query.edit_message_text(
            "❓ Задайте свой вопрос, и я передам его учителю.\n\n"
            "Просто напишите вопрос в следующем сообщении."
        )
        context.user_data['awaiting_question'] = True
    
    elif query.data == 'feedback':
        await query.edit_message_text(
            "💬 Напишите ваш отзыв или предложение.\n\n"
            "Ваше мнение очень важно для нас!"
        )
        context.user_data['awaiting_feedback'] = True
    
    elif query.data == 'back_to_menu':
        keyboard = [
            [InlineKeyboardButton("📝 Пройти тест", callback_data='start_test')],
            [InlineKeyboardButton("📚 Учебные материалы", callback_data='materials')],
            [InlineKeyboardButton("📊 Моя статистика", callback_data='stats')],
            [InlineKeyboardButton("💬 Задать вопрос", callback_data='question')],
            [InlineKeyboardButton("📋 Обратная связь", callback_data='feedback')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выберите действие:", reply_markup=reply_markup)

async def show_test_menu(query):
    """Меню выбора предмета для теста"""
    keyboard = [
        [InlineKeyboardButton("➕ Математика", callback_data='test_math')],
        [InlineKeyboardButton("📜 История", callback_data='test_history')],
        [InlineKeyboardButton("⚡ Физика", callback_data='test_physics')],
        [InlineKeyboardButton("💻 Информатика", callback_data='test_cs')],
        [InlineKeyboardButton("📖 Русский язык", callback_data='test_russian')],
        [InlineKeyboardButton("🏠 Все предметы", callback_data='test_all')],
        [InlineKeyboardButton("◀️ Назад", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "📝 Выберите предмет для тестирования:",
        reply_markup=reply_markup
    )

async def start_test(query, user_id, subject):
    """Начало теста"""
    # Выбор вопросов по предмету
    if subject == 'all':
        questions = QUESTIONS
    else:
        questions = [q for q in QUESTIONS if q['subject'] == subject]
    
    if not questions:
        await query.edit_message_text("❌ Вопросов по этому предмету пока нет.")
        return
    
    # Инициализация теста
    user_data[user_id] = {
        'current_question': 0,
        'score': 0,
        'questions': questions,
        'total': len(questions)
    }
    
    await send_question(query, user_id)

async def send_question(query, user_id):
    """Отправка вопроса"""
    if user_id not in user_data:
        await query.edit_message_text("❌ Ошибка! Начните тест заново.")
        return
    
    current = user_data[user_id]['current_question']
    questions = user_data[user_id]['questions']
    
    if current >= len(questions):
        await show_test_results(query, user_id)
        return
    
    question = questions[current]
    
    # Кнопки с вариантами
    keyboard = []
    for i, option in enumerate(question['options']):
        keyboard.append([InlineKeyboardButton(option, callback_data=f'answer_{i}')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"❓ Вопрос {current + 1} из {len(questions)}:\n\n{question['q']}",
        reply_markup=reply_markup
    )

async def check_answer(query, user_id, answer_index):
    """Проверка ответа"""
    if user_id not in user_data:
        return
    
    current = user_data[user_id]['current_question']
    questions = user_data[user_id]['questions']
    question = questions[current]
    
    is_correct = answer_index == question['correct']
    
    if is_correct:
        user_data[user_id]['score'] += 1
        feedback = "✅ Правильно!"
    else:
        correct_answer = question['options'][question['correct']]
        feedback = f"❌ Неправильно. Правильный ответ: {correct_answer}"
    
    user_data[user_id]['current_question'] += 1
    
    await query.edit_message_text(feedback)
    await asyncio.sleep(1)
    
    # Следующий вопрос
    if user_data[user_id]['current_question'] < len(questions):
        message = await query.message.reply_text("Следующий вопрос...")
        query.message = message
        await send_question(query, user_id)
    else:
        await show_test_results(query, user_id)

async def show_test_results(query, user_id):
    """Показ результатов"""
    score = user_data[user_id]['score']
    total = user_data[user_id]['total']
    percentage = (score / total) * 100
    
    # Обновление статистики
    user_stats[user_id]['tests_completed'] += 1
    user_stats[user_id]['total_questions'] += total
    user_stats[user_id]['correct_answers'] += score
    save_user_stats()
    
    if percentage >= 85:
        emoji = '🏆'
        grade = 'Отлично!'
    elif percentage >= 70:
        emoji = '👍'
        grade = 'Хорошо!'
    elif percentage >= 50:
        emoji = '📚'
        grade = 'Удовлетворительно'
    else:
        emoji = '📖'
        grade = 'Нужно подучиться'
    
    keyboard = [
        [InlineKeyboardButton("🔄 Пройти ещё раз", callback_data='start_test')],
        [InlineKeyboardButton("🏠 Главное меню", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        f"{emoji} Тест завершён!\n\n"
        f"Правильных ответов: {score} из {total}\n"
        f"Процент: {percentage:.0f}%\n"
        f"Оценка: {grade}",
        reply_markup=reply_markup
    )
    
    del user_data[user_id]

async def show_materials(query):
    """Показ учебных материалов"""
    text = """
📚 УЧЕБНЫЕ МАТЕРИАЛЫ

📖 Математика:
• [Учебник 9 класс](https://example.com)
• [Задачник](https://example.com)

📜 История:
• [Конспекты лекций](https://example.com)

💻 Информатика:
• [Python для начинающих](https://example.com)

Для получения файлов напишите /files
"""
    
    keyboard = [[InlineKeyboardButton("◀️ Назад", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup)

async def show_stats(query, user_id):
    """Показ статистики"""
    if user_id not in user_stats:
        await query.edit_message_text("У вас пока нет статистики.")
        return
    
    stats = user_stats[user_id]
    
    if stats['total_questions'] > 0:
        accuracy = (stats['correct_answers'] / stats['total_questions']) * 100
    else:
        accuracy = 0
    
    text = f"""
📊 ВАША СТАТИСТИКА

👤 Имя: {stats['name']}
📅 Дата регистрации: {stats['joined_date']}

🎯 Тестирование:
• Пройдено тестов: {stats['tests_completed']}
• Всего вопросов: {stats['total_questions']}
• Правильных ответов: {stats['correct_answers']}
• Точность: {accuracy:.1f}%
"""
    
    keyboard = [[InlineKeyboardButton("◀️ Назад", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    if context.user_data.get('awaiting_question'):
        # Сохранение вопроса
        with open('questions.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{datetime.now()}: {update.message.from_user.first_name} - {update.message.text}")
        
        await update.message.reply_text("✅ Ваш вопрос передан учителю!")
        context.user_data['awaiting_question'] = False
    
    elif context.user_data.get('awaiting_feedback'):
        # Сохранение отзыва
        with open('feedback.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{datetime.now()}: {update.message.from_user.first_name} - {update.message.text}")
        
        await update.message.reply_text("✅ Спасибо за ваш отзыв!")
        context.user_data['awaiting_feedback'] = False

def main():
    """Главная функция"""
    load_user_stats()
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("🤖 Образовательный бот запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()
```

---

## Критерии оценивания

| Критерий | Баллы |
|----------|-------|
| Система тестирования (15+ вопросов) | 25 |
| Интерактивное меню с кнопками | 15 |
| Отправка материалов | 10 |
| Статистика пользователей | 15 |
| Сбор обратной связи | 10 |
| Сохранение данных | 15 |
| Качество кода и оформление | 10 |
| **Итого** | **100** |

Удачи! 🤖

