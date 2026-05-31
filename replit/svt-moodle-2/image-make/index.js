import express from 'express';
import sharp from 'sharp';

const app = express();

const login = "1140095"; // Ваш логин в системе MOODLE

// Маршрут для получения логина
app.get('/login', (req, res) => {
  res.send(login);
});

// Маршрут для создания изображения
app.get('/makeimage', async (req, res) => {
  const { width, height } = req.query;

  if (!width || !height) {
    return res.status(400).send('Width and height parameters are required.');
  }

  try {
    const imageBuffer = await sharp({
      create: {
        width: parseInt(width),
        height: parseInt(height),
        channels: 4, // RGBA
        background: { r: 255, g: 255, b: 255, alpha: 1 } // White background
      }
    })
    .png()
    .toBuffer();

    res.set('Content-Type', 'image/png');
    res.send(imageBuffer);
  } catch (error) {
    console.error(error);
    res.status(500).send('Failed to create image.');
  }
});

// Запуск сервера
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
