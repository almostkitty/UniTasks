import express from 'express';
import axios from 'axios';

const app = express();

const login = "1140095"; // Ваш логин в системе MOODLE

// Маршрут для получения логина
app.get('/login', (req, res) => {
  res.send(login);
});

// Маршрут для получения логина пользователя по идентификатору
app.get('/id/:userId', async (req, res) => {
  const userId = req.params.userId;

  try {
    const response = await axios.get(`https://nd.kodaktor.ru/users/${userId}`);
    const userData = response.data;

    res.send(userData.login);
  } catch (error) {
    console.error(error);
    res.status(500).send('Failed to fetch user data.');
  }
});

// Запуск сервера
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
