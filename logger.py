import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh=logging.FileHandler('WOLONG.txt',encoding='utf-8')
hd= logging.StreamHandler()
logger.addHandler(fh)
logger.addHandler(hd)