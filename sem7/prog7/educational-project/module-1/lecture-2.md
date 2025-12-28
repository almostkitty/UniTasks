# Лекция 2: JavaScript и интерактивность на веб-страницах

**Продолжительность:** 2 академических часа

## План лекции

1. Введение в JavaScript для образовательных проектов (15 минут)
2. Основы синтаксиса и работа с DOM (35 минут)
3. События и обработка пользовательского ввода (25 минут)
4. Создание интерактивных образовательных элементов (25 минут)
5. Практическая демонстрация (10 минут)

---

## 1. Введение в JavaScript для образовательных проектов

### Что такое JavaScript?

JavaScript - это язык программирования, который делает веб-страницы интерактивными. Если HTML - это структура, а CSS - это оформление, то JavaScript - это поведение и логика.

### Зачем педагогу JavaScript?

**Образовательные возможности:**
- ✅ Интерактивные тесты с мгновенной проверкой
- ✅ Образовательные игры и симуляции
- ✅ Калькуляторы и конвертеры для задач
- ✅ Анимированные объяснения сложных концепций
- ✅ Динамические формы обратной связи
- ✅ Таймеры для контрольных работ
- ✅ Визуализация данных и графиков

### Примеры применения

1. **Тест по истории** с подсчётом баллов
2. **Интерактивная таблица умножения**
3. **Симулятор физических процессов**
4. **Викторина с таймером**
5. **Генератор примеров для устного счёта**

### Способы подключения JavaScript

**1. Внешний файл (рекомендуется):**
```html
<script src="script.js"></script>
```

**2. Внутри HTML:**
```html
<script>
    console.log('Привет, мир!');
</script>
```

**3. Inline (не рекомендуется):**
```html
<button onclick="alert('Привет!')">Нажми</button>
```

---

## 2. Основы синтаксиса и работа с DOM

### Основные типы данных

```javascript
// Числа
let age = 15;
let pi = 3.14;

// Строки
let name = "Иван";
let greeting = 'Привет, ' + name + '!';
let template = `Привет, ${name}!`; // Шаблонные строки

// Булевы значения
let isPassed = true;
let isFailed = false;

// Массивы
let grades = [5, 4, 5, 3, 4];
let students = ["Иван", "Мария", "Пётр"];

// Объекты
let student = {
    name: "Иван",
    age: 15,
    grade: 9,
    subjects: ["математика", "физика"]
};
```

### Переменные

```javascript
// let - изменяемая переменная (блочная область видимости)
let score = 0;
score = 5; // можно изменить

// const - константа (нельзя переназначить)
const MAX_SCORE = 100;

// var - старый способ (не рекомендуется)
```

### Операторы

```javascript
// Арифметические
let sum = 10 + 5;        // 15
let diff = 10 - 5;       // 5
let product = 10 * 5;    // 50
let quotient = 10 / 5;   // 2
let remainder = 10 % 3;  // 1 (остаток от деления)

// Сравнение
5 == "5"   // true (сравнение значений)
5 === "5"  // false (сравнение значений и типов)
5 != 3     // true
5 > 3      // true
5 <= 5     // true

// Логические
true && false  // false (И)
true || false  // true (ИЛИ)
!true          // false (НЕ)
```

### Условные конструкции

```javascript
// if-else
let score = 85;
if (score >= 90) {
    console.log("Отлично!");
} else if (score >= 75) {
    console.log("Хорошо!");
} else if (score >= 60) {
    console.log("Удовлетворительно");
} else {
    console.log("Нужно подтянуть знания");
}

// Тернарный оператор
let result = score >= 75 ? "Сдал" : "Не сдал";
```

### Циклы

```javascript
// for - когда знаем количество итераций
for (let i = 0; i < 5; i++) {
    console.log(i); // 0, 1, 2, 3, 4
}

// while - когда не знаем количество итераций
let attempts = 0;
while (attempts < 3) {
    console.log("Попытка " + attempts);
    attempts++;
}

// forEach - для массивов
let grades = [5, 4, 5, 3, 4];
grades.forEach(function(grade) {
    console.log("Оценка: " + grade);
});
```

### Функции

```javascript
// Объявление функции
function calculateAverage(grades) {
    let sum = 0;
    for (let i = 0; i < grades.length; i++) {
        sum += grades[i];
    }
    return sum / grades.length;
}

// Использование
let studentGrades = [5, 4, 5, 3, 4];
let average = calculateAverage(studentGrades);
console.log("Средний балл: " + average); // 4.2

// Стрелочные функции (современный синтаксис)
const multiply = (a, b) => a * b;
console.log(multiply(5, 3)); // 15
```

