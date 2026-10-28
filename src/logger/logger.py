import logging, sys


log = logging.getLogger()
log.setLevel(logging.INFO)

file_handler = logging.FileHandler("./src/logger/logs/log.txt", mode="a", )
stream_handler = logging.StreamHandler(stream=sys.stdout,)

log_format = '%(asctime)s %(levelname)s: %(message)s'
formatter = logging.Formatter(log_format)
log.addHandler(stream_handler)
log.addHandler(file_handler)

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

