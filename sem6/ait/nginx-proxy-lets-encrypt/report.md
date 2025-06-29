## Отчёт по проделанной работе
#### Пальчук Г.А. ИВТ 2.1

### Развертывание приложений через Docker Compose, с автоматическим выпуском сертификатов  Let's Encrypt
1. Docker Compose, 2 контейнера whoami + контейнер nginx-proxy
![](/nginx-proxy-lets-encrypt/img/1.png)
2. Запуск
![](/nginx-proxy-lets-encrypt/img/2.png)
3. Проверка whoami1.almostkitty.ru в браузере. На странице – id контейнера whoami1. Все работает правильно.
![](/nginx-proxy-lets-encrypt/img/3.png)
4. По примеру из ```acme-companion/docs/Docker-Compose.md```. Добавляю компаньона ```acme-companion``` + указываю версию 2, чтобы убрать ошибку с ``volumes_from```.
![](/nginx-proxy-lets-encrypt/img/5.png)
5. Запуск
![](/nginx-proxy-lets-encrypt/img/6.png)
6. Генерация сертификата для whoami2
![](/nginx-proxy-lets-encrypt/img/7.png)
![](/nginx-proxy-lets-encrypt/img/8.png)
8. Генерация сертификата для whoami1
![](/nginx-proxy-lets-encrypt/img/9.png)
![](/nginx-proxy-lets-encrypt/img/10.png)
9. Проверка в браузере. Соединение безопасное, сертификат есть.
![](/nginx-proxy-lets-encrypt/img/11.png)
![](/nginx-proxy-lets-encrypt/img/12.png)