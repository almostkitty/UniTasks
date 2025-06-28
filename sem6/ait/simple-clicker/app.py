from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import redis
import os


REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
EMOJI = os.getenv("EMOJI", "🐄")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def main_page():
    count = int(r.get("clicks") or 0)
    icons = EMOJI * count
    return f"""
    <html>
    <head>
        <title>Кнопка {EMOJI}</title>
    </head>
    <body style="font-family:sans-serif; text-align:center; margin-top:50px;">
        <h1>Кнопка {EMOJI}</h1>
        <div id="icons" style="font-size:2rem;margin:20px;">{icons}</div>
        <p>Нажато: <span id="counter">{count}</span></p>
        <button onclick="addIcon()">Добавить {EMOJI}</button>
        <script>
            function addIcon() {{
                fetch('/add', {{method: 'POST'}})
                .then(r => r.json())
                .then(data => {{
                    let div = document.getElementById('icons');
                    div.innerHTML += '{EMOJI}';
                    document.getElementById('counter').textContent = data.count;
                }});
            }}
        </script>
    </body>
    </html>
    """


@app.post("/add")
async def add():
    count = r.incr("clicks")
    return {"count": count}
