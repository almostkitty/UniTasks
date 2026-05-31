const https = require('https');

const options = {
  hostname: 'kodaktor.ru',
  port: 443,
  path: '/api/chunks',
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  }
};

const data = new URLSearchParams({ login: 1140095 }).toString();

const req = https.request(options, (res) => {
  let chunkCount = 0;

  res.on('data', (chunk) => {
    chunkCount++;
  });

  res.on('end', () => {
    console.log(chunkCount);
  });
});

req.on('error', (e) => {
  console.error(e);
});

req.write(data);
req.end();