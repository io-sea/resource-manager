import logging

logger = logging.getLogger('resource_manager_logger')  

logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('logfile.log')
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', datefmt='%d.%m.%Y %I:%M:%S %p')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
