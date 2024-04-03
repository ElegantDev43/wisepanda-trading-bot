import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_event_time = 0

    def on_any_event(self, event):
        # Ignore events that occur within a short time interval to avoid duplicates
        current_time = time.time()
        if current_time - self.last_event_time < 1:
            return
        self.last_event_time = current_time

        print(f'Restarting due to {event.event_type}')
        python_executable = sys.executable
        python_script = 'app.py'
        command = [python_executable, python_script]
        subprocess.run(command)

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
