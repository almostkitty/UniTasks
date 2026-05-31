const express = require('express');
const multer = require('multer');
const crypto = require('crypto');

const app = express();

const upload = multer();

app.get('', (req, res) => {
  res.send('...');
});

app.get('/login', (req, res) => {
  res.send('1140095');
});

app.post('/decypher', upload.fields([{ name: 'key' }, { name: 'secret' }]), (req, res) => {
  const key = req.files['key'][0].buffer.toString();
  const secret = req.files['secret'][0].buffer;

  const decrypted = crypto.privateDecrypt(key, secret)

  res.send(decrypted.toString());
});

app.listen(3000, () => {
  console.log(`Server listening on port 3000`);
});