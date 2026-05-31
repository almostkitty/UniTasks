<?php 
  header('Content-type: text/plain; charset=utf-8' );
  header ('Access-Control-Allow-Origin: *');
?>function task(x) {
    let promiseA = new Promise((resolve, reject) =>     {
        if (x < 18) {
            resolve("yes");
        }
        else {
            reject("no");
        }
    });
    return promiseA
}