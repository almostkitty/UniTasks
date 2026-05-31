function initializeApp(express, bodyParser, createReadStream, crypto, http, path, mongoose, cors, axios, morgan, pug, puppeteer, createProxyMiddleware) {
  const app = express();

  app.use(morgan('dev'));
  app.use(bodyParser.text())
  app.use(bodyParser.urlencoded({ extended: false }));
  app.use(bodyParser.json());
  app.use(cors())

  app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,OPTIONS,DELETE');
    next();
  });

  app.get('/login/', (req, res) => {
    res.setHeader('Content-Type', 'text/plain; charset=UTF-8')
    res.send('almst');
  });


  app.get('/wordpress*', (req, res) => {
    res.setHeader('Content-Type', 'application/json')
    res.send({'id': 5, 'title': {'rendered':'almst'}});
    });



  app.all('/render/', async (req, res) => {
    res.setHeader('Content-Type', 'text/plain; charset=UTF-8')
    console.log(`Hello World!`)

    const { random2, random3 } = req.body;
    const addr = req.query.addr;

    const response = await axios.get(addr);
    const fileContent = response.data;

    console.log(`Шаблон: ${fileContent}`)
    console.log(`random2: ${random2}`)
    console.log(`random3: ${random3}`)
    console.log(`addr: ${addr}`)

    const template = pug.compile(fileContent);
    const html = template({ random2, random3});

    console.log(`html: ${html}`)

    res.send(html);
  });

    app.get('/test/', async (req, res) => {
    res.setHeader('Content-Type', 'text/plain; charset=UTF-8')
    console.log(req.query.URL)
    const browser = await puppeteer.launch({executablePath: '/nix/store/x205pbkd5xh5g4iv0g58xjla55has3cx-chromium-108.0.5359.94/bin/chromium-browser', headers: true, args:['--no-sandbox']});
    const page = await browser.newPage();
    await page.goto(req.query.URL)
    await page.waitForSelector('#bt')
    await page.click('#bt')
    const number = await page.$eval('#inp', el => el.value)
    console.log(number)
    res.send(number)
  });

  return app;
};

export default initializeApp;