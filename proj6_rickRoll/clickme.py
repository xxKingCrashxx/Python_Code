import webbrowser
import time

def run_script():
    controller = webbrowser.get()
    for i in range(10):
        controller.open("https://www.youtube.com/watch?v=rS9vLE0JeEE", new=2)
        time.sleep(1.0)

run_script()
