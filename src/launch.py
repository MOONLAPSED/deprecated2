import logging

if 'ml' not in logging.Logger.manager.loggerDict:
    logging.basicConfig(level=logging.INFO)
ml = logging.getLogger('ml')