### Работа с DOM (Document Object Model)

DOM - это представление HTML-документа в виде дерева объектов, с которым можно работать через JavaScript.

**Выбор элементов:**

```javascript
// По ID
let title = document.getElementById('main-title');

// По классу
let buttons = document.getElementsByClassName('btn');

// По селектору CSS (один элемент)
let firstButton = document.querySelector('.btn');

// По селектору CSS (все элементы)
let allButtons = document.querySelectorAll('.btn');
```

**Изменение содержимого:**

```javascript
// Изменить текст
let heading = document.getElementById('title');
heading.textContent = "Новый заголовок";

// Изменить HTML
let container = document.getElementById('content');
container.innerHTML = '<p>Новый <strong>параграф</strong></p>';
```

**Изменение стилей:**

```javascript
let box = document.getElementById('box');
box.style.backgroundColor = 'blue';
box.style.fontSize = '20px';
box.style.display = 'none'; // скрыть элемент
```

**Работа с классами:**

```javascript
let element = document.getElementById('myElement');

// Добавить класс
element.classList.add('active');

// Удалить класс
element.classList.remove('active');

// Переключить класс (добавить если нет, удалить если есть)
element.classList.toggle('active');

// Проверить наличие класса
if (element.classList.contains('active')) {
    console.log('Элемент активен');
}
```

**Создание и удаление элементов:**

```javascript
// Создание нового элемента
let newParagraph = document.createElement('p');
newParagraph.textContent = 'Это новый параграф';
newParagraph.classList.add('highlight');

// Добавление в DOM
let container = document.getElementById('content');
container.appendChild(newParagraph);

// Удаление элемента
let oldElement = document.getElementById('old');
oldElement.remove();
```

---

## 3. События и обработка пользовательского ввода

### Что такое события?

События - это действия, которые происходят в браузере: клики, ввод текста, движение мыши, загрузка страницы и т.д.

### Основные типы событий

- `click` - клик по элементу
- `dblclick` - двойной клик
- `mouseenter` - наведение мыши
- `mouseleave` - увод мыши
- `input` - ввод в поле
- `change` - изменение значения
- `submit` - отправка формы
- `keydown` - нажатие клавиши
- `load` - загрузка страницы

### Добавление обработчиков событий

**Способ 1: addEventListener (рекомендуется)**

```javascript
let button = document.getElementById('myButton');

button.addEventListener('click', function() {
    alert('Кнопка нажата!');
});

// Стрелочная функция
button.addEventListener('click', () => {
    alert('Кнопка нажата!');
});
```

**Способ 2: Свойство on...**

```javascript
button.onclick = function() {
    alert('Кнопка нажата!');
};
```

### Объект события

```javascript
button.addEventListener('click', function(event) {
    console.log('Тип события:', event.type);
    console.log('Элемент:', event.target);
    console.log('Координаты:', event.clientX, event.clientY);
});
```

### Практические примеры

**Пример 1: Счётчик кликов**

```html
<button id="clickButton">Кликни меня!</button>
<p>Количество кликов: <span id="counter">0</span></p>

<script>
let count = 0;
let button = document.getElementById('clickButton');
let counterDisplay = document.getElementById('counter');

button.addEventListener('click', function() {
    count++;
    counterDisplay.textContent = count;
});
</script>
```

**Пример 2: Переключение видимости**

```html
<button id="toggleButton">Показать/Скрыть</button>
<div id="content" style="display: none;">
    <p>Это скрытый контент!</p>
</div>

<script>
let toggleBtn = document.getElementById('toggleButton');
let content = document.getElementById('content');

toggleBtn.addEventListener('click', function() {
    if (content.style.display === 'none') {
        content.style.display = 'block';
    } else {
        content.style.display = 'none';
    }
});
</script>
```

**Пример 3: Валидация формы**

