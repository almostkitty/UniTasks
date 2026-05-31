<?php
// Установка заголовков
header("Content-Type: text/plain; charset=UTF-8");
header("Access-Control-Allow-Origin: *");

// Маршрут /login/
if ($_SERVER['REQUEST_URI'] === '/login/') {
    echo 'almst';
    exit(); // Завершаем выполнение скрипта после отправки ответа
}

// Маршрут /sample/
if ($_SERVER['REQUEST_URI'] === '/sample/') {
    // Функция task
    function task($x) {
        // Возвращаем значение аргумента x в верхнем регистре
        return strtoupper($x);
    }

    // Получаем параметр x из запроса
    $x = $_GET['x'] ?? null;

    // Проверяем, был ли передан параметр x
    if ($x !== null) {
        // Вызываем функцию task с переданным значением x и выводим результат
        echo task($x);
        exit(); // Завершаем выполнение скрипта после отправки ответа
    } else {
        // Если параметр x не был передан, выводим сообщение об ошибке
        echo 'Parameter x is missing';
        exit(); // Завершаем выполнение скрипта после отправки ответа
    }
}

// Если ни один из маршрутов не совпал, возвращаем ошибку 404
http_response_code(404);
echo 'Not Found';
?>
