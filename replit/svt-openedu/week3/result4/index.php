<?php
header('Content-type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: x-test, ngrok-skip-browser-warning, Content-Type, Accept, Access-Control-Allow-Headers');

$data = array(
    'message' => 'almst',
    'x-result' => isset($_SERVER['HTTP_X_TEST']) ? $_SERVER['HTTP_X_TEST'] : null,
    'x-body' => file_get_contents('php://input')
);
echo json_encode($data);
?>