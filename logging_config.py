import os

if os.environ['ENVCHARLOTTE'] == "PROD":
    log_file_path = ".charlotte/logs/charlotte.log"
else:
    log_file_path = "charlotte.log"


config = {
    "version": 1,
    "formatters": {
        "MainFormatter" :{
            "format":  "[%(asctime)s.%(msecs)03d] - %(levelname)-8s - %(name)-20s - %(message)s",
            "datefmt": "%y-%m-%d %H:%M:%S"
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
