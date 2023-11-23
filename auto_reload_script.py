from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        subprocess.run(["python", "./frontend/streamlit/app.py"])  # Replace 'your_script.py' with your Python file name

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
