import asyncio
from datetime import datetime
from termcolor import colored
from pynput import keyboard


stop_program = False

colors = ["red", "green", "yellow", "blue"]

def on_press(key):
    global stop_program
    try:
        if key == keyboard.Key.esc:
            stop_program = True
            return False
    except AttributeError:
        pass

async def show_time():
    color_index = 0
    while not stop_program:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(colored(f"\rТекущее время: {now}", colors[color_index % len(colors)]), end="")
        color_index += 1
        await asyncio.sleep(1)
    print("\nПрограмма завершена")

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        asyncio.run(show_time())
    except KeyboardInterrupt:
        print("\nПрервано пользователем")
