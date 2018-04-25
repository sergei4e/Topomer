# coding: utf-8
import logging

FORMAT = '%(levelname)s : %(asctime)s : %(pathname)s : %(funcName)s : %(lineno)d : %(message)s'
logging.basicConfig(format=FORMAT, filename='scaner.log')
logger = logging.getLogger()
logger.setLevel(logging.WARNING)
