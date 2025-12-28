# Лекция 3: Создание образовательных веб-приложений с использованием фреймворков

**Продолжительность:** 2 академических часа

## План лекции

1. Введение в современные фреймворки (15 минут)
2. Знакомство с Vue.js для образовательных проектов (30 минут)
3. Реактивность и компонентный подход (30 минут)
4. Создание образовательного приложения с Vue.js (25 минут)
5. Вопросы и обсуждение (10 минут)

---

## 1. Введение в современные фреймворки

### Что такое фреймворк?

Фреймворк - это набор инструментов и библиотек, которые упрощают разработку веб-приложений. Если раньше нам приходилось писать много кода вручную, фреймворки автоматизируют рутинные задачи.

### Зачем нужны фреймворки в образовании?

**Преимущества:**
- ⚡ Быстрая разработка интерактивных приложений
- 🔄 Автоматическое обновление интерфейса при изменении данных
- 🧩 Переиспользование компонентов
- 📱 Легко создавать сложные интерфейсы
- 🎨 Структурированный и понятный код

**Примеры использования:**
- Интерактивные дашборды успеваемости
- Сложные образовательные игры
- Системы тестирования с разными типами вопросов
- Личные кабинеты учеников
- Образовательные симуляции

### Популярные фреймворки

1. **Vue.js** 🟢 - простой для начинающих, гибкий
2. **React** 🔵 - самый популярный, много материалов
3. **Angular** 🔴 - мощный, но сложный для начинающих

**Мы выберем Vue.js** потому что:
- Легко изучить
- Можно подключить без сборки
- Отличная документация на русском
- Подходит для небольших и средних проектов
- Можно начать использовать постепенно

---

## 2. Знакомство с Vue.js для образовательных проектов

### Подключение Vue.js

**Способ 1: CDN (для обучения)**
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Мое первое Vue-приложение</title>
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
</head>
<body>
    <div id="app">
        {{ message }}
    </div>

    <script>
        const { createApp } = Vue;
        
        createApp({
            data() {
                return {
                    message: 'Привет, Vue!'
                }
            }
        }).mount('#app');
    </script>
</body>
</html>
```

### Основы синтаксиса Vue.js

**Интерполяция (вывод данных):**
```html
<div id="app">
    <h1>{{ title }}</h1>
    <p>{{ 2 + 2 }}</p>
    <p>{{ message.toUpperCase() }}</p>
</div>
```

**Директивы:**

1. **v-bind** - привязка атрибутов
```html
<img v-bind:src="imageSrc">
<!-- Сокращённая запись -->
<img :src="imageSrc">
<a :href="link">Ссылка</a>
```

2. **v-if, v-else, v-show** - условное отображение
```html
<p v-if="score >= 90">Отлично!</p>
<p v-else-if="score >= 75">Хорошо!</p>
<p v-else>Нужно подтянуть знания</p>

<!-- v-show просто скрывает элемент -->
<p v-show="isVisible">Видимый текст</p>
```

3. **v-for** - циклы
```html
<ul>
    <li v-for="student in students" :key="student.id">
        {{ student.name }} - {{ student.grade }}
    </li>
</ul>

<ul>
    <li v-for="(item, index) in items" :key="index">
        {{ index + 1 }}. {{ item }}
    </li>
