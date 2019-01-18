import os

if os.environ['ENVCHARLOTTE'] == "PROD":
    log_file_path = "/var/log/charlotte/charlotte.log"
else:
    log_file_path = "charlotte.log"


config = {
    "version": 1,
    "formatters": {
        "MainFormatter" :{
            "format":  "[%(asctime)s] - %(levelname)-8s - %(name)-35s - %(message)s",
            "datefmt": "%y-%m-%d %H:%M:%S.%f"
        }
    },
    "handlers": {
        "MainHandler": {
            "class":     "logging.handlers.TimedRotatingFileHandler",
            "level":     "DEBUG",
            "formatter": "MainFormatter",
            "filename":  log_file_path,
            "when":      "midnight"
        }
    },
    "root": {
        "level":    "DEBUG",
        "handlers": ["MainHandler"]
    }
}
