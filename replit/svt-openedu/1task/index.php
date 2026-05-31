<?php
// Устанавливаем заголовки CORS
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET,POST,PUT,DELETE,OPTIONS");
header("Access-Control-Allow-Headers: x-test,ngrok-skip-browser-warning,Content-Type,Accept,Access-Control-Allow-Headers");

// Проверяем метод запроса
if ($_SERVER['REQUEST_METHOD'] === 'POST' || $_SERVER['REQUEST_METHOD'] === 'GET' || $_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    // Если метод - OPTIONS, просто возвращаем успех
    if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
        http_response_code(200);
        exit();
    }

    // Проверяем путь запроса
    if ($_SERVER['REQUEST_URI'] === '/result4/') {
        // Получаем значение заголовка x-test
        $xTest = isset($_SERVER['HTTP_X_TEST']) ? $_SERVER['HTTP_X_TEST'] : '';

        // Получаем тело запроса
        $requestBody = file_get_contents('php://input');

        // Создаем массив для ответа
        $response = array(
            'message' => 'almst',
            'x-result' => $xTest,
            'x-body' => $requestBody
        );

        // Устанавливаем заголовок Content-Type
        header('Content-Type: application/json');

        // Выводим ответ в формате JSON
        echo json_encode($response);
    } else {
        // Если путь не соответствует /result4/, отправляем ошибку 404
        http_response_code(404);
        echo 'Not Found';
    }
} else {
    // Если метод запроса не POST, GET или OPTIONS, отправляем ошибку метода
    http_response_code(405);
    echo 'Method Not Allowed';
}
?>
