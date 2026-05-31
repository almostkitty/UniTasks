export default (express, bodyParser, createReadStream, crypto, http, m, UserSchema) => {
    const app = express();

    const User = m.model('User', UserSchema);

    const CORS = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,PATCH,OPTIONS,DELETE',
        'Access-Control-Allow-Headers': 'Content-Type, Accept, Access-Control-Allow-Headers, ngrok-skip-browser-warning',
        'Content-Type': 'text/plain; charset=utf-8'
    };


    app
        .use((r, res, next) => { r.res.set(CORS); next(); })
        .use(bodyParser.urlencoded({ extended: true }))
        .get('/sha1/:input', r => {
            const shasum = crypto.createHash('sha1');
            shasum.update(r.params.input);

            r.res.send(shasum.digest('hex'));
        })

        .get('/login/', (req, res) => res.send('almst'))
        .get('/code/', (req, res) => {
            res.set({ 'Content-Type': 'text/plain; charset=utf-8' });
            createReadStream(import.meta.url.substring(7)).pipe(res);
        })
        ;

    app.post('/insert/', async (req, res) => {
        const { URL, login, password } = req.body;
        try {
            await m.connect(URL, { useNewUrlParser: true, useUnifiedTopology: true });
        } catch (e) {
            res.send(e.stack);
        }

        const newUser = new User({ login, password });
        await newUser.save();
        res.status(201).json({ successsss: true, login });
    });

    app.all('/req/', (req, res) => {
        const addr = req.method === 'POST' ? req.body.addr : req.query.addr;

        http.get(addr, (r, b = '') => {
            r
                .on('data', d => b += d)
                .on('end', () => res.send(b));
        });
    })
        .get('/hello/', (req, res) => res.send('almst'));

    return app;

}