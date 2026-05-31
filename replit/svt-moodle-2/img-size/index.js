import express from 'express';
import multer from 'multer';
import sharp from 'sharp';

const app = express();
const upload = multer();

const login = "1140095"; // Ваш логин в системе MOODLE

// Маршрут для получения логина
app.get('/login', (req, res) => {
  res.send(login);
});

// Маршрут для загрузки изображения и получения размеров
app.route('/size2json')
  .get((req, res) => {
    res.status(405).send('GET method not allowed. Use POST method to upload images.');
  })
  .post(upload.single('image'), (req, res) => {
    if (!req.file) {
      return res.status(400).json({ error: 'No image uploaded' });
    }

    sharp(req.file.buffer)
      .metadata()
      .then(metadata => {
        res.json({ width: metadata.width, height: metadata.height });
      })
      .catch(err => {
        console.error(err);
        res.status(500).json({ error: 'Failed to process image' });
      });
  });

// Запуск сервера
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