```html
<form id="studentForm">
    <input type="text" id="studentName" placeholder="Имя студента">
    <input type="number" id="studentAge" placeholder="Возраст" min="6" max="18">
    <button type="submit">Отправить</button>
</form>
<div id="message"></div>

<script>
let form = document.getElementById('studentForm');
let message = document.getElementById('message');

form.addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем отправку формы
    
    let name = document.getElementById('studentName').value;
    let age = document.getElementById('studentAge').value;
    
    if (name === '' || age === '') {
        message.textContent = 'Заполните все поля!';
        message.style.color = 'red';
    } else {
        message.textContent = `Данные сохранены: ${name}, ${age} лет`;
        message.style.color = 'green';
        form.reset();
    }
});
</script>
```

---

## 4. Создание интерактивных образовательных элементов

### Пример 1: Простой калькулятор для уроков математики

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Калькулятор</title>
    <style>
        .calculator {
            max-width: 300px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 10px;
        }
        input {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            font-size: 18px;
        }
        button {
            width: 48%;
            padding: 10px;
            margin: 5px 1%;
            font-size: 16px;
            cursor: pointer;
        }
        #result {
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <h2>Калькулятор</h2>
        <input type="number" id="num1" placeholder="Число 1">
        <input type="number" id="num2" placeholder="Число 2">
        <button onclick="calculate('+')">+</button>
        <button onclick="calculate('-')">-</button>
        <button onclick="calculate('*')">×</button>
        <button onclick="calculate('/')">÷</button>
        <div id="result"></div>
    </div>
    
    <script>
        function calculate(operation) {
            let num1 = parseFloat(document.getElementById('num1').value);
            let num2 = parseFloat(document.getElementById('num2').value);
            let result = document.getElementById('result');
            
            if (isNaN(num1) || isNaN(num2)) {
                result.textContent = 'Введите оба числа!';
                result.style.color = 'red';
                return;
            }
            
            let answer;
            switch(operation) {
                case '+':
                    answer = num1 + num2;
                    break;
                case '-':
                    answer = num1 - num2;
                    break;
                case '*':
                    answer = num1 * num2;
                    break;
                case '/':
                    if (num2 === 0) {
                        result.textContent = 'Делить на ноль нельзя!';
                        result.style.color = 'red';
                        return;
                    }
                    answer = num1 / num2;
                    break;
            }
            
            result.textContent = `Результат: ${answer}`;
            result.style.color = 'green';
        }
    </script>
</body>
</html>
```

### Пример 2: Интерактивная викторина

```javascript
const questions = [
    {
        question: "Столица России?",
        options: ["Москва", "Санкт-Петербург", "Казань", "Новосибирск"],
        correct: 0
    },
    {
        question: "Сколько планет в Солнечной системе?",
        options: ["7", "8", "9", "10"],
        correct: 1
    },
    {
        question: "Кто написал 'Евгений Онегин'?",
        options: ["Лермонтов", "Пушкин", "Толстой", "Достоевский"],
        correct: 1
    }
];

let currentQuestion = 0;
let score = 0;

function loadQuestion() {
    let q = questions[currentQuestion];
    document.getElementById('question').textContent = q.question;
    
    let optionsDiv = document.getElementById('options');
    optionsDiv.innerHTML = '';
    
    q.options.forEach((option, index) => {
        let button = document.createElement('button');
        button.textContent = option;
        button.onclick = () => checkAnswer(index);
        optionsDiv.appendChild(button);
    });
}

function checkAnswer(selectedIndex) {
    if (selectedIndex === questions[currentQuestion].correct) {
        score++;
        alert('Правильно! ✓');
    } else {
        alert('Неправильно ✗');
    }
    
    currentQuestion++;
    
    if (currentQuestion < questions.length) {
        loadQuestion();
    } else {
        showResults();
    }
}

function showResults() {
    document.getElementById('quiz').innerHTML = 
        `<h2>Викторина завершена!</h2>
         <p>Ваш результат: ${score} из ${questions.length}</p>
         <button onclick="location.reload()">Начать заново</button>`;
}

// Загрузить первый вопрос при загрузке страницы
window.onload = loadQuestion;
```

### Пример 3: Таймер для контрольной работы

```javascript
let timeLeft = 600; // 10 минут в секундах
let timerInterval;

function startTimer() {
    timerInterval = setInterval(function() {
        timeLeft--;
        updateDisplay();
        
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            alert('Время вышло!');
        }
    }, 1000);
}

function updateDisplay() {
    let minutes = Math.floor(timeLeft / 60);
    let seconds = timeLeft % 60;
    
    // Добавляем ведущий ноль
    if (seconds < 10) seconds = '0' + seconds;
    
    document.getElementById('timer').textContent = 
        `Осталось времени: ${minutes}:${seconds}`;
    
    // Предупреждение за минуту
    if (timeLeft === 60) {
        document.getElementById('timer').style.color = 'red';
    }
}

