import datetime
from typing import List

class ProductionLogger:
    _instance = None
    _logs: List[str] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProductionLogger, cls).__new__(cls)
        return cls._instance

    def log(self, module: str, message: str, level: str = "INFO"):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{module.upper()}] {level.upper()}: {message}"
        self._logs.append(log_entry)
        print(log_entry)  # Still print to terminal for convenience

    def get_logs(self) -> List[str]:
        return self._logs

    def clear(self):
        self._logs = []

# Singleton instance
logger = ProductionLogger()
