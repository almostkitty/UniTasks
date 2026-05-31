import express from 'express';
import multer from 'multer';
import crypto from 'crypto';

const app = express();
const upload = multer();

const login = "1140095"; // Ваш логин в системе MOODLE

// Маршрут для получения логина
app.get('/login', (req, res) => {
  res.send(login);
});

// Маршрут для расшифровки сообщения
app.post('/decypher', upload.fields([{ name: 'key' }, { name: 'secret' }]), (req, res) => {
  const { key, secret } = req.files;

  if (!key || !secret) {
    return res.status(400).json({ error: 'Key and secret fields are required.' });
  }

  // Чтение ключа и сообщения из файлов
  const keyBuffer = Buffer.from(key[0].buffer);
  const secretBuffer = Buffer.from(secret[0].buffer);

  try {
    // Убеждаемся, что ключ имеет длину 32 байта (256 бит)
    const paddedKey = Buffer.concat([keyBuffer, Buffer.alloc(32 - keyBuffer.length)]);
    // Расшифровка с использованием AES
    const decipher = crypto.createDecipheriv('aes-256-cbc', paddedKey, Buffer.alloc(16, 0));
    let decrypted = decipher.update(secretBuffer, 'hex', 'utf-8');
    decrypted += decipher.final('utf-8');

    res.send(decrypted);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to decrypt message.' });
  }
});

// Запуск сервера
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
