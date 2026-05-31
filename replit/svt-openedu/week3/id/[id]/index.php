<?php 
  header('Content-type: text/html; charset=utf-8');
  header('Access-Control-Allow-Origin: *');

fetch(document.querySelector('#inp').value)
.then(response => response.text());
?>

<body>
  <script>


      const response = await fetch(`https://nd.kodaktor.ru/users/${N}`);
      const userData = await response.json();
      const login = userData.login;

    });
  </script>
</body>