</ul>
```

4. **v-on** - обработка событий
```html
<button v-on:click="increment">Нажми меня</button>
<!-- Сокращённая запись -->
<button @click="increment">Нажми меня</button>
<input @input="handleInput" type="text">
```

5. **v-model** - двусторонняя привязка
```html
<input v-model="username" type="text">
<p>Привет, {{ username }}!</p>
```

### Пример: Список дел для учителя

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Список дел учителя</title>
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <style>
        #app {
            max-width: 600px;
            margin: 50px auto;
            font-family: Arial, sans-serif;
        }
        .task {
            padding: 10px;
            margin: 5px 0;
            background: #f0f0f0;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .completed {
            text-decoration: line-through;
            opacity: 0.6;
        }
        button {
            cursor: pointer;
            padding: 5px 10px;
        }
        input[type="text"] {
            width: 70%;
            padding: 10px;
            font-size: 16px;
        }
        .add-btn {
            width: 25%;
            padding: 10px;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div id="app">
        <h1>📝 Список дел учителя</h1>
        
        <div>
            <input 
                v-model="newTask" 
                @keyup.enter="addTask"
                type="text" 
                placeholder="Добавить задачу...">
            <button @click="addTask" class="add-btn">Добавить</button>
        </div>
        
        <div v-if="tasks.length === 0">
            <p>Задач пока нет. Добавьте первую!</p>
        </div>
        
        <div v-else>
            <div 
                v-for="(task, index) in tasks" 
                :key="index"
                class="task"
                :class="{ completed: task.done }">
                
                <span @click="toggleTask(index)" style="cursor: pointer; flex-grow: 1;">
                    {{ task.text }}
                </span>
                
                <button @click="removeTask(index)">❌</button>
            </div>
            
            <p style="margin-top: 20px;">
                Выполнено: {{ completedCount }} из {{ tasks.length }}
            </p>
        </div>
    </div>

    <script>
        const { createApp } = Vue;
        
        createApp({
            data() {
                return {
                    newTask: '',
                    tasks: [
                        { text: 'Проверить контрольные работы', done: false },
                        { text: 'Подготовить материалы к уроку', done: false },
                        { text: 'Провести родительское собрание', done: false }
                    ]
                }
            },
            computed: {
                completedCount() {
                    return this.tasks.filter(task => task.done).length;
                }
            },
            methods: {
                addTask() {
                    if (this.newTask.trim() !== '') {
                        this.tasks.push({
                            text: this.newTask,
                            done: false
                        });
                        this.newTask = '';
                    }
                },
                removeTask(index) {
                    this.tasks.splice(index, 1);
                },
                toggleTask(index) {
                    this.tasks[index].done = !this.tasks[index].done;
                }
            }
        }).mount('#app');
    </script>
</body>
</html>
```

---

## 3. Реактивность и компонентный подход

### Что такое реактивность?

Реактивность - это автоматическое обновление интерфейса при изменении данных. Вам не нужно вручную обновлять DOM!

**Без Vue (ручное обновление):**
```javascript
let count = 0;
document.getElementById('counter').textContent = count;

function increment() {
    count++;
    document.getElementById('counter').textContent = count; // Вручную!
}
```

**С Vue (автоматическое обновление):**
```javascript
createApp({
    data() {
        return { count: 0 }
    },
    methods: {
        increment() {
            this.count++; // Интерфейс обновится автоматически!
        }
    }
}).mount('#app');
```

### Вычисляемые свойства (Computed)

Вычисляемые свойства автоматически пересчитываются при изменении зависимостей:

```javascript
createApp({
    data() {
        return {
            grades: [5, 4, 5, 3, 4, 5]
        }
    },
    computed: {
        average() {
            let sum = this.grades.reduce((a, b) => a + b, 0);
            return (sum / this.grades.length).toFixed(2);
        },
        passedCount() {
            return this.grades.filter(g => g >= 3).length;
        }
    }
}).mount('#app');
```

### Методы (Methods)

Методы - это функции, которые можно вызывать:

```javascript
methods: {
    addGrade(grade) {
        this.grades.push(grade);
    },
    removeGrade(index) {
        this.grades.splice(index, 1);
    },
    clearAll() {
        this.grades = [];
    }
}
```

### Наблюдатели (Watchers)

Watchers следят за изменениями данных:

```javascript
watch: {
    score(newValue, oldValue) {
        if (newValue > 90) {
            alert('Отличный результат!');
        }
    }
}
```

### Жизненный цикл компонента

```javascript
createApp({
    data() {
        return {
            message: 'Привет!'
        }
    },
    created() {
        console.log('Компонент создан');
        // Хорошее место для загрузки данных
    },
    mounted() {
        console.log('Компонент добавлен в DOM');
        // Можно работать с DOM-элементами
    }
}).mount('#app');
```

