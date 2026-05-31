export default (express, bodyParser, createReadStream, crypto, http, CORS, puppeteer) => {
    const app = express();
    app.use(bodyParser.json());

    // Обработчик для корневого маршрута
    app.get('/', (req, res) => {
        res.send('Hello, world!');
    });

    // Маршрут для /login/
    app.get('/login/', (req, res) => {
        res.send('almst');
    });

    // Маршрут для /test/
    app.get('/test/', async (req, res) => {
        const { URL } = req.query;
        console.log('Requested URL:', URL);
        // Запускаем браузер с использованием Puppeteer
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        try {
            // Переходим по указанному URL
            await page.goto(URL);
            try {
                // Находим кнопку и кликаем по ней
                await page.click('#bt');
            } catch (error) {
                console.error('Error clicking the button:', error);
                res.status(500).send('Error clicking the button');
                await browser.close();
                return; // Stop processing the request
            }
            try {
                // Ждем появления числа в поле ввода
                await page.waitForSelector('#inp');
                // Получаем текст из поля ввода
                const result = await page.$eval('#inp', input => input.value);
                // Возвращаем результат в качестве ответа на запрос
                res.send(result);
            } catch (error) {
                console.error('Error getting the input value:', error);
                res.status(500).send('Error getting the input value');
                await browser.close();
                return; // Stop processing the request
            }
        } catch (error) {
            console.error('Error during test:', error);
            res.status(500).send('Internal Server Error');
        } finally {
            // Закрываем браузер после завершения
            await browser.close();
        }
    });

    // Запуск сервера
    const server = http.createServer(app);
    const PORT = process.env.PORT || 3000;
    server.listen(PORT, () => console.log(`Server is running on port ${PORT}`));

    return app; // Важно вернуть экземпляр Express приложения
};