function pauseTimer() {
    clearInterval(timerInterval);
}

function resetTimer() {
    clearInterval(timerInterval);
    timeLeft = 600;
    updateDisplay();
}
```

---

## 5. Практическая демонстрация

### Создание интерактивной таблицы умножения

**HTML:**
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Тренажёр таблицы умножения</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            text-align: center;
        }
        #question {
            font-size: 36px;
            margin: 30px 0;
        }
        #answer {
            font-size: 24px;
            padding: 10px;
            width: 100px;
        }
        button {
            font-size: 20px;
            padding: 10px 20px;
            margin: 10px;
            cursor: pointer;
        }
        #feedback {
            font-size: 24px;
            margin: 20px;
            min-height: 30px;
        }
        .correct {
            color: green;
        }
        .incorrect {
            color: red;
        }
        #stats {
            margin-top: 30px;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <h1>🎓 Тренажёр таблицы умножения</h1>
    <div id="question"></div>
    <input type="number" id="answer" placeholder="Ответ">
    <br>
    <button onclick="checkAnswer()">Проверить</button>
    <button onclick="nextQuestion()">Следующий пример</button>
    <div id="feedback"></div>
    <div id="stats">
        <p>Правильных ответов: <span id="correct">0</span></p>
        <p>Неправильных ответов: <span id="incorrect">0</span></p>
    </div>
    
    <script>
        let num1, num2;
        let correctCount = 0;
        let incorrectCount = 0;
        
        function generateQuestion() {
            num1 = Math.floor(Math.random() * 10) + 1;
            num2 = Math.floor(Math.random() * 10) + 1;
            document.getElementById('question').textContent = 
                `${num1} × ${num2} = ?`;
            document.getElementById('answer').value = '';
            document.getElementById('feedback').textContent = '';
            document.getElementById('answer').focus();
        }
        
        function checkAnswer() {
            let userAnswer = parseInt(document.getElementById('answer').value);
            let correctAnswer = num1 * num2;
            let feedback = document.getElementById('feedback');
            
            if (isNaN(userAnswer)) {
                feedback.textContent = 'Введите ответ!';
                feedback.className = '';
                return;
            }
            
            if (userAnswer === correctAnswer) {
                feedback.textContent = '✓ Правильно!';
                feedback.className = 'correct';
                correctCount++;
                document.getElementById('correct').textContent = correctCount;
            } else {
                feedback.textContent = `✗ Неправильно. Правильный ответ: ${correctAnswer}`;
                feedback.className = 'incorrect';
                incorrectCount++;
                document.getElementById('incorrect').textContent = incorrectCount;
            }
        }
        
        function nextQuestion() {
            generateQuestion();
        }
        
        // Обработка нажатия Enter
        document.getElementById('answer').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                checkAnswer();
            }
        });
        
        // Генерируем первый вопрос при загрузке
        generateQuestion();
    </script>
</body>
</html>
```

---

## Домашнее задание

Создать одно из следующих приложений на выбор:

1. **Конвертер единиц измерения** (температура, длина, вес)
2. **Генератор случайных примеров** для устного счёта
3. **Интерактивную викторину** по вашему предмету (минимум 5 вопросов)
4. **Калькулятор среднего балла** с возможностью добавления/удаления оценок

**Требования:**
- Использовать обработку событий
- Валидация пользовательского ввода
- Стилизация с помощью CSS
- Обратная связь пользователю (правильно/неправильно, ошибки ввода)

---

## Вопросы для самопроверки

1. Какие типы данных существуют в JavaScript?
2. В чём разница между `let` и `const`?
3. Что такое DOM?
4. Как выбрать элемент по ID?
5. Какие способы добавления обработчиков событий вы знаете?
6. Как предотвратить отправку формы?
7. Что такое `event.preventDefault()`?

---

## Полезные ресурсы

- [Learn JavaScript](https://learn.javascript.ru/) - отличный русскоязычный учебник
- [MDN JavaScript Guide](https://developer.mozilla.org/ru/docs/Web/JavaScript/Guide)
- [JavaScript.info](https://javascript.info/) - современный учебник
- [CodeWars](https://www.codewars.com/) - практика программирования

