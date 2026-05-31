<?php
header("Content-Type: text/plain; charset=UTF-8");
header("Access-Control-Allow-Origin: *");

$request_uri = $_SERVER['REQUEST_URI'];

if ($request_uri == '/login/') {
    echo "1140095";
} elseif ($request_uri == '/sample/') {
    $functionCode = <<<EOD
function task(x) {
    return x * Math.pow(this, 2);
}
EOD;
    echo $functionCode;
} else {
    http_response_code(404);
    echo "404 Not Found";
}
?>