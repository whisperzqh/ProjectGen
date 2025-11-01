import logging
import os

RESET = "\033[0m"
COLORS = {
    "DEBUG": "\033[36m",   
    "INFO": "\033[32m",    
    "WARNING": "\033[33m", 
    "ERROR": "\033[31m",   
    "CRITICAL": "\033[41m" 
}
TIME_COLOR = "\033[35m"   

class ColorFormatter(logging.Formatter):
    def format(self, record):
        log_color = COLORS.get(record.levelname.strip("[]"), RESET)  
        record.levelname = f"{log_color}[{record.levelname.strip('[]')}]{RESET}"
        record.asctime = f"{TIME_COLOR}{self.formatTime(record, self.datefmt)}{RESET}"
        return super().format(record)


_logger = None

def get_logger(log_file_path=None, level=logging.INFO):
    global _logger
    if _logger is None:
        logger = logging.getLogger("multi_agent")
        logger.setLevel(level)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            ColorFormatter(fmt="%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        )
        logger.addHandler(console_handler)

        _logger = logger

    if log_file_path and not any(isinstance(h, logging.FileHandler) for h in _logger.handlers):
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
        file_handler.setFormatter(
            logging.Formatter(fmt="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        )
        _logger.addHandler(file_handler)

    return _logger
