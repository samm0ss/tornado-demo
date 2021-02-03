import logging.handlers
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)sZ - %(levelname)s - %(message)s')
logging.Formatter.converter = time.gmtime

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
