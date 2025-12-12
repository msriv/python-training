import logging
import os
from datetime import datetime
 
log_file = f"app_{datetime.now().strftime('%Y%m%d')}.log"
 
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=log_file,
    filemode='a'
)
 
console_handler = logging.StreamHandler()
 
console_handler.setLevel(logging.INFO)
 
console_formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)
 
root_logger = logging.getLogger()
root_logger.addHandler(console_handler)
 
logging.debug('This is a debug message')
logging.info('This is a Information message')
 