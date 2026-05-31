<?php 
  header('Content-type: text/html; charset=utf-8');
  header('Access-Control-Allow-Origin: *');
?>

<body>
  <input type="text" value="" id="inp">
  <button id="bt">Выполнить задание</button>

  <script>
    document.getElementById('bt').addEventListener('click', async function() {
      const inp = await fetch(document.querySelector('#inp').value)
        .then(response => response.text());

      /* запись результата */
      document.querySelector('#inp').value = inp; 

      console.log(document.querySelector('#inp').value);
    });
  </script>
</body>