---

## 4. Создание образовательного приложения с Vue.js

### Проект: Интерактивный журнал оценок

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Журнал оценок</title>
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        #app {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        h1 {
            color: #667eea;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .add-student {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        
        input {
            flex-grow: 1;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
        }
        
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            padding: 12px 24px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        button:hover {
            background: #5568d3;
            transform: translateY(-2px);
        }
        
        .student-card {
            background: #f8f9fa;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .student-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .student-name {
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }
        
        .average {
            font-size: 18px;
            font-weight: bold;
            padding: 5px 15px;
            border-radius: 20px;
            background: #e3f2fd;
            color: #1976d2;
        }
        
        .grades {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 10px;
        }
        
        .grade {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            font-weight: bold;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .grade:hover {
            transform: scale(1.1);
        }
        
        .grade-5 { background: #4caf50; color: white; }
        .grade-4 { background: #8bc34a; color: white; }
        .grade-3 { background: #ffc107; color: white; }
        .grade-2 { background: #f44336; color: white; }
        
        .add-grade {
            display: flex;
            gap: 5px;
        }
        
        .grade-btn {
            width: 40px;
            height: 40px;
            padding: 0;
            font-size: 18px;
            font-weight: bold;
        }
        
        .delete-btn {
            background: #f44336;
            padding: 8px 16px;
            font-size: 14px;
        }
        
        .delete-btn:hover {
            background: #d32f2f;
        }
        
        .stats {
            margin-top: 30px;
            padding: 20px;
            background: #e8eaf6;
            border-radius: 10px;
        }
        
        .stats h2 {
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .stats p {
            font-size: 18px;
            margin: 5px 0;
        }
        
        .empty {
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div id="app">
        <h1>📚 Журнал оценок класса</h1>
        
        <div class="add-student">
            <input 
                v-model="newStudentName" 
                @keyup.enter="addStudent"
                placeholder="Введите имя ученика..."
                type="text">
            <button @click="addStudent">➕ Добавить ученика</button>
        </div>
        
        <div v-if="students.length === 0" class="empty">
            Список учеников пуст. Добавьте первого ученика!
        </div>
        
        <div v-else>
            <div 
                v-for="(student, studentIndex) in students" 
                :key="studentIndex"
                class="student-card">
                
                <div class="student-header">
                    <span class="student-name">{{ student.name }}</span>
                    <span class="average">Средний балл: {{ calculateAverage(student.grades) }}</span>
                    <button @click="removeStudent(studentIndex)" class="delete-btn">
                        🗑️ Удалить
                    </button>
                </div>
                
                <div class="grades">
                    <div 
                        v-for="(grade, gradeIndex) in student.grades"
                        :key="gradeIndex"
                        :class="['grade', `grade-${grade}`]"
                        @click="removeGrade(studentIndex, gradeIndex)"
                        title="Нажмите для удаления">
                        {{ grade }}
                    </div>
                </div>
                
                <div class="add-grade">
                    <button 
                        v-for="grade in [5, 4, 3, 2]"
                        :key="grade"
                        @click="addGrade(studentIndex, grade)"
                        :class="['grade-btn', `grade-${grade}`]">
                        {{ grade }}
                    </button>
                </div>
            </div>
            
            <div class="stats">
                <h2>📊 Статистика класса</h2>
                <p>Всего учеников: {{ students.length }}</p>
                <p>Средний балл класса: {{ classAverage }}</p>
                <p>Отличников (>= 4.5): {{ excellentStudents }}</p>
                <p>Хорошистов (>= 3.5): {{ goodStudents }}</p>
            </div>
        </div>
    </div>

    <script>
        const { createApp } = Vue;
        
        createApp({
            data() {
                return {
                    newStudentName: '',
                    students: [
                        { name: 'Иванов Иван', grades: [5, 4, 5, 5] },
                        { name: 'Петрова Мария', grades: [4, 5, 4, 5] },
                        { name: 'Сидоров Пётр', grades: [3, 4, 3, 4] }
                    ]
                }
            },
            computed: {
                classAverage() {
                    if (this.students.length === 0) return '0.00';
                    
                    let totalSum = 0;
                    let totalCount = 0;
                    
                    this.students.forEach(student => {
                        if (student.grades.length > 0) {
                            totalSum += student.grades.reduce((a, b) => a + b, 0);
                            totalCount += student.grades.length;
                        }
                    });
                    
                    return totalCount > 0 ? (totalSum / totalCount).toFixed(2) : '0.00';
                },
                excellentStudents() {
                    return this.students.filter(student => {
                        return this.calculateAverageNum(student.grades) >= 4.5;
                    }).length;
                },
                goodStudents() {
                    return this.students.filter(student => {
                        let avg = this.calculateAverageNum(student.grades);
                        return avg >= 3.5 && avg < 4.5;
                    }).length;
                }
            },
            methods: {
                addStudent() {
                    if (this.newStudentName.trim() !== '') {
                        this.students.push({
                            name: this.newStudentName,
                            grades: []
                        });
                        this.newStudentName = '';
                    }
                },
                removeStudent(index) {
                    if (confirm('Удалить ученика?')) {
                        this.students.splice(index, 1);
                    }
                },
                addGrade(studentIndex, grade) {
                    this.students[studentIndex].grades.push(grade);
                },
                removeGrade(studentIndex, gradeIndex) {
                    this.students[studentIndex].grades.splice(gradeIndex, 1);
                },
                calculateAverage(grades) {
                    if (grades.length === 0) return 'Нет оценок';
                    let sum = grades.reduce((a, b) => a + b, 0);
                    return (sum / grades.length).toFixed(2);
                },
                calculateAverageNum(grades) {
                    if (grades.length === 0) return 0;
                    let sum = grades.reduce((a, b) => a + b, 0);
                    return sum / grades.length;
                }
            }
        }).mount('#app');
    </script>
</body>
</html>
```

---

## 5. Преимущества использования Vue.js в образовании

### Для учителя:
- ✅ Быстрое создание интерактивных материалов
- ✅ Легко поддерживать и обновлять
- ✅ Можно создавать сложные приложения
- ✅ Переиспользование компонентов

### Для учеников:
- ✅ Современный интерфейс
- ✅ Быстрая обратная связь
- ✅ Интерактивность повышает вовлечённость
- ✅ Удобство использования

---

## Домашнее задание

Создать одно из следующих приложений с использованием Vue.js:

1. **Трекер домашних заданий** - ученики могут добавлять задания, отмечать выполненные
2. **Калькулятор итоговой оценки** - расчёт итоговой оценки с учётом весов (контрольные, домашние работы, экзамен)
3. **База знаний** - FAQ по предмету с поиском и фильтрацией
4. **Планировщик уроков** - расписание с возможностью добавления тем и материалов

**Требования:**
- Использовать v-for для списков
- Использовать v-model для форм
- Минимум одно вычисляемое свойство (computed)
- Минимум 3 метода
- Стилизация CSS

---

## Вопросы для самопроверки

1. Что такое реактивность?
2. В чём разница между методами и вычисляемыми свойствами?
3. Для чего используется директива v-model?
4. Как вывести список элементов с помощью Vue?
5. Зачем нужен атрибут :key в v-for?

---

## Полезные ресурсы

- [Официальная документация Vue.js (русский)](https://v3.ru.vuejs.org/)
- [Vue Mastery](https://www.vuemastery.com/) - видеокурсы
- [Vue School](https://vueschool.io/) - интерактивные уроки
- [Awesome Vue](https://github.com/vuejs/awesome-vue) - коллекция ресурсов

---

## Дополнительно: Следующие шаги

После освоения базового Vue.js можно изучить:
- **Vue Router** - для многостраничных приложений
- **Vuex/Pinia** - управление состоянием
- **Vue CLI** - инструменты для разработки
- **Nuxt.js** - фреймворк на основе Vue

