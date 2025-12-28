# Лекция 2: Создание ботов для образовательных платформ

**Продолжительность:** 2 академических часа

## Цель лекции

Научиться создавать Telegram-ботов для образовательных целей: проведение опросов, тестирования, консультаций, отправка материалов.

---

## 1. Введение в Telegram Bot API

### Создание бота

1. Найдите в Telegram: **@BotFather**
2. Отправьте команду: `/newbot`
3. Придумайте имя бота: `МойОбразовательныйБот`
4. Придумайте username: `my_edu_bot` (должен заканчиваться на `bot`)
5. Получите **токен** (храните в секрете!)

### Установка библиотеки

```bash
pip install python-telegram-bot
```

---

## 2. Первый простой бот

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Ваш токен от BotFather
TOKEN = 'YOUR_BOT_TOKEN_HERE'

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Привет! Я образовательный бот.\n'
        'Используй /help для списка команд.'
    )

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
Доступные команды:
/start - Начать работу
/help - Помощь
/test - Пройти тест
/schedule - Расписание
"""
    await update.message.reply_text(help_text)

# Обработчик текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Вы написали: {update.message.text}')

# Главная функция
def main():
    # Создание приложения
    application = Application.builder().token(TOKEN).build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Запуск бота
    print("Бот запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()
```

---

## 3. Образовательный бот с тестированием

```python
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = 'YOUR_BOT_TOKEN_HERE'

# База вопросов
QUESTIONS = [
    {
        'question': 'Сколько будет 2+2?',
        'options': ['3', '4', '5', '6'],
        'correct': 1
    },
    {
        'question': 'Столица России?',
        'options': ['Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск'],
        'correct': 0
    },
    {
        'question': 'Сколько дней в неделе?',
        'options': ['5', '6', '7', '8'],
        'correct': 2
    }
]

# Хранилище данных пользователей
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие"""
    keyboard = [
        [InlineKeyboardButton("📝 Пройти тест", callback_data='start_test')],
        [InlineKeyboardButton("📊 Моя статистика", callback_data='stats')],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        '👋 Привет! Я образовательный бот.\n\n'
        'Выбери действие:',
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == 'start_test':
        # Инициализация теста
        user_data[user_id] = {
            'current_question': 0,
            'score': 0,
            'total': len(QUESTIONS)
        }
        await send_question(query, user_id)
    
    elif query.data.startswith('answer_'):
        # Обработка ответа
        answer_index = int(query.data.split('_')[1])
        await check_answer(query, user_id, answer_index)
    
    elif query.data == 'stats':
        await show_stats(query, user_id)
    
    elif query.data == 'help':
        await query.edit_message_text(
            'ℹ️ Помощь:\n\n'
            '1. Нажмите "Пройти тест" для начала\n'
            '2. Отвечайте на вопросы\n'
            '3. Получите результат\n\n'
            'Используйте /start для возврата в меню'
        )

async def send_question(query, user_id):
    """Отправка вопроса"""
    if user_id not in user_data:
        await query.edit_message_text('Ошибка! Начните тест заново командой /start')
        return
    
    current = user_data[user_id]['current_question']
    
    if current >= len(QUESTIONS):
        await show_results(query, user_id)
        return
    
    question_data = QUESTIONS[current]
    
    # Создание кнопок с вариантами ответа
    keyboard = []
    for i, option in enumerate(question_data['options']):
        keyboard.append([InlineKeyboardButton(option, callback_data=f'answer_{i}')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"❓ Вопрос {current + 1} из {len(QUESTIONS)}:\n\n"
        f"{question_data['question']}",
        reply_markup=reply_markup
    )

async def check_answer(query, user_id, answer_index):
    """Проверка ответа"""
    if user_id not in user_data:
        await query.edit_message_text('Ошибка! Начните тест заново командой /start')
        return
    
    current = user_data[user_id]['current_question']
    question_data = QUESTIONS[current]
    
    is_correct = answer_index == question_data['correct']
    
    if is_correct:
        user_data[user_id]['score'] += 1
        feedback = '✅ Правильно!'
    else:
        correct_answer = question_data['options'][question_data['correct']]
        feedback = f'❌ Неправильно. Правильный ответ: {correct_answer}'
    
    # Переход к следующему вопросу
    user_data[user_id]['current_question'] += 1
    
    await query.edit_message_text(feedback)
    
    # Небольшая задержка перед следующим вопросом
    import asyncio
    await asyncio.sleep(1)
    
    if user_data[user_id]['current_question'] < len(QUESTIONS):
        # Отправка следующего вопроса
        message = await query.message.reply_text('Следующий вопрос...')
        # Обновляем объект query для следующего вопроса
        query.message = message
        await send_question(query, user_id)
    else:
        await show_results(query, user_id)

async def show_results(query, user_id):
    """Показ результатов"""
    if user_id not in user_data:
        return
    
    score = user_data[user_id]['score']
    total = user_data[user_id]['total']
    percentage = (score / total) * 100
    
    if percentage >= 80:
        emoji = '🏆'
        message = 'Отлично!'
    elif percentage >= 60:
        emoji = '👍'
        message = 'Хорошо!'
    else:
        emoji = '📚'
        message = 'Нужно подтянуть знания'
    
    keyboard = [[InlineKeyboardButton("🔄 Пройти ещё раз", callback_data='start_test')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        f'{emoji} Тест завершён!\n\n'
        f'Результат: {score} из {total} ({percentage:.0f}%)\n'
        f'{message}',
        reply_markup=reply_markup
    )

async def show_stats(query, user_id):
    """Показ статистики"""
    if user_id in user_data and 'score' in user_data[user_id]:
        score = user_data[user_id]['score']
        total = user_data[user_id]['total']
        await query.edit_message_text(
            f'📊 Ваша статистика:\n\n'
            f'Последний результат: {score}/{total}\n\n'
            'Используйте /start для возврата в меню'
        )
    else:
        await query.edit_message_text(
            '📊 Вы ещё не проходили тесты.\n\n'
            'Используйте /start для возврата в меню'
        )

def main():
    """Главная функция"""
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 Образовательный бот запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()
```

---

## 4. Отправка файлов и документов

```python
async def send_materials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка учебных материалов"""
    
    # Отправка текстового файла
    with open('лекция.txt', 'rb') as file:
        await update.message.reply_document(
            document=file,
            filename='Лекция_1.txt',
            caption='📄 Материалы лекции'
        )
    
    # Отправка изображения
    with open('схема.png', 'rb') as photo:
        await update.message.reply_photo(
            photo=photo,
            caption='📊 Схема по теме'
        )
    
    # Отправка PDF
    with open('задания.pdf', 'rb') as pdf:
        await update.message.reply_document(
            document=pdf,
            filename='Задания_для_практики.pdf'
        )
```

---

## 5. Расписание и напоминания

```python
from datetime import time

async def set_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Ежедневное напоминание"""
    job = context.job
    await context.bot.send_message(
        chat_id=job.chat_id,
        text='⏰ Напоминание: Не забудьте выполнить домашнее задание!'
    )

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Установка напоминания"""
    chat_id = update.effective_chat.id
    
    # Напоминание каждый день в 18:00
    context.job_queue.run_daily(
        set_reminder,
        time=time(hour=18, minute=0),
        chat_id=chat_id,
        name=str(chat_id)
    )
    
    await update.message.reply_text(
        '✅ Напоминание установлено!\n'
        'Вы будете получать уведомления каждый день в 18:00'
    )
```

---

## Домашнее задание

Создать Telegram-бота для вашего предмета, который включает:
1. Команды /start, /help
2. Викторину (минимум 10 вопросов)
3. Отправку учебных материалов
4. Статистику прохождения тестов
5. Интерактивные кнопки

---

## Полезные ресурсы

- [python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Примеры ботов](https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples)

Удачи! 🤖

