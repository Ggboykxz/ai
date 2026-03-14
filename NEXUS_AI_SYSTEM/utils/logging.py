import datetime

class Logger:
    def __init__(self, component_name):
        self.component_name = component_name

    def log(self, message, level="info"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{self.component_name}] [{level.upper()}] {message}"
        print(log_message